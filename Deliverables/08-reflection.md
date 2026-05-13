# D#8 — Reflection Document

**Engagement:** MedFlex Healthcare Staffing  
**Prepared by:** Andrzej Bihun  
**Date:** 2026-05-13

---

## What this engagement produced — and what was missing

I built a three-agent architecture, two capability specs, and a working demo in under two days. The starting point was one 60-minute discovery session with one person — the CEO, Marcus. The design is technically correct. But several gaps appeared during the build-loop and through Marcus's feedback. All of them have the same root cause: the design was based on Marcus's description of the business, not on what the business actually looks like day to day.

If I had more time, I would have done four things differently.

---

## 1. Learn more about the business before proposing a solution

I focused almost entirely on the main problem Marcus described: matching nurses to shifts faster. I did not explore the wider business context.

For example, I do not know how MedFlex earns money on each placement. I do not know whether the 7% mismatch rate is spread evenly across all hospitals or concentrated in a few accounts. I do not know whether emergency same-day fills are more profitable than planned shifts.

These details matter. If most mismatches happen at two hospitals, the confidence scoring should be calibrated differently for those accounts. If emergency fills bring much higher revenue, Agent 3 (no-show prevention) might deliver more value in year one than Agent 2. I made assumptions because I did not have the data. In a real engagement, I would spend time understanding the economics and the patterns before deciding what to build.

---

## 2. Observe workflows and talk to employees before writing specs

The most costly mistake in this engagement was writing a key spec requirement without first checking how coordinators actually work.

In Requirement 5 of D#4b, I set a 30-minute recall window for MEDIUM-confidence proposals. This assumed coordinators are watching the system continuously. But Kim — the senior coordinator — confirmed to Marcus that coordinators check the queue every one to two hours during busy periods. The 30-minute window would expire before they ever saw the alert.

I only learned this from Marcus's feedback. If I had spent 90 minutes talking to Kim before writing the spec, this window would have been 90 minutes from the start. One conversation would have saved a spec revision, an architecture ADR update, and a code change.

The same applies to the nurse availability data. I flagged it as an "unverified assumption" in D#3 because I never asked Kim or Aaron how the availability database is actually updated. In a production engagement, that kind of assumption must be verified before the spec is finalised.

The lesson is simple: one hour of talking to the people doing the work is worth more than a full day of design.

---

## 3. Draw a process diagram and break it into jobs to be done

I assigned delegation archetypes — Fully Agentic, Agent-Led, Human-Led — to each workflow step based on what Marcus told me. What I did not do was map what a coordinator actually thinks and does when they match a nurse to a shift.

As a BA, my natural next step would be to draw a process diagram and decompose each step into Jobs to Be Done: what is the person trying to achieve, what information do they need, where do they feel uncertain, and where do they spend most of their time?

This decomposition would have answered questions that the current spec leaves open. For example: what does "hospital preference" really mean to a coordinator? Is it one number, or a combination of factors? At what point does urgency override credentials? What is the actual reason a MEDIUM-confidence match goes wrong — is it the wrong credentials, or is it a nurse who accepted the shift but did not really want it?

Without this analysis, the scoring weights in Agent 2 (proximity 0.30, preference 0.25, reliability 0.25, specialty 0.20) are reasonable guesses. A 30-minute interview with a senior coordinator would have confirmed or replaced them with real data. Agent designs built on unverified weights will need recalibration in production.

---

## 4. Document employee pain points before defining success metrics

The success metrics in D#1 are Marcus's metrics: fill time under one hour, mismatch rate below 1%, more than 50% of matches handled automatically. These are the right metrics for a board presentation. They are not the metrics that matter to a coordinator.

A coordinator handling 120 decisions per day has different pain points: a request that arrives at the end of the day with no date, a nurse who confirms by text but cannot be reached by phone, a hospital that calls at 6am to report a no-show. These situations are the real source of the 12% no-show rate, the escalation backlog, and the coordinator frustration that caused Marcus's previous two AI projects to fail.

If I had documented these pain points — ideally through conversations with Kim and one or two other coordinators — the agent designs would have been built around the real edge cases, not the typical case. The validation plan in D#7 would have included failure scenarios drawn from actual experience. And the argument for why this engagement is different from the chatbot and the recommendation engine would have been backed by coordinator voices, not only by the CEO's view.

---

## Overall lesson

This engagement produced a working design in two days. The trade-off for that speed is that several important assumptions were never verified: how coordinators actually review proposals, how up to date the availability data is, and where the mismatch rate really comes from. In a real production project, any one of these gaps could block Phase 1 launch.

The FDE methodology says clearly: start from lived work, not from documented processes. The time constraint at Gate 3 made that impossible to do fully. The right response to an incomplete discovery is not to ignore the gaps, but to build safeguards into the design that compensate for them. Shadow review, leading drift indicators, and the 30-day calibration gate are all in the architecture for exactly that reason. They exist because the discovery was incomplete, and because I knew it.
