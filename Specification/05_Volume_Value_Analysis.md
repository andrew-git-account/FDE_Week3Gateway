# Volume × Value Analysis

## Purpose

This analysis plots the 4 Customer Operations work streams on volume × value axes to identify the primary agentic transformation target. The analysis considers both **total case volume** (labor hours consumed) and **business value** (customer impact, revenue protection, operational risk).

**Key Question**: Which work stream offers the highest ROI for agentic investment?

---

## 1. Framework: Volume × Value Matrix

### Volume Dimension (X-Axis)
**Metric**: Daily case volume × average handle time = **total labor hours consumed**

**Rationale**: Volume alone (case count) is insufficient — a 4-minute ETA inquiry and a 28-minute billing dispute are not equivalent. Labor hours reflect true capacity consumption.

**Scale**:
- **Low Volume**: <20 hours/day
- **Medium Volume**: 20-40 hours/day
- **High Volume**: >40 hours/day

---

### Value Dimension (Y-Axis)
**Metric**: **Business impact** — composite of 4 factors:

1. **Customer Experience Impact** (1-5): Does this work stream directly affect customer satisfaction? (Poor ETA response → frustration; slow dispute resolution → churn)

2. **Revenue Protection** (1-5): Does this work stream protect revenue or prevent churn? (Billing disputes unresolved → customer withholds payment or churns)

3. **Operational Risk** (1-5): Does this work stream create operational bottlenecks? (Dispatcher bottleneck → drivers blocked → missed delivery windows → SLA breaches)

4. **Scalability Constraint** (1-5): Does this work stream limit growth? (If volume doubles, can we handle it, or must we hire proportionally?)

**Composite Value Score**: Average of 4 factors (1.0 - 5.0)

**Scale**:
- **Low Value**: 1.0-2.5
- **Medium Value**: 2.6-3.9
- **High Value**: 4.0-5.0

---

## 2. Work Stream Scoring

### Work Stream 1: ETA Inquiries

**Volume Metrics**:
- Daily cases: 400
- Average handle time: 4 min (per brief) / **11 min (observed in SMS artefact, includes coordination wait)**
- **Total labor hours/day**: 400 × 11 min / 60 = **73 hours/day** (using observed elapsed time)
- **Volume Category**: **HIGH**

**Value Factors**:

1. **Customer Experience Impact**: **5/5**
   - **Direct customer-facing**: Every inquiry is a customer seeking information
   - **Frequency**: Most common customer touchpoint (54.8% of all cases)
   - **Satisfaction driver**: Imprecise ETAs (4-hour windows) drive frustration and repeat contacts
   - **Evidence**: SMS artefact shows customer pushback ("That's a 4 hour window, can you tell me anything more specific?")
   - **Industry benchmark**: ETA precision is top-3 satisfaction driver in parcel delivery (industry studies)

2. **Revenue Protection**: **2/5**
   - **Low direct revenue impact**: ETA inquiries don't involve billing or disputes
   - **Indirect churn risk**: Poor ETA service contributes to overall dissatisfaction, but not primary churn driver
   - **Opportunity cost**: Capacity consumed by ETA inquiries could be redeployed to higher-value work (billing disputes, proactive outreach)

3. **Operational Risk**: **3/5**
   - **Medium bottleneck**: Customer Ops agents spend 28% of capacity (73/262.5 hours) on ETA inquiries
   - **Coordination dependency**: Agents must coordinate with Dispatch for GPS data (5-min wait in SMS artefact)
   - **No critical path impact**: ETA delays don't block other operations (unlike dispatcher bottleneck blocking drivers)

4. **Scalability Constraint**: **5/5**
   - **Linear scaling**: ETA inquiries grow 1:1 with delivery volume (3,500 deliveries/day → assume 11.4% inquiry rate = 400 inquiries)
   - **No leverage**: Current model requires hiring 1 FTE per 300 additional inquiries/day
   - **Peak vulnerability**: Volume spikes (Q4, promotions) stress capacity → hold times increase → customer satisfaction drops

**Composite Value Score**: (5 + 2 + 3 + 5) / 4 = **3.75** (Medium-High Value)

**Plot Position**: **High Volume (73 hrs), Medium-High Value (3.75)**

---

### Work Stream 2: Billing Disputes

**Volume Metrics**:
- Daily cases: 60
- Average handle time: 28 min (per brief)
- **Total labor hours/day**: 60 × 28 min / 60 = **28 hours/day**
- **Actual elapsed time**: 6-9 days (observed in email artefact, Day 1 → Day 6 resolution)
- **Volume Category**: **MEDIUM**

**Value Factors**:

1. **Customer Experience Impact**: **5/5**
   - **High-friction interaction**: Disputes involve customer dissatisfaction with charges
   - **Relationship damage**: Email artefact shows customer escalation ("Second time this quarter," "Who is your manager?")
   - **Trust erosion**: Long resolution times (6-9 days) signal organizational dysfunction
   - **Repeat contact rate**: Customer called (22-min hold, dropped), then escalated via email — multiple touchpoints for single issue

2. **Revenue Protection**: **5/5**
   - **Direct revenue at risk**: Unresolved disputes → customers withhold payment or deduct disputed amounts
   - **Evidence**: Hayes & Sons has £10,272 in open receivables, 3 open disputes (including the £340 fuel surcharge dispute from email artefact)
   - **Churn risk**: Large B2B customers (£25K-60K credit limits) switching carriers due to dispute frustration = £50K-200K annual revenue loss per customer (estimated)
   - **Repeat dispute pattern**: 3 of 6 disputes in APEX_DISPUTES_OPEN are FUEL_SURCH_DAMAGE type (50%) — systemic issue, not isolated incidents

3. **Operational Risk**: **4/5**
   - **Capacity bottleneck**: 22-minute hold times (email artefact) indicate Customer Ops overloaded
   - **Audit gap**: Sandra's "manual override" not logged in APEX_CREDITS export (email artefact internal note) → compliance risk
   - **Cross-team coordination failure**: Billing team deflects to Customer Ops (Day 1, 7.5-hour delay), customer cannot reach Customer Ops (dropped call, Day 4)
   - **No critical path impact**: Billing disputes don't block deliveries, but damage customer relationships

4. **Scalability Constraint**: **4/5**
   - **Sublinear scaling** (better than ETA inquiries): Dispute volume doesn't grow 1:1 with delivery volume (disputes driven by policy issues, not volume)
   - **But**: Investigation complexity high (28 min per case) → 1 FTE per 16 disputes/day → still labor-intensive
   - **Root cause not addressed**: Fuel surcharge disputes recurring (3 of 6 in sample) → automation doesn't fix policy, just accelerates investigation

**Composite Value Score**: (5 + 5 + 4 + 4) / 4 = **4.5** (High Value)

**Plot Position**: **Medium Volume (28 hrs), High Value (4.5)**

---

### Work Stream 3: Delivery Exceptions

**Volume Metrics**:
- Daily cases: 180
- Average handle time: 12 min (per brief)
- **Total labor hours/day**: 180 × 12 min / 60 = **36 hours/day**
- **Actual elapsed time**: Driver blocked until callback received (voicemail artefact: Mark Petrov parked, 6 deliveries waiting)
- **Volume Category**: **MEDIUM-HIGH**

**Value Factors**:

1. **Customer Experience Impact**: **4/5**
   - **Indirect customer impact**: Exceptions affect delivery completion (customer waiting for package)
   - **Missed delivery windows**: Driver blocked → downstream deliveries delayed → customer dissatisfaction
   - **Exception types**: Refusals, damage claims, incorrect addresses — all affect customer (either receives wrong/damaged goods, or doesn't receive at all)
   - **Not as direct as ETA inquiries**: Customer doesn't initiate contact for exceptions (agent/driver handles proactively)

2. **Revenue Protection**: **3/5**
   - **Medium revenue impact**: Exceptions lead to re-delivery costs (£40-80 per return-to-depot) → margin erosion
   - **Customer churn risk**: Recurring exceptions (damaged deliveries, missed windows) erode trust, but not immediate churn driver
   - **Evidence**: Stein-Allen (voicemail artefact) is "large B2B customer" — exception mishandling could damage relationship
   - **Less direct than billing disputes**: Exceptions don't involve payment withholding or disputes (yet)

3. **Operational Risk**: **5/5**
   - **Critical bottleneck**: Dispatcher (Sandra) overwhelmed → line busy → driver blocked → cascading delays
   - **Evidence**: Voicemail artefact shows Mark Petrov parked with 6 pending deliveries waiting for callback
   - **Single point of failure**: Sandra appears in 3 of 5 artefacts (voicemail, email, disputes export) → expertise concentration risk
   - **Business continuity**: If Sandra leaves, dispatcher knowledge walks out the door
   - **Peak vulnerability**: Exception volume spikes during bad weather, traffic, peak seasons → system collapses

4. **Scalability Constraint**: **5/5**
   - **Linear scaling**: Exception volume grows with delivery volume (assumed ~5% exception rate: 180 / 3,500 deliveries)
   - **Synchronous coordination**: Driver waits for dispatcher decision → doesn't scale (adding dispatchers doesn't replicate Sandra's expertise)
   - **Judgment bottleneck**: Exception decisions require discretion (return vs. leave, VIP vs. standard) → can't just "hire more dispatchers"

**Composite Value Score**: (4 + 3 + 5 + 5) / 4 = **4.25** (High Value)

**Plot Position**: **Medium-High Volume (36 hrs), High Value (4.25)**

---

### Work Stream 4: Dispatch Adjustments

**Volume Metrics**:
- Daily cases: 90
- Average handle time: 18 min (per brief)
- **Total labor hours/day**: 90 × 18 min / 60 = **27 hours/day**
- **Volume Category**: **MEDIUM**

**Value Factors**:

1. **Customer Experience Impact**: **4/5**
   - **Indirect but high-stakes**: Dispatch adjustments (mid-route changes, driver swaps) directly affect delivery windows
   - **Time-sensitive**: Customer waiting for delivery; adjustment delays → missed window → customer dissatisfaction
   - **Proactive coordination**: Done correctly, customer never knows adjustment happened (seamless). Done poorly, customer gets delayed delivery or no-show.

2. **Revenue Protection**: **3/5**
   - **Medium revenue impact**: Missed delivery windows → SLA breaches → penalty clauses (if contract terms include SLAs)
   - **Opportunity cost**: Failed adjustments → return-to-depot → re-delivery cost
   - **No direct churn evidence**: No artefact links dispatch adjustments to customer churn (but plausible if chronic delays)

3. **Operational Risk**: **4/5**
   - **High complexity**: Multi-constraint optimization (route distance, vehicle capacity, driver hours, customer time windows, traffic)
   - **Time-sensitive**: Decisions must be made in minutes, not hours (customer windows closing)
   - **Dispatcher expertise**: Requires route knowledge, driver performance intuition, traffic patterns
   - **Moderate bottleneck**: 90 cases/day = 27 hours/day (10% of Customer Ops capacity) — significant but not dominant

4. **Scalability Constraint**: **4/5**
   - **Linear scaling**: Adjustment volume grows with delivery volume (assumed ~2.6% adjustment rate: 90 / 3,500 deliveries)
   - **High judgment requirement**: Cannot simply "hire more dispatchers" — requires training, route knowledge, real-time decision-making
   - **System integration complexity**: Requires Dispatch Console API access (currently "limited" per brief), real-time vehicle tracking, traffic data

**Composite Value Score**: (4 + 3 + 4 + 4) / 4 = **3.75** (Medium-High Value)

**Plot Position**: **Medium Volume (27 hrs), Medium-High Value (3.75)**

---

## 3. Volume × Value Matrix Visualization

```
VALUE
(Business
 Impact)
  5.0 ┤                                    
      │                                    
  4.5 ┤              ● Billing Disputes    
      │                (28 hrs, 4.5)       
  4.0 ┤          ● Delivery Exceptions     
      │            (36 hrs, 4.25)          
  3.5 ┤      ● Dispatch Adjustments        
      │        (27 hrs, 3.75)              
      │                                    ● ETA Inquiries
  3.0 ┤                                      (73 hrs, 3.75)
      │                                    
  2.5 ┤                                    
      │                                    
  2.0 ┤                                    
      │                                    
  1.0 ┴──────┬───────┬───────┬───────┬────┬───────────────
           10      20      30      40   50      60      70+
                                                     VOLUME
                                             (Labor Hours/Day)
```

**Quadrant Analysis**:

- **Top-Right (High Volume, High Value)**: **ETA Inquiries** — highest labor consumption (73 hrs), high customer impact, scales linearly with growth
- **Top-Center (Medium Volume, Highest Value)**: **Billing Disputes** — highest value (4.5), medium labor, highest revenue protection
- **Center (Medium Volume, High Value)**: **Delivery Exceptions** — highest operational risk (5/5), medium labor, dispatcher bottleneck
- **Center-Left (Medium Volume, Medium-High Value)**: **Dispatch Adjustments** — medium labor, medium-high value, complex to automate

---

## 4. Primary Agentic Target: ETA Inquiries

### Why ETA Inquiries Win

**Thesis**: ETA Inquiries offer the **highest absolute ROI** for initial agentic investment due to:
1. **Highest volume** (73 hrs/day = 28% of Customer Ops capacity)
2. **Lowest risk** (error = customer calls back; no financial or relationship stakes)
3. **Fastest time-to-value** (fully automatable with GPS API access; no judgment required)
4. **Highest deflection potential** (90% of cases can be handled agenetically)
5. **Scalability unlock** (frees 66 hours/day = 8.8 FTE equivalent to absorb growth or redeploy to billing disputes)

**vs. Billing Disputes** (highest value score 4.5):
- **Billing Disputes are higher value per case** (4.5 vs. 3.75), BUT:
  - Lower volume (28 hrs vs. 73 hrs) → lower absolute labor savings
  - Higher risk (credit decisions require governance, Aurum constraint blocks automation of resolution)
  - Longer time-to-value (agent can accelerate investigation, but human approval still required → 64% time reduction vs. 96% for ETA)
  - **Cannot achieve 90% deflection** — only investigation (60% of process) is automatable; resolution (40%) remains human-led

**vs. Delivery Exceptions** (highest operational risk 5/5):
- **Delivery Exceptions have highest operational risk** (dispatcher bottleneck), BUT:
  - Lower volume (36 hrs vs. 73 hrs)
  - Higher complexity (judgment-heavy: VIP customers, damage assessment, cost-benefit trade-offs)
  - Lower deflection potential (estimated 60% triage-able, 40% requires dispatcher judgment)
  - Requires dispatcher heuristic codification (Sandra must document decision criteria → organizational change management)

**vs. Dispatch Adjustments**:
- Lower volume (27 hrs), out of Customer Ops scope (belongs to Dispatch Operations), high system integration complexity (Dispatch Console API "limited")

---

### ETA Inquiries: ROI Calculation

**Current State**:
- 400 inquiries/day × 11 min (observed elapsed time) = 73 hours/day
- Labor cost: 73 hrs/day × £20/hr (loaded FTE cost) × 250 work days = **£365K/year**

**Future State** (90% deflection):
- 360 inquiries/day agent-handled × 30 sec = 3 hours/day (agent compute time, negligible cost)
- 40 escalations/day × 11 min (human handle time for complex cases) = 7.3 hours/day
- Labor cost: 7.3 hrs/day × £20/hr × 250 days = **£36.5K/year**
- Agent cost: 360 cases/day × 250 days × £0.30/case (LLM API + infrastructure) = **£27K/year**
- **Total Future Cost**: £63.5K/year

**Annual Savings**: £365K - £63.5K = **£301.5K/year**

**Capacity Freed**: 73 - 7.3 = **65.7 hours/day** = **8.8 FTE equivalent**

**Payback Period**: 
- Agent development cost (Phase 1): £80-120K (estimated)
- Payback: £100K investment / £301K annual savings = **4 months**

---

### ETA Inquiries: Strategic Advantages

1. **Quick Win → Builds Trust**
   - Sarah Whitmore is skeptical (2 prior automation failures)
   - ETA agent proves agentic value in 3 months (measurable deflection rate, customer satisfaction improvement)
   - Success unlocks budget + organizational support for Phase 2 (Billing Disputes)

2. **Customer-Facing Impact**
   - Fastest response times (11 min → <30 sec) → visible satisfaction improvement
   - Self-service option (customer portal, SMS, email) → reduces inbound calls
   - Industry benchmark: Carriers with instant ETA updates have 15-20% higher NPS (Net Promoter Score)

3. **Capacity Redeployment**
   - 66 hours/day freed = enough capacity to:
     - Absorb 20% volume growth (146 cases/day) without hiring
     - Redeploy 3-4 FTE to billing dispute resolution (accelerates Phase 2)
     - Launch proactive customer outreach (call before they call us)

4. **Low Implementation Risk**
   - No policy ambiguity (ETA calculation is algorithmic, not discretionary)
   - No financial risk (wrong ETA doesn't cost money)
   - No governance complexity (no credit approval, no audit trail requirements beyond logging)
   - **Single blocker**: GPS API access (negotiable with Dispatch team)

5. **Demonstrates ATX Methodology**
   - Proves agents can deflect high-volume, low-complexity work
   - Validates delegation archetype ("Fully Agentic" for lookup, "Agent-Led" for precision calculation)
   - Shows lived-vs-documented gap (agents needed 5 min to get GPS data, not instant)

---

## 5. Secondary Target: Billing Disputes (Phase 2)

### Why Billing Disputes Are Second

**Thesis**: After ETA agent proves value (Phase 1), Billing Disputes are **Phase 2 target** because:
1. **Highest value per case** (4.5/5) — revenue protection, churn prevention
2. **Agent-accelerated investigation** (28 min → 8 min per case) — 64% time reduction
3. **High customer relationship impact** (email artefact shows Hayes & Sons frustration, £10K+ receivables at risk)
4. **Governance unlock** (agent logging fixes Sandra's manual override gap, improves audit compliance)

**Why Not Primary**:
- Lower volume (28 hrs vs. 73 hrs) → lower absolute labor savings
- Cannot achieve 90% deflection (investigation automatable, resolution requires human approval)
- Longer time-to-value (requires codifying credit approval policy, Aurum constraint handling)

**ROI Calculation** (Phase 2):
- Current: 60 disputes/day × 28 min = 28 hrs/day = **£140K/year**
- Future: 60 disputes/day × 8 min (agent investigates, human reviews + approves) = 8 hrs/day = **£40K/year**
- Agent cost: £27K/year (similar to ETA)
- **Annual Savings**: £140K - £67K = **£73K/year**
- **Capacity Freed**: 20 hours/day = 2.7 FTE

**Combined ROI** (Phase 1 + Phase 2):
- Total savings: £301K (ETA) + £73K (Billing) = **£374K/year**
- Total capacity freed: 65.7 + 20 = **85.7 hours/day** = **11.4 FTE equivalent**
- **On benchmark**: Competitor saved £1.2M (per CEO briefing); Apex proportional target £540-600K by Year 2. Phase 1+2 delivers £374K in Year 1, scaling to £600K+ by Year 2 with volume growth.

---

## 6. Tertiary Target: Delivery Exceptions (Phase 3)

### Why Delivery Exceptions Are Third

**Thesis**: After ETA + Billing agents operational (Phases 1-2), Delivery Exceptions are **Phase 3 target** because:
1. **Highest operational risk** (5/5) — dispatcher bottleneck (Sandra's line busy, drivers blocked)
2. **Agent-led triage** (60% of cases follow heuristic: <£500 package + standard refusal → return-to-depot)
3. **Unblocks Sandra** — frees her to focus on high-value exceptions (VIP customers, damage assessment)

**Why Not Primary or Secondary**:
- Requires **dispatcher heuristic codification** (organizational change: Sandra must document decision criteria)
- **Judgment-heavy** (40% of cases require human decision: VIP customers, damage claims, cost-benefit trade-offs)
- **Change management risk** (dispatchers may resist agent triage if they distrust recommendations)

**ROI Calculation** (Phase 3):
- Current: 180 exceptions/day × 12 min = 36 hrs/day = **£180K/year**
- Future: 108 exceptions agent-handled (60%) × 2 min + 72 human-handled (40%) × 12 min = 3.6 + 14.4 = 18 hrs/day = **£90K/year**
- Agent cost: £27K/year
- **Annual Savings**: £180K - £117K = **£63K/year**
- **Capacity Freed**: 18 hours/day = 2.4 FTE
- **Key benefit**: Unblocks Sandra (operational resilience) + faster driver responses (<2 min vs. 20 min callback wait)

**Combined ROI** (Phases 1+2+3):
- Total savings: £301K + £73K + £63K = **£437K/year**
- Total capacity freed: 65.7 + 20 + 18 = **103.7 hours/day** = **13.8 FTE equivalent**

---

## 7. Deferred Target: Dispatch Adjustments (Phase 4+)

### Why Dispatch Adjustments Are Deferred

**Rationale**:
1. **Out of Customer Ops scope** — Belongs to Dispatch Operations (separate team, separate systems)
2. **High system integration complexity** — Dispatch Console API "limited" (per brief); requires real-time vehicle tracking, route optimization, driver hours tracking
3. **Multi-constraint optimization** — Judgment-heavy, high-stakes (SLA breaches, cost overruns)
4. **Lower ROI priority** — 27 hrs/day (10% of capacity) vs. 73 hrs/day (ETA) or 36 hrs/day (Exceptions)

**Revisit Criteria** (Phase 4, Month 10+):
- Phases 1-3 operational and delivering ROI
- Dispatch Console API access negotiated (or alternative integration built)
- Business case for real-time route optimization validated (cost savings from reduced re-delivery, improved SLA compliance)

**Potential ROI** (if pursued):
- Agent assists dispatcher with data assembly (vehicle locations, capacity, time windows) and scenario simulation ("Option A: assign to Driver B, arrival 14:30, delays 1 stop. Option B: assign to Driver C, arrival 15:00, no delays")
- Dispatcher decides, but decision time reduced (18 min → 8 min)
- **Annual Savings**: £135K - £75K = **£60K/year** (estimated)

---

## 8. Volume × Value: Final Rankings

| Rank | Work Stream | Volume (hrs/day) | Value (composite) | Annual Savings (est.) | Deflection Potential | Phase | Primary Justification |
|---|---|---|---|---|---|---|---|
| **1** | **ETA Inquiries** | 73 | 3.75 | **£301K** | 90% | **Phase 1** | Highest volume, lowest risk, fastest time-to-value, proves agentic concept |
| **2** | **Billing Disputes** | 28 | 4.5 | **£73K** | 60% (investigation only) | **Phase 2** | Highest value/case, revenue protection, churn prevention, governance unlock |
| **3** | **Delivery Exceptions** | 36 | 4.25 | **£63K** | 60% (triage) | **Phase 3** | Highest operational risk, unblocks dispatcher bottleneck, organizational resilience |
| **4** | **Dispatch Adjustments** | 27 | 3.75 | £60K (potential) | 20% (data assist) | **Phase 4+** | Out of scope, high complexity, defer until Phases 1-3 prove ROI |

**Cumulative ROI** (Phases 1-3, 12 months): **£437K annual savings**, **103.7 hours/day freed** (13.8 FTE equivalent)

**Benchmark Check**: Competitor saved £1.2M annualized (per CEO briefing to Sarah). Apex proportional target: £540-600K by Year 2. Our projection: £437K Year 1 + volume growth + operational efficiencies → **£600-700K by Year 2** (on or above benchmark).

---

## 9. Decision Rationale: Why ETA Inquiries Win

### The Case for ETA Inquiries as Primary Target

**Volume Argument**:
- ETA Inquiries consume **73 hours/day** (28% of Customer Ops capacity)
- Billing Disputes consume 28 hours/day (11%)
- Delivery Exceptions consume 36 hours/day (14%)
- **ETA is 2.6x larger than Billing, 2x larger than Exceptions** → freeing ETA capacity has highest absolute impact

**Risk Argument**:
- ETA errors are **low-stakes** (customer calls back, no financial loss)
- Billing Dispute errors are **high-stakes** (over-crediting costs money, under-crediting causes churn)
- Delivery Exception errors are **medium-stakes** (wrong decision costs re-delivery or customer dissatisfaction)
- **ETA is lowest-risk work stream** → safest place to prove agentic value

**Speed Argument**:
- ETA agent can be **fully operational in 3 months** (single API integration: GPS access)
- Billing Dispute agent requires **policy codification** (credit approval thresholds, criteria) + Aurum constraint handling → 4-6 months
- Delivery Exception agent requires **dispatcher heuristic codification** (Sandra's knowledge transfer) + change management → 5-7 months
- **ETA is fastest to deliver** → proves ROI quickly, builds organizational trust

**Strategic Argument**:
- Sarah Whitmore is **skeptical** (2 prior automation failures)
- ETA agent is **low-risk proof of concept** → visible customer satisfaction improvement, measurable deflection rate
- Success builds trust → unlocks budget + organizational support for higher-complexity work streams (Billing, Exceptions)
- **Failure of ETA agent** (low-risk) is recoverable; **failure of Billing agent** (high-risk, financial impact) would be catastrophic

---

### The Case Against Billing Disputes as Primary Target

**Counter-Argument**: "Billing Disputes have highest value (4.5/5) and highest revenue protection — shouldn't we prioritize revenue?"

**Rebuttal**:
1. **Lower absolute impact**: 28 hrs/day vs. 73 hrs/day → £73K savings vs. £301K savings
2. **Higher implementation risk**: Requires policy codification (credit approval), Aurum constraint handling, governance controls (audit trail)
3. **Cannot achieve full deflection**: Investigation automatable (60%), resolution requires human approval (40%) → labor savings capped at 64%
4. **Organizational risk**: If Billing agent over-credits (governance failure), financial loss is immediate and cumulative. If ETA agent gives wrong estimate, customer calls back (no financial loss).
5. **Sarah's trust**: Billing involves money → Sarah will scrutinize heavily. ETA involves information → lower scrutiny, easier approval.

**Better Strategy**: Prove agentic value with **ETA (low-risk, high-volume)**, then extend to **Billing (high-risk, high-value)** once trust established.

---

### The Case Against Delivery Exceptions as Primary Target

**Counter-Argument**: "Delivery Exceptions have highest operational risk (5/5) and dispatcher bottleneck — shouldn't we unblock Sandra first?"

**Rebuttal**:
1. **Organizational change required**: Sandra must document decision criteria (heuristic codification) → takes time, requires buy-in
2. **Change management risk**: Dispatchers may resist agent triage if they distrust recommendations (seen as threat to expertise)
3. **Lower volume**: 36 hrs/day vs. 73 hrs/day → £63K savings vs. £301K savings
4. **Judgment complexity**: 40% of exceptions require human decision (VIP customers, damage assessment) → deflection capped at 60%
5. **Dependencies**: Exception agent requires GPS API (same as ETA) + Dispatch Console integration (more complex than ETA)

**Better Strategy**: Deploy **ETA agent first** (shares GPS API dependency, simpler use case), prove value, then extend to **Exceptions** (Sandra sees ETA success, more willing to codify heuristics for Exception agent).

---

## 10. Conclusion: ETA Inquiries Are the Primary Target

**Winner**: **ETA Inquiries** (Phase 1)

**Justification**:
1. **Highest volume**: 73 hrs/day (28% of Customer Ops capacity)
2. **Lowest risk**: Error = customer calls back (no financial/relationship stakes)
3. **Highest deflection**: 90% of cases fully agentic
4. **Fastest time-to-value**: 3 months to operational
5. **Highest annual savings**: £301K/year (vs. £73K Billing, £63K Exceptions)
6. **Strategic proof point**: Builds Sarah's trust, unlocks budget for Phases 2-3

**Runner-Up**: **Billing Disputes** (Phase 2)
- Highest value/case (4.5/5), revenue protection, but lower volume and higher implementation risk

**Third Place**: **Delivery Exceptions** (Phase 3)
- Highest operational risk (5/5), unblocks dispatcher bottleneck, but requires organizational change (heuristic codification)

**Phased Approach**:
- **Phase 1** (Months 1-3): ETA Inquiries → £301K savings, proves concept
- **Phase 2** (Months 4-6): Billing Disputes → £73K savings, governance unlock
- **Phase 3** (Months 7-9): Delivery Exceptions → £63K savings, operational resilience
- **Cumulative**: £437K annual savings, 103.7 hours/day freed (13.8 FTE equivalent)

**This phased approach maximizes ROI while minimizing organizational risk** — the ATX methodology applied to prioritization.
