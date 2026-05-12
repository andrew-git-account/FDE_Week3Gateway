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
│  Agent 1: Intake     │  Fully Agentic
│  Parsing             │  Free text → structured shift record
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

**Delegation:** Fully Agentic  
**Trigger:** New item enters ServiceNow queue (email/portal/phone captured)  
**Output:** Structured ShiftRequest (shift date/time, location, required credentials, specialty, hospital ID, urgency)  
**Escalation trigger:** Confidence in parsed output <80%, or required fields cannot be extracted → flag for coordinator to clarify with hospital  

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
| >85% | Fully Agentic | Auto-submit proposal to hospital; log decision |
| 70-85% | Agent-Led + Human Oversight | Auto-submit; coordinator gets async alert with 30-min recall window |
| <70% | Human-Led + Agent Support | Agent surfaces ranked candidates with rationale; coordinator makes final decision |
| No viable match | Human Only | Escalate to coordinator with summary of why no match found |

**Key constraint:** Nurse must be soft-reserved at the moment of proposal (15-min lock). If hospital accepts, lock becomes confirmed assignment. If hospital rejects or lock expires, nurse released.

---

### Agent 3 — Confirmation & No-Show Prevention Agent

**Job to be done:** Ensure committed nurses show up by replacing silent acceptance with explicit confirmation and proactive follow-up.

**Why agentic:** Current process: notify nurse → assume accepted → find out at shift time if no-show. Agent introduces a confirmation state machine that detects risk before the shift.

**Confirmation state machine:**
- T+0: Hospital accepts → agent sends nurse confirmation request (SMS/email per preference)
- T+24h: No confirmation received → escalate to coordinator
- T+2h before shift: Confirmed nurse not yet en route → alert coordinator
- No-show detected (hospital calls) → immediately open emergency replacement flow (re-triggers Agent 2)

**Delegation:** Fully Agentic for routine confirmation; Human-Led for unconfirmed or conflict cases

**Concurrency conflict resolution:** If two hospitals accept the same nurse before reservation expires (race condition), agent immediately notifies both coordinators. Second hospital gets escalated to human for manual re-match with priority queue.

---

## 3. Delegation Archetype Summary

| Workflow Step | Archetype | Rationale |
|---------------|-----------|-----------|
| Free-text intake parsing | Fully Agentic | Low risk; output feeds matching queue, not hospital |
| HIGH-confidence matching | Fully Agentic | >85% score; matches current senior coordinator quality bar |
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

### ADR-03: Coordinator Oversight Model (Async vs. Synchronous)

**Decision:** Coordinator oversight of MEDIUM-confidence cases is asynchronous (30-minute recall window after agent submits), not synchronous (approve before submission).

**Context:** Synchronous approval kills the speed advantage. Async oversight maintains quality control without blocking the proposal.

**Alternatives considered:**

| Option | Pros | Cons |
|--------|------|------|
| A: Synchronous approval (block until reviewed) | Zero coordinator bypass | Adds latency; coordinator becomes bottleneck again |
| **B: Async recall window (30 min)** | **Hospital gets fast response; coordinator can intervene** | **If coordinator misses the window, proposal stands unchecked** |
| C: Post-submission audit only | No latency impact | No ability to correct before hospital sees the match |

**Decision rationale:** Option B matches how experienced coordinators actually work — they glance at the queue, spot problems, and intervene. The 30-minute window gives them that without making them gatekeepers.

**Trade-offs accepted:** Some coordinators may not check the dashboard consistently, especially during peak hours. Mitigation: push notification to coordinator's preferred channel; escalation alert if dashboard unreviewed for >20 min during business hours.

**Revisitation conditions:**
- If coordinator recall rate is high (>10% of MEDIUM proposals recalled) → async window may not be sufficient; consider reverting to sync for specific hospitals or credential types
- Marcus's team resistance to dashboard adoption → escalate to Kim for process change management

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
| Phase 1 | Agent 1 + Agent 2 (HIGH only) + Dashboard | 50% autonomous; <1h fill time | Weeks 1-8 |
| Phase 2 | MEDIUM auto-submit + Agent 3 confirmation loop | 75% autonomous; no-show rate decline | Weeks 9-16 |
| Phase 3 | Reputation model; predictive no-show; LOW confidence assist | 85% autonomous; coordinator = exception manager | Weeks 17-24 |

**Phase 1 is the 8-week ROI signal Marcus is asking for.** It does not require the full architecture — it proves the matching agent works on the highest-confidence subset, demonstrating value before Phase 2 investment is approved.
