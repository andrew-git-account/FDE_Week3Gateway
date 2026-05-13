# Deliverable 5 — Build-Loop Response Memo

**Engagement:** MedFlex (Gate 3)
**Fixture:** Cascade Public Libraries — Hold Queue Management & Notification
**Signals reviewed:** 8
**Date:** 2026-05-12

---

## Context

This memo diagnoses the simulated build output produced against the Cascade Public Libraries Hold Queue spec. Each signal is classified into one of five categories — builder misread, unjustified implementation choice, test/environment issue, spec gap, or legitimate clarification request — and answered in the tone the category requires.

The diagnostic approach: read the spec requirement alongside the code before classifying. The ownership question drives tone — if the spec is clear and the code contradicts it, the builder re-does the code; if the spec left something ambiguous or unresolved, the FDE owns the revision.

---

## Signal 1 — 72-hour notification window

**Classification:** Builder misread

**Rationale:** R3 states that holds expire "if unclaimed" — the code expires all notified holds older than 72 hours without checking claim status, contradicting the explicit condition.

**Response:**
R3 requires an explicit "if unclaimed" check before expiring a hold. The current implementation calls `expire_hold()` on any hold in `get_notified_holds()` that is older than 72 hours, regardless of whether the patron has already claimed it. Add a condition to check claim status before expiring — for example, `if not hold.claimed` — or confirm that `get_notified_holds()` already filters to unclaimed holds only, in which case add an inline comment to document that assumption so the business logic is explicit in the code.

---

## Signal 2 — Accessibility queue position

**Classification:** Builder misread

**Rationale:** R4 specifies that accessibility-priority patrons "jump to queue position 1" — a positional assignment — but the builder added a new file implementing a weight multiplier (0.25×), which is a different mechanism not present in the spec.

**Response:**
R4 specifies a positional jump to queue position 1, not a weighted score. A 0.25× weight produces an effective position (e.g., raw position 5 × 0.25 = 2.5) that is neither the specified queue position nor consistent with how other tiers are handled. Please remove `accessibility_priority.py` and implement the queue-jump logic in R4 directly: when an accessibility-priority patron places a hold, insert them at position 1, or at position 2 if another accessibility-priority patron already occupies position 1 (FIFO between them per R4).

---

## Signal 3 — Return reminder in auto-checkout handler

**Classification:** Unjustified implementation choice

**Rationale:** R7 specifies auto-checkout only — performing the loan automatically and notifying the patron; no return reminder is mentioned anywhere in the spec.

**Response:**
The return reminder is a thoughtful UX addition, but the spec doesn't authorise it, and shipping unspecified functionality expands scope and testing surface without a business decision behind it. Please remove the `schedule_reminder()` call and the comment block. If return reminders are worth adding, file a spec change request so the feature can be evaluated against other priorities and the email copy agreed before implementation.

---

## Signal 4 — Overdrive refresh test fixture

**Classification:** Test/environment issue

**Rationale:** The implementation in `overdrive_refresh.py` correctly advances the queue by the number of new copies per R8; the test fails because the fixture `overdrive_refresh_2025_q4.json` encodes Q4 2025 queue state in `expected_advances`, which no longer matches current queue state when run in 2026.

**Response:**
The implementation is correct — the test failure is caused by a date-bound fixture, not incorrect code. Either regenerate `overdrive_refresh_2025_q4.json` with current queue state, or refactor the test to mock catalog additions explicitly (e.g., inject a refresh event with a known `added_copies` count and assert `advance_queue` was called that many times) so the test no longer depends on live queue state. Do not change the implementation.

---

## Signal 5 — Duplicate hold check ignores format type

**Classification:** Builder misread

**Rationale:** R11 explicitly states that ebook and audiobook editions of the same title "are treated as two separate holds," but `place_hold()` rejects any second hold on the same `title_id` regardless of `format_type`, blocking the behaviour R11 requires.

**Response:**
R11 requires that ebook and audiobook editions count as separate holds. The current duplicate check `patron_has_active_hold_on_title(patron, title_id)` only compares title, which prevents a patron from holding both formats simultaneously. Replace it with a check that compares the combination of `title_id` and `format_type` — for example, `patron_has_active_hold_on_title_and_format(patron, title_id, format_type)`. Verify that both holds still count toward the active-hold limit per R9.

---

## Signal 6 — Paused hold skip notification

**Classification:** Unjustified implementation choice

**Rationale:** R6 specifies that paused holds are skipped and the next eligible patron notified — it says nothing about notifying the patron whose hold was skipped.

**Response:**
R6 only specifies notifying the next eligible patron when a paused hold is skipped. The `send_email()` call informing the paused patron that their hold was skipped (lines 175–179) is not in the spec. Please remove it. If the business wants to notify patrons when their paused holds are skipped, that's a reasonable feature, but it needs to be added to the spec with agreed email copy before being built — particularly since it changes the notification volume and patron experience.

---

## Signal 7 — SMS-only vs dual-channel notification

**Classification:** Spec gap

**Rationale:** R12 Note explicitly flags "the business has not yet decided whether SMS-opted patrons should receive both email and SMS, or only SMS" — the builder made a reasonable choice (SMS-only for opted-in patrons) but the spec left the decision unresolved, which is an FDE ownership failure.

**Response:**
I should have resolved this business decision before the spec was finalised. The builder made a reasonable interpretation of "opt-in to SMS" as replacing email, but the implications are material — SMS-only means patrons who miss a text lose their 72-hour claim window with no fallback. Updating R12 to specify dual-channel behaviour: patrons who have opted in to SMS receive both email and SMS notifications; email is always sent. Rationale: hold notifications are time-critical (72-hour window); dual-channel reduces the risk of a missed notification forfeiting the hold. Revise `sms_notification.py` accordingly.

---

## Signal 8 — Academic + Accessibility-priority intersection

**Classification:** Legitimate clarification request

**Rationale:** The Assumptions section explicitly flags the Academic + Accessibility-priority intersection as "not specified" and "pending FDE confirmation" — the builder correctly identified the unresolved spec gap, held the PR, and articulated the ambiguity precisely rather than guessing.

**Response:**
Good catch — you're right that the Assumptions section left this unresolved. Going with option (a): R4 wins completely. An academic-tier accessibility-priority patron jumps to position 1, and the 0.5× academic weight does not apply when the patron already holds the accessibility modifier. The academic weight is relevant only when comparing academic vs standard patrons who are not accessibility-priority; it has no effect once a patron qualifies for the position-1 jump. Updating the spec: R4 will include an explicit statement that the accessibility jump takes precedence over the academic weight, and the "pending FDE confirmation" flag in Assumptions will be removed. Thank you for holding the PR — this is the right behaviour.

---

## Reflection

The hardest diagnostic move in this set was Signal 7. My first instinct was builder misread, because "opt-in" language linguistically implies additive behaviour (email plus SMS), and the builder chose SMS-only, which contradicts that reading. But the R12 Note and Assumptions section explicitly flagged this as an unresolved business decision — meaning the spec itself created the ambiguity, not the builder. The ownership question forced a different answer: the artefact that needs to change is the spec, not the code. That reclassification from builder misread to spec gap changed the response tone entirely — from "you misread R12" to "I should have gotten the business decision before closing the spec." 

The learning: when a spec flags uncertainty in Assumptions or a Note, I own it even if the main text seemed clear. Defensive reading — the impulse to blame the builder for not inferring the right behaviour from ambiguous language — is the failure mode. If I ran this exercise again, I would read the Assumptions section before classifying any signal, not after. The flags there change the ownership of several signals that otherwise look like misreads on first impression.
