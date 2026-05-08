# Discovery Questions for Main Stakeholder (Sarah Whitmore, COO)

## Purpose

These discovery questions are designed for the **10-minute live clarification round** with Sarah Whitmore (COO). Each question is crafted so that **the answer would materially change the agent design scope, delegation level, or implementation approach**.

**Not Included**: Generic questions ("Tell me about your process," "What are your pain points"). These are exploratory, not diagnostic.

**Included**: Questions whose answers determine:
- Whether a work stream is automatable (vs. human-only)
- What delegation archetype applies (fully agentic vs. human-led)
- What system integrations are feasible (vs. blocked)
- What governance controls are required (credit thresholds, audit trails)
- What organizational resistance to expect (dispatcher trust, change management risk)

---

## Question Structure

Each question follows the **ATX discovery framework**:
1. **Context**: Why we're asking (what we've observed in artefacts or inferred from brief)
2. **Question**: Specific, answerable
3. **What Answer Changes**: How different answers affect agent design
4. **Follow-Up** (if needed): Probing question to detect evasion or ambiguity

---

## Category 1: Dispatcher Heuristic Codification (Delivery Exceptions)

### Question 1.1: Exception Decision Criteria

**Context**: 
Voicemail artefact shows Mark Petrov (driver) blocked at Stein-Allen with leaning pallet. He says "looks fine to me," but warehouse worker refused. Driver asks Sandra (dispatcher): "Do I return, leave, or what?" This reveals **dispatcher discretion drives exception decisions**, but criteria not documented (SOP Section 4.3 "Damaged consignments" incomplete).

**Question**:
> "Sandra, when Mark called about the leaning pallet at Stein-Allen, what factors would make you decide to **return-to-depot** versus **override the refusal and leave it**? Is there a pattern — like, if it's a VIP customer, you always override; if it's low-value, you always return — or is it different every time?"

**What Answer Changes**:

| Answer | Design Impact |
|---|---|
| **"There's a clear pattern"** (e.g., VIP customers get override attempts, standard customers get return-to-depot if value <£500) | **Agent-led triage** feasible for low-stakes cases (standard customers, low-value packages). Agent can apply heuristic autonomously, escalate VIP/high-value. |
| **"It depends on too many factors"** (customer relationship history, driver judgment reliability, re-delivery cost, time sensitivity — all subjective) | **Human-led with agent support**. Agent surfaces data (customer tier, package value, re-delivery cost), but Sandra must decide. Agent cannot replicate judgment. |
| **"I trust my gut / I just know"** (tacit knowledge, not articulable) | **Human-only** for exceptions. Agent cannot codify "gut feel." Phase 3 (exception triage) deferred until Sandra can document criteria. |

**Follow-Up** (if answer is vague):
> "If I asked 3 other dispatchers the same question about the Stein-Allen pallet, would they make the same decision you would, or would each decide differently?"

**Why This Follow-Up Matters**: If different dispatchers make different decisions, the process is not codified — agent cannot replicate inconsistent judgment. This signals organizational change management is needed (standardize dispatcher heuristics) before agent can assist.

---

### Question 1.2: Exception Frequency by Type

**Context**:
Brief states 180 exceptions/day (avg 12 min handle time). Voicemail shows 1 example (refused delivery). SOP mentions "refused," "damaged," "unattended addresses" as exception types. But we don't know **distribution** — are 80% refusals (relatively simple), or are exceptions evenly split across types (varied complexity)?

**Question**:
> "Of the 180 exceptions per day, roughly what percentage are **standard refusals** (customer not ready, wrong time), versus **damage claims** (pallet leaning, broken items), versus **address issues** (customer moved, wrong address)? And which type takes longest to resolve?"

**What Answer Changes**:

| Answer | Design Impact |
|---|---|
| **"80% are standard refusals, 10% damage, 10% address"** | **High automation potential**. Standard refusals follow heuristic (return-to-depot if low-value, re-attempt if VIP). Agent can handle 80% autonomously. |
| **"It's evenly split — 33% each"** | **Medium automation potential**. Only 1/3 of exceptions are simple (refusals). Damage and address issues require judgment → agent handles 33%, escalates 67%. |
| **"Damage claims are 50%, and those take 30 min each (investigation, photo review, insurance)"** | **Low automation potential**. Highest-volume exception type is also most complex → agent can assist investigation (retrieve customer history, delivery notes), but cannot decide. |

**Why This Matters**: If simple exceptions (refusals) are 80% of volume, agent can deflect majority. If complex exceptions (damage, address) dominate, agent's value is investigation support, not decision automation.

---

## Category 2: Customer Operations Capacity Reality Check

### Question 2.1: Handle Time vs. Elapsed Time

**Context**:
Brief states ETA inquiries average **4 min handle time**. But SMS artefact shows 11 min **elapsed time** (11:14 → 11:25) for a 2-message exchange. This suggests handle time = agent active time, not total time including waits (coordination with Dispatch, customer thinking, etc.).

Also, brief calculates 118 hours/day total labor (730 cases × ~10 min avg). But 35 FTE × 7.5 hours = 262.5 hours available → 55% apparent headroom. Yet email artefact shows **22-minute hold times**, suggesting capacity bottleneck, not excess capacity.

**Question**:
> "When you report that ETA inquiries take 4 minutes on average, does that include the time the agent is **waiting for Dispatch to provide GPS data** (like in the SMS example where the agent said 'one moment, checking with dispatch'), or is that just the time the agent is actively working?"

**What Answer Changes**:

| Answer | Design Impact |
|---|---|
| **"4 min is active time only; waits for Dispatch add 5-10 min on top"** | **True handle time is 9-14 min** (not 4 min). Agent's value is **eliminating coordination waits** (5-10 min saved per inquiry) by querying GPS directly. ROI calculation adjusted: 73 hrs/day current (not 27 hrs) → 7 hrs/day future = **£301K annual savings** (vs. £135K if using 4-min baseline). |
| **"4 min includes everything"** | Brief's 4-min figure is accurate. Agent's value is **speed** (4 min → <30 sec), not wait elimination. ROI lower: £135K annual savings. |

**Follow-Up**:
> "You have 35 people in Customer Ops, which is 262 hours/day available. But your case metrics suggest only 118 hours/day are on tracked cases. What's consuming the other 144 hours — meetings, training, email triage, rework?"

**Why This Matters**: If 55% of capacity is "untracked work," agent deflection won't reduce headcount (capacity freed is absorbed by untracked work). Instead, agent enables **growth absorption** (handle 20% more volume without hiring). This shifts ROI narrative from "cost reduction" to "cost avoidance."

---

## Category 3: GPS Data Architecture & Freshness

### Question 3.1: GPS API Access for Customer Ops

**Context**:
SMS artefact shows Customer Ops agent must **ask Dispatch** for GPS data (5-min wait: 11:19 → 11:24). This suggests Customer Ops does not have direct access to Driver App GPS backend. If agent inherits same constraint (must coordinate with Dispatch), deflection purpose defeated.

**Question**:
> "Currently, when a Customer Ops agent needs driver GPS data for an ETA inquiry, do they have **direct access** to the Driver App system, or do they have to **call Dispatch** to get that information?"

**What Answer Changes**:

| Answer | Design Impact |
|---|---|
| **"They call Dispatch"** (information silo) | **GPS API access is a prerequisite** for Phase 1B (precision ETA). Agent cannot deflect inquiries if it must coordinate with Dispatch. **Negotiation required**: Grant Customer Ops (via agent) read-only GPS API access. If denied, Phase 1B blocked → Phase 1A only (scheduled window, 50% deflection vs. 90% target). |
| **"They can query Driver App system directly, but it's slow/manual"** | **API exists but not optimized**. Agent can use existing access, but may need API performance improvements (faster queries, batch endpoints). Phase 1B feasible. |
| **"They have access, it's just that our GPS updates every 30 min"** | **Data freshness issue, not access issue**. Agent can query GPS, but staleness (30 min) limits accuracy. Phase 1B proceeds, but escalation rate higher (GPS stale → escalate). Budget for GPS polling interval increase (5-10 min target). |

**Follow-Up** (if answer is "they can access"):
> "When they query GPS, how fresh is the data? Are we talking 5 minutes old, 30 minutes, or real-time?"

**Why This Matters**: If GPS is 30+ min stale, agent provides low-confidence ETAs → customer dissatisfaction → defeats deflection purpose. Freshness target: <15 min for precision ETA.

---

### Question 3.2: GPS Polling Interval & Infrastructure

**Context**:
SMS artefact shows GPS timestamp 10:48, query response 11:24 → **36 minutes stale**. Industry standard for delivery tracking is 5-10 min polling. If Apex's polling interval is 30 min, agent cannot provide accurate ETAs without infrastructure upgrade.

**Question**:
> "How often does the Driver App send GPS updates — every 5 minutes, 15 minutes, 30 minutes? And is that something we could increase to 5-10 minutes if it helps with customer ETA precision?"

**What Answer Changes**:

| Answer | Design Impact |
|---|---|
| **"It's 30 min to save driver phone battery"** | **Polling interval is configurable** but constrained by battery life. **Trade-off decision needed**: Increase polling to 10 min (better ETA precision) vs. maintain 30 min (longer battery). **Mitigation**: Vehicle charging docks for driver devices, or newer devices with better battery. Budget £5-10K for device upgrades (if required). |
| **"It's 5-10 min, but coverage gaps in rural areas"** | **Network coverage issue, not polling config**. Agent handles GPS staleness gracefully (if >30 min stale, escalate). No infrastructure fix available (mobile network coverage not under Apex control). |
| **"Drivers can disable GPS to save battery"** | **Driver behavior issue**. Agent monitors GPS availability (% of drivers with GPS <15 min fresh). If <90%, escalate to Dispatch for driver coaching ("keep GPS enabled"). Consider incentives (GPS uptime score affects performance bonus). |

**Why This Matters**: If polling interval cannot be increased, agent's ETA accuracy is capped at 80-85% (vs. 90-95% target). This affects CSAT and repeat inquiry rate.

---

## Category 4: Goodwill Credit Governance (Billing Disputes)

### Question 4.1: Credit Approval Threshold & Policy

**Context**:
Email artefact shows Sandra applied **£170 goodwill credit** (50% of £340 fuel surcharge dispute) with no documented rationale. Internal note: "no entry in credits audit log" → suggests manual override bypassed standard approval process. We need to know: (a) What's the approval threshold? (b) What's the policy for goodwill vs. policy-required credits?

**Question**:
> "When Sandra applies a goodwill credit like the £170 for Hayes & Sons, is there a **threshold above which she needs manager approval** — like, she can approve up to £200 on her own, but anything higher requires your sign-off? And how does she decide **how much** to credit — is there a policy (e.g., 50% for first offense, 100% for repeat), or is it her judgment call?"

**What Answer Changes**:

| Answer | Design Impact |
|---|---|
| **"Sandra can approve up to £200; above that, I approve"** | **Agent can recommend credits up to £200**, human approves (Sandra or manager). Agent logs recommendation + approval in CRM (audit trail). Above £200, agent escalates to Sarah directly. Governance clear. |
| **"There's no formal threshold; Sandra uses her judgment"** | **Governance gap** (audit risk). Agent must enforce threshold even if current process doesn't (e.g., £200 limit, manager approval above). **Organizational change**: Codify credit approval policy as part of agent deployment. |
| **"We don't do goodwill credits; all credits are policy-required (invoice errors, damaged goods)"** | **No discretionary credits**. Agent design simpler: If damage claim valid (driver confirmed), apply 100% credit. If invoice error, correct and credit. No judgment required → **agent-led with oversight** (not human-led). |

**Follow-Up** (if answer is "judgment call"):
> "For the Hayes & Sons case, Sandra credited £170 (50% of £340). Was that because it's their first fuel surcharge dispute, or because the damage was minor, or some other reason? I'm trying to understand if there's a pattern we can code into the agent."

**Why This Matters**: If no pattern exists (every credit decision is unique), agent cannot recommend credit amounts — can only aggregate investigation data (invoice, delivery notes, customer history) and say "human must decide amount."

---

### Question 4.2: Credit Logging & Audit Trail

**Context**:
Email artefact internal note: "no entry in credits audit log for this £170; Sandra applied it via manual override." This suggests either (a) credits are logged with lag (will appear in tomorrow's Aurum export), or (b) Sandra has a workaround that bypasses Aurum entirely (CRM credit, spreadsheet, manual journal entry).

**Question**:
> "The email notes that Sandra's £170 credit wasn't in the audit log yet. How does Sandra actually **apply** that credit — does she enter it in CRM and it syncs to Aurum overnight, or does she have to submit a ticket to Aurum support (48-hour turnaround), or is there a faster workaround?"

**What Answer Changes**:

| Answer | Design Impact |
|---|---|
| **"She enters it in CRM, syncs to Aurum nightly"** | **Agent can log credit recommendations in CRM** (same workflow Sandra uses). Credit appears on customer's next statement (7-30 day cycle). Audit trail in CRM → Aurum. Governance acceptable. |
| **"She submits Aurum ticket (48h turnaround), but uses CRM credit as 'interim' until Aurum processes"** | **Dual system**: CRM credit (fast, interim) + Aurum ticket (slow, official). Agent follows same workflow: log CRM credit immediately, submit Aurum ticket. **Risk**: CRM and Aurum may diverge (reconciliation required weekly). |
| **"She has a spreadsheet where she tracks goodwill credits offline, then manually tickets Aurum monthly"** | **Audit gap** (compliance risk). Credits not logged in real-time → potential for fraud (over-crediting without oversight). **Agent deployment fixes this**: Agent logs every credit recommendation in CRM (audit trail), even if Sandra's current process doesn't. |

**Why This Matters**: If current process has audit gaps, agent deployment is opportunity to **fix governance** (not just automate existing broken process). Frame this as "agent improves compliance" when pitching to Sarah.

---

## Category 5: Repeat Dispute Pattern (Policy vs. Process Issue)

### Question 5.1: Fuel Surcharge on Damaged Deliveries

**Context**:
APEX_DISPUTES_OPEN shows **3 of 6 disputes are FUEL_SURCH_DAMAGE type** (50%). Hayes & Sons alone has 2 such disputes (current + one 61-90 days aged). This pattern suggests **policy-process misalignment**: Fuel surcharges applied regardless of delivery outcome, but customers perceive this as unfair when goods arrive damaged.

**Question**:
> "I noticed that 3 of the 6 open disputes in the system are about fuel surcharges on damaged deliveries — including Hayes & Sons, who's had this issue twice now. Is this a **known recurring problem**, or is it just bad luck with a few customers? And have you considered changing the policy so that fuel surcharges are waived automatically when a delivery is confirmed damaged?"

**What Answer Changes**:

| Answer | Design Impact |
|---|---|
| **"It's a known issue; we've discussed changing the policy but haven't yet"** | **Agent can flag pattern** to Sarah ("3 of 6 disputes are this type; customer frustration high; consider policy change"). Agent design: In the meantime, agent recommends 100% fuel surcharge credit when damage is driver-confirmed (standardizes Sandra's discretion). **Long-term**: Policy change eliminates this dispute type → reduces agent workload. |
| **"Fuel surcharges are non-negotiable per our contract terms"** | **Policy is contractual, not discretionary**. Agent design: Investigate whether damage voids surcharge per contract terms. If contract silent, agent recommends goodwill credit (relationship preservation vs. policy adherence trade-off). |
| **"This is the first I'm hearing about it being a pattern"** | **Visibility gap**. Sarah doesn't see dispute patterns (no reporting/analytics). **Agent deployment benefit**: Agent generates weekly dispute pattern report (top dispute types, customers with repeat disputes, resolution time trends) → Sarah can address root causes proactively. |

**Why This Matters**: If 50% of disputes are one recurring issue (fuel surcharge + damage), fixing the **policy** (not just automating dispute handling) eliminates 30 disputes/month → more impactful than agent deflection. Frame agent as "policy issue detector" not just "dispute resolver."

---

## Category 6: Organizational Resistance & Change Management

### Question 6.1: Dispatcher Trust in Agent Recommendations

**Context**:
Sandra appears in 3 of 5 artefacts (voicemail, email, disputes export) → she's central to operations, likely respected by team. If agent triages exceptions (Phase 3), Sandra and other dispatchers must **trust agent recommendations**. Prior automation failures (2024 chatbot, RPA billing recon) eroded trust.

**Question**:
> "You mentioned two prior automation projects that didn't work out — the chatbot customers hated, and the RPA that broke when Aurum's schema changed. When we design the ETA and billing agents, what would make **your dispatchers and Customer Ops team** trust the agent's recommendations? What did those prior projects get wrong that we need to avoid?"

**What Answer Changes**:

| Answer | Design Impact |
|---|---|
| **"Chatbot was too robotic; customers wanted empathy, not scripts"** | **Agent response templates** must include empathy phrasing ("I understand you're waiting..."). CSAT surveys mandatory (track sentiment). If CSAT <4.0/5 for 2 weeks, pause rollout and revise tone. |
| **"RPA broke because it couldn't handle edge cases; everything went to exception queue"** | **Agent must handle edge cases gracefully** (stale GPS → escalate with explanation, not silent failure). Escalation triggers explicit (not "everything is an edge case"). Human spot-checks 10% of agent interactions weekly → catch edge cases early. |
| **"Dispatchers felt the RPA was imposed on them; they weren't consulted"** | **Change management required**. Before Phase 3 (exception triage), workshop with dispatchers to codify heuristics (Sandra documents decision criteria). Dispatchers see agent as **extension of their expertise**, not replacement. Pilot with 20% of exceptions (low-stakes cases only), dispatchers review agent decisions daily → build trust incrementally. |

**Why This Matters**: If dispatchers distrust agent, they'll override 70% of recommendations → agent unused, investment wasted. Change management is as critical as technical design.

---

### Question 6.2: Customer Ops Team Involvement

**Context**:
Brief doesn't specify if Customer Ops team has been briefed on agentic transformation. If they learn about agent via top-down mandate ("This is launching Monday"), resistance likely.

**Question**:
> "Have you discussed the idea of an ETA agent with your Customer Ops team yet, or are we still in the exploration phase? And if we move forward, how would you prefer to roll this out — pilot with a small group of agents who volunteer, or launch for everyone at once?"

**What Answer Changes**:

| Answer | Design Impact |
|---|---|
| **"I haven't told them yet; I wanted to see if it's feasible first"** | **Early involvement critical**. Before Phase 1A, hold team workshop: Explain agent purpose (deflect routine inquiries so team can focus on disputes/exceptions), demo prototype, collect feedback. Address concerns early (job security, workload changes). Pilot with volunteers (3-5 agents) for 4 weeks → gather feedback → adjust → full rollout. |
| **"They know I'm looking into AI; some are excited, others are skeptical"** | **Mixed reactions**. Identify champions (excited agents) → involve them in design/testing (UX feedback, edge case identification). Address skeptics' concerns directly (job security: "agent handles volume growth, not replacing you"; workload: "freed capacity redeployed to higher-value work like dispute resolution"). |
| **"We've had high turnover (20% annually); team is stretched thin"** | **Agent framed as relief**, not threat. "Agent handles ETA inquiries so you're not overwhelmed during peak seasons." Turnover signals burnout → agent reduces burnout by deflecting low-value work. |

**Why This Matters**: If team resists, they'll find ways to undermine agent (e.g., manually handling inquiries instead of routing to agent, telling customers "the agent is wrong, let me help"). Change management is non-negotiable for success.

---

## Category 7: Volume Growth & Scaling Constraints

### Question 7.1: Peak Season Volume & Capacity Planning

**Context**:
Brief states 3,500 deliveries/day (baseline). ETA inquiries = 400/day (11.4% inquiry rate). But no mention of peak season (Q4, Black Friday, Christmas) — typical delivery volume spikes 2-3x during peaks.

**Question**:
> "The brief says you handle 3,500 deliveries per day normally. During **peak season** (November-December), does that volume double or triple? And when volume spikes, what breaks first — do you hire temps for Customer Ops, or do hold times just skyrocket?"

**What Answer Changes**:

| Answer | Design Impact |
|---|---|
| **"Volume doubles (7,000 deliveries/day), and we hire 15 temps for Customer Ops"** | **Agent's value is peak season cost avoidance**. Without agent: 800 ETA inquiries/day during peak → need 15 temps (£150K for 8-week season). With agent: 720 inquiries deflected → need 3 temps (£30K). **Seasonal ROI**: £120K saved per peak season. |
| **"Volume doubles, but we don't hire — we just extend hold times and customers complain"** | **Agent's value is customer satisfaction during peaks**. Without agent: 22-min hold times become 60-min hold times → customer churn. With agent: hold times stay <5 min (inquiries deflected). **Churn prevention value**: 5-10 customers retained (£50K-200K revenue protected). |
| **"Peaks are manageable; volume is flat year-round"** | **Agent's value is not peak-driven**. Focus on baseline ROI (£301K annual savings, growth absorption). No seasonal spike argument. |

**Why This Matters**: If Sarah is under pressure to handle Q4 (8 months away), framing agent as "peak season solution" accelerates budget approval ("deploy by October, save £120K in temp costs").

---

## Category 8: Benchmark & CEO Expectations

### Question 8.1: Competitor Benchmark Details

**Context**:
Brief states: "CEO heard about a competitor saving £1.2M annualised on customer service using AI; he asked her to 'look into it.'" This sets Sarah's expectation bar. Our model projects £437K (Phases 1-3, Year 1) → £600-700K (Year 2 with growth). We're **on benchmark**, but Sarah may expect £1.2M immediately.

**Question**:
> "You mentioned your CEO heard about a competitor saving £1.2M on AI for customer service. Do you know if that competitor is similar size to Apex (800 employees, 3,500 deliveries/day), or are they significantly larger? I'm trying to benchmark what's realistic for Apex."

**What Answer Changes**:

| Answer | Design Impact |
|---|---|
| **"They're twice our size (1,600 employees, 7,000 deliveries/day)"** | **Proportional target confirmed**: Competitor £1.2M / 2 = **£600K target** for Apex. Our model (£437K Year 1 → £700K Year 2) is **on or above benchmark**. Frame to Sarah: "Our plan matches or exceeds the competitor's results, adjusted for size." |
| **"They're about our size, maybe 10% larger"** | **Higher bar**: Competitor at same scale achieved £1.2M → Sarah may expect £1M+. **Response**: Our Phase 1-3 plan delivers £437K Year 1, but **Phase 4+ potential** (dispatch optimization, proactive outreach) could add £300-400K → total £800K-1M by Year 3. Frame as multi-year roadmap. |
| **"I don't know the details; CEO just said 'they're using AI'"** | **Vague benchmark**. Sarah's expectation unclear. **Response**: Propose £600K as target (proportional to Apex's size), demonstrate ROI model is conservative (90% ETA deflection, 64% billing time reduction). If Sarah pushes for £1M, negotiate Phase 4 scope (dispatch optimization, exception automation). |

**Why This Matters**: If Sarah's expectation is £1.2M immediately (unrealistic for Apex's size), need to recalibrate early. Better to set realistic £600K target and exceed it, than promise £1.2M and under-deliver.

---

## Category 9: Critical Path Dependencies

### Question 9.1: IT Resource Availability

**Context**:
Agent deployment requires IT support: GPS API access negotiation, CRM schema documentation, Aurum CSV ingestion pipeline, secrets management (API tokens). If IT is overloaded (other projects), Phase 1 timeline at risk.

**Question**:
> "For the ETA agent to work, we'll need IT support — things like providing CRM schema documentation, setting up GPS API access for the agent, and configuring the Aurum CSV ingestion pipeline. Does your IT team have capacity to support this over the next 3 months, or are they tied up with other priorities?"

**What Answer Changes**:

| Answer | Design Impact |
|---|---|
| **"IT is stretched thin; they're migrating our warehouse system through Q3"** | **Timeline risk**. Phase 1 may slip to Month 4-5 (vs. Month 3 target). **Mitigation**: Prioritize GPS API access (Phase 1 blocker) over nice-to-haves (web portal UI). Negotiate dedicated IT resource (1 person, 50% time for 3 months). Escalate to Sarah if IT pushback. |
| **"IT can support; they're excited about this project"** | **Green light**. Phase 1 timeline feasible. Assign IT project lead (single point of contact for agent team). Weekly syncs to track API access, schema docs, CSV pipeline. |
| **"We can hire a vendor/contractor to handle IT integration if our team is busy"** | **Budget flexibility**. Vendor option available if IT bottleneck. Budget £30-50K for 3-month vendor engagement (API integration, CSV pipeline, agent infrastructure setup). |

**Why This Matters**: IT bottleneck is #1 cause of agent project delays. If IT unavailable, Phase 1 slips → ROI delayed → Sarah loses confidence. Need commitment upfront.

---

## Question Priority Ranking (for 10-Minute Round)

**Top Priority** (Must Ask, Materially Changes Design):
1. **Question 1.1**: Dispatcher exception decision criteria (codifiable or tacit?)
2. **Question 3.1**: Customer Ops GPS API access (direct or via Dispatch coordination?)
3. **Question 4.1**: Goodwill credit approval threshold & policy
4. **Question 7.1**: Peak season volume & capacity planning (agent value = peak cost avoidance?)

**Medium Priority** (Ask if Time Permits):
5. **Question 2.1**: Handle time vs. elapsed time (true ROI validation)
6. **Question 5.1**: Fuel surcharge dispute pattern (policy fix vs. agent automation)
7. **Question 6.1**: Dispatcher trust in agent (change management risk)
8. **Question 9.1**: IT resource availability (timeline risk)

**Low Priority** (Optional, Informational):
9. **Question 8.1**: Competitor benchmark details (expectation calibration)
10. **Question 6.2**: Customer Ops team involvement (change management timing)

---

## Questioning Strategy: Detecting Evasion

### Red Flag: Vague Answers

**Example**: Question 1.1 (exception decision criteria)  
**Vague Answer**: "It depends on the situation; every case is different."

**Probing Follow-Up**:
> "I understand each case is unique. But if I shadow you for a day and watch you handle 10 exceptions, would I see **any patterns** — like, 7 out of 10 times you make the same decision for the same type of case, or is it truly unpredictable?"

**Why This Works**: Forces Sarah to quantify variability. If 70% of cases follow pattern, agent can handle those 70%. If truly unpredictable (30% pattern recognition), agent cannot assist.

---

### Red Flag: Contradictory Answers

**Example**: Question 2.1 (capacity)  
**Sarah says**: "We have 55% unused capacity" (262 hrs available - 118 hrs on cases = 144 hrs unused)  
**But email artefact shows**: 22-min hold times, dropped calls (capacity bottleneck)

**Probing Follow-Up**:
> "You mentioned 55% of capacity isn't on tracked cases, but the email from Hayes & Sons shows 22-minute hold times and dropped calls — that sounds like you're **overloaded**, not under-utilized. Can you help me understand what's consuming the other 144 hours per day?"

**Why This Works**: Surfaces the "untracked work" (meetings, email triage, rework, escalations) that consumes capacity but isn't measured. This informs ROI model: Agent won't reduce headcount, but will free capacity for growth absorption.

---

## Conclusion: Discovery Questions Framework

These 10 questions are designed to **surface design-critical information** that artefacts + brief don't provide:

1. **Dispatcher heuristics** → determines if exception triage is automatable (Phase 3 feasibility)
2. **GPS API access** → determines if precision ETA is feasible (Phase 1B blocker)
3. **Credit approval policy** → determines agent's delegation level (agent-led vs. human-led)
4. **Peak season volume** → determines agent's value proposition (cost avoidance vs. CX improvement)
5. **Handle time reality** → validates ROI model (£301K vs. £135K savings)
6. **Fuel surcharge pattern** → identifies policy fix opportunity (higher ROI than automation)
7. **Dispatcher trust** → identifies change management risk (adoption blocker)
8. **IT availability** → identifies timeline risk (Phase 1 slip)
9. **Competitor benchmark** → calibrates Sarah's expectations (£600K realistic vs. £1.2M)
10. **Ops team involvement** → identifies change management timing (pilot vs. full rollout)

**Each question is paired with "What Answer Changes"** — explicit decision tree showing how different answers affect agent design scope, delegation level, timeline, or ROI.

**Questioning discipline**: Don't ask "What are your pain points?" (too open-ended). Ask "Of the 180 exceptions per day, what percentage are standard refusals vs. damage claims?" (specific, answerable, diagnostic).

**This is ATX discovery applied to stakeholder clarification** — every question tied to agent design trade-off, not general exploration.
