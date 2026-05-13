# Capability Spec: Agent 1 — Intake Parsing Agent

**Client:** MedFlex Healthcare Staffing  
**Version:** 1.0 — Thursday interim draft  
**Prepared by:** Andrzej Bihun

---

## Shared Entity Glossary

> Referenced by all three capability specs. Treat these definitions as authoritative.

### ShiftRequest
| Field | Type | Constraints |
|-------|------|-------------|
| `id` | UUID | System-generated on creation |
| `hospital_id` | string | Must match a known hospital in the hospital registry |
| `shift_date` | date (ISO 8601) | Must be ≥ today's date at creation time |
| `shift_start_time` | time (HH:MM 24h) | Required |
| `shift_end_time` | time (HH:MM 24h) | Required; must be after shift_start_time unless overnight shift |
| `required_credentials` | string[] | Minimum 1 entry; values from the credential taxonomy (see §1.3) |
| `specialty` | string | From controlled vocabulary (see §1.3); null if not extractable |
| `unit` | string | Free text; null if not mentioned |
| `urgency` | enum | `STANDARD` \| `URGENT` \| `EMERGENCY` |
| `raw_input` | string | Original text verbatim; never modified after creation |
| `parse_confidence` | float | 0.00–1.00; two decimal places |
| `status` | enum | `PENDING_REVIEW` \| `RELEASED` \| `ESCALATED` |
| `source_channel` | enum | `EMAIL` \| `PORTAL` \| `PHONE` |
| `created_at` | timestamp (UTC) | System-generated |
| `preview_expires_at` | timestamp (UTC) | `created_at + 5 minutes` |
| `reviewed_by` | string? | Coordinator user ID; null if auto-released |
| `coordinator_notes` | string? | Free text; null if untouched |

### NurseProfile (read-only for Agent 1)
| Field | Type |
|-------|------|
| `nurse_id` | UUID |
| `credentials` | string[] |
| `compliance_valid_until` | date |
| `availability` | AvailabilitySlot[] |
| `communication_preference` | enum: `SMS` \| `EMAIL` |
| `reliability_score` | float 0.00–1.00 |
| `soft_reserved_until` | timestamp? |

### Credential Taxonomy (controlled vocabulary)
```
Licenses:    RN, LPN, CNA, NP, PA, MD
Certifications: ACLS, BLS, PALS, NRP, TNCC, CCRN, CEN, PCCN
Specialties: ICU, PICU, NICU, ER, OR, PACU, L&D, MedSurg, Telemetry, Psych, Oncology, Pediatrics
```
**Abbreviation expansions known to the agent:**
- "critical care" → ICU
- "labor and delivery" → L&D  
- "neo" / "neonatal" → NICU
- "peds" → Pediatrics
- "tele" → Telemetry
- "advanced cardiac life support" → ACLS

---

## Constraints (Read First!)

**DO:**
- Extract all credential requirements mentioned explicitly or implied by specialty context (e.g., "ICU nurse" implies RN + ICU; ACLS is implied for ICU unless stated otherwise — flag as assumed, not confirmed)
- Resolve relative date expressions ("tomorrow", "this Friday", "next Tuesday") against the UTC timestamp of the incoming message
- Preserve `raw_input` verbatim in every ShiftRequest record, regardless of parse outcome
- Set `status = PENDING_REVIEW` and start the 5-minute preview timer on every new ShiftRequest
- Escalate (set `status = ESCALATED`) if `parse_confidence < 0.80` or if any required field cannot be extracted
- Log every parse attempt with input hash, confidence score, extracted fields, and escalation decision

**DO NOT:**
- Modify or summarise `raw_input` — store it exactly as received
- Infer hospital identity from email domain alone without cross-referencing the hospital registry
- Auto-release a ShiftRequest with `parse_confidence < 0.80`, even if the 5-minute timer expires
- Create a ShiftRequest with a `shift_date` in the past
- Use credentials outside the controlled taxonomy; map to closest taxonomy term and flag if ambiguous

---

## Requirement 1: Parse Shift Date and Time

### Description
Extract the shift date and start/end times from the raw input. Resolve all relative date expressions against the UTC timestamp of the incoming message. Detect overnight shifts (end time < start time) and set a flag rather than treating it as an error.

### Worked Examples

**Example 1 — Absolute date and time:**
```
Input: "Need an ICU RN for Thursday June 12th, 7am to 7pm"
Parsed: shift_date=2026-06-12, shift_start_time=07:00, shift_end_time=19:00
Confidence contribution: +0.25 (date/time fully resolved)
```

**Example 2 — Relative date:**
```
Input received at 2026-05-12T14:30:00Z: "Urgent — need a nurse tomorrow night, 19:00-07:00"
Parsed: shift_date=2026-05-13, shift_start_time=19:00, shift_end_time=07:00, overnight=true
Confidence contribution: +0.25
```

**Example 3 — Date missing, time present:**
```
Input: "RN needed 8am-4pm, ASAP"
Parsed: shift_date=null, shift_start_time=08:00, shift_end_time=16:00
Confidence contribution: 0.00 (required field missing)
Action: parse_confidence capped at <0.80 → escalate
```

**Example 4 — Ambiguous date:**
```
Input: "Next Tuesday" (received on a Tuesday)
Parsed: ambiguous — could be tomorrow (+7 days) or today
Action: flag field as AMBIGUOUS; confidence contribution: +0.05 only; escalate
```

### Edge Cases
| Scenario | Behaviour |
|----------|-----------|
| Overnight shift (e.g., 19:00–07:00) | Set `overnight=true`; do not error on end < start |
| 12-hour format ("7am", "3pm") | Convert to 24h; assume local hospital timezone (default: US/Eastern unless hospital profile specifies otherwise) |
| Date in the past at parse time | Set `shift_date` but add validation error; `parse_confidence` capped at 0.60; escalate |
| No time mentioned at all | `shift_start_time=null`, `shift_end_time=null`; escalate |
| "As soon as possible" / "ASAP" | Set `urgency=EMERGENCY`; do not set shift_date from this signal |

---

## Requirement 2: Parse Credential Requirements

### Description
Extract all required credentials from the raw input. Map to the controlled taxonomy. Flag implied credentials as `ASSUMED` (not `CONFIRMED`). If a credential term is unrecognised, store it in `unresolved_credentials[]` and include it in the escalation payload.

### Worked Examples

**Example 1 — Explicit credentials:**
```
Input: "ICU RN with ACLS and BLS required"
Parsed: required_credentials=["RN", "ICU", "ACLS", "BLS"], all CONFIRMED
Confidence contribution: +0.25
```

**Example 2 — Specialty implies credential:**
```
Input: "Need a critical care nurse"
Parsed: required_credentials=["RN", "ICU"], both ASSUMED (mapped from "critical care")
Confidence contribution: +0.15 (assumed, not explicit)
Note added: "ICU and RN inferred from 'critical care' — coordinator should confirm"
```

**Example 3 — Unrecognised credential:**
```
Input: "RN with TCAR certification required"
Parsed: required_credentials=["RN"], unresolved_credentials=["TCAR"]
Action: parse_confidence capped at 0.70; escalate with note: "Unrecognised credential: TCAR"
```

**Example 4 — Conflicting signals:**
```
Input: "CNA or RN, either is fine"
Parsed: required_credentials=["CNA", "RN"], qualification_mode=ANY_OF
Confidence contribution: +0.10 (ambiguous requirement; coordinator must confirm minimum)
```

### Edge Cases
| Scenario | Behaviour |
|----------|-----------|
| Same credential mentioned twice | Deduplicate; store once |
| Credential listed as "preferred not required" | Store in `preferred_credentials[]`, not `required_credentials[]` |
| "Fully vaccinated" or non-standard compliance phrase | Store in `unresolved_credentials[]`; escalate |
| All caps abbreviation not in taxonomy | Store in `unresolved_credentials[]`; do not discard |

---

## Requirement 3: Parse Hospital Identity and Urgency

### Description
Identify the submitting hospital by cross-referencing the sender email domain, portal account ID, or explicit hospital name against the hospital registry. Classify urgency from explicit signals ("urgent", "ASAP", "emergency") and implicit signals (shift date within 24 hours).

### Worked Examples

**Example 1 — Email domain match:**
```
Sender: scheduling@stmarys-boston.org
Registry lookup: matches hospital_id="HOSP-0042" (St. Mary's Boston)
Confidence contribution: +0.25
```

**Example 2 — Explicit urgency signal:**
```
Input contains: "URGENT — shift starts in 6 hours"
Parsed: urgency=URGENT
Additional: shift within 6 hours also triggers urgency=EMERGENCY override
Final: urgency=EMERGENCY
```

**Example 3 — Hospital name in body, no email match:**
```
Sender: noreply@genericmailserver.com
Body contains: "from General Hospital Springfield"
Registry lookup: 3 hospitals match "General Hospital Springfield" in different states
Action: hospital_id=null; escalate with note: "Multiple hospital matches — coordinator to confirm"
```

**Example 4 — Unknown sender:**
```
Sender domain not in registry; no hospital name in body
Action: hospital_id=null; parse_confidence capped at 0.50; escalate
```

### Urgency Classification Rules
| Signal | Urgency |
|--------|---------|
| Shift starts within 2 hours of message receipt | EMERGENCY |
| Shift starts within 24 hours OR explicit "urgent"/"ASAP" | URGENT |
| Explicit "emergency" in text | EMERGENCY |
| No urgency signal; shift ≥ 48 hours out | STANDARD |
| Conflicting signals | Take highest urgency level |

---

## Requirement 4: Confidence Scoring

### Description
Calculate `parse_confidence` as a weighted sum of four component scores. If the total is below 0.80, set `status=ESCALATED`. If ≥ 0.80, set `status=PENDING_REVIEW` and start the 5-minute preview timer.

### Scoring Components

| Component | Max Score | Condition for full score |
|-----------|-----------|--------------------------|
| Date/time | 0.25 | Both shift_date and start/end times resolved unambiguously |
| Credentials | 0.25 | At least one credential CONFIRMED from taxonomy; no unresolved credentials |
| Hospital identity | 0.25 | Single hospital_id match in registry |
| Specialty/unit | 0.25 | Specialty mapped to controlled vocabulary |

**Deductions:**
- Each ASSUMED credential: −0.05
- Each unresolved credential: −0.10
- Hospital matched but not unique (multiple candidates): −0.15
- Date ambiguous (but resolvable): −0.10
- Overnight shift detected: −0.00 (not a confidence issue)

### Worked Examples

**Example 1 — High confidence:**
```
date/time: 0.25, credentials: 0.25, hospital: 0.25, specialty: 0.20 (unit not mentioned)
Total: 0.95 → status=PENDING_REVIEW
```

**Example 2 — Assumed credentials, known hospital:**
```
date/time: 0.25, credentials: 0.15 (one assumed), hospital: 0.25, specialty: 0.20
Total: 0.85 → status=PENDING_REVIEW (note added about assumed credential)
```

**Example 3 — Missing date:**
```
date/time: 0.00, credentials: 0.25, hospital: 0.25, specialty: 0.20
Total: 0.70 → status=ESCALATED
```

---

## Requirement 5: Preview Queue and Auto-Release

### Description
Every ShiftRequest with `status=PENDING_REVIEW` enters the coordinator preview queue. A coordinator may edit any field and mark as reviewed. If no action is taken within 5 minutes (`preview_expires_at` passes), the agent auto-releases the record by setting `status=RELEASED`. Escalated records (`status=ESCALATED`) never auto-release — they require explicit coordinator action.

### Process Steps
1. Create ShiftRequest record with `status=PENDING_REVIEW`, set `preview_expires_at = created_at + 5 minutes`
2. Write record to coordinator dashboard queue
3. At `preview_expires_at`: check `status`
   - If still `PENDING_REVIEW` and `parse_confidence ≥ 0.80`: set `status=RELEASED`; publish to Agent 2 input queue
   - If `ESCALATED`: do not change status; send push notification to coordinator if not already notified
4. If coordinator edits any field before expiry: set `reviewed_by = coordinator_id`, recalculate confidence, log change
5. If coordinator manually releases an ESCALATED record: set `status=RELEASED`; log override with coordinator ID

### Edge Cases
| Scenario | Behaviour |
|----------|-----------|
| Coordinator edits field that drops confidence below 0.80 | Set status=ESCALATED; do not auto-release |
| Two coordinators edit simultaneously | Last-write-wins with conflict log entry; alert both coordinators |
| Agent 2 queue unavailable at release time | Retry 3× at 30s intervals; if all fail, set status=QUEUE_ERROR and alert on-call |
| ShiftRequest created outside business hours | Preview timer runs; coordinator notified on next login |

---

## Requirement 6: Escalation

### Description
Escalated records require a coordinator to resolve before the ShiftRequest can be released to Agent 2. The escalation payload must include the specific reason for escalation so the coordinator knows exactly what to verify or correct.

### Escalation Trigger Conditions
| Trigger | Code |
|---------|------|
| `parse_confidence < 0.80` | LOW_CONFIDENCE |
| `shift_date` null or ambiguous | MISSING_DATE |
| `hospital_id` null or multiple matches | HOSPITAL_AMBIGUOUS |
| `required_credentials[]` empty | MISSING_CREDENTIALS |
| One or more unresolved credentials | UNRESOLVED_CREDENTIAL |
| `shift_date` in the past | PAST_DATE |

### Escalation Payload (to coordinator dashboard)
```json
{
  "shift_request_id": "uuid",
  "escalation_codes": ["LOW_CONFIDENCE", "UNRESOLVED_CREDENTIAL"],
  "parse_confidence": 0.62,
  "extracted_fields": { ... },
  "unresolved_credentials": ["TCAR"],
  "coordinator_action_required": "Confirm credential 'TCAR' and verify hospital identity",
  "raw_input": "original text verbatim"
}
```

---

## API Failure Modes

| Failure | Detection | Response |
|---------|-----------|----------|
| ServiceNow API timeout (>5s) | Request timer | Retry 3× with exponential backoff (1s, 2s, 4s); if all fail, write to dead-letter queue and alert on-call |
| ServiceNow returns 500 | HTTP status code | Same as timeout |
| ServiceNow returns 429 (rate limit) | HTTP status + Retry-After header | Pause for Retry-After seconds; resume queue processing |
| ServiceNow returns 401 | HTTP status code | Do not retry; alert on-call immediately (credential rotation required) |
| Hospital registry API unavailable | Connection error / timeout | Set `hospital_id=null`, add escalation code HOSPITAL_REGISTRY_UNAVAILABLE; process continues |
| LLM API timeout during parse | Request timer (10s) | Retry once; if second attempt fails, set all extracted fields to null, set parse_confidence=0.0, escalate |
| LLM returns partial response | Token count < expected | Treat as extraction failure for affected fields; escalate affected fields only |

---

## Observability

**Log on every parse attempt:**
```
level=INFO fields: shift_request_id, hospital_id, parse_confidence, escalation_codes[], duration_ms, source_channel
```

**Log on every coordinator action:**
```
level=INFO fields: shift_request_id, coordinator_id, fields_changed[], old_confidence, new_confidence, action=EDIT|RELEASE|ESCALATE
```

**Metrics to track:**
- `intake.parse_confidence.histogram` — distribution of confidence scores
- `intake.escalation_rate` — % of records escalated (target: <20%)
- `intake.auto_release_rate` — % released without coordinator touch
- `intake.parse_duration_ms` — LLM response latency
- `intake.preview_queue_depth` — records awaiting coordinator review

**Alerts:**
- Escalation rate exceeds 30% over any 1-hour window → alert on-call
- Preview queue depth > 50 records → alert coordinator team lead
- LLM API error rate > 5% in 10 minutes → alert on-call

---

## Acceptance Criteria

- [ ] **Accuracy:** parse_confidence ≥ 0.80 for ≥ 90% of well-formed hospital emails in regression test set
- [ ] **Escalation precision:** 100% of records with missing required fields are escalated; 0% of complete records are incorrectly escalated
- [ ] **Latency:** parse completion within 8 seconds of message receipt for 95th percentile
- [ ] **Auto-release:** PENDING_REVIEW records auto-release within 5 minutes ± 10 seconds
- [ ] **Audit:** every ShiftRequest has a complete audit trail (created → reviewed/auto-released → released/escalated)
- [ ] **Concurrency:** two simultaneous edits to the same record produce a logged conflict; no data loss
- [ ] **Error handling:** all API failure modes in the table above are covered by tests with mock failures
