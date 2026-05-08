# Problem Statement and Success Metrics

## Executive Summary

Apex Distribution's Customer Operations function handles 730 daily cases with 35 FTE, yet customers experience 22-minute hold times, 9-day dispute resolutions, and imprecise ETA estimates. The root causes are **information silos, legacy system constraints, and expertise concentration in key individuals**. This creates customer dissatisfaction, operational bottlenecks, and relationship risk with high-value accounts.

Agentic transformation can deflect routine inquiries, accelerate dispute investigation, and scale decision-making expertise — **without requiring Aurum system replacement or dispatcher replacement**. Success means faster customer response, reduced cognitive load on high-value staff, and measurable cost avoidance in FTE scaling.

**Target**: 40-50% reduction in human-handled case volume within 6 months, enabling Customer Operations to absorb 20% volume growth without headcount increase.

---

## 1. Current State: Quantified Problems

### Problem 1: High-Volume Routine Inquiries Consume Disproportionate Capacity

**Work Stream**: ETA Inquiries

**Current State Metrics**:
- **Volume**: 400 inquiries/day (54.8% of total case load)
- **Handle time**: 4 minutes average per case (from brief)
- **Actual elapsed time**: 11 minutes observed in SMS artefact (includes coordination with Dispatch)
- **Total labor consumption**: 27 hours/day using brief avg, **73 hours/day** using observed elapsed time
- **Customer experience**: 4-hour ETA windows, hedged responses ("best guess"), 5-minute waits for GPS data

**Root Causes**:
1. Customer Ops agents lack direct access to Driver App GPS data
2. Coordination with Dispatch team required for precision beyond scheduled window
3. GPS data lags (36 minutes in SMS artefact: last ping 10:48, query response 11:24)
4. No self-service option for customers (must contact agent)

**Business Impact**:
- **Opportunity cost**: Agents spend 18-30% of capacity on low-complexity lookups
- **Customer satisfaction**: Imprecise ETAs drive repeat inquiries ("where is it NOW?")
- **Scaling constraint**: As delivery volume grows, ETA inquiries grow proportionally — current model requires 1 new FTE per 1,500 monthly inquiry increase

**Why This Matters**:
ETA inquiries are **high-volume, low-complexity, low-risk** — the ideal agentic deflection target. Solving this frees capacity for higher-value work (billing disputes, complex exceptions).

---

### Problem 2: Dispatcher Expertise Bottleneck Blocks Operations

**Work Stream**: Delivery Exceptions

**Current State Metrics**:
- **Volume**: 180 exceptions/day
- **Handle time**: 12 minutes average (from brief)
- **Bottleneck evidence**: Sandra's line busy (voicemail artefact), driver blocked with 6 pending deliveries
- **Expertise concentration**: Sandra appears in 3 of 5 operational artefacts (voicemail, email, disputes export)

**Root Causes**:
1. Dispatcher judgment required for exception decisions (return-to-depot, leave-and-reattempt, override refusal)
2. Judgment criteria not codified (no decision matrix for value/risk trade-offs)
3. Synchronous coordination required (driver calls, waits for callback)
4. Single point of failure (key dispatchers overwhelmed during peak hours)

**Business Impact**:
- **Driver productivity loss**: Blocked drivers waiting for decision = delayed downstream deliveries
- **Missed delivery windows**: 6 deliveries in queue while Mark Petrov waits for callback
- **Scalability limit**: Dispatcher expertise doesn't scale linearly with volume — adding FTE doesn't replicate Sandra's institutional knowledge
- **Business continuity risk**: If Sandra leaves, knowledge walks out the door

**Why This Matters**:
Exceptions are **judgment-heavy but pattern-based** — many follow heuristics (e.g., "low-value package + first refusal + non-critical customer = return to depot"). Agent can triage routine cases, escalate complex ones. Frees dispatchers to focus on true edge cases.

---

### Problem 3: Billing Dispute Resolution is Slow, Inconsistent, and Risks Customer Relationships

**Work Stream**: Billing Disputes

**Current State Metrics**:
- **Volume**: 60 disputes/day
- **Handle time**: 28 minutes average per case
- **Observed resolution time**: 6-9 days (Hayes & Sons email artefact)
- **Repeat dispute rate**: Hayes & Sons has 3 open disputes; 3 of 6 sample disputes are FUEL_SURCH_DAMAGE type
- **Customer friction**: 22-minute hold time, dropped calls, escalation to "who is your manager?"

**Root Causes**:
1. **Investigation slowness**: Agent must manually query 3+ systems (Aurum export, CRM, delivery exception log) and cross-reference data
2. **Aurum constraint**: Cannot query real-time billing data; T-1 lag means agent working with yesterday's snapshot
3. **Resolution bottleneck**: Cannot apply credits directly; 48-hour Aurum ticket turnaround for official adjustments
4. **Policy ambiguity**: "Goodwill credit" decisions are discretionary — Sandra applies £170 (50% of £340 dispute) with no documented rationale
5. **Audit gap**: Manual overrides not logged in Aurum (per email artefact internal note)

**Business Impact**:
- **Customer churn risk**: Hayes & Sons (£25K credit limit, large account) frustrated, £10,272 in open receivables
- **Revenue at risk**: If high-value customers churn due to slow dispute resolution, lost annual revenue = £50-200K per customer (estimated based on credit limits)
- **Labor intensity**: 28 hours/day consumed by 60 cases (46.7 min per case if uninterrupted)
- **Inconsistent outcomes**: No clear policy on when to apply goodwill credits or how much — agent discretion varies

**Why This Matters**:
Disputes are **investigation-heavy, judgment-light** — agent can automate data aggregation (80% of time), human approves resolution (20% of time). Speeds resolution from 6-9 days to 1-2 days while improving consistency.

---

### Problem 4: Information Silos Force Multi-Step Coordination for Simple Tasks

**Cross-Cutting Issue** (affects all work streams)

**Current State Metrics**:
- **Systems involved**: CRM, Driver App, Dispatch Console, Aurum Billing — minimal integration
- **Coordination overhead**: ETA inquiry agent waits 5 min for Dispatch GPS data; billing agent deflects customer to Customer Ops; Customer Ops waits for Aurum nightly export

**Root Causes**:
1. Driver App GPS not accessible to Customer Ops (must ask Dispatch)
2. Aurum batch-only exports (no API, T-1 lag)
3. Dispatch Console "limited API surface" (per brief)
4. Each team has different system access permissions

**Business Impact**:
- **Coordination tax**: Every cross-system query adds 3-8 minutes of wait time
- **Handoff failures**: Customer told to call Customer Ops → 22-minute hold → dropped call (lost effort)
- **Data staleness**: Decisions made on T-1 data when T-0 data exists but is inaccessible

**Why This Matters**:
Agents can serve as **integration layer** — aggregate data from multiple systems, present unified view to human decision-maker. Eliminates coordination waits even without changing underlying systems.

---

### Problem 5: Undocumented Process Reality Creates Inconsistency

**Cross-Cutting Issue** (process governance)

**Current State Evidence**:
- **SOP drift**: References retired DispatchHub system (replaced Oct 2024), SOP last revised Oct 2023
- **Incomplete documentation**: Section 4.3 "Damaged consignments" marked "TBD pending review of insurance protocol"
- **Workarounds**: Sandra applies credits via "manual override" not in formal process
- **Discretionary decisions**: Goodwill credits, exception routing, escalation thresholds not codified

**Business Impact**:
- **Training difficulty**: New hires onboarded with outdated SOP, must learn "real way" by shadowing
- **Inconsistent outcomes**: Different agents make different decisions on similar cases
- **Knowledge concentration**: Expertise trapped in Sandra's head, not transferable
- **Audit risk**: Manual overrides not logged → compliance gap

**Why This Matters**:
Agent design requires **codifying lived processes**, not documented processes. Side benefit: Creates institutional knowledge capture and consistency.

---

## 2. Desired Future State: What Good Looks Like

### Vision Statement

**Customer Operations becomes a scalable, responsive function where agents handle exceptions and relationship management while AI handles routine inquiries, data aggregation, and decision support.**

Customers get instant ETA updates. Billing disputes resolved in 24-48 hours. Dispatchers freed from routine triage to focus on complex exceptions. High-value staff (Sandra, senior agents) spend time on judgment and customer relationships, not data entry and lookups.

---

### Future State Operating Model

#### **Tier 1: Fully Agentic** (No human in loop)
- **ETA inquiries (90% of volume)**: Agent queries GPS, calculates ETA, responds to customer via SMS/email/portal
- **Standard billing lookups**: Agent retrieves invoice, payment status, aging from Aurum exports
- **Delivery confirmation queries**: Agent confirms scan-on-delivery timestamp, recipient name

**Human escalation**: If GPS data stale (>30 min), customer demands callback, or edge case detected

#### **Tier 2: Agent-Led, Human Approves** (Human in review loop)
- **Billing dispute investigation**: Agent aggregates data (invoice, delivery exception, customer history), drafts resolution recommendation
- **Low-risk exception triage**: Agent recommends return-to-depot for <£500 packages with standard refusal reasons

**Human role**: Review recommendation, approve/modify, execute (apply credit, instruct driver)

#### **Tier 3: Human-Led, Agent Assists** (Human decides, agent supports)
- **High-value exceptions**: Agent surfaces decision-supporting data (customer tier, past exceptions, delivery value, re-delivery cost), human decides
- **Complex disputes**: Agent summarizes case, human interprets policy and decides resolution

**Agent role**: Data aggregation, context assembly, recommendation generation (if requested)

#### **Tier 4: Human-Only** (No agent involvement)
- **Relationship management**: Calls to high-value customers after major service failures
- **Policy exceptions**: CEO calls demanding special handling
- **Legal/regulatory**: Disputes involving litigation, compliance violations

---

## 3. Success Metrics: Lagging Indicators (Business Outcomes)

### 3.1 Customer Experience Metrics

| Metric | Baseline (Current) | Target (6 Months) | Target (12 Months) | Measurement Method |
|---|---|---|---|---|
| **ETA Inquiry Response Time** (p50) | 4 min (brief) / 11 min (observed) | <30 seconds (agent-handled) | <10 seconds | CRM case timestamps: create → first response |
| **ETA Inquiry Response Time** (p95) | 15-20 min (estimated) | <2 min | <30 seconds | CRM case timestamps |
| **Billing Dispute Resolution Time** (median) | 6-9 days (observed) | <48 hours investigation + Aurum lag | <24 hours investigation + Aurum lag | APEX_DISPUTES_OPEN: OPEN_DT → LAST_UPDT (status change to RESOLVED) |
| **Customer Hold Time** (avg) | 22 min (email artefact) | <5 min | <2 min | Phone system metrics |
| **Call Abandonment Rate** | Unknown (but dropped calls observed) | <5% | <2% | Phone system: calls offered vs. calls answered |
| **Repeat Contact Rate** (same issue <7 days) | Unknown (needs baseline) | <15% | <10% | CRM: customer ID + issue type clustering |

**Data Source**: CRM case logs, phone system (existing), APEX_DISPUTES_OPEN export (existing)

**Why These Matter**: Customer-facing metrics directly reflect service quality. Hold time and resolution time are top drivers of satisfaction in service operations (industry benchmark: <3 min hold, <24h resolution for tier 1 issues).

---

### 3.2 Operational Efficiency Metrics

| Metric | Baseline (Current) | Target (6 Months) | Target (12 Months) | Measurement Method |
|---|---|---|---|---|
| **Case Deflection Rate** (ETA inquiries) | 0% (all human-handled) | 85-90% | 95% | Agent-resolved cases / total ETA inquiries |
| **Human Handle Time per Case** (ETA inquiries, human-escalated only) | 4 min avg | 8-10 min (complex cases only) | 10-12 min (edge cases only) | CRM case duration for human-handled subset |
| **Billing Dispute Investigation Time** (agent-assisted) | 28 min (baseline) | 8-10 min (human review + decision) | 5-8 min | CRM case timestamps: assign → resolution decision |
| **Exception Escalation Rate** (dispatcher callbacks) | ~100% (all require callback) | 40-50% (routine triaged by agent) | 25-30% | Dispatch Console: exception cases → dispatcher-handled |
| **Cases Handled per FTE per Day** | 20.9 cases/FTE/day (730 / 35) | 30-35 cases/FTE/day | 40-45 cases/FTE/day | Total cases / FTE headcount |
| **Total Daily Labor Hours** (Customer Ops) | 118 hrs/day (from brief) | 70-80 hrs/day | 60-70 hrs/day | Sum of (case volume × handle time) by stream |

**Data Source**: CRM case logs (existing), Dispatch Console logs (may need instrumentation), internal time tracking

**Why These Matter**: Efficiency gains translate to cost avoidance (no need to hire as volume grows) and capacity redeployment (freed FTE hours can handle growth or shift to higher-value work).

---

### 3.3 Cost & Capacity Metrics

| Metric | Baseline (Current) | Target (6 Months) | Target (12 Months) | Measurement Method |
|---|---|---|---|---|
| **Cost per Case** (Customer Ops labor) | £X (needs baseline) | -30% | -40-50% | (FTE headcount × avg salary) / annual case volume |
| **Headcount Growth vs. Volume Growth** | 1:1 (linear scaling) | 1:0.5 (50% efficiency) | 1:0.3 (70% efficiency) | ΔHeadcount / ΔCase Volume over 6-month periods |
| **Capacity Headroom** (% of available hours not on cases) | 55% (262.5 avail - 118 tracked = 144.5 hrs) | 40-45% (some freed by deflection, some absorbed by growth) | 35-40% | 1 - (Tracked Case Hours / Available FTE Hours) |
| **Agent Cost per Deflected Case** | N/A | <£0.50 | <£0.30 | (LLM API cost + infrastructure) / agent-handled cases |

**Assumptions for Cost Calculation**:
- Customer Ops FTE fully-loaded cost: £35-45K/year (£140-180/day, £18-24/hour)
- Current cost per case: (35 FTE × £40K avg) / (730 cases/day × 250 days/year) = £1.4M / 182,500 = **£7.67 per case**
- Target cost per case (12 months): 50% reduction → **£3.84 per case**
- Annual savings: (182,500 cases/yr × £3.83 savings) = **£699K annualized**

**Benchmark Check**: Competitor saved £1.2M annualized (per CEO briefing to Sarah). Apex is ~45% the scale (estimated), so proportional target is **£540-600K annualized**. Our projection of £699K is **above benchmark** — achievable if deflection rates hit targets.

**Data Source**: Finance (FTE cost), CRM (case volume), infrastructure (agent cost)

---

### 3.4 Quality & Risk Metrics

| Metric | Baseline (Current) | Target (6 Months) | Target (12 Months) | Measurement Method |
|---|---|---|---|---|
| **Agent Accuracy** (ETA inquiries) | N/A | >95% | >98% | Human spot-check: agent ETA vs. actual delivery time (±30 min tolerance) |
| **Agent Accuracy** (billing dispute recommendations) | N/A | >90% accepted by human | >95% | Human approvals / agent recommendations |
| **Escalation Precision** (agent escalates correctly) | N/A | >85% | >90% | Human review: escalated cases that needed escalation / total escalations |
| **Escalation Recall** (agent escalates when should) | N/A | >95% | >98% | Human spot-check: cases that should have escalated but didn't |
| **Audit Compliance** (credits logged correctly) | Unknown (gap identified in email artefact) | 100% | 100% | All credits in CRM match APEX_CREDITS export (reconciliation check) |
| **Policy Consistency** (goodwill credit variance) | High (Sandra applies £170, no documented rationale) | <20% variance from policy | <10% variance | Standard deviation of goodwill credits for same dispute type |

**Data Source**: Human QA reviews (sample 5% of agent-handled cases weekly), APEX_CREDITS export (audit trail)

**Why These Matter**: Accuracy and escalation precision prevent customer dissatisfaction from agent errors. Audit compliance and policy consistency address governance gaps identified in email artefact (Sandra's manual override, no audit log).

---

## 4. Success Metrics: Leading Indicators (Early Signals)

Leading indicators provide early warning if implementation is off track — before lagging indicators (outcomes) become visible.

| Leading Indicator | What It Signals | Target Threshold | Measurement Frequency |
|---|---|---|---|
| **Agent Utilization Rate** (% of eligible cases routed to agent) | Adoption/trust — if low, humans bypassing agent | >80% within 4 weeks of launch | Weekly |
| **Agent Escalation Rate** (% of agent-handled cases escalated) | Agent confidence calibration — if >20%, too cautious; if <5%, over-confident | 10-15% (should decline over time as training improves) | Weekly |
| **Human Override Rate** (% of agent recommendations modified) | Agent recommendation quality — if >30%, recommendations not helpful | <20% within 8 weeks | Weekly |
| **Agent Response Time** (p95) | Infrastructure performance — if >10s, degrades CX | <5s for ETA inquiries, <30s for dispute summaries | Daily |
| **Data Freshness** (GPS lag, Aurum export lag) | Integration health — if GPS >30 min stale, ETA accuracy suffers | GPS <15 min stale, Aurum T-1 expected | Daily |
| **Customer Feedback Score** (CSAT for agent interactions) | Customer acceptance — if <4/5, agent responses not meeting expectations | >4.2/5 within 12 weeks | Per interaction (sample) |

**Data Source**: Agent logs, CRM case routing, CSAT surveys (post-interaction)

**Why Leading Indicators Matter**: Lagging indicators (cost savings, resolution time) take 3-6 months to show trends. Leading indicators give weekly feedback to course-correct during rollout.

---

## 5. Economic Impact: The Business Case

### Cost Avoidance Model (12 Months)

**Scenario: 20% Volume Growth Without Headcount Increase**

| Item | Current State | Future State (12 Months) | Delta |
|---|---|---|---|
| **Daily Case Volume** | 730 | 876 (20% growth) | +146 |
| **FTE Required (at current productivity)** | 35 | 42 (linear scaling) | +7 FTE |
| **FTE Required (with agentic deflection)** | 35 | 35 (no increase due to efficiency) | 0 FTE |
| **Cost Avoided** | — | 7 FTE × £40K = **£280K/year** | **£280K** |

**Scenario: Labor Redeployment (Capacity Freed)**

| Work Stream | Current Hours/Day | Future Hours/Day (Agent-Assisted) | Hours Freed |
|---|---|---|---|
| ETA Inquiries (90% deflection) | 73 hrs (observed) | 7 hrs (10% escalations) | **66 hrs** |
| Billing Disputes (investigation accelerated) | 28 hrs | 10 hrs (human review/decision only) | **18 hrs** |
| Delivery Exceptions (triage agent) | 36 hrs | 22 hrs (complex cases only) | **14 hrs** |
| **TOTAL** | **137 hrs/day** | **39 hrs/day** | **98 hrs/day freed** |

**Redeployment Options**:
1. **Absorb growth**: 98 hrs/day = 13 FTE equivalent freed to handle volume growth
2. **Improve service**: Redeploy to proactive outreach (call customers before they call us), dispute prevention (address fuel surcharge policy)
3. **Cost reduction**: If volume flat, could reduce headcount by 13 FTE = **£520K annual savings** (but risky — prefer growth absorption)

**Combined Business Case** (Cost Avoidance + Efficiency):
- **Year 1**: £280K cost avoidance (growth absorption) + £50-100K efficiency gains (faster resolution → fewer repeat contacts) = **£330-380K total value**
- **Year 2**: Cumulative volume growth 40%, cost avoidance £560K + efficiency gains scale = **£600-700K total value**

**Benchmark**: Competitor saved £1.2M (per CEO briefing). Apex target: **£540-600K by Year 2** (proportional to size). Our model shows **£600-700K** — **on benchmark or better**.

---

### ROI Assumptions

**Investment (Year 1)**:
- Agent development (internal or vendor): £150-250K
- Infrastructure (LLM API, hosting): £30-50K/year
- Change management (training, pilot, rollout): £50-80K
- **Total Year 1 Investment**: **£230-380K**

**Payback Period**: 
- Conservative: £330K value / £380K investment = **13.8 months**
- Optimistic: £380K value / £230K investment = **7.3 months**

**3-Year NPV** (assuming 10% discount rate, £600K annual value Year 2-3):
- Investment: £380K (Year 1)
- Returns: £330K (Y1), £600K (Y2), £600K (Y3)
- NPV = **£820K** (conservative)

**IRR**: ~80-120% (high return driven by labor cost avoidance)

---

## 6. What Success Does NOT Look Like (Anti-Patterns)

### Anti-Pattern 1: High Deflection, Low Customer Satisfaction
**Scenario**: Agent handles 95% of ETA inquiries, but CSAT drops to 2.5/5 because responses are robotic, inaccurate, or unhelpful.

**Why This Fails**: Deflection without quality is cost-shifting to customer (they have to call back, escalate, or churn).

**Guard Rail**: CSAT must be >4.0/5 for agent-handled interactions. If <4.0 for 2 consecutive weeks, pause rollout and diagnose.

---

### Anti-Pattern 2: Agent Becomes "The New Manual Process"
**Scenario**: Agent requires so much human oversight (every recommendation reviewed, every escalation validated) that total handle time doesn't decrease.

**Why This Fails**: We've automated data aggregation but not decision-making — no labor savings, just shifted work.

**Guard Rail**: Human review time must be <30% of original handle time. If >30%, agent recommendations not actionable — redesign delegation boundary.

---

### Anti-Pattern 3: Aurum Constraint Ignored, Solutions Fail in Production
**Scenario**: Agent design assumes real-time billing data access. Launches, customers call asking about invoices not yet in nightly export. Agent says "no record found." Customer frustrated, escalates.

**Why This Fails**: Ignored documented constraint (T-1 lag).

**Guard Rail**: All agent designs must explicitly handle Aurum T-1 lag (e.g., "Your invoice from yesterday is still processing; I can check again tomorrow, or would you like to speak with a specialist now?").

---

### Anti-Pattern 4: Dispatcher Resistance Kills Adoption
**Scenario**: Agent triages delivery exceptions, but dispatchers (Sandra et al.) distrust recommendations, override 70% of cases. Agent stops being used, investment wasted.

**Why This Fails**: Didn't involve dispatchers in design, didn't codify their heuristics, agent recommendations don't match lived decision criteria.

**Guard Rail**: Dispatcher workshops during design phase to codify decision heuristics. Override rate monitored; if >30% for 4 consecutive weeks, agent logic tuned based on override reasons.

---

### Anti-Pattern 5: "Everything is Fully Agentic" → Edge Cases Break Catastrophically
**Scenario**: Billing dispute agent applies £1,500 goodwill credit automatically (no human approval) to resolve dispute. Customer was fraudulent, credit abused. Finance audit flags £50K in improper credits over 3 months.

**Why This Fails**: Delegation boundary wrong — goodwill credits require human judgment, especially above policy threshold.

**Guard Rail**: Credit approval authority must stay with humans. Agent can recommend, human must approve (especially >£200 threshold). Audit reconciliation (CRM credits vs. APEX_CREDITS export) weekly.

---

## 7. Measurement Cadence & Governance

### Weekly: Operations Review (Internal)
**Audience**: Customer Ops team lead, Agent operations owner
**Metrics**: Leading indicators (utilization, escalation rate, override rate, response time)
**Action**: Tune agent confidence thresholds, adjust escalation rules, identify training data gaps

### Monthly: Business Review (Leadership)
**Audience**: Sarah Whitmore (COO), Finance, Customer Ops Director
**Metrics**: Lagging indicators (case volume, handle time, cost per case, CSAT)
**Action**: Assess ROI trajectory, approve scope expansions (e.g., add next work stream), adjust targets

### Quarterly: Strategic Review (Board/CEO)
**Audience**: CEO, CFO, COO
**Metrics**: Annualized cost savings, customer retention impact, headcount vs. volume growth
**Action**: Validate business case, approve Year 2 investments, benchmark vs. competitor

---

## 8. Success Metrics Summary Table

| Category | Key Metric | Baseline | 6-Month Target | 12-Month Target | Data Source |
|---|---|---|---|---|---|
| **Customer Experience** | ETA Response Time (p50) | 4-11 min | <30 sec | <10 sec | CRM |
| | Dispute Resolution Time (median) | 6-9 days | <48 hrs + lag | <24 hrs + lag | APEX_DISPUTES |
| | Hold Time (avg) | 22 min | <5 min | <2 min | Phone system |
| **Efficiency** | Case Deflection Rate (ETA) | 0% | 85-90% | 95% | CRM |
| | Cases per FTE per Day | 20.9 | 30-35 | 40-45 | CRM |
| | Daily Labor Hours | 118 hrs | 70-80 hrs | 60-70 hrs | Time tracking |
| **Economics** | Cost per Case | £7.67 | £5.37 (30% ↓) | £3.84 (50% ↓) | Finance + CRM |
| | Annual Savings (vs. growth) | — | £140-190K | £280-380K | Finance model |
| | ROI | — | Positive | 80-120% IRR | Finance model |
| **Quality** | Agent Accuracy (ETA) | N/A | >95% | >98% | QA spot-check |
| | Audit Compliance (credits) | Gap identified | 100% | 100% | APEX_CREDITS reconciliation |

---

## 9. Critical Success Factors

For this transformation to achieve targets, the following must be true:

1. **Driver App GPS API access granted** — Without this, ETA deflection limited to scheduled windows (poor CX)
2. **Dispatcher heuristics codified** — Sandra and team must articulate decision criteria for exception triage
3. **Aurum T-1 lag designed into solution** — No assumptions of real-time billing data
4. **Goodwill credit governance implemented** — Approval thresholds, audit trail, policy consistency
5. **Change management with Customer Ops team** — Not imposed top-down; co-designed with front-line agents
6. **Sarah Whitmore champions internally** — COO sponsorship essential to overcome skepticism from past failures

**If any of these fail**, ROI and customer satisfaction targets at risk. These are design dependencies, not nice-to-haves.

---

## 10. Conclusion: Measurable, Achievable, Transformative

This problem statement and metrics framework provides:

- **Clear baseline**: Current state quantified (730 cases/day, 22-min hold times, 6-9 day disputes)
- **Specific targets**: 90% ETA deflection, 48-hour dispute resolution, £330-700K annual value
- **Leading indicators**: Weekly signals to course-correct during rollout
- **Realistic constraints**: Aurum T-1 lag, dispatcher judgment, credit approval governance
- **Anti-pattern awareness**: What failure looks like, how to detect and prevent

Success means **Apex Customer Operations handles 20% volume growth with zero headcount increase while improving customer experience** — freeing Sarah Whitmore from choosing between service quality and cost control.

The metrics are ambitious but grounded in observed data (artefacts, CSV exports). The economics are benchmarked against competitor results (£1.2M → £600K proportional). The governance model ensures early detection of drift.

**This is the "what good looks like" foundation for agent design.**
