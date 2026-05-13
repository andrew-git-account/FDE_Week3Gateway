### Signal 1 — [Notification deadline]

**Classification:** builder misread

**Rationale:** 
R3 explicitly states "If unclaimed, the hold expires," but the code expires all holds older than 72 hours without verifying they remain unclaimed (line 79): 
```code
        if hold.notified_at < cutoff:
            expire_hold(hold)
            advance_queue(hold.title_id)
```

**Response:**
R3 specifies that holds expire 'if unclaimed' — the current implementation doesn't check claim status before expiring. 
Add a condition to verify the hold is still unclaimed before calling expire_hold(). 
If get_notified_holds() already filters for unclaimed status, please add a comment documenting this assumption so the business logic is explicit.


### Signal 2 — [Accessibility priority]

**Classification:** builder misread

**Rationale:** 
R4 specifies that accessibility-priority patrons "jump to queue position 1," but the code implements a weight-based system (0.25×) not mentioned in the spec, contradicting the explicit jump mechanism: 
```code
    ACCESSIBILITY = 0.25
```

**Response:**
R4 specifies that accessibility-priority patrons 'jump to queue position 1' when placing a hold — this is a positional assignment, not a weight calculation. 
The current implementation applies a 0.25x weight that isn't in the spec and doesn't match the required behavior. 
Revise accessibility_priority.py to implement the queue-jump logic described in R4: insert the patron at position 1 (or position 2 if another accessibility-priority patron is already at position 1, per R4's FIFO rule).


### Signal 3 — [Auto checkout handler]

**Classification:** unjustified implementation choice

**Rationale:** 
The code correctly implements auto-checkout (R7) but adds an unspecified return reminder feature scheduled 3 days before loan expiration, which is not mentioned anywhere in the requirements.

**Response:**
Appreciate the thinking on the return reminder feature — it's a thoughtful UX addition. However, the spec doesn't ask for it, and adding unspecified functionality expands scope and testing surface area. 
Please remove the schedule_reminder() call for now. 
If you think return reminders are worth adding, let's file a spec change request and evaluate it properly against other priorities.
   

### Signal 4 — [Test override refresh]

**Classification:** test/environment issue 

**Rationale:** 
The implementation correctly advances the queue per R8, but the test fixture overdrive_refresh_2025_q4.json encodes Q4 2025 queue state in expected_advances, causing failures when run in 2026 with different queue state.
   
**Response:**
The test failure is caused by date-bound fixture data, not incorrect implementation. 
The fixture overdrive_refresh_2025_q4.json has an expected_advances field that was accurate for Q4 2025 queue state but is now outdated. 
Either regenerate the fixture with current queue state, or refactor the test to mock the queue explicitly rather than depending on live state. 
The implementation correctly follows R8.
  

### Signal 5 — [Place hold]

**Classification:** builder misread

**Rationale:** 
R11 explicitly states that holds on different formats of the same title should be treated as "two separate holds," but the duplicate check rejects any second hold on the same title_id regardless of format_type, preventing the behavior R11 requires:
```code
    if patron_has_active_hold_on_title(patron, title_id):
        raise DuplicateHoldError(
            f"Patron {patron.id} already holds title {title_id}.")
```

**Response:**
R11 specifies that ebook and audiobook editions of the same title should be treated as separate holds — the current duplicate check blocks this by only comparing title_id. 
Update the duplicate check to verify the combination of title_id AND format_type, allowing a patron to hold both the ebook and audiobook of the same title simultaneously.
For example, patron_has_active_hold_on_title() should be replaced with patron_has_active_hold_on_title_and_format(patron, title_id, format_type).


### Signal 6 — [Paused hold]

**Classification:** unjustified implementation choice 

**Rationale:** 
R6 specifies that paused holds are "skipped over" with "the next eligible patron notified," but the code adds an unspecified notification feature  that proactively emails paused patrons to inform them they were skipped: 
```code
            send_email(hold.patron,
                       subject=f"A title you held became available",
                       body="Your hold is paused, so we've skipped over it. "
                            "Resume your hold from your account settings if "
                            "you'd like to be notified next time.")
```

**Response:**
R6 only specifies notifying the next eligible patron, and adding this notification expands scope without explicit authorization. 
Please remove the send_email() call for paused holds (lines 175-179) for now. 
If we think this notification is valuable, let's add it to the spec explicitly after discussing the email copy and patron experience.


### Signal 7 — [SMS Notification]

**Classification:** spec gap

**Rationale:** 
R12's main text suggests email is "by default" with SMS as an "opt-in" addition (implying both), but the Note and Assumptions section flag this as an unresolved business decision, creating ambiguity the FDE should have clarified before the spec was complete.

**Response:**
You're right that R12 flags this as undecided — I should have gotten the business decision before spec completion.
Based on the 'opt-in' language suggesting additive behavior and the critical nature of hold notifications (patrons have only 72 hours to claim), updating R12 to specify dual-channel: SMS-opted patrons receive both email and SMS. 
This ensures notifications reach patrons reliably even if they miss one channel. 
Update the notification logic to send email to all patrons, plus SMS to those who have opted in.


### Signal 8 — [Builder question]

**Classification:** legitimate clarification request

**Rationale:** 
The Assumptions section explicitly flags the Academic + Accessibility-priority intersection as "not specified" and "pending FDE confirmation"; the builder correctly identified the ambiguity, blocked the PR, and articulated specific interpretation options rather than guessing. 

**Response:**
Good catch — you're right that the Assumptions section left this unresolved. 
Going with option (a): 
Accessibility R4 wins completely, so academic+accessibility patrons jump to position 1 and the 0.5x weight doesn't apply at all when the patron has the accessibility modifier. 
The academic weight is only relevant when comparing academic vs standard patrons, not for accessibility-priority logic. 
Thanks for catching this before implementing — updating the spec to make this explicit in R4 and removing the 'pending' flag from Assumptions.


### Reflection 
The hardest distinction for me was differentiating spec ambiguity (Category 1) from builder misread (Category 2), particularly in Signal 7. 
My initial instinct was builder misread because "opt-in" linguistically suggests additive behavior, but the Note and Assumptions section explicitly flagging it as "pending decision" meant the FDE created ambiguity rather than the builder misreading clear language. This taught me that the ownership question — "whose artifact needs to change?" — is critical: when the spec itself flags uncertainty, I own it even if the wording seemed clear. If I ran this exercise again, I'd force myself to read Assumptions first before classifying any signal, since those flags change whether ambiguity is intentional (legitimate clarification) or accidental (spec gap). 
I also realized I need to check my impulse toward defensive reading when I agree with the builder's interpretation.
