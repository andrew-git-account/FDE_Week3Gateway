# Capability Spec: Agent 3 — Confirmation & No-Show Prevention Agent

**Client:** MedFlex Healthcare Staffing  
**Version:** 1.0 — Thursday interim draft  
**Prepared by:** Andrzej Bihun

> **Shared entity definitions** (ShiftRequest, NurseProfile, Credential Taxonomy) are in `04a-capability-spec-intake-parsing.md`.  
> **MatchProposal and NurseReservation** definitions are in `04b-capability-spec-shift-matching.md`.

---

## Additional Entities

### NurseAssignment
| Field | Type | Constraints |
|-------|------|-------------|
| `id` | UUID | System-generated |
| `match_proposal_id` | UUID | FK → MatchProposal.id |
| `nurse_id` | UUID | FK → NurseProfile.nurse_id |
| `shift_request_id` | UUID | FK → ShiftRequest.id |
| `hospital_id` | string | Denormalised for query efficiency |
| `shift_date` | date | Denormalised from ShiftRequest |
| `shift_start_time` | time | Denormalised |
| `confirmation_status` | enum | `PENDING_CONFIRMATION` \| `CONFIRMED` \| `UNCONFIRMED_ESCALATED` \| `CANCELLED` \| `NO_SHOW` \| `COMPLETED` |
| `notification_sent_at` | timestamp (UTC)? | null until first notification sent |
| `notification_channel` | enum | `SMS` \| `EMAIL` (from NurseProfile.communication_preference) |
| `notification_delivery_status` | enum | `PENDING` \| `DELIVERED` \| `FAILED` |
| `confirmed_at` | timestamp (UTC)? | null until explicit confirmation received |
| `confirmation_method` | enum? | `SMS_REPLY` \| `EMAIL_REPLY` \| `PORTAL` \| `COORDINATOR_MANUAL` |
| `cancellation_flag` | boolean | Set by coordinator when nurse cancels by phone |
| `cancellation_logged_at` | timestamp? | When coordinator set the flag |
| `escalated_at` | timestamp? | When first escalation was triggered |
| `escalation_reason` | enum? | `NO_CONFIRMATION_24H` \| `PRE_SHIFT_UNACKNOWLEDGED` \| `DELIVERY_FAILED` \| `AMBIGUOUS_REPLY` \| `PHONE_CANCELLATION` \| `NO_SHOW_DETECTED` |
| `no_show_reported_at` | timestamp? | When hospital reported no-show |
| `created_at` | timestamp (UTC) | |

### ConfirmationEvent (audit log)
| Field | Type |
|-------|------|
| `id` | UUID |
| `assignment_id` | UUID |
| `event_type` | enum: `NOTIFICATION_SENT` \| `DELIVERY_CONFIRMED` \| `DELIVERY_FAILED` \| `REPLY_RECEIVED` \| `CONFIRMED` \| `ESCALATED` \| `CANCELLATION_LOGGED` \| `NO_SHOW_REPORTED` \| `REMATCH_TRIGGERED` |
| `occurred_at` | timestamp (UTC) |
| `actor` | string — agent ID or coordinator ID |
| `notes` | string? |

---

## Constraints (Read First!)

**DO:**
- Create a NurseAssignment record immediately when MatchProposal.status transitions to ACCEPTED
- Send confirmation notification within 2 minutes of NurseAssignment creation
- Use `NurseProfile.communication_preference` to determine notification channel (SMS or EMAIL)
- Retry failed delivery 3× before escalating (see §3 for retry schedule)
- Escalate to coordinator for ALL failure modes — agent handles the happy path only
- Log every state transition in ConfirmationEvent with timestamp and actor
- Re-trigger Agent 2 immediately when a no-show is detected (do not wait for coordinator instruction)

**DO NOT:**
- Treat silence as confirmation — only an explicit reply (SMS reply, email reply, portal click) counts as CONFIRMED
- Auto-confirm an assignment based on a message that contains hedging language ("probably", "should be", "I'll try")
- Contact the nurse more than 5 times total across retries and reminders for a single assignment
- Send a cancellation notification to the hospital — coordinators make that call
- Automatically reassign a nurse after cancellation without coordinator approval for the new assignment

---

## Requirement 1: Confirmation Notification Dispatch

### Description
When a hospital accepts a MatchProposal, create a NurseAssignment and immediately send a confirmation request to the nurse via their preferred channel. The message must include: shift date, start/end time, hospital name, unit, and an explicit confirmation link or reply instruction.

### Notification Message Templates

**SMS template:**
```
MedFlex: You've been matched for a shift.
Hospital: [hospital_name]
Date: [shift_date] [shift_start_time]–[shift_end_time]
Unit: [unit or "TBD"]
Reply YES to confirm or NO to decline. Reply by [confirmation_deadline].
```

**Email template subject:** `Action required: Confirm your shift at [hospital_name] on [shift_date]`

### Process Steps
1. Receive ACCEPTED event from MatchProposal
2. Create NurseAssignment with `confirmation_status=PENDING_CONFIRMATION`
3. Look up `NurseProfile.communication_preference`
4. Render notification using template; populate all fields from ShiftRequest and MatchProposal
5. Submit to SMS/email gateway; record `notification_sent_at` and `notification_delivery_status=PENDING`
6. On delivery receipt from gateway: set `notification_delivery_status=DELIVERED`
7. On delivery failure: trigger Requirement 2 (retry logic)

### Worked Examples

**Example 1 — SMS delivery confirmed:**
```
NurseAssignment created at 14:05:00
SMS sent at 14:05:47; gateway returns delivery receipt at 14:06:03
notification_delivery_status=DELIVERED
State: PENDING_CONFIRMATION (awaiting nurse reply)
```

**Example 2 — Email preferred:**
```
NurseProfile.communication_preference=EMAIL
Email sent at 14:05:55; delivery confirmed at 14:06:10
notification_delivery_status=DELIVERED
State: PENDING_CONFIRMATION
```

**Example 3 — Shift accepted less than 2 hours before start:**
```
shift_start_time=16:00, hospital acceptance received at 14:10
Urgency flag set; notification sent immediately with confirmation_deadline=14:40 (30-minute window instead of standard 24h)
If no reply by 14:40 → escalate immediately (not T+24h)
```

### Edge Cases
| Scenario | Behaviour |
|----------|-----------|
| NurseProfile.communication_preference is null | Default to SMS; log warning |
| Shift details have changed since proposal (hospital edits) | Re-send updated notification; log NOTIFICATION_SENT event with note "updated shift details" |
| Hospital accepts outside business hours | Send notification immediately regardless of time; confirmation_deadline set to min(T+24h, T-2h before shift) |

---

## Requirement 2: Delivery Retry Logic

### Description
If the gateway returns a delivery failure for SMS or email, retry up to 3 times on an escalating schedule before escalating to coordinator. Each retry uses the same channel. Do not switch channels automatically (nurse preference must be respected unless coordinator overrides).

### Retry Schedule
| Attempt | Delay after previous failure |
|---------|------------------------------|
| Retry 1 | 10 minutes |
| Retry 2 | 20 minutes |
| Retry 3 | 30 minutes |
| All 3 retries failed | Escalate to coordinator (see §6) |

### Worked Examples

**Example 1 — Retry succeeds on attempt 2:**
```
14:05 — initial SMS sent; delivery failure returned
14:15 — Retry 1; delivery failure
14:35 — Retry 2; delivery confirmed
notification_delivery_status=DELIVERED; continue normal flow
Total contact attempts: 2
```

**Example 2 — All retries fail:**
```
14:05, 14:15, 14:35, 15:05 — all fail
escalation_reason=DELIVERY_FAILED; coordinator notified to contact nurse directly
NurseAssignment.confirmation_status=UNCONFIRMED_ESCALATED
```

**Example 3 — Gateway returns 429 (rate limit):**
```
Retry respects Retry-After header from gateway; adds Retry-After duration to retry schedule
Log: DELIVERY_RATE_LIMITED; resume after delay
```

### Edge Cases
| Scenario | Behaviour |
|----------|-----------|
| Nurse replies during retry window | Stop retries; process reply as normal; log REPLY_RECEIVED |
| Gateway returns 401 | Do not retry; alert on-call immediately (credential issue); escalate assignment to coordinator |
| Gateway returns 500 | Treat as delivery failure; retry as per schedule |

---

## Requirement 3: Confirmation State Machine

### Description
The NurseAssignment moves through a defined set of states. State transitions are triggered by nurse replies, system timers, or coordinator actions. Only explicit positive replies advance to CONFIRMED.

### State Transition Diagram
```
PENDING_CONFIRMATION
    │
    ├─ Explicit "YES" reply ──────────────────────────► CONFIRMED
    │
    ├─ Explicit "NO" reply ──────────────────────────► CANCELLED (→ re-match)
    │
    ├─ Ambiguous reply ("probably", "I'll try") ─────► UNCONFIRMED_ESCALATED (coordinator interprets)
    │
    ├─ T+24h, no reply ──────────────────────────────► UNCONFIRMED_ESCALATED
    │
    ├─ Delivery failed (all retries) ───────────────► UNCONFIRMED_ESCALATED
    │
    ├─ Cancellation flag set by coordinator ─────────► CANCELLED (→ re-match)
    │
    └─ Shift completed ──────────────────────────────► COMPLETED

CONFIRMED
    │
    ├─ T-2h pre-shift, no acknowledgement ──────────► UNCONFIRMED_ESCALATED (alert coordinator)
    │
    ├─ No-show reported by hospital ────────────────► NO_SHOW (→ emergency re-match)
    │
    └─ Shift completed ──────────────────────────────► COMPLETED
```

### Confirmation Reply Parsing Rules

| Reply text (case-insensitive) | Classification |
|-------------------------------|----------------|
| "yes", "y", "confirmed", "confirm", "ok", "sure", "on my way" | CONFIRMED |
| "no", "n", "can't", "cannot", "declining", "decline", "not available" | CANCELLED |
| "probably", "should be", "i'll try", "maybe", "hopefully" | AMBIGUOUS → UNCONFIRMED_ESCALATED |
| Any other text | AMBIGUOUS → UNCONFIRMED_ESCALATED |
| No reply within deadline | Timer-triggered → UNCONFIRMED_ESCALATED |

### Worked Examples

**Example 1 — Happy path:**
```
T+0:  Notification sent
T+2h: Nurse replies "YES"
State: CONFIRMED
Coordinator notified (informational only)
```

**Example 2 — T+24h no reply:**
```
T+0:   Notification sent; delivery confirmed
T+24h: Timer fires; no reply received
State: UNCONFIRMED_ESCALATED; escalation_reason=NO_CONFIRMATION_24H
Coordinator alerted: "Nurse [name] has not confirmed shift [date]. Action required."
```

**Example 3 — Ambiguous reply:**
```
T+3h: Nurse replies "I'll probably be there"
State: UNCONFIRMED_ESCALATED; escalation_reason=AMBIGUOUS_REPLY
Escalation payload: {original_reply: "I'll probably be there", nurse_id: ..., shift_date: ...}
Coordinator interprets; can manually set to CONFIRMED or CANCELLED
```

---

## Requirement 4: Pre-Shift Alert (T-2h)

### Description
At 2 hours before shift start, check that the nurse's assignment is CONFIRMED. If the nurse has not acknowledged pre-shift (no response since the original confirmation), alert the coordinator. This is a risk signal, not a no-show — the nurse is still expected.

### Process Steps
1. Schedule timer at NurseAssignment creation: fire at `shift_start_time - 2 hours`
2. At timer fire: check `confirmation_status`
   - `CONFIRMED` and nurse has communicated within 6h: no action; log heartbeat
   - `CONFIRMED` but last contact > 12h ago: send coordinator alert: "Shift in 2 hours — nurse confirmed but no recent contact"
   - `UNCONFIRMED_ESCALATED`: escalate reminder to coordinator
   - `PENDING_CONFIRMATION`: treat as urgent escalation; re-attempt contact once; alert coordinator immediately

### Worked Examples

**Example 1 — Confirmed, recent contact:**
```
Nurse confirmed at T+1h; no further contact
T-2h timer fires; last contact was 10h ago → alert coordinator: "Shift in 2h — nurse confirmed but no contact in 10h"
```

**Example 2 — Still pending at T-2h:**
```
Nurse has not confirmed; delivery was successful; coordinator has not acted
T-2h timer fires → send one final SMS; simultaneously alert coordinator as URGENT
```

---

## Requirement 5: No-Show Detection and Emergency Re-Match

### Description
When a hospital reports a no-show (nurse did not arrive), immediately update the NurseAssignment, re-trigger Agent 2 for emergency matching, and notify the coordinator. The coordinator notifies the hospital — the agent does not contact the hospital directly.

### Process Steps
1. Hospital no-show report received (via inbound hospital message or coordinator logging it in system)
2. Set `NurseAssignment.confirmation_status=NO_SHOW`; set `no_show_reported_at=now`
3. Log ConfirmationEvent: NO_SHOW_REPORTED
4. Immediately publish ShiftRequest to Agent 2 input queue with flags: `urgency=EMERGENCY`, `rematch=true`, `previous_nurse_id=nurse_id` (to exclude this nurse)
5. Simultaneously send notification to coordinator: "No-show reported — [hospital] shift [date/time]. Emergency re-match in progress."
6. Update NurseProfile.reliability_score: decrement (reliability score update rules owned by external system; Agent 3 sends a reliability_event)

### Worked Examples

**Example 1 — Hospital calls coordinator:**
```
Coordinator logs no-show in dashboard at shift start time
Agent 3 receives NO_SHOW event
Emergency re-match triggered for same shift; previous nurse excluded
Coordinator receives: "Emergency re-match triggered. Agent 2 working."
```

**Example 2 — No-show with no viable replacement:**
```
Agent 2 returns NO_MATCH for emergency re-match
Agent 3 forwards NO_MATCH result to coordinator
Coordinator handles hospital communication and manual sourcing
```

### Edge Cases
| Scenario | Behaviour |
|----------|-----------|
| No-show reported after shift end time | Log; do not trigger re-match (shift is over); trigger reliability_event only |
| Duplicate no-show report for same assignment | Idempotent: second report logged but no second re-match triggered |
| No-show for a nurse who was on UNCONFIRMED_ESCALATED | Still trigger re-match; note in re-match payload that this was a previously unconfirmed assignment |

---

## Requirement 6: Coordinator Escalation Payloads

### Description
Every escalation sent to the coordinator must include sufficient context to act without referencing the original request. Each escalation type has a defined payload.

### Escalation Payloads by Type

**DELIVERY_FAILED:**
```json
{
  "assignment_id": "uuid",
  "nurse_name": "Jane Smith",
  "nurse_id": "uuid",
  "shift_date": "2026-06-12",
  "shift_start_time": "07:00",
  "hospital_name": "St. Mary's Boston",
  "channel_attempted": "SMS",
  "retry_count": 3,
  "action_required": "Contact nurse directly to confirm shift"
}
```

**NO_CONFIRMATION_24H:**
```json
{
  "assignment_id": "uuid",
  "nurse_name": "Jane Smith",
  "shift_date": "2026-06-12",
  "shift_start_time": "07:00",
  "hospital_name": "St. Mary's Boston",
  "notification_sent_at": "2026-06-11T14:05:00Z",
  "action_required": "Reach nurse to confirm or cancel assignment"
}
```

**AMBIGUOUS_REPLY:**
```json
{
  "assignment_id": "uuid",
  "nurse_name": "Jane Smith",
  "original_reply": "I'll probably be there",
  "reply_received_at": "2026-06-11T16:30:00Z",
  "action_required": "Interpret reply and mark as CONFIRMED or CANCELLED"
}
```

**PHONE_CANCELLATION:**
```
Coordinator-initiated: coordinator sets cancellation_flag=true via dashboard
Agent 3 reacts: set confirmation_status=CANCELLED; trigger re-match; log event
No automated detection possible — requires coordinator to log the call
Process dependency: coordinators must log all phone cancellations within 10 minutes of receiving the call (process change requirement for Phase 2 launch)
```

---

## Requirement 7: Heartbeat and System Health

### Description
Agent 3 manages long-running timers (T+24h, T-2h). If the state machine stops advancing (system failure, timer not firing), a heartbeat check detects the stall and alerts on-call.

### Heartbeat Rules
- Every NurseAssignment in `PENDING_CONFIRMATION` state is checked every 15 minutes
- Expected state transitions:
  - `PENDING_CONFIRMATION` → should transition within 24h of notification sent
  - `CONFIRMED` → should remain stable until shift or T-2h timer fires
- If an assignment has been in `PENDING_CONFIRMATION` for > 25h without any state change (timer should have fired at 24h): alert on-call with assignment_id and last_event_at
- If `shift_start_time` has passed and assignment is still `PENDING_CONFIRMATION` or `CONFIRMED` (not COMPLETED or NO_SHOW): alert on-call as potential missed state transition

---

## API Failure Modes

| Failure | Detection | Response |
|---------|-----------|----------|
| SMS gateway timeout (>10s) | Request timer | Retry per schedule (§2); do not count as a delivery failure until gateway confirms failure |
| SMS gateway returns 429 | HTTP status + Retry-After | Honour Retry-After; resume retry schedule |
| SMS gateway returns 401 | HTTP status | Alert on-call immediately; escalate assignment to coordinator |
| Email gateway unavailable | Connection error | Retry 3×; if all fail, escalate to coordinator as DELIVERY_FAILED |
| Agent 2 input queue unavailable (emergency re-match) | Connection error | Retry 3× at 30s intervals; if all fail, alert on-call and coordinator directly: "Emergency re-match could not be triggered — manual action required" |
| ConfirmationEvent write failure | DB error | Retry once; if fails, log to error log but do not block state transition (state transitions take priority over audit writes) |
| NurseProfile.communication_preference unavailable | DB timeout | Default to SMS; log WARNING |

---

## Observability

**Log on every state transition:**
```
level=INFO fields: assignment_id, nurse_id, from_status, to_status, trigger, actor, occurred_at
```

**Log on every notification send:**
```
level=INFO fields: assignment_id, channel, delivery_status, attempt_number, gateway_response_code
```

**Metrics to track:**
- `confirmation.confirmation_rate` — % of assignments confirmed within 24h (target >85%)
- `confirmation.escalation_rate_by_reason` — breakdown by escalation_reason
- `confirmation.no_show_rate` — % of CONFIRMED assignments that result in NO_SHOW (target <7%)
- `confirmation.delivery_failure_rate` — % of notifications failing all retries
- `confirmation.ambiguous_reply_rate` — % of replies classified as AMBIGUOUS
- `confirmation.rematch_success_rate` — % of emergency re-matches that result in a placed nurse

**Alerts:**
- No-show rate exceeds 10% over any 7-day window → alert on-call and coordinator team lead
- Delivery failure rate exceeds 5% over any 1-hour window → alert on-call (gateway issue)
- Any NurseAssignment stalled for >25h without state transition → alert on-call
- Emergency re-match queue depth > 5 simultaneously → alert coordinator team lead

---

## Acceptance Criteria

- [ ] **Confirmation rate:** ≥ 85% of nurses explicitly confirm within 24h of notification (after launch)
- [ ] **No silent acceptance:** 0% of assignments marked CONFIRMED without an explicit nurse reply
- [ ] **Escalation completeness:** 100% of DELIVERY_FAILED, NO_CONFIRMATION_24H, AMBIGUOUS_REPLY, and PHONE_CANCELLATION events produce a coordinator notification within 2 minutes
- [ ] **Emergency re-match:** Agent 2 re-triggered within 60 seconds of NO_SHOW event
- [ ] **State machine integrity:** no assignment remains in PENDING_CONFIRMATION beyond 25h without a state transition or on-call alert
- [ ] **Retry ceiling:** no nurse contacted more than 5 times total (initial + 3 retries + 1 pre-shift) per assignment
- [ ] **Audit completeness:** every state transition has a corresponding ConfirmationEvent record
- [ ] **Error handling:** all API failure modes tested with mock failures; emergency re-match path tested with Agent 2 queue unavailable
