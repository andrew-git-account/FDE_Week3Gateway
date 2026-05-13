# D#7 — Validation Plan

**Client:** MedFlex Healthcare Staffing  
**Engagement:** AI-native shift matching transformation  
**Prepared by:** Andrzej Bihun | Thursday interim draft

---

## 1. Validation Scope

This plan covers three validation concerns across all three agents and their integrations:

1. **Accuracy** — does each agent produce correct outputs against its spec?
2. **Failure modes** — what breaks, how badly, and what mitigates it?
3. **Compliance and regulatory risk** — what legal or regulatory exposure does the system create?

Validation is phased to match the delivery plan. Phase 1 (Weeks 1-8) validates Agent 1 + Agent 2 HIGH-confidence path only. Phase 2 adds Agent 3 and MEDIUM-confidence routing. Phase 3 adds the reputation model and predictive signals.

---

## 2. Agent 1 — Intake Parsing Validation

### 2.1 Accuracy Targets

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| Required fields extracted correctly | ≥ 90% of well-formed emails | Regression test set of 200 historical hospital emails, manually labelled |
| Credential mapping accuracy | ≥ 95% of known abbreviations resolved correctly | Test set covers all entries in credential taxonomy + 20 known hospital-specific abbreviations |
| Hospital identity match rate | ≥ 95% single-match resolution | Test set covers all hospitals in registry |
| Confidence score calibration | Records scoring ≥ 0.80 should have ≤ 10% field errors | Cross-check parsed output against coordinator-corrected ground truth |
| Escalation precision | 100% of records with missing required fields escalated | No false passes — any record missing shift_date, hospital_id, or required_credentials must escalate |
| Escalation recall | < 20% of complete, unambiguous records escalated | Measures over-escalation (coordinator burden) |

### 2.2 Edge Cases to Test

| Case | Expected Behaviour |
|------|--------------------|
| Relative date "next Tuesday" received on a Tuesday | Flagged as AMBIGUOUS; escalated |
| Overnight shift (19:00–07:00) | overnight=true; no error |
| Credential not in taxonomy ("TCAR") | Stored in unresolved_credentials; escalated |
| Same hospital submits duplicate shift request | Two separate ShiftRequests created; deduplication is out of scope (coordinator notices via dashboard) |
| Email with no shift date ("ASAP") | shift_date=null; escalated; urgency=EMERGENCY set independently |
| Hospital email domain matches multiple registry entries | hospital_id=null; escalated with note |
| LLM returns partial response (token cutoff) | Affected fields null; escalated; partial data preserved in raw_input |

### 2.3 Failure Modes

| Failure | Impact | Mitigation |
|---------|--------|------------|
| LLM prompt drift — model updates change extraction behaviour | Silent accuracy degradation; wrong fields extracted at high confidence | Weekly automated regression run against labelled test set; alert if accuracy drops >2% |
| LLM hallucinates a credential not in source text | Nurse proposed for shift she's not qualified for | Hard filter in Agent 2 catches credential mismatches; Agent 1 accuracy tracked separately |
| ServiceNow queue polling fails silently | Shift requests not processed; hospital waits indefinitely | Heartbeat monitor on queue depth; alert if no new items processed in 30 minutes during business hours |
| Hospital registry stale (new hospital not yet added) | hospital_id=null; every request from that hospital escalates | Aaron to confirm registry update SLA before Phase 1 go-live |
| Preview queue timer not firing | Records stuck in PENDING_REVIEW; never reach Agent 2 | Heartbeat check on records older than 10 minutes in PENDING_REVIEW; alert on-call |

---

## 3. Agent 2 — Shift Matching Validation

### 3.1 Accuracy Targets

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| Hard filter false positive rate | 0% — no proposals for nurses failing any hard filter criterion | Automated test: inject nurses with expired compliance and mismatched credentials; verify they never appear in proposals |
| Confidence score calibration | AUTO_SUBMIT proposals (>0.85) should have ≤ 3% mismatch rate after 30-day Phase 1 | Shadow review flag rate tracked daily; if >3% → pause AUTO_SUBMIT |
| Routing accuracy | 100% of proposals with confidence <0.70 routed to HUMAN_ESCALATE | Automated test: score override to force each routing band; verify correct routing |
| Reservation collision rate | 0% double-booking incidents | Monitor NurseReservation conflicts; any confirmed double-booking = P1 incident |
| NO_MATCH false rate | < 5% of NO_MATCH escalations have a viable nurse available in retrospect | Coordinator feedback loop: when coordinator manually matches after NO_MATCH, log whether Agent 2 missed a valid candidate |

### 3.2 Edge Cases to Test

| Case | Expected Behaviour |
|------|--------------------|
| All nurses fail hard filter | NO_MATCH escalation with breakdown; no proposal sent |
| Two nurses have identical confidence score | Tie-break by reliability → distance → nurse_id; deterministic result |
| Nurse availability changes between filter and reservation lock | Reservation fails; agent moves to next-ranked nurse |
| Hospital preference store empty (Phase 1) | Default 0.50 applied; noted in score_breakdown; no error |
| Distance API unavailable | Proximity score 0.40 (neutral); warning logged; match proceeds |
| ASSUMED credential in ShiftRequest (from Agent 1 ambiguity) | Hard filter applied on ASSUMED credential; flag noted in proposal rationale |
| Nurse reliability_score null (new nurse) | Default 0.60 applied; NEW_NURSE flag in rationale |

### 3.3 Failure Modes

| Failure | Impact | Mitigation |
|---------|--------|------------|
| Confidence threshold miscalibrated | Too many HUMAN_ESCALATE → coordinator bottleneck returns; too many AUTO_SUBMIT → mismatch rate rises | 30-day shadow review with explicit 3% flag rate gate; threshold adjustable without code deploy |
| Hospital preference data never populated | 25% of score is always default 0.50; quality ceiling lower than designed | Kim and coordinators must input historical preference data before Phase 2; flagged as Phase 1 assumption |
| Nurse availability data stale (>24h lag) | Proposals sent for unavailable nurses; hospital accepts; nurse declines last minute | Confirmation loop (Agent 3) catches this before shift; but increases coordinator workload. Confirm staleness SLA with Kim before go-live |
| Reservation database unavailable | Agent cannot lock nurse; cannot safely submit proposal | Hold proposals in PENDING_RESERVATION queue; retry 5 minutes; escalate if unresolved. Do not submit without a lock. |
| Soft scoring weights wrong for MedFlex context | Proximity weighted too high; hospital preference too low; matches technically valid but hospitals reject more | Track hospital acceptance/rejection rate per routing band; recalibrate weights after 30 days of data |

### 3.4 Phase 1 Calibration Gates

Before removing Phase 1 shadow review and moving to Phase 2:

| Gate | Threshold | Action if failed |
|------|-----------|-----------------|
| AUTO_SUBMIT mismatch rate | < 3% over 30 days | Raise confidence threshold to 0.90; investigate scoring weights |
| ASYNC_REVIEW coordinator recall rate | < 10% | If high: revert ASYNC_REVIEW to synchronous approval for specific credential types |
| NO_MATCH rate | < 15% of daily volume | If high: supply-side gap; alert Kim; do not lower confidence threshold |
| Coordinator adoption of dashboard | > 80% of ASYNC_REVIEW proposals reviewed within 30 min | If low: Marcus to drive adoption; consider push notification escalation |

---

## 4. Agent 3 — Confirmation & No-Show Prevention Validation

### 4.1 Accuracy Targets

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| Notification delivery rate | ≥ 98% delivered within 5 minutes of assignment creation | Gateway delivery receipts; alert if rate drops below 95% |
| Confirmation rate | ≥ 85% of nurses explicitly confirm within 24h | Track CONFIRMED transitions; baseline against current 0% explicit confirmation |
| Ambiguous reply rate | < 5% of all replies | Monitor AMBIGUOUS_REPLY escalation rate; if high, expand classification rules |
| No-show rate (post-Phase 2) | < 7% (down from 12%) | Compare against pre-launch baseline; track monthly |
| Emergency re-match success rate | > 70% of no-shows result in a placed replacement nurse | Track NO_SHOW → ACCEPTED transitions in Agent 2 |

### 4.2 Edge Cases to Test

| Case | Expected Behaviour |
|------|--------------------|
| Nurse replies after confirmation deadline but before shift | Accept as confirmation if shift not yet started; log late confirmation |
| Two replies from same nurse (e.g., "Yes" then "No") | Last reply wins; log both; alert coordinator if reversal is post-confirmation |
| Hospital accepts within 2 hours of shift start | confirmation_deadline shortened to 30 minutes; escalation triggered faster |
| No-show reported after shift end time | Log reliability event; no re-match triggered |
| Nurse cancels by phone but coordinator doesn't log it | Agent has no signal; sends T-2h alert to nurse who already cancelled; coordinator receives both alert and no-show risk — gap acknowledged in spec (Phase 2 process dependency) |
| Emergency re-match: Agent 2 returns NO_MATCH | Coordinator receives both no-show alert and NO_MATCH notification; manual sourcing required |

### 4.3 Failure Modes

| Failure | Impact | Mitigation |
|---------|--------|------------|
| SMS gateway outage | Nurses not notified; silent no-show risk returns | Retry logic + delivery failure escalation to coordinator; dual-channel fallback requires coordinator override (cannot auto-switch) |
| Nurses don't reply to SMS confirmation requests | Confirmation rate stays low; T+24h escalations flood coordinator queue | Monitor confirmation rate weekly; if <70% after 30 days, consider simplifying reply mechanism (one-click portal link instead of SMS reply) |
| State machine timer not firing (system failure) | Assignment stuck in PENDING_CONFIRMATION; nurse never chased | Heartbeat check every 15 minutes; alert on-call if any assignment in PENDING_CONFIRMATION for >25h without transition |
| Coordinator doesn't act on UNCONFIRMED_ESCALATED | Nurse unconfirmed; potential no-show undetected | Push notification + escalation reminder at 20-minute inactivity; track unactioned escalation rate |
| Phone cancellation not logged by coordinator | Agent sends pre-shift alert to cancelled nurse; wasted contact; hospital may receive confirmed assignment for no-show | Process enforcement: coordinator team lead tracks phone cancellation logging compliance; flagged metric |

---

## 5. Integration Validation

### 5.1 ServiceNow

| Risk | Mitigation |
|------|------------|
| API access not confirmed (Aaron TBD) | Confirm API credentials and rate limits with Aaron before Phase 1 build begins |
| ServiceNow rate limits trigger 429 during peak hours | Implement Retry-After handling; test at 2× expected peak volume |
| ShiftRequest write-back fails silently | Confirm write operation with read-back verification in staging |

### 5.2 Nurse Database

| Risk | Mitigation |
|------|------------|
| Availability data lag >24h (Kim TBD) | Confirm actual lag with Kim; if >24h, add staleness warning to every proposal |
| Credential data schema differs from spec | Aaron to confirm schema before Agent 2 hard filter is built; mock data in Phase 1 staging |
| Read-only access confirmed but not tested at load | Load test with 10× daily query volume before Phase 1 go-live |

### 5.3 Hospital Portal / Email Gateway

| Risk | Mitigation |
|------|------------|
| Hospital portal submission API not available for all hospitals | Confirm with Aaron which hospitals use portal vs. email; email submission path must be validated separately |
| Proposal format rejected by hospital portal | Test with each hospital's portal in staging before Phase 1 go-live |

---

## 6. Compliance and Regulatory Risk

### 6.1 Credential Check Automation

| Risk | Detail | Mitigation |
|------|--------|------------|
| State law requires human sign-off on credential verification | Some states may prohibit fully automated credential checks for healthcare staffing | Confirm with Linda before Phase 1 go-live; Agent 2 reads credential data, does not re-verify — this distinction must be documented and defensible |
| Credential data pulled from internal store, not state portal | Internal data may be stale or incorrect; agent proposes nurse with lapsed credential | Confirm re-verification cadence with Linda; add compliance_valid_until staleness check in Agent 2 |
| State regulatory requirements differ across 5 states | Credential requirements vary by state; single taxonomy may not cover all states | Linda to review credential taxonomy against each state's requirements before Phase 1 |

### 6.2 Data Privacy

| Risk | Detail | Mitigation |
|------|--------|------------|
| Nurse PII processed by LLM (Agent 1) | Hospital emails may contain nurse names or patient references | Confirm with Aaron whether LLM API processes data outside the US; if so, review HIPAA BAA requirement |
| Coordinator dashboard exposes nurse reliability scores | Reliability scores constitute employment-relevant data | Confirm with Linda/legal whether reliability score display requires consent or union agreement |
| Audit logs retained indefinitely | ShiftRequest raw_input stores original hospital email verbatim | Define retention policy with Aaron before Phase 1; default to 90-day rolling retention |

### 6.3 Regulatory Drift

| Risk | Detail | Mitigation |
|------|--------|------------|
| State adds new mandatory credential requirement | Agent 2 hard filter misses the new requirement; non-compliant nurse proposed | Quarterly review of credential taxonomy against state regulatory updates; Linda owns this process |
| State portal rate limits change | Agent 1 or Agent 2 credential lookups start failing or being throttled | Monitor API response codes; alert on 429 rate increase; Aaron to maintain API agreements |

---

## 7. Model Accuracy Drift

| Risk | Detection | Response |
|------|-----------|----------|
| LLM model update changes extraction behaviour (Agent 1) | Weekly regression run against 200-email labelled test set; alert if accuracy drops >2% | Freeze model version; evaluate new version against test set before promoting |
| Confidence score distribution shifts over time (Agent 2) | Track routing band distribution weekly; alert if AUTO_SUBMIT share drops >10% or NO_MATCH share rises >5% | Re-examine scoring weights; check for upstream data changes (availability staleness, compliance data quality) |
| Hospital preference data grows stale | Preference scores reflect old matching patterns; hospital preferences change | Recency-weight preference score: interactions >6 months old contribute at 50%; >12 months at 25% |
| Reliability score not updated after no-shows (Agent 3) | Unreliable nurses keep high reliability scores; matched repeatedly | Confirm reliability_event consumption by the external reliability scoring system; test end-to-end in staging |

---

## 8. Single Points of Failure

| Component | Failure Mode | Impact | Mitigation |
|-----------|-------------|--------|------------|
| LLM API (Agent 1) | Outage | All intake parsing stops; no new ShiftRequests created | Queue incoming messages; process when API recovers; alert coordinator team that intake is paused |
| Reservation database (Agent 2) | Outage | Cannot lock nurses; cannot safely submit proposals | Hold proposals; do not submit without lock; alert on-call |
| SMS/email gateway (Agent 3) | Outage | Nurses not notified; confirmation loop silent | Coordinator manually contacts nurses for all active assignments; alert team lead |
| ServiceNow queue (Agent 1) | Outage | Shift requests not ingested | Hospitals can submit directly to coordinator as fallback; alert Aaron |
| Coordinator dashboard | Outage | ASYNC_REVIEW proposals unreviewed; escalations unseen | Send escalations via push notification to coordinator mobile as backup channel |
| Single on-call coordinator | Overwhelmed by simultaneous escalations | Multiple unactioned escalations during peak hours | Define escalation routing: primary + secondary coordinator per shift; never single point |

---

## 9. Validation Timeline

| Phase | Validation Activity | Owner | Gate |
|-------|---------------------|-------|------|
| Pre-Phase 1 | Confirm ServiceNow API access and nurse DB schema | Aaron | Must complete before build |
| Pre-Phase 1 | Confirm credential taxonomy against state requirements | Linda | Must complete before Phase 1 go-live |
| Pre-Phase 1 | Confirm availability data staleness SLA | Kim | Must complete before Phase 1 go-live |
| Phase 1 (Weeks 1-8) | Shadow review calibration: track AUTO_SUBMIT flag rate daily | Coordinator team | <3% flag rate = gate to Phase 2 |
| Phase 1 (Weeks 1-8) | Weekly LLM regression run: Agent 1 parsing accuracy | Engineering | Alert if accuracy drops >2% |
| Phase 1 (Weeks 1-8) | Dashboard adoption tracking: ASYNC_REVIEW review rate | Marcus/Kim | >80% reviewed in 30 min = Phase 2 prerequisite |
| Phase 2 entry | No-show rate baseline established (pre-Agent 3) | Operations | Baseline required to measure Phase 2 impact |
| Phase 2 (Weeks 9-16) | Confirmation rate tracking: % explicit confirmations | Agent 3 metrics | <85% → review nurse UX |
| Phase 2 (Weeks 9-16) | No-show rate: compare to pre-Phase 2 baseline | Operations | Target <7% by Week 16 |
| Phase 3 entry | Reputation model accuracy: does preference score predict acceptance? | Engineering | Validate before lowering confidence thresholds further |
