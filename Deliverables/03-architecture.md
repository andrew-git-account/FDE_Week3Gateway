# D#3 — Agentic Solution Architecture

**Client:** MedFlex Healthcare Staffing  
**Engagement:** AI-native shift matching transformation  
**Prepared by:** Andrzej Bihun | Thursday interim draft

---

## 1. Architecture Overview

Three agents operating in sequence, with a coordinator oversight layer that handles exceptions and medium-confidence cases. The agents are the primary mechanism for all standard shift matching — coordinators are supervisors, not decision-makers for routine work.

```
Hospital Request (email/portal/phone)
        │
        ▼
┌──────────────────────┐
│  Agent 1: Intake     │  Agent-Led + Human Oversight
│  Parsing             │  Free text → structured shift record (5-min preview)
└──────────┬───────────┘
           │ Structured ShiftRequest
           ▼
┌──────────────────────┐
│  Agent 2: Shift      │  Confidence-gated delegation
│  Matching            │  HIGH → auto-propose to hospital
└──────────┬───────────┘  MEDIUM → propose + coordinator alert
           │              LOW → escalate to coordinator
           │ (on hospital acceptance)
           ▼
┌──────────────────────┐
│  Agent 3:            │  Fully Agentic (standard)
│  Confirmation &      │  Human-Led (conflict/no-confirm)
│  No-Show Prevention  │
└──────────────────────┘

Coordinator Oversight Dashboard: async review queue, escalation inbox, audit trail
```

---

## 2. Agent Definitions

### Agent 1 — Intake Parsing Agent

**Job to be done:** Transform unstructured shift requests into structured ShiftRequest records that Agent 2 can act on.

**Why agentic:** Hospital emails use varied formats, abbreviations, and implicit credential requirements. A rule-based parser would require hospital-specific templates. LLM handles variability.

**Delegation:** Agent-Led + Human Oversight  
**Trigger:** New item enters ServiceNow queue (email/portal/phone captured)  
**Output:** Structured ShiftRequest (shift date/time, location, required credentials, specialty, hospital ID, urgency)  
**Oversight mechanism:** Parsed ShiftRequest enters a 5-minute coordinator preview queue before releasing to matching. If untouched in 5 minutes, proceeds automatically. Coordinator can correct any field before matching begins.  
**Rationale for downgrade from Fully Agentic:** A confident wrong parse (e.g., "ICU RN with ACLS" read as generic RN) produces no escalation signal but drives the entire downstream pipeline — Agent 2 will match the wrong nurse at high confidence. The error is invisible at source and attributed to the matching agent. The 5-minute preview catches this at zero speed cost against the 4.2h baseline.  
**Escalation trigger:** Confidence in parsed output <80%, or required fields cannot be extracted → flag for coordinator to clarify with hospital directly  

---

### Agent 2 — Shift Matching Agent

**Job to be done:** Find the best-qualified nurse for a shift, score match confidence, and route to hospital or coordinator based on confidence level.

**Why agentic:** Matching is multi-dimensional — credentials, availability, proximity, hospital preference history, nurse reputation, compliance status, soft signals from past interactions. A rule-based system handles the credential filter; it cannot handle the contextual weighting. The agent encodes the senior coordinator's tacit judgment as replicable logic.

**Matching logic (in order):**
1. Hard filter: credentials match, compliance valid on shift date, nurse marked available
2. Soft scoring: proximity (weighted), hospital preference for nurse (from past matches), nurse reliability history, specialty fit
3. Concurrency check: nurse not currently soft-reserved for another hospital
4. Confidence score calculated; routing decision applied

**Delegation by confidence:**

| Confidence | Delegation | Action |
|------------|------------|--------|
| >85% | Fully Agentic (Phase 2+) / Agent-Led shadow review (Phase 1) | Auto-submit proposal to hospital; log decision. Phase 1 only: coordinator sees all HIGH-confidence proposals in audit log and can flag errors within 90 min (non-blocking). Leading drift signals tracked weekly from week 2 (acceptance rate trend + flag rate). Shadow review removed after 30-day calibration. |
| 70-85% | Agent-Led + Human Oversight | Auto-submit; coordinator gets async alert with 90-min recall window; unreviewed expiry escalates to team lead, not auto-cleared |
| <70% | Human-Led + Agent Support | Agent surfaces ranked candidates with rationale; coordinator makes final decision |
| No viable match | Human Only | Escalate to coordinator with summary of why no match found |

**Key constraint:** Nurse must be soft-reserved at the moment of proposal (15-min lock). If hospital accepts, lock becomes confirmed assignment. If hospital rejects or lock expires, nurse released.

---

### Agent 3 — Confirmation & No-Show Prevention Agent

**Job to be done:** Ensure committed nurses show up by replacing silent acceptance with explicit confirmation and proactive follow-up.

**Why agentic:** Current process: notify nurse → assume accepted → find out at shift time if no-show. Agent introduces a confirmation state machine that detects risk before the shift.

**Confirmation state machine (happy path — Fully Agentic):**
- T+0: Hospital accepts → agent sends nurse confirmation request (SMS/email per preference)
- T+24h: No confirmation received → escalate to coordinator
- T-2h before shift: Confirmed nurse not yet acknowledged → alert coordinator
- No-show detected (hospital calls) → immediately open emergency replacement flow (re-triggers Agent 2)

**Failure mode handling (explicit):**

| Failure | Response |
|---------|----------|
| SMS/email delivery fails | Retry 3× over 30 min; if all fail → escalate to coordinator for manual nurse contact |
| Nurse cancels by phone (no system signal) | Requires coordinators to log phone cancellations in system; Agent 3 reads cancellation flag. This is a process change requirement for Phase 2 launch. |
| Ambiguous reply ("will try", "probably") | Flag as unconfirmed; escalate to coordinator for interpretation |
| State machine stops advancing (system failure) | Heartbeat check every 15 min; alert on-call if no state transition after expected window |
| Emergency re-match at T=0 | Agent 2 re-triggered immediately; coordinator notified in parallel; hospital told replacement is in progress (human coordinator makes that call) |

**Delegation:** Fully Agentic for happy path; Human-Led for any failure mode above

**Concurrency conflict resolution:** If two hospitals accept the same nurse before reservation expires (race condition), agent immediately notifies both coordinators. Second hospital gets escalated to human for manual re-match with priority queue.

---

## 3. Delegation Archetype Summary

| Workflow Step | Archetype | Rationale |
|---------------|-----------|-----------|
| Free-text intake parsing | Agent-Led + Human Oversight | 5-min coordinator preview before matching; bad parse cascades silently through entire pipeline if unchecked |
| HIGH-confidence matching | Fully Agentic (Phase 2+); shadow review Phase 1 | Phase 1 runs without preference data — threshold unvalidated until 30-day calibration confirms <3% mismatch |
| MEDIUM-confidence matching | Agent-Led + Human Oversight | Async coordinator review preserves quality without blocking speed |
| LOW-confidence matching | Human-Led + Agent Support | Agent narrows candidates; coordinator decides |
| Nurse confirmation follow-up | Fully Agentic | Deterministic state machine; no judgment required |
| No-show emergency re-match | Agent-Led + Human Oversight | Speed critical; coordinator validates before hospital told |
| Nurse re-credentialing | Human Only | Compliance team; out of scope |
| Hospital contract negotiation | Human Only | Commercial sensitivity; out of scope |

*Anti-pattern avoided: NOT everything is Fully Agentic. MEDIUM and LOW cases maintain human oversight where quality risk is real.*

---

## 4. Architecture Decision Records

### ADR-01: Confidence Threshold for Autonomous Proposal Submission

**Decision:** Set autonomous submission threshold at >85% confidence. 70-85% auto-submits with a 30-minute coordinator recall window.

**Context:** The core tension is speed vs. quality. MedFlex competes on response time; every minute of coordinator approval adds latency. But the 7% mismatch rate and hospital relationship risk mean unchecked auto-submission could increase mismatch.

**Alternatives considered:**

| Option | Pros | Cons |
|--------|------|------|
| A: All matches require coordinator approval | Zero mismatch risk | No throughput gain; defeats the engagement purpose |
| B: Auto-submit >70% confidence | Maximum speed; ~90% autonomous | Higher mismatch risk in 70-85% band; hospital trust damage |
| **C: Auto-submit >85%; async recall for 70-85%** | **Balances speed and quality; coordinator not blocked** | **Coordinator must respond within 30 min; requires dashboard adoption** |

**Decision rationale:** Option C gives Marcus the speed benefit immediately (HIGH confidence = ~60-65% of daily volume) while maintaining a human safety net for edge cases. The 30-minute window means hospital still gets a fast response; coordinator isn't in the critical path.

**Trade-offs accepted:** ~30-35% of matches still touch coordinator queue in Phase 1. This is intentional — trust must be built before lowering the threshold.

**Revisitation conditions:**
- If mismatch rate in HIGH-confidence band >5% after 30 days → raise threshold to 90%
- If <5% of matches fall in MEDIUM band → lower threshold to 80% (most coordinator tribal knowledge has been captured)
- If coordinator recall rate in MEDIUM band <2% → remove recall window; auto-submit all >70%

---

### ADR-02: Nurse Reservation Mechanism for Concurrent Hospital Submissions

**Decision:** Implement a soft time-lock reservation (15-minute window) when a nurse is proposed to a hospital. The lock prevents the same nurse being proposed elsewhere during the window.

**Context:** MedFlex submits the same nurses to multiple hospitals simultaneously (confirmed in discovery). At current scale (8 coordinators), conflicts are caught manually. At 10x scale, the same nurse could be accepted by two hospitals within seconds — with no automated resolution. Marcus had no answer for this when directly asked.

**Alternatives considered:**

| Option | Pros | Cons |
|--------|------|------|
| A: No reservation (current state) | No implementation complexity | Double-booking cascades; hospital gets confirmed nurse who won't show |
| B: Hard exclusive reservation | Eliminates double-booking | Serializes proposals; kills the "submit to multiple hospitals" speed advantage; coordinator workaround |
| **C: Soft time-lock (15 min)** | **Preserves parallel submission; prevents double-booking within window** | **15 min may not cover all hospital response latency; requires calibration** |
| D: Optimistic reservation with conflict compensation | Most flexible | Complex conflict resolution; hospital experience suffers |

**Decision rationale:** Option C solves the race condition without sacrificing the competitive strategy of parallel multi-hospital submission. The 15-minute window is an assumption — Aaron needs to confirm typical hospital acceptance latency before the window is finalized.

**Trade-offs accepted:** If a hospital takes >15 min to respond, the nurse could be re-proposed elsewhere. This is a known gap; the confirmation loop (Agent 3) catches post-acceptance conflicts.

**Revisitation conditions:**
- If >5% of conflicts occur outside the 15-minute window → extend to 30 min or introduce competing-hospital notification
- After 30 days of acceptance latency data from Aaron → recalibrate window

---

### ADR-03: Coordinator Oversight Model (Async vs. Synchronous) — **Revised after Marcus feedback**

**Decision:** Coordinator oversight of MEDIUM-confidence cases is asynchronous with a **90-minute recall window** (revised from 30 minutes). Original spec assumed continuous dashboard monitoring; Kim's operational input confirmed coordinators batch-check the queue every 1–2 hours during volume spikes.

**Context:** Synchronous approval kills the speed advantage. Async oversight maintains quality control without blocking the proposal. The window length is critical: too short and it expires before coordinators can act; treating an unreviewed expiry as implicit approval is a risk Marcus correctly identified.

**Alternatives considered:**

| Option | Pros | Cons |
|--------|------|------|
| A: Synchronous approval (block until reviewed) | Zero coordinator bypass | Adds latency; coordinator becomes bottleneck again |
| B: Async recall window (30 min) — original design | Hospital gets fast response | Expires during peak hours before coordinator batch-checks; 30 min < batch-check interval of 60–120 min |
| **C: Async recall window (90 min) + escalate on lapse** | **Matches real coordinator workflow; unreviewed = escalated, not approved** | **Hospital sees a slightly longer window before proposal finalises; still faster than current 4.2h baseline** |
| D: Post-submission audit only | No latency impact | No ability to correct before hospital sees the match |

**Decision rationale:** Option C is the right response to Kim's input. The 90-minute window covers at least one batch-check cycle. Crucially, an expired unreviewed proposal is now escalated to team lead — it is never silently logged as coordinator-cleared. This directly addresses Marcus's question: "What happens to the proposal when that window lapses unreviewed?"

**Trade-offs accepted:** A small number of proposals may have a longer time-to-confirmation (up to 90 min + 15 min team lead window vs. the original 30 min). For hospital response time this is still a 3–4× improvement over the 4.2h baseline. The lapse-escalation adds a new team lead workload that must be factored into staffing.

**Revisitation conditions:**
- If coordinator recall rate is high (>10% of MEDIUM proposals recalled within the 90-min window) → 90 min may not be long enough; consider extending or flagging specific hospital/credential combinations as HUMAN_ESCALATE
- If LAPSED_UNREVIEWED rate is low (<5%) → window may be excessive; consider shortening to 60 min after 30 days of data
- If team lead escalation volume is too high → investigate coordinator workflow adoption; escalate to Kim for process change management

---

## 5. Systems Integration

| System | Agent Interaction | Notes |
|--------|-------------------|-------|
| ServiceNow | Agent 1 reads queue; writes structured ShiftRequest back | API access required (confirm with Aaron) |
| Nurse database | Agent 2 reads credentials, availability, history | Read-only for matching; confirm schema with Aaron |
| Compliance status store | Agent 2 reads credential expiry per nurse | Must reflect real-time re-verification status |
| Hospital preference store | Agent 2 reads hospital-specific nurse history | Needs to be built/populated; currently in coordinator heads |
| SMS/email gateway | Agent 3 sends confirmation notifications | Per nurse communication preference |
| Coordinator dashboard | MEDIUM/LOW cases surfaced; recall window; audit log | New system to build |

**Critical assumption (unverified):** Nurse availability data in the database reflects current availability with <24h lag. If staleness is worse, the matching agent will generate false proposals. Confirm with Kim before Phase 1 go-live.

---

## 6. Phase Delivery

| Phase | Scope | Target | Timeline |
|-------|-------|--------|----------|
| Phase 1 | Agent 1 + Agent 2 (HIGH + MEDIUM routing) without dashboard UI — coordinators work from raw alerts + audit log | 50% autonomous; <1h fill time; board-demo-ready | Weeks 1-6 |
| Phase 1b | Dashboard UI (coordinator review queue, audit trail, recall interface) | Full coordinator workflow adoption | Weeks 7-8 |
| Phase 2 | Agent 3 confirmation loop + no-show prevention | 75% autonomous; no-show rate decline | Weeks 9-16 |
| Phase 3 | Reputation model; predictive no-show; LOW confidence assist | 85% autonomous; coordinator = exception manager | Weeks 17-24 |

**Phase 1 board demo target is week 6.** Dashboard UI is deferred to weeks 7–8. Coordinators work off raw alerts during weeks 1–6 — acceptable operational trade-off to hit Marcus's board deadline. The matching agent functionality is unchanged; only the review UX is deferred.

**What is NOT in Phase 1 (deferred to maintain week-6 commitment):**
- Coordinator review dashboard UI
- Full Agent 3 confirmation state machine
- Non-email intake channels (portal and phone remain manual)
- Reputation model (data collection begins Phase 1; model trained Phase 2)
