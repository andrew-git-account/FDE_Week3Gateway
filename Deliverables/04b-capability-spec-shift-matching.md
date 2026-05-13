# Capability Spec: Agent 2 — Shift Matching Agent

**Client:** MedFlex Healthcare Staffing  
**Version:** 1.0 — Thursday interim draft  
**Prepared by:** Andrzej Bihun

> **Shared entity definitions** (ShiftRequest, NurseProfile, Credential Taxonomy) are in `04a-capability-spec-intake-parsing.md`. This spec extends those definitions with matching-specific entities.

---

## Additional Entities

### MatchProposal
| Field | Type | Constraints |
|-------|------|-------------|
| `id` | UUID | System-generated |
| `shift_request_id` | UUID | FK → ShiftRequest.id |
| `nurse_id` | UUID | FK → NurseProfile.nurse_id |
| `confidence_score` | float | 0.00–1.00; two decimal places |
| `routing` | enum | `AUTO_SUBMIT` \| `ASYNC_REVIEW` \| `HUMAN_ESCALATE` \| `NO_MATCH` |
| `score_breakdown` | object | See §2.2 |
| `status` | enum | `PROPOSED` \| `ACCEPTED` \| `REJECTED` \| `RECALLED` \| `EXPIRED` \| `SHADOW_REVIEW` |
| `proposed_at` | timestamp (UTC) | Set when submitted to hospital |
| `reservation_expires_at` | timestamp (UTC) | `proposed_at + 15 minutes` |
| `recall_window_expires_at` | timestamp (UTC) | `proposed_at + 90 minutes` |
| `hospital_response_at` | timestamp? | null until hospital responds |
| `reviewing_coordinator_id` | string? | null unless ASYNC_REVIEW routing |
| `shadow_review_flag` | boolean | true during Phase 1 for AUTO_SUBMIT proposals |

### NurseReservation
| Field | Type | Constraints |
|-------|------|-------------|
| `nurse_id` | UUID | FK → NurseProfile |
| `reserved_for_proposal_id` | UUID | FK → MatchProposal.id |
| `reserved_at` | timestamp (UTC) | |
| `expires_at` | timestamp (UTC) | `reserved_at + 15 minutes` |
| `status` | enum | `ACTIVE` \| `CONFIRMED` \| `EXPIRED` \| `RELEASED` |

### HospitalPreference
| Field | Type | Constraints |
|-------|------|-------------|
| `hospital_id` | string | |
| `nurse_id` | UUID | |
| `acceptance_count` | int | Total past acceptances |
| `rejection_count` | int | Total past rejections |
| `preference_score` | float | 0.00–1.00; computed as acceptance_count / (acceptance_count + rejection_count); null if no history |
| `last_interaction_date` | date | |

---

## Constraints (Read First!)

**DO:**
- Apply hard filters first; discard non-qualifying nurses before soft scoring
- Acquire a NurseReservation lock before submitting any MatchProposal to the hospital
- Release the NurseReservation immediately if the proposal is rejected or the lock expires
- Set `shadow_review_flag=true` for all AUTO_SUBMIT proposals during Phase 1 (first 30 days)
- Log the full `score_breakdown` for every evaluated nurse, including those that fail hard filters
- Surface ranked candidates with rationale for HUMAN_ESCALATE routing — do not pick for the coordinator
- Escalate to NO_MATCH with an explanation if no nurses pass the hard filter

**DO NOT:**
- Submit a proposal for a nurse whose `compliance_valid_until` date falls before the shift date
- Submit a proposal for a nurse with an active NurseReservation for another proposal
- Auto-submit proposals where `confidence_score < 0.70`
- Apply soft scoring weights without the hard filter pass — soft scoring never overrides a hard filter failure
- Retry a failed proposal submission by automatically selecting the second-ranked nurse; re-route to HUMAN_ESCALATE instead

---

## Requirement 1: Hard Filter

### Description
Before scoring, eliminate all nurses who fail any mandatory criterion. A nurse failing the hard filter is logged with the specific failure reason but never surfaced to the coordinator unless all candidates fail (NO_MATCH case).

### Hard Filter Criteria (all must pass)
| Criterion | Check |
|-----------|-------|
| Credential match | Every entry in `ShiftRequest.required_credentials` (CONFIRMED) must appear in `NurseProfile.credentials` |
| Compliance valid | `NurseProfile.compliance_valid_until ≥ ShiftRequest.shift_date` |
| Availability | `ShiftRequest.shift_date` and time range falls within an `AvailabilitySlot` in NurseProfile |
| Not already reserved | No active NurseReservation for this nurse at this time |

### Worked Examples

**Example 1 — Pass:**
```
ShiftRequest: requires ["RN", "ACLS", "ICU"], shift_date=2026-06-12
NurseProfile: credentials=["RN", "ACLS", "ICU", "BLS"], compliance_valid_until=2027-01-01, available 2026-06-12 07:00-19:00
Result: PASS — proceeds to soft scoring
```

**Example 2 — Credential fail:**
```
ShiftRequest: requires ["RN", "ACLS", "ICU"]
NurseProfile: credentials=["RN", "BLS"] (ACLS and ICU missing)
Result: FAIL — logged as CREDENTIAL_MISMATCH; excluded from soft scoring
```

**Example 3 — Compliance expiry fail:**
```
ShiftRequest: shift_date=2026-06-12
NurseProfile: compliance_valid_until=2026-05-31
Result: FAIL — logged as COMPLIANCE_EXPIRED; excluded
```

**Example 4 — All nurses fail hard filter:**
```
0 nurses pass hard filter for this ShiftRequest
Result: routing=NO_MATCH; escalation payload lists: total_evaluated=14, failure_breakdown={CREDENTIAL_MISMATCH:9, COMPLIANCE_EXPIRED:3, UNAVAILABLE:2}
```

### Edge Cases
| Scenario | Behaviour |
|----------|-----------|
| ASSUMED credential in ShiftRequest (from Agent 1) | ASSUMED credentials are NOT hard filter criteria — they reduce soft scoring confidence only. Coordinator sees assumed credentials in the proposal rationale and can override soft scoring. Do not exclude nurses for missing ASSUMED credentials. |
| Nurse marks themselves unavailable mid-filter (race condition) | Re-check availability at reservation lock time; if now unavailable, release and re-rank |
| compliance_valid_until is today and shift is today | Pass — valid on shift date means same-day is permitted |
| NurseProfile.credentials contains a superset credential (e.g., CCRN implies ICU) | Treat as satisfying the ICU requirement; log the mapping |

---

## Requirement 2: Soft Scoring

### Description
Score each nurse who passes the hard filter on four dimensions. Compute a weighted sum. The result becomes `confidence_score`. Weights are configurable but defaults are defined here.

### Scoring Components

| Component | Weight | How Calculated |
|-----------|--------|----------------|
| Proximity | 0.30 | Distance from nurse home zip to hospital zip; 0→≤5 miles: 1.0, 5→15 miles: 0.75, 15→30 miles: 0.50, 30→50 miles: 0.25, >50 miles: 0.0 |
| Hospital preference | 0.25 | `HospitalPreference.preference_score` for this (hospital, nurse) pair; 0.50 if no history |
| Nurse reliability | 0.25 | `NurseProfile.reliability_score` (computed externally; read-only) |
| Specialty fit | 0.20 | Exact specialty match: 1.0; related specialty: 0.50; no specialty data: 0.40 |

**confidence_score = Σ (component_score × weight)**

### Worked Examples

**Example 1 — Strong match:**
```
Proximity: 8 miles → 0.75 × 0.30 = 0.225
Hospital preference: 0.90 (accepted 9 of 10 past proposals) × 0.25 = 0.225
Reliability: 0.88 × 0.25 = 0.220
Specialty: exact ICU match → 1.0 × 0.20 = 0.200
confidence_score = 0.870 → routing=AUTO_SUBMIT
```

**Example 2 — No preference history:**
```
Proximity: 3 miles → 1.0 × 0.30 = 0.300
Hospital preference: no history → 0.50 × 0.25 = 0.125
Reliability: 0.72 × 0.25 = 0.180
Specialty: related (MedSurg for Telemetry shift) → 0.50 × 0.20 = 0.100
confidence_score = 0.705 → routing=ASYNC_REVIEW
```

**Example 3 — Low reliability, far distance:**
```
Proximity: 45 miles → 0.25 × 0.30 = 0.075
Hospital preference: 0.60 × 0.25 = 0.150
Reliability: 0.55 × 0.25 = 0.138
Specialty: exact match → 1.0 × 0.20 = 0.200
confidence_score = 0.563 → routing=HUMAN_ESCALATE
```

### Edge Cases
| Scenario | Behaviour |
|----------|-----------|
| Distance API unavailable | Set proximity score to 0.40 (neutral); flag in score_breakdown; log warning |
| HospitalPreference record does not exist | Use default 0.50; note "no history" in rationale |
| Two nurses have identical confidence_score | Break tie by: (1) higher reliability_score, (2) lower distance, (3) nurse_id alphabetically |
| reliability_score is null (new nurse) | Use 0.60 as default; flag as NEW_NURSE in rationale |

---

## Requirement 3: Confidence Routing

### Description
After scoring, select the top-ranked nurse and apply routing based on `confidence_score`. Routing determines whether the proposal is auto-submitted, submitted with a coordinator alert, or escalated to human decision.

### Routing Rules

| confidence_score | Routing | Action |
|-----------------|---------|--------|
| > 0.85 | `AUTO_SUBMIT` | Submit proposal to hospital immediately; set shadow_review_flag=true in Phase 1 |
| 0.70–0.85 | `ASYNC_REVIEW` | Submit proposal to hospital; send async alert to coordinator with 90-minute recall window |
| < 0.70 | `HUMAN_ESCALATE` | Do not submit; surface top 3 ranked nurses to coordinator with full score_breakdown |
| 0 nurses pass hard filter | `NO_MATCH` | Escalate with failure breakdown; do not submit |

### Phase 1 Shadow Review (first 30 days)
For every `AUTO_SUBMIT` proposal:
- Set `shadow_review_flag=true`
- Write to coordinator audit log with full score_breakdown
- Coordinator can flag an error within 90 minutes (non-blocking — proposal has already been sent)
- Track: flagged_count / total_auto_submit per week; if rate exceeds 3% in any 7-day window → alert on-call and pause AUTO_SUBMIT pending review
- **Leading signals (visible from week 2):** weekly coordinator flag rate trend + hospital acceptance rate per band. These provide drift visibility before any mismatch report arrives. Do not treat the 30-day gate as the only signal.
- Shadow review removed after 30 days if mismatch rate < 3% AND weekly flag rate has been flat or declining for the last 2 weeks

### Worked Examples

**Example 1 — AUTO_SUBMIT:**
```
confidence_score=0.870 → submit to hospital immediately
Shadow review: log to audit trail; coordinator notified (non-blocking)
reservation_expires_at = now + 15 minutes
```

**Example 2 — ASYNC_REVIEW:**
```
confidence_score=0.740 → submit to hospital
Coordinator alert: "MEDIUM confidence proposal submitted — recall window open until [timestamp]"
recall_window_expires_at = proposed_at + 90 minutes
```

**Example 3 — HUMAN_ESCALATE:**
```
confidence_score=0.563 → do not submit
Dashboard: surface top 3 nurses with score_breakdown for each
Coordinator sees: Nurse A (0.563), Nurse B (0.541), Nurse C (0.498) with rationale per candidate
```

---

## Requirement 4: Nurse Reservation (Soft Lock)

### Description
Before submitting a proposal to a hospital, acquire a NurseReservation lock on the selected nurse. The lock prevents the nurse from being proposed to another hospital during the 15-minute window. If the lock cannot be acquired (nurse already reserved), select the next-ranked nurse.

### Process Steps
1. Select top-ranked nurse from soft scoring
2. Attempt to create NurseReservation record:
   - Check: no active NurseReservation exists for this nurse at this time
   - If clear: write NurseReservation with `status=ACTIVE`, `expires_at = now + 15 minutes`
   - If blocked: move to next-ranked nurse; repeat
3. If no nurse can be reserved (all reserved): set `routing=NO_MATCH` temporarily; retry in 5 minutes once; if still blocked → HUMAN_ESCALATE
4. Submit proposal to hospital
5. On hospital acceptance: set `NurseReservation.status=CONFIRMED`; create NurseAssignment
6. On hospital rejection OR lock expiry: set `NurseReservation.status=RELEASED`; nurse becomes available again

### Worked Examples

**Example 1 — Clean lock:**
```
Nurse A selected; no active reservation found
NurseReservation created: reserved_at=14:00:00, expires_at=14:15:00, status=ACTIVE
Proposal submitted to hospital
```

**Example 2 — Nurse already reserved:**
```
Nurse A selected; active reservation found (reserved for Hospital B until 14:12:00)
Move to Nurse B (next ranked); check reservation → clear
NurseReservation created for Nurse B
```

**Example 3 — Race condition (two hospitals accept same nurse):**
```
Hospital A and Hospital B both accept Nurse A within the same 15-minute window
Hospital A accepted first → NurseReservation.status=CONFIRMED for Hospital A proposal
Hospital B acceptance arrives → NurseReservation already CONFIRMED for different proposal
Action: notify Hospital B coordinator and Hospital B that placement is in conflict; re-trigger Agent 2 for Hospital B as HUMAN_ESCALATE
```

### Edge Cases
| Scenario | Behaviour |
|----------|-----------|
| Reservation expires before hospital responds | NurseReservation.status=EXPIRED; nurse released; if hospital later accepts, treat as conflict — notify coordinator |
| Reservation database write fails | Do not submit proposal; retry once; if fails again → HUMAN_ESCALATE |
| Two agents attempt to reserve the same nurse simultaneously | Database row-level lock ensures only one succeeds; second agent moves to next-ranked nurse |

---

## Requirement 5: Coordinator Recall (ASYNC_REVIEW)

### Description
For ASYNC_REVIEW proposals, the coordinator has a 90-minute recall window after the proposal is submitted. The 90-minute window reflects Kim's operational input: coordinators batch-check the ServiceNow queue every 1–2 hours during volume spikes; a 30-minute window would expire unreviewed during the busiest part of the day. Recalling a proposal cancels it with the hospital and releases the nurse reservation.

### Process Steps
1. Proposal submitted at `proposed_at`; `recall_window_expires_at = proposed_at + 90 minutes`
2. Push notification sent to assigned coordinator: proposal details + link to recall action
3. If coordinator recalls within window:
   - Set `MatchProposal.status=RECALLED`
   - Release NurseReservation
   - Send cancellation to hospital: "We are revising our proposal — updated recommendation within [X] minutes"
   - Re-trigger matching for this ShiftRequest with coordinator override flag
4. If window expires unreviewed (coordinator did not open the proposal before `recall_window_expires_at`): set `status=LAPSED_UNREVIEWED`; escalate to team lead with proposal details; team lead has 15 minutes to intervene or proposal is finalised. Do NOT log as coordinator-cleared — unreviewed ≠ approved.
5. If coordinator dashboard is unreviewed for > 45 minutes during business hours: send escalation reminder to coordinator (not team lead; first-level nudge)

### Edge Cases
| Scenario | Behaviour |
|----------|-----------|
| Hospital accepts before coordinator recalls | Status=ACCEPTED takes precedence; recall window closes; notify coordinator that recall is no longer possible |
| Coordinator tries to recall after hospital accepted | Return error: "Recall window closed — hospital has accepted. Contact coordinator for manual resolution." |
| Coordinator dashboard not accessed for entire 90 minutes | Status=LAPSED_UNREVIEWED; escalate to team lead; do not log as coordinator-cleared; track LAPSED_UNREVIEWED rate; alert team lead if >15% of ASYNC_REVIEW proposals lapse unreviewed |
| Coordinator reviews but does not recall within window | Counts as reviewed (coordinator saw the proposal and accepted it); log as REVIEWED_NO_ACTION |

---

## API Failure Modes

| Failure | Detection | Response |
|---------|-----------|----------|
| Nurse database timeout (>5s) | Request timer | Retry 3× with backoff; if all fail → HUMAN_ESCALATE with note: "Nurse data unavailable" |
| Compliance store returns stale data (>24h) | Timestamp check on record | Flag proposal with STALE_COMPLIANCE warning; still submit but add to coordinator alert |
| Hospital portal submission timeout | Request timer (10s) | Retry 2×; if fails → set status=SUBMISSION_FAILED; alert coordinator to submit manually |
| Hospital portal returns 500 | HTTP status | Same as timeout |
| Hospital portal returns 401 | HTTP status | Alert on-call immediately; do not retry |
| Distance API unavailable | Connection error | Use proximity score 0.40 (neutral); log WARNING |
| Reservation database unavailable | Connection error | Do not submit proposal; hold in PENDING_RESERVATION queue; retry every 30s for 5 minutes; escalate if unresolved |

---

## Observability

**Log on every match attempt:**
```
level=INFO fields: shift_request_id, nurses_evaluated, nurses_passed_hard_filter, top_nurse_id, confidence_score, routing, reservation_acquired, duration_ms
```

**Log on every hard filter failure:**
```
level=DEBUG fields: shift_request_id, nurse_id, failure_reason
```

**Metrics to track:**
- `matching.confidence_score.histogram` — distribution (target: >60% of proposals in AUTO_SUBMIT band)
- `matching.routing_distribution` — % AUTO_SUBMIT / ASYNC_REVIEW / HUMAN_ESCALATE / NO_MATCH
- `matching.reservation_conflict_rate` — % proposals where first-choice nurse was already reserved
- `matching.shadow_review_flag_rate` — % of AUTO_SUBMIT proposals flagged by coordinators (Phase 1 only; target <3%)
- `matching.match_duration_ms` — end-to-end latency per ShiftRequest (target p95 < 30s)
- `matching.hospital_acceptance_rate_by_band.weekly` — hospital acceptance rate per routing band (AUTO_SUBMIT / ASYNC_REVIEW), trended weekly. A declining acceptance rate in the AUTO_SUBMIT band is a **leading drift indicator** visible from week 2; does not require waiting for a mismatch report from the hospital.
- `matching.coordinator_flag_rate_by_week` — shadow review flag count per week, not aggregated to 30-day total. A rising weekly flag rate triggers review well before the 30-day gate. Target: flat or declining week-over-week from week 3 onward.
- `matching.async_review_lapsed_unreviewed_rate` — % of ASYNC_REVIEW proposals that expire with status=LAPSED_UNREVIEWED (target <10%)

**Alerts:**
- Shadow review flag rate > 3% in any 7-day window (Phase 1) → pause AUTO_SUBMIT; alert on-call
- Hospital acceptance rate in AUTO_SUBMIT band declines >5 percentage points week-over-week → alert on-call (leading drift signal; do not wait for mismatch report)
- Weekly coordinator flag count doubles vs. prior week → alert on-call (early calibration signal)
- NO_MATCH rate > 20% over any 2-hour window → alert coordinator team lead (supply shortage signal)
- ASYNC_REVIEW lapsed_unreviewed rate > 15% → alert team lead

---

## Acceptance Criteria

- [ ] **Hard filter:** 0% of proposals submitted for nurses with expired compliance or missing required credentials
- [ ] **Confidence routing:** 100% of proposals with confidence_score < 0.70 are routed to HUMAN_ESCALATE (never auto-submitted)
- [ ] **Reservation:** 0% double-booking incidents (same nurse accepted by two hospitals for overlapping shifts)
- [ ] **Phase 1 shadow review:** flag rate < 3% after 30-day calibration before shadow review is removed
- [ ] **Latency:** match completed and proposal submitted within 60 seconds of ShiftRequest release for p95
- [ ] **Audit:** every evaluated nurse logged with score_breakdown; every routing decision traceable
- [ ] **Error handling:** all API failure modes tested with mock failures; no silent failures
