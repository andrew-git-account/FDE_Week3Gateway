# D#6 — Client Feedback Response

**Engagement:** MedFlex Healthcare Staffing  
**To:** Marcus Reyes, CEO  
**From:** Andrzej Bihun, FDE  
**Re:** Your three questions before Phase 1 approval  
**Date:** 2026-05-15

---

Marcus —

Thank you for the specific questions. Below is a concrete answer to each one. I've updated the specs and architecture to reflect two changes your feedback surfaced; the third I'm pushing back on with a rationale.

---

## Point 1 — Board update is in 6 weeks, not 8

**My answer: Yes to 6 weeks. Here is what I'm cutting and what that costs you.**

The matching agent (Agent 1 + Agent 2) runs on real volume by week 6. That is the deliverable. What is not in week 6:

**Deferred to weeks 7–8:**
- The coordinator review dashboard UI. Coordinators will work off raw alerts (email/SMS notification with proposal details) and a lightweight audit log for the first two weeks of live operation. This is not a capability gap — it is a UX gap. The agent is still matching, still routing, still producing the proposal. Coordinators just review it in a less polished interface.

**Deferred to Phase 2 (weeks 9–16):**
- Agent 3 confirmation and no-show prevention state machine
- Portal and phone intake (email-only in Phase 1; the other two channels remain manual)

**What you can demo at week 6:** Agent 1 parses a hospital email → Agent 2 matches a nurse and auto-submits a HIGH-confidence proposal → coordinator sees a MEDIUM-confidence proposal with a recall link. That is the core loop. The board sees a working matching agent on real MedFlex volume. You do not need the dashboard for that demo.

**The trade-off I want you to acknowledge:** Without the dashboard in weeks 1–6, coordinators have a slightly higher review burden — they're reading alert emails rather than a purpose-built queue. If Kim tells you this is operationally unacceptable, I need to know now, because accommodating it either slips the timeline back to week 8 or drops something else from scope.

I need a "yes, coordinators can work from alerts for two weeks" before I lock week 6 as the delivery date.

---

## Point 2 — You need a drift signal in week 2, not a number on day 30

**My answer: You are right. The spec was incomplete. I've added two leading indicators.**

The original design had one signal: mismatch rate after 30 days. You correctly identified the problem — that's a lagging outcome measure. By the time a mismatch appears in the rate, a proposal has gone out, been accepted, and the wrong nurse has already shown up. I should have caught this before the spec was finalised.

**Two leading indicators, both visible from week 2:**

**1. Hospital acceptance rate trend by confidence band (weekly)**  
Each week, I track what percentage of AUTO_SUBMIT proposals the hospital actually accepts. If that rate starts declining — hospitals are rejecting or ignoring our highest-confidence matches — the agent is drifting before any mismatch is logged. A 5-percentage-point week-over-week drop triggers an on-call alert. This is visible from week 2 as soon as you have enough AUTO_SUBMIT volume to compute a rate.

**2. Coordinator flag rate per week (not per 30 days)**  
During Phase 1, coordinators can flag any AUTO_SUBMIT proposal in the shadow audit log. I originally reported this as a 30-day aggregate. I've changed it to a weekly count with a trend line. If the flag count doubles week-over-week, that's an early calibration signal — the agent's judgment and coordinator judgment are diverging, before any hospital has complained.

**The 30-day gate stays**, but it is now one of three signals, not the only one. At week 2 you can look at the dashboard and say "acceptance rate is holding at 91%, flag count is flat — we're calibrated." Or "acceptance rate dropped 8 points this week — investigate before we go further." That is the signal you asked for.

I've updated the Observability section of the Shift Matching spec (D#4b) with both metrics and their alert thresholds.

---

## Point 3 — Kim's concern about the 30-minute recall window

**My answer: The 30-minute window was wrong. I've updated it to 90 minutes and changed the lapse behaviour.**

Kim's input changes the design assumption directly. A 30-minute recall window assumes coordinators are monitoring continuously. They are not — they batch-check the queue every 1–2 hours when volume spikes, which is exactly when MEDIUM-confidence proposals are most likely to appear. A window that expires during the busiest part of the day is functionally non-operative.

**Two changes I've made to the spec:**

**1. Recall window extended to 90 minutes**  
This covers at least one full batch-check cycle. Coordinators working a busy queue have a realistic chance of reviewing a MEDIUM-confidence proposal before the window closes.

**2. Lapse behaviour changed: unreviewed ≠ approved**  
The original spec said: "if window expires without action, log as coordinator-cleared." That is the scenario you flagged — the wrong nurse gets confirmed because nobody looked. I've removed that. The new behaviour: if a proposal reaches `recall_window_expires_at` without the coordinator opening it, status becomes `LAPSED_UNREVIEWED` and it escalates to the team lead with a 15-minute intervention window. The proposal is not finalised until a human has either reviewed it or the team lead clears it.

**What this costs:** Proposals now take up to 105 minutes (90 min window + 15 min team lead) to finalise in the worst case. That is still a 2.4× improvement on the 4.2-hour baseline. The team lead escalation adds a new workload; Kim should confirm this is operationally manageable before Phase 1 go-live.

I've updated D#3 ADR-03 and D#4b Requirement 5 to reflect both changes.

---

## Summary of changes I've made

| Marcus's question | Change made | Where |
|-------------------|-------------|-------|
| 6-week board demo | Phase 1 scope reduced; dashboard deferred to weeks 7–8 | D#3 Phase Delivery |
| Week-2 drift signal | Hospital acceptance rate + weekly flag rate added as leading indicators | D#4b Observability |
| Recall window lapse | Window extended to 90 min; lapse escalates to team lead (not auto-cleared) | D#3 ADR-03, D#4b Requirement 5 |

One open item requiring your sign-off before I lock week 6: **Can coordinators work from raw email alerts (no dashboard UI) for the first two weeks of live operation?** If yes, week 6 is confirmed. If no, the timeline is week 8 or we cut scope further.

— Andrzej
