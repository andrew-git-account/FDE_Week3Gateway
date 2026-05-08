# Stakeholder Presentation Strategy: Sarah Whitmore (COO)

## Purpose

This document outlines how to present the agentic transformation proposal to Sarah Whitmore in a way that:
- **Addresses her skepticism** (2 prior automation failures)
- **Uses her language** (operations metrics, not AI buzzwords)
- **Demonstrates understanding** of her constraints (Aurum, dispatcher expertise, team capacity)
- **Offers low-risk proof** before big commitments
- **Frames as augmentation**, not replacement

---

## 1. Opening: Acknowledge Her Skepticism (First 2 Minutes)

### What NOT to Say
❌ "AI will revolutionize your operations"  
❌ "Our cutting-edge machine learning models..."  
❌ "This chatbot can handle all customer inquiries"  
❌ "Just trust us, it'll work"

### What TO Say

> **"Sarah, I know you've been burned twice — the chatbot customers hated, and the RPA that broke every time Aurum's schema changed. I'm not here to sell you another chatbot. I'm here to show you three specific things your team does every day that we can make faster, without touching Aurum's batch system or replacing your dispatchers' judgment."**

**Why This Works**:
- Names the failures explicitly (shows we listened)
- Promises specificity (not vague "AI transformation")
- Acknowledges Aurum constraint upfront (we're not naive)
- Frames as augmentation ("make faster") not replacement

---

## 2. The Problem in Her Language (3 Minutes)

### Frame 1: Capacity vs. Volume Growth

**Visual**: Simple bar chart

```
Customer Ops Capacity
┌─────────────────────────────────────┐
│ Available: 262 hrs/day (35 FTE)     │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░│
│                                     │
│ On Cases: 118 hrs/day               │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓                      │
│                                     │
│ ETA Inquiries: 73 hrs/day (28%)     │
│ ▓▓▓▓▓▓▓▓                           │
└─────────────────────────────────────┘

Problem: When volume grows 20% (next year), 
you need 7 more people just to handle ETA inquiries.
```

**Narrative**:
> "Your team handles 730 cases a day across 4 work types. But 400 of those — more than half — are customers asking 'Where's my delivery?' That's 73 hours a day spent on lookups. When your CEO talks about that competitor saving £1.2M, this is what they automated: the high-volume, low-complexity work that scales linearly with delivery growth."

**Key Message**: Volume growth is coming. Without automation, you hire proportionally. With automation, you absorb growth with current headcount.

---

### Frame 2: The Hayes & Sons Problem

**Visual**: Timeline of the email thread (from artefact)

```
Hayes & Sons Dispute Timeline
Day 1  09:14  Customer emails: "Remove £340 surcharge, delivery damaged"
       16:48  Billing deflects: "Contact Customer Ops"
                ⬇️ 3 days lost

Day 4  11:02  Customer escalates: "On hold 22 min, dropped call. 
              Second time this quarter. Who's your manager?"
                ⬇️ 2 days lost

Day 6  15:30  Sandra resolves: "£170 goodwill credit applied"
                ⬇️ 6 days total

Problem: Sandra spent 20 min investigating (across 4 systems).
         Customer waited 6 days and threatened escalation.
         This is your 3rd fuel-surcharge-on-damage dispute this month.
```

**Narrative**:
> "Hayes & Sons has a £25K credit limit and £10K in open receivables. They're frustrated — this is their second fuel surcharge dispute this quarter. Sandra resolved it in 6 days with a £170 credit. But 20 of those minutes were Sandra pulling data from Aurum exports, CRM, delivery logs, and receivables aging. An agent can do that in 2 minutes. Sandra still decides the credit amount — she's the expert. But she gets the investigation summary instantly, not after 20 minutes of clicking through systems."

**Key Message**: Agent doesn't replace Sandra's judgment. It replaces the 20 minutes of data gathering that Sandra hates doing anyway.

---

## 3. The Solution: Three Concrete Capabilities (5 Minutes)

### Capability 1: ETA Inquiries → 90% Automated

**Customer View**:
```
BEFORE (Current):
Customer SMS: "Where is order AX-771-3344?"
          ⬇️ 11 minutes (agent queries CRM, calls Dispatch for GPS)
Agent SMS: "Your order is on route 028. ETA window 13:00-17:00."
Customer: "That's 4 hours, be more specific?"
          ⬇️ 5 more minutes (agent waits for Dispatch callback)
Agent SMS: "Best guess 14:00-15:00. Traffic: moderate."

Total: 11-16 minutes, customer frustrated by wait + imprecision


AFTER (Agent):
Customer SMS: "Where is order AX-771-3344?"
          ⬇️ <30 seconds (agent queries CRM + GPS + traffic)
Agent SMS: "Based on driver location (Watford), your delivery 
            is estimated 14:00-14:30 today. Traffic: moderate. 
            I'll notify you when driver is nearby."

Total: <30 seconds, customer satisfied, no human involved
```

**What We're NOT Doing**:
- ❌ Building a chatbot (conversational AI that customers hate)
- ❌ Replacing your Customer Ops team
- ❌ Handling complex inquiries (complaints, exceptions, disputes)

**What We ARE Doing**:
- ✅ Automating the 400 daily lookups (GPS query + ETA calculation)
- ✅ Freeing 66 hours/day (8.8 FTE worth of capacity)
- ✅ Escalating to human when GPS stale, customer demands callback, or order not found

**Sarah's Concern**: "What if the agent gives wrong ETAs?"

**Response**:
> "Fair concern. Here's how we handle that: Agent only provides high-confidence ETAs when GPS data is <15 minutes old and traffic data is available. If GPS is stale (30+ min), agent escalates to your team with a message like 'Driver location data is outdated, connecting you with dispatch for live update.' We track accuracy weekly — if it drops below 90%, we tune the agent. And customers can always reply 'AGENT' to speak with a person immediately."

---

### Capability 2: Billing Dispute Investigation → 64% Faster

**Sandra's Current Workflow** (28 minutes):
1. Read customer email (2 min)
2. Query Aurum export for invoice (5 min — find CSV file, search for invoice)
3. Query Aurum for fuel surcharge detail (3 min)
4. Check CRM for customer history (4 min — past disputes, payment behavior)
5. Check delivery logs for damage claim (4 min — was damage reported by driver?)
6. Review receivables aging (2 min — is customer current or 90-day aged?)
7. Decide credit amount (5 min — judgment call: £0, partial, full?)
8. Draft email to customer (3 min)

**Agent-Assisted Workflow** (8 minutes):
1. Agent reads email, queries all 4 systems in parallel (2 min — automated)
2. Agent presents investigation summary to Sandra:
   ```
   Dispute: INV-2026-04318, Hayes & Sons
   Invoice: £3,816 total, £340 fuel surcharge (Route R-008, Tier T3)
   Damage Claim: Driver noted "pallet leaning" in delivery log
   Customer History: 2 prior FUEL_SURCH_DAMAGE disputes (90 days)
   Payment Behavior: £10,272 open receivables (aged 0-90 days)
   Recommendation: £170 credit (50% split, preserves relationship)
   Confidence: Medium (pattern-based on similar disputes)
   ```
3. Sandra reviews summary (2 min)
4. Sandra decides: Accept £170, modify to £200, or reject (1 min — her judgment)
5. Agent drafts email based on decision (1 min — automated)
6. Sandra approves email, agent logs credit in CRM (2 min)

**What We're NOT Doing**:
- ❌ Deciding credit amounts automatically (that's Sandra's call)
- ❌ Bypassing Aurum (still batch exports, still 48-hour tickets)
- ❌ Replacing Sandra's relationship knowledge

**What We ARE Doing**:
- ✅ Aggregating data from 4 systems (Aurum, CRM, delivery logs, aging) in 2 minutes vs. 20
- ✅ Recommending credit amounts based on past patterns (Sandra can override)
- ✅ Creating audit trail (every credit logged in CRM, fixes Sandra's "manual override" gap)

**Sarah's Concern**: "What about Aurum? You can't change that system."

**Response**:
> "Correct — and we're not trying to. Aurum's batch exports (T-1 lag, no API) are a constraint we design around, not a problem we solve. The agent reads yesterday's CSV files, which is fine — most disputes are for invoices 3-7 days old anyway. If a customer disputes today's invoice, agent says 'Your invoice is being processed, I'll have details tomorrow morning.' The agent doesn't need real-time Aurum access to save Sandra 20 minutes of investigation time."

---

### Capability 3: Delivery Exception Triage → Unblock Drivers (Phase 3, Months 7-9)

**Current Problem** (from voicemail artefact):
- Mark Petrov (driver, route 042) at Stein-Allen with leaning pallet
- Recipient refuses, driver uncertain (damaged or just cosmetic?)
- Driver calls Sandra → line busy
- Driver parked, 6 more deliveries waiting
- **Result**: 20+ min wait for callback, downstream deliveries delayed

**Agent-Assisted Workflow**:
- Driver reports exception via Driver App ("Recipient refused, pallet leaning")
- Agent triages:
  - Package value? £280 (low-value)
  - Customer tier? STANDARD (not VIP)
  - Refusal reason? Cosmetic damage (not structural)
  - **Agent decision**: "Return to depot" (low-stakes, follows heuristic)
- Driver receives instruction in <2 min, proceeds to next delivery

**BUT** if:
- Package value >£500, OR
- Customer tier = VIP (Stein-Allen is large account), OR
- Structural damage (safety risk)
- **Agent escalates**: "Hold position, dispatcher reviewing. ETA 5 min."

**What We're NOT Doing**:
- ❌ Replacing dispatcher judgment on VIP customers or high-value packages
- ❌ Making damage assessment decisions (safety, insurance implications)

**What We ARE Doing**:
- ✅ Handling 60% of routine exceptions (low-value, standard refusals) that follow clear heuristics
- ✅ Freeing Sandra to focus on 40% complex cases (VIP customers, damage claims)
- ✅ Reducing driver wait time from 20 min to <2 min

**Sarah's Concern**: "Sandra's judgment is why we don't have more problems. How do you replicate that?"

**Response**:
> "We don't replicate it — we codify the 60% of cases that follow a pattern, and escalate the 40% that require her expertise. Before Phase 3, we sit with Sandra for a day, shadow her handling 20 exceptions, and document: 'For packages under £500 with standard refusals from non-VIP customers, you always say return to depot.' That becomes the agent's rule. For everything else — VIP customers, damage claims, high-value packages — agent escalates to Sandra. She's still making the hard calls. Agent just handles the routine ones."

---

## 4. The Proof: Phased Rollout (Low-Risk) (3 Minutes)

### Phase 1A: Prove It Works (Months 1-2, £0 Risk)

**Scope**: ETA inquiries, scheduled window only (no GPS API needed yet)

**Pilot**:
- 50 inquiries/day (12.5% of volume)
- SMS channel only
- 3 Customer Ops agents volunteer to review agent responses before sending
- **Success Metric**: 80% of responses approved by human reviewers without modification

**Sarah's Decision Point** (End of Month 2):
- If success: Proceed to Phase 1B (GPS integration, 90% deflection)
- If failure: Pause, diagnose, adjust, or stop (£0 sunk cost — pilot is internal only)

---

### Phase 1B: Scale to Full Volume (Month 3)

**Scope**: ETA inquiries with precision calculation (GPS + traffic)

**Prerequisite**: GPS API access negotiated with Dispatch/IT

**Rollout**:
- 400 inquiries/day (100% of ETA volume)
- Multi-channel (SMS, email, web portal)
- Human agents handle escalations (10-15% of cases)

**Success Metric**: 
- 85-90% deflection rate
- <30 sec response time (p50)
- >4.0/5 CSAT (customer satisfaction)
- >90% ETA accuracy (±30 min tolerance)

**Sarah's Decision Point** (End of Month 3):
- If success: Proceed to Phase 2 (billing disputes)
- If partial success (e.g., 70% deflection): Tune agent for 4 weeks, re-assess
- If failure: Stop Phase 1, do NOT proceed to Phase 2 (cut losses early)

---

### Phase 2: Billing Disputes (Months 4-6)

**Scope**: Dispute investigation (agent-accelerated), human approval (Sandra decides credit)

**Rollout**:
- 60 disputes/day (100% of billing volume)
- Agent investigates, Sandra approves
- Aurum CSV pipeline operational (daily ingestion)

**Success Metric**:
- Investigation time: 28 min → 8 min (64% reduction)
- Resolution time: 6-9 days → <48 hours (customer-facing)
- Audit compliance: 100% (all credits logged in CRM)

**Sarah's Decision Point** (End of Month 6):
- If success: Proceed to Phase 3 (exception triage)
- If failure: Keep Phase 1 (ETA deflection working), stop Phase 2

---

### Phase 3: Exception Triage (Months 7-9)

**Scope**: Low-value, routine exceptions (agent-led), complex exceptions (human-led)

**Prerequisite**: Dispatcher heuristics codified (workshop with Sandra)

**Rollout**:
- 108 exceptions/day (60% of volume — low-stakes cases only)
- 72 exceptions/day (40%) escalate to Sandra
- Driver wait time: 20 min → <2 min (for agent-handled cases)

**Success Metric**:
- Driver wait time <2 min (agent-handled)
- Dispatcher override rate <20% (agent decisions correct)
- Sandra's line not constantly busy

---

## 5. The Business Case in Her Language (2 Minutes)

### Year 1 (Phases 1-3 Complete):

```
Cost Avoidance (Growth Absorption):
┌────────────────────────────────────────────┐
│ Volume grows 20% next year                 │
│ Without agent: Hire 7 FTE (£280K)          │
│ With agent: Hire 0 FTE (growth absorbed)   │
│ ────────────────────────────────────────   │
│ Savings: £280K                             │
└────────────────────────────────────────────┘

Capacity Freed (Redeployment):
┌────────────────────────────────────────────┐
│ ETA inquiries: 66 hrs/day freed            │
│ Billing disputes: 20 hrs/day freed         │
│ Exceptions: 18 hrs/day freed               │
│ ────────────────────────────────────────   │
│ Total: 104 hrs/day = 13.8 FTE equivalent   │
│                                            │
│ Redeployment options:                      │
│ • Absorb growth (20%+ volume)              │
│ • Improve service (proactive outreach)     │
│ • Reduce backlog (disputes <48 hr)         │
└────────────────────────────────────────────┘

Customer Experience:
┌────────────────────────────────────────────┐
│ ETA response: 11 min → <30 sec             │
│ Billing disputes: 6-9 days → <48 hrs       │
│ Driver wait: 20 min → <2 min               │
└────────────────────────────────────────────┘

Total Year 1 Value: £437K
(vs. competitor's £1.2M / 2 = £600K target — we're 73% there)
```

---

### Year 2 (With Volume Growth + Phase 4 Exploration):

```
Year 1 baseline: £437K
+ Volume growth (20%): +£140K (more cases deflected)
+ Operational efficiencies: +£50K (fewer repeat contacts)
────────────────────────────────────
Year 2 Total: £627K

Phase 4 potential (dispatch optimization): +£60K
────────────────────────────────────
Year 2 with Phase 4: £687K

Competitor benchmark (adjusted): £600K
Our projection: £627-687K (ON OR ABOVE benchmark)
```

**Key Message**: 
> "We're not promising £1.2M Year 1 — that's the competitor's number, and they're twice your size. Our plan delivers £437K Year 1, scaling to £600-700K by Year 2 with volume growth. That's proportional to the competitor's results, and it's conservative — we're not counting Phase 4 (dispatch optimization) which could add another £60-100K."

---

## 6. What We're NOT Promising (Critical: Address Skepticism) (2 Minutes)

### Honest Limitations

**What This Is NOT**:
1. ❌ **Not a chatbot**: Customers don't "chat" with an AI. Agent handles structured inquiries (ETA lookups, dispute investigations), not open-ended conversations ("I'm unhappy, what can you do for me?").

2. ❌ **Not replacing your team**: 35 FTE stays 35 FTE. Freed capacity absorbs growth or redeploys to higher-value work (proactive outreach, dispute prevention, relationship management).

3. ❌ **Not touching Aurum**: We accept Aurum's batch-only constraint (T-1 lag, 48-hour tickets). Agent works around it, not through it.

4. ❌ **Not 100% accurate**: ETA accuracy target is 90-95% (±30 min), not 100%. When GPS is stale or traffic unpredictable, agent escalates to human. We track accuracy weekly and tune.

5. ❌ **Not zero human oversight**: Phases 1-2 are heavily monitored (10% spot-checks weekly). Phase 3 requires dispatcher workshops (codify heuristics). This is organizational change, not just tech deployment.

---

### What We Learned from Your Prior Failures

**2024 Chatbot (Customers Hated)**:
- **Failure Mode**: Too conversational, too robotic, couldn't handle edge cases
- **Our Design**: Agent handles structured inquiries only (ETA, billing investigation). Conversational AI is out of scope. Empathy phrases in templates ("I understand you're waiting...") but not trying to replicate human conversation.
- **Fail-Safe**: If customer replies "AGENT" at any point, immediate human escalation (no friction).

**RPA Billing Recon (Broke When Aurum Schema Changed)**:
- **Failure Mode**: Brittle integration, no schema change monitoring, silent failures
- **Our Design**: 
  - Monitor CSV parse success rate daily (alert if <90%)
  - Flexible CSV parsing (column name + position matching, not hardcoded)
  - If Aurum schema changes, agent flags parse errors and escalates to IT (doesn't silently break)
  - Weekly reconciliation: CRM credits vs. Aurum credits (catch divergence early)

---

## 7. Your Decision Points (1 Minute)

### Decision 1 (Today): Proceed to Phase 1A Pilot?

**If YES**:
- Next step: 2-week sprint to build Phase 1A (ETA scheduled window)
- Your commitment: 3 Customer Ops agents volunteer for pilot (4 weeks, 50 inquiries/day)
- Our commitment: Weekly progress reviews, honest about what's working and what's not
- Decision Point 2: End of Month 2 (proceed to Phase 1B or stop)

**If NO**:
- That's fine. What would need to change for you to say yes? (e.g., smaller pilot, different work stream, more IT involvement?)

---

### Decision 2 (End of Month 2): Scale Phase 1A → Phase 1B?

**Criteria**:
- Did Phase 1A achieve 80% approval rate from human reviewers?
- Did customers accept scheduled window responses (no complaints about agent being robotic)?
- Did agent handle escalations correctly (no cases where agent should have escalated but didn't)?

**If YES**: Proceed to Phase 1B (GPS API integration, 90% deflection target)

**If NO**: Diagnose failure (tone issues, accuracy issues, escalation logic), tune for 4 weeks, re-pilot

---

### Decision 3 (End of Month 3): Proceed to Phase 2 (Billing Disputes)?

**Criteria**:
- Did Phase 1B achieve 85-90% deflection rate?
- Is ETA accuracy >90%?
- Is CSAT >4.0/5?

**If YES**: Proceed to Phase 2 (billing dispute investigation)

**If NO**: Keep Phase 1 operational (it's working), stop further phases (don't expand failure)

---

## 8. Presentation Structure (Total: 20 Minutes)

### Slide 1: Opening (2 min)
**Title**: "Three Things We Can Make Faster — Without Touching Aurum or Replacing Your Dispatchers"

**Content**:
- Acknowledge prior failures (chatbot, RPA)
- Promise specificity (not vague AI transformation)
- Frame as augmentation (not replacement)

---

### Slide 2-3: The Problem (3 min)
**Title**: "Capacity vs. Growth" + "The Hayes & Sons Problem"

**Content**:
- Bar chart: 73 hrs/day on ETA inquiries (28% of capacity)
- Timeline: 6-day billing dispute (20 min investigation, customer frustrated)

---

### Slide 4-6: The Solution (5 min)
**Title**: "Capability 1: ETA Inquiries → 90% Automated"  
**Title**: "Capability 2: Billing Disputes → 64% Faster"  
**Title**: "Capability 3: Exception Triage → Unblock Drivers"

**Content**:
- Before/After workflows (visual)
- "What We're NOT Doing" (address skepticism)
- "What We ARE Doing" (specific, measurable)

---

### Slide 7: The Proof (3 min)
**Title**: "Phased Rollout: Prove It Works Before Committing"

**Content**:
- Phase 1A (Months 1-2): Pilot, 50 inquiries/day, £0 risk
- Phase 1B (Month 3): Scale to 400/day, GPS integration
- Phase 2 (Months 4-6): Billing disputes
- Phase 3 (Months 7-9): Exception triage
- Decision Points: Stop early if not working

---

### Slide 8: The Business Case (2 min)
**Title**: "Year 1: £437K Value, Year 2: £627K (On Benchmark)"

**Content**:
- Cost avoidance: £280K (7 FTE avoided)
- Capacity freed: 104 hrs/day (13.8 FTE equivalent)
- Customer experience: 11 min → <30 sec (ETA), 6 days → <48 hrs (disputes)

---

### Slide 9: Honest Limitations (2 min)
**Title**: "What We're NOT Promising"

**Content**:
- Not a chatbot (structured inquiries only)
- Not replacing team (35 FTE stays 35 FTE)
- Not touching Aurum (work within T-1 lag constraint)
- Not 100% accurate (90-95% ETA accuracy target)
- Not zero oversight (10% spot-checks, dispatcher workshops)

---

### Slide 10: Your Decision (1 min)
**Title**: "Decision 1: Proceed to Phase 1A Pilot?"

**Content**:
- If YES: 2-week sprint, 3 agents volunteer, 4-week pilot
- If NO: What would need to change?
- Decision Point 2: End of Month 2 (scale or stop)

---

### Slide 11: Q&A (2 min)
**Anticipated Questions**:
1. "What if GPS API isn't available?" → Phase 1A works without it (scheduled window only), Phase 1B deferred until API access negotiated
2. "What if dispatchers resist Phase 3?" → Don't proceed to Phase 3 unless dispatcher workshops successful (heuristics codified)
3. "What if agent gives wrong ETAs?" → Track accuracy weekly, escalate when GPS stale, customer can always request human

---

## 9. Closing: The "Something That Actually Works" Test

**Sarah's Criteria** (inferred from brief):
1. **Proves value quickly** (not 18-month pilot → production journey)
2. **Doesn't break when constraints change** (Aurum schema, GPS outage)
3. **Augments team, doesn't replace** (Sandra still makes credit decisions, dispatchers still handle VIP exceptions)
4. **Delivers on CEO benchmark** (£600K by Year 2, proportional to competitor's £1.2M)

**Our Response**:
> "Sarah, here's why this is 'something that actually works':
> 
> **Proves value quickly**: Phase 1A is 2 months, not 18. You'll see 50 inquiries/day deflected in Week 4. If it doesn't work, we stop. No sunk cost fallacy.
> 
> **Doesn't break when constraints change**: We're not integrating with Aurum (batch exports are fine). If GPS API goes down, agent falls back to scheduled window (graceful degradation, not catastrophic failure). If Aurum schema changes, agent flags parse errors and alerts IT (doesn't silently break like RPA did).
> 
> **Augments your team**: Sandra still decides credit amounts. Dispatchers still handle VIP exceptions. Agent handles the 60-70% of work that's routine — the lookups, the data gathering, the pattern-based triage. Your team focuses on the 30-40% that requires judgment and relationship knowledge.
> 
> **Delivers on benchmark**: £437K Year 1, £627K Year 2. That's proportional to the competitor your CEO mentioned (£1.2M at 2x your scale). And it's conservative — we're not counting Phase 4 (dispatch optimization) or proactive outreach, which could add another £60-100K.
> 
> **Most importantly**: If Phase 1A doesn't work in 2 months, we stop. You've lost 2 months of 3 agents' time (50 inquiries/day, ~4 hours/week). That's it. No million-pound contract, no 18-month implementation, no 'trust us it'll work eventually.' You decide every 2 months whether to continue or stop."

---

## 10. Follow-Up Materials to Leave Behind

1. **One-Pager**: "ETA Inquiry Agent — Phase 1A Pilot Plan"
   - 2-month timeline
   - 3 volunteer agents needed
   - Success criteria (80% approval rate)
   - Decision Point (end of Month 2: scale or stop)

2. **FAQ Document**: "10 Questions Sarah Will Ask"
   - GPS API access? (negotiate with Dispatch/IT)
   - Aurum constraint? (designed around it, not solving it)
   - Dispatcher resistance? (workshops before Phase 3, stop if no buy-in)
   - Cost? (£230-380K investment, £437K Year 1 return, 7-13 month payback)
   - What if it fails? (stop early, cut losses, no sunk cost fallacy)

3. **Case Study**: "How [Competitor] Saved £1.2M"
   - Break down competitor's approach (if known)
   - Map to Apex's scale (£600K proportional target)
   - Show our plan meets or exceeds benchmark

---

## Conclusion: Skepticism → Cautious Optimism

**Goal of Presentation**: Not to get full commitment (unrealistic given her skepticism), but to get **Decision 1: YES to Phase 1A Pilot**.

**Success Looks Like**:
- Sarah says: "Okay, let's try Phase 1A. But if it doesn't work in 2 months, we stop."
- Sarah assigns 3 Customer Ops agents to pilot (volunteers preferred)
- Sarah agrees to weekly progress reviews (transparency, no surprises)
- Sarah reserves judgment on Phases 2-3 (fair — prove Phase 1 first)

**Failure Looks Like**:
- Sarah says: "I've heard this before. Come back when you have a working prototype." (unrealistic ask, but signals deep distrust)
- Sarah says: "I can't spare 3 agents for 4 weeks." (capacity excuse, may be legitimate or resistance in disguise)
- Sarah delegates decision to IT ("Talk to IT about integrations first"). (punt, avoids ownership)

**If Failure**:
- Don't push. Ask: "What would need to be different for you to say yes? Smaller pilot (1 agent, 2 weeks)? Different work stream (billing disputes instead of ETA)? External validation (reference call with competitor who succeeded)?"

**The "Something That Actually Works" bar is high — and that's fair. She's been burned twice. Our job is to show we understand why those failed, and how our approach is different.**
