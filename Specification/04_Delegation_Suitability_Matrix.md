# Delegation Suitability Matrix

## Purpose

This matrix scores each major task cluster from Customer Operations on ATX delegation dimensions and assigns **delegation archetypes** with explicit rationale. Every archetype assignment is justified with reference to cognitive load, risk profile, and system constraints.

**Critical Anti-Pattern Avoided**: This matrix does NOT default to "fully agentic" for all tasks. Delegation boundaries reflect lived work reality, system constraints (Aurum batch-only architecture), and governance requirements (credit approval, dispatcher judgment).

---

## 1. ATX Delegation Dimensions (Scoring Framework)

Each task cluster is scored on 6 dimensions, scale 1-5:

| Dimension | 1 (Low Suitability) | 5 (High Suitability) |
|---|---|---|
| **Determinism** | Highly variable, judgment-heavy | Rule-bound, consistent patterns |
| **Pattern Stability** | Process changes frequently | Process stable over time |
| **Data Availability** | Data scattered, incomplete, stale | Data centralized, structured, real-time |
| **Time Sensitivity** | Must respond immediately (<1 min) | Can process asynchronously (batch) |
| **Risk of Error** | High stakes (financial, legal, relationship) | Low stakes (easily reversible) |
| **Codifiability** | Tacit knowledge, intuition-based | Explicit rules, documentable |

**Composite Score**: Average of 6 dimensions (1.0 - 5.0)
- **4.0-5.0**: Fully Agentic candidate
- **3.0-3.9**: Agent-Led with Oversight candidate
- **2.0-2.9**: Human-Led with Agent Support candidate
- **1.0-1.9**: Human-Only (do not automate)

**Important**: Composite score is a signal, not a decision. Archetype assignment considers score + constraints + risk profile.

---

## 2. Task Cluster Definitions

Based on the 4 work streams (from brief) and cognitive load map (Deliverable 3), we define 8 task clusters:

### Work Stream 1: ETA Inquiries (400/day)
- **TC1.1**: Standard ETA Lookup (order ID → route → scheduled window)
- **TC1.2**: Precision ETA Calculation (GPS-based, traffic-adjusted)

### Work Stream 2: Billing Disputes (60/day)
- **TC2.1**: Dispute Intake & Classification
- **TC2.2**: Dispute Investigation (data aggregation across systems)
- **TC2.3**: Resolution Decision & Approval (credit amount, policy interpretation)

### Work Stream 3: Delivery Exceptions (180/day)
- **TC3.1**: Low-Value Exception Triage (packages <£500, standard refusal reasons)
- **TC3.2**: High-Value Exception Decision (packages >£500, VIP customers, damage assessment)

### Work Stream 4: Dispatch Adjustments (90/day)
- **TC4.1**: Dispatch Re-Planning & Driver Coordination (out of scope for Gate 2, scored for completeness)

---

## 3. Delegation Suitability Scoring

### TC1.1: Standard ETA Lookup

**Description**: Customer asks "Where is my order?" Agent retrieves order ID, route assignment, and scheduled ETA window from CRM.

**Evidence**: SMS artefact, 11:14-11:16 (2 min response with scheduled window 13:00-17:00)

| Dimension | Score | Justification |
|---|---|---|
| **Determinism** | 5 | Order ID → route → ETA window is direct database lookup. No judgment required. |
| **Pattern Stability** | 5 | Process identical across all customers (B2B, DTC). No variation by customer type. |
| **Data Availability** | 5 | Order + route data in CRM (assumed real-time). GPS data siloed but not required for basic lookup. |
| **Time Sensitivity** | 4 | Customer expects <5 min response. Async acceptable but real-time preferred. |
| **Risk of Error** | 5 | Worst case: Customer receives scheduled window (already known). No financial/legal risk. |
| **Codifiability** | 5 | Fully codifiable: IF order_id EXISTS THEN RETURN route + scheduled_window. |
| **COMPOSITE** | **4.8** | |

**Delegation Archetype**: **FULLY AGENTIC**

**Rationale**: 
- Deterministic lookup with zero judgment
- Data available in CRM (no cross-system coordination)
- Error risk negligible (customer can escalate if unsatisfied)
- High volume (400/day) + low complexity = ideal deflection target

**Human Escalation Trigger**: 
- Order ID not found in system
- Customer explicitly requests callback (e.g., "I need to speak to someone")

---

### TC1.2: Precision ETA Calculation (GPS-Based)

**Description**: Customer dissatisfied with 4-hour window, requests specific time. Agent queries GPS data, calculates ETA based on current driver location, stops remaining, and traffic conditions.

**Evidence**: SMS artefact, 11:17-11:24 (agent waits 5 min for Dispatch GPS data, responds with "best guess" 14:00-15:00)

| Dimension | Score | Justification |
|---|---|---|
| **Determinism** | 4 | Calculation rule-based (distance, traffic, stops), but requires heuristic for stop duration. |
| **Pattern Stability** | 4 | Calculation logic stable, but traffic conditions variable. |
| **Data Availability** | 3 | **GPS data siloed in Dispatch Console** (architectural constraint). If API available, score → 5. |
| **Time Sensitivity** | 4 | Customer waiting on SMS, expects <2 min response. Real-time preferred. |
| **Risk of Error** | 4 | Inaccurate ETA → customer plans incorrectly → frustration. But reversible (customer calls back). |
| **Codifiability** | 4 | Algorithmic: GPS location + stops remaining + traffic API + avg stop duration (15 min) → ETA. Heuristic trainable. |
| **COMPOSITE** | **3.8** | |

**Delegation Archetype**: **AGENT-LED WITH OVERSIGHT** (trending toward Fully Agentic once GPS API available)

**Rationale**:
- **Currently**: Data availability constraint (GPS siloed) forces human coordination → agent-led with human validation
- **Future**: Once Driver App GPS API accessible, agent can calculate autonomously → fully agentic
- Calculation is algorithmic (not judgment), but data staleness (36 min in SMS artefact) introduces uncertainty
- Agent should escalate if GPS >30 min stale (confidence too low)

**Human Escalation Trigger**:
- GPS data stale (>30 min since last ping)
- Customer demands callback (wants human reassurance, not algorithm)
- Route has unplanned stop (accident, traffic jam) not reflected in GPS

**Implementation Note**: This task cluster is **blocked by GPS API access**. If Dispatch Console API unavailable, agent cannot operate autonomously → must escalate to Dispatch team (defeats deflection purpose). **Prerequisite negotiation with Sarah: Grant Customer Ops (via agent) read-only GPS API access.**

---

### TC2.1: Dispute Intake & Classification

**Description**: Customer email/call received (e.g., billing@ mailbox). Agent parses inquiry, extracts dispute type (fuel surcharge, dimensional weight, redelivery fee, damage), and routes to appropriate queue.

**Evidence**: Email artefact, Day 1 09:14 customer email → 16:48 Billing team deflects to Customer Ops (classification correct but slow)

| Dimension | Score | Justification |
|---|---|---|
| **Determinism** | 5 | Keyword matching: "fuel surcharge" + "damaged" → FUEL_SURCH_DAMAGE dispute type. |
| **Pattern Stability** | 5 | Dispute types stable (APEX_DISPUTES_OPEN shows 5 types: FUEL_SURCH_DAMAGE, DIM_WEIGHT, REDELIVERY_FEE). |
| **Data Availability** | 5 | Email/call transcript available at intake. No cross-system query needed. |
| **Time Sensitivity** | 3 | Customer expects acknowledgment <24 hours. Not real-time urgent. |
| **Risk of Error** | 4 | Misclassification → routed to wrong queue → delay. But correctable. No financial risk at intake stage. |
| **Codifiability** | 5 | Fully codifiable: IF email CONTAINS "fuel surcharge" AND ("damaged" OR "damage") THEN dispute_type = FUEL_SURCH_DAMAGE. |
| **COMPOSITE** | **4.5** | |

**Delegation Archetype**: **FULLY AGENTIC**

**Rationale**:
- Pure pattern matching (NLP classification)
- No judgment required at intake (just routing)
- Error risk low (misrouted cases self-correct when human reviews queue)
- High value: Immediate acknowledgment improves customer experience (vs. 7.5-hour delay in email artefact)

**Human Escalation Trigger**:
- Ambiguous dispute (multiple types overlap, e.g., fuel surcharge + dimensional weight)
- Customer language suggests legal/regulatory issue (keywords: "solicitor," "Ombudsman," "lawsuit")

---

### TC2.2: Dispute Investigation (Data Aggregation)

**Description**: Once dispute classified, agent retrieves invoice, fuel surcharge detail, delivery exception log, customer history (past disputes, receivables aging, payment behavior) from 4 systems. Presents unified summary to human.

**Evidence**: Email artefact, Sandra's investigation (Day 6) required querying APEX_BILL_DAILY, APEX_FUEL_SURCH, Driver App/Dispatch Console (delivery exception), CRM (customer history), APEX_DISPUTES_OPEN (past disputes), APEX_AGED_RECEIVABLES (aging).

| Dimension | Score | Justification |
|---|---|---|
| **Determinism** | 5 | Data retrieval is deterministic: invoice_no → query all systems. No judgment. |
| **Pattern Stability** | 5 | Systems stable (Aurum exports daily, CRM updated continuously). |
| **Data Availability** | 3 | **Aurum T-1 lag** (batch export, not real-time). Driver App/Dispatch Console integration unclear. If yesterday's invoice disputed, data available; if today's invoice disputed, data not yet in export → agent must wait or escalate. |
| **Time Sensitivity** | 4 | Investigation can happen asynchronously (customer doesn't need instant resolution, just acknowledgment). Agent can batch-process overnight. |
| **Risk of Error** | 5 | Data aggregation errors (wrong invoice retrieved) are easily detectable by human reviewer. Low risk. |
| **Codifiability** | 5 | Fully codifiable: Query 4 systems in parallel, JOIN on customer_id and invoice_no, return structured summary. |
| **COMPOSITE** | **4.5** | |

**Delegation Archetype**: **FULLY AGENTIC** (with Aurum lag caveat)

**Rationale**:
- Agent aggregates data 10x faster than human (parallel queries vs. sequential manual lookups)
- No judgment required — pure data retrieval and assembly
- Aurum T-1 lag is constraint, not blocker: Agent can operate on yesterday's data (acceptable for most disputes; if customer disputes today's invoice, agent flags "data not yet available, will investigate tomorrow")
- Human reviews summary, not raw data → cognitive load reduction

**Human Escalation Trigger**:
- Invoice not found in Aurum export (too recent, or data quality issue)
- Delivery exception not logged in Driver App (driver didn't report damage, but customer claims damage)
- Customer requests immediate resolution (cannot wait for T-1 lag)

**Implementation Note**: Agent must handle Aurum lag gracefully. Suggested response: "Your invoice from [date] is being processed. I'll have full details by tomorrow morning. In the meantime, I've flagged your case as high-priority. Would you like to speak with a specialist now, or is tomorrow acceptable?"

---

### TC2.3: Resolution Decision & Approval (Credit Amount)

**Description**: Based on investigation summary, determine credit amount (£0, partial, full), apply policy interpretation (goodwill vs. policy-required), and approve/execute credit.

**Evidence**: Email artefact, Sandra decides £170 (50% of £340 dispute). Rationale not documented. Internal note: "manual override," no audit log entry.

| Dimension | Score | Justification |
|---|---|---|
| **Determinism** | 2 | **Low**: Credit amount is discretionary. Sandra chose £170 (not £0, not £340) — no rule documented. |
| **Pattern Stability** | 3 | Dispute types stable, but resolution varies by customer (VIP gets full credit, standard gets partial?). Pattern exists but not codified. |
| **Data Availability** | 4 | All data available (via TC2.2 investigation). Decision input complete. |
| **Time Sensitivity** | 3 | Customer expects resolution <48 hours (industry standard). Not real-time urgent. |
| **Risk of Error** | 2 | **High**: Over-crediting → financial loss (cumulative £50K+ if unchecked). Under-crediting → customer churn (Hayes & Sons at risk). Both high-stakes outcomes. |
| **Codifiability** | 2 | **Low**: Policy states "goodwill credit allowed" but no criteria for amount. Heuristic exists (50% split for first offense, 100% for repeat?) but not explicit. |
| **COMPOSITE** | **2.7** | |

**Delegation Archetype**: **HUMAN-LED WITH AGENT SUPPORT**

**Rationale**:
- **Judgment-heavy**: Credit decision requires customer relationship intuition (churn risk assessment), cost-benefit trade-off (£170 goodwill cost vs. £X customer lifetime value), and policy interpretation (when is goodwill appropriate?)
- **Financial risk**: Unsupervised agent could over-credit (customer learns to dispute for free credits) or under-credit (churn)
- **Governance requirement**: Credits >£200 likely require manager approval (inferred from Sandra's role, no explicit threshold in artefacts)
- **Agent value**: Agent can **recommend** credit amount based on past dispute resolutions (e.g., "Similar FUEL_SURCH_DAMAGE disputes resolved at 50% credit. Suggested: £170. Confidence: Medium."), but human must approve

**Human Decision Criteria** (to be codified in discovery):
- Customer tier (VIP → full credit, standard → partial?)
- Dispute frequency (first-time → goodwill, repeat → policy enforcement or escalation to address root cause?)
- Damage evidence (driver confirmed → full credit, customer claim only → partial?)
- Financial threshold (>£200 requires manager approval?)

**Human Escalation Trigger**:
- **Always** — This task cannot be fully agentic. Human must approve every credit decision.
- Exception: Invoice correction errors (e.g., duplicate charge) may be auto-creditable if policy allows (but not in current scope — no evidence of rule-based credits in artefacts)

**Implementation Note**: Agent drafts resolution email for human review. Human can accept, modify credit amount, or escalate to manager. Agent logs approval in audit trail (fixes gap identified in email artefact: Sandra's manual override not logged).

---

### TC3.1: Low-Value Exception Triage (<£500 Packages)

**Description**: Driver calls/messages: "Recipient refused delivery" or "Address incorrect." Agent triages based on package value, customer tier, and refusal reason. For low-value, standard customers, agent instructs return-to-depot.

**Evidence**: Voicemail artefact, Mark Petrov route 042 at Stein-Allen (large customer). Driver blocked, 6 deliveries pending, Sandra's line busy.

| Dimension | Score | Justification |
|---|---|---|
| **Determinism** | 3 | **Medium**: Simple cases (low-value + standard refusal) have clear heuristic (return-to-depot). But edge cases require judgment (customer history, delivery urgency). |
| **Pattern Stability** | 4 | Exception types stable (refusal, damage, incorrect address, unattended). Process stable. |
| **Data Availability** | 4 | Package value in order system, customer tier in CRM, refusal reason in Driver App. GPS for route impact assessment. |
| **Time Sensitivity** | 5 | **Critical**: Driver blocked until decision received. Every minute = delayed downstream deliveries. <2 min response required. |
| **Risk of Error** | 3 | **Medium**: Wrong decision (return vs. leave) costs re-delivery (£40-80) or customer dissatisfaction. Reversible but costly. |
| **Codifiability** | 3 | **Medium**: Heuristic exists ("If package <£500 AND customer tier = STANDARD AND refusal reason = STANDARD THEN return-to-depot") but edge cases require judgment (e.g., "customer called ahead to delay delivery" vs. "recipient just refused"). |
| **COMPOSITE** | **3.7** | |

**Delegation Archetype**: **AGENT-LED WITH OVERSIGHT**

**Rationale**:
- **Low-stakes cases** (low-value packages, standard customers) follow heuristic → agent can decide autonomously, human spot-checks
- **High-stakes cases** (high-value, VIP customers, damage claims) require human judgment → agent escalates
- **Time-sensitivity critical**: Driver cannot wait 20 min for Sandra's callback (voicemail artefact). Agent must respond <2 min or driver defaults to return-to-depot (loses delivery window).
- **Agent value**: Unblocks drivers for 60-70% of exceptions (estimated: <£500 packages represent majority of volume). Frees Sandra to focus on complex cases (TC3.2).

**Human Escalation Trigger**:
- Package value >£500 (per SOP artefact: "high-value consignments escalate to Duty Manager")
- Customer tier = VIP (account value >£50K credit limit, per APEX_CUSTOMER_MASTER)
- Refusal reason = damage claim (requires photo evidence, insurance protocol per incomplete SOP Section 4.3)
- Driver judgment conflicts with heuristic (e.g., driver says "looks fine to me" but recipient claims damage — voicemail artefact)

**Implementation Note**: Agent must respond to driver within 2 min. If unable to decide (ambiguous case), agent escalates to human but provides **hold instruction** to driver: "Stand by, escalating to dispatcher. ETA 5 min." Prevents driver from parking indefinitely (6 deliveries blocked in voicemail artefact).

---

### TC3.2: High-Value Exception Decision (>£500, VIP Customers)

**Description**: Same as TC3.1, but for high-value packages or VIP customers. Requires dispatcher judgment on cost-benefit trade-off (re-delivery cost vs. customer relationship risk).

**Evidence**: Voicemail artefact, Stein-Allen account (large B2B customer, inferred high-value). Driver uncertain if pallet damaged, warehouse worker (not site manager) refused. Sandra must decide.

| Dimension | Score | Justification |
|---|---|---|
| **Determinism** | 2 | **Low**: Decision depends on customer relationship (Stein-Allen likely large account), damage assessment (driver says fine, recipient says damaged), and cost-benefit (re-delivery vs. force acceptance). |
| **Pattern Stability** | 3 | Exception types stable, but resolution varies by customer. VIP customers get override attempts; standard customers get return. |
| **Data Availability** | 4 | Customer tier, package value, driver notes available. But damage assessment subjective (no photo in voicemail artefact). |
| **Time Sensitivity** | 5 | **Critical**: Driver blocked, 6 deliveries pending. <5 min response required (longer than TC3.1 due to complexity, but still urgent). |
| **Risk of Error** | 2 | **High**: Wrong decision → customer relationship damaged (VIP churns) OR financial loss (re-delivery cost + driver time). |
| **Codifiability** | 2 | **Low**: Judgment criteria not documented. Sandra's decision process is tacit knowledge (customer relationship intuition, historical precedent). |
| **COMPOSITE** | **3.0** | |

**Delegation Archetype**: **HUMAN-LED WITH AGENT SUPPORT**

**Rationale**:
- **High-stakes judgment**: VIP customer decisions require relationship context (past delivery issues, account manager input, contract terms) not fully captured in systems
- **Damage assessment**: Driver says "looks fine," recipient says "damaged" — requires human judgment, possibly photo evidence or third-party inspection
- **Agent value**: Agent surfaces decision-supporting data (customer tier, account value, past exceptions, re-delivery cost estimate, driver reliability score if available), but **human decides**
- **Time-sensitivity**: Even with human decision, agent accelerates by presenting data instantly (vs. Sandra manually querying CRM + Dispatch Console)

**Human Decision Criteria** (to be codified in discovery with Sandra):
- Customer account value (credit limit, annual revenue)
- Delivery urgency (time-sensitive shipment vs. standard)
- Damage evidence (photo, driver notes, recipient notes)
- Cost of re-delivery (distance, driver availability, time to re-attempt)
- Relationship history (first exception vs. recurring issues)

**Human Escalation Trigger**:
- **Always** — This task cannot be agent-decided. Agent presents data, human decides within 5 min.

**Implementation Note**: Agent must provide **hold instruction** to driver while human reviews: "Hold position. Decision in progress, ETA 5 min. Do not return to depot yet." Prevents premature action.

---

### TC4.1: Dispatch Re-Planning & Driver Coordination

**Description**: Mid-route change required (new pickup, driver swap, traffic delay). Dispatcher re-optimizes route, reassigns stops, coordinates with multiple drivers.

**Evidence**: Not directly in artefacts, but inferred from brief: "~90/day, avg 18 min/case, tight time pressure."

| Dimension | Score | Justification |
|---|---|---|
| **Determinism** | 2 | **Low**: Multi-constraint optimization (route distance, vehicle capacity, driver hours, customer time windows, traffic). No single "right" answer. |
| **Pattern Stability** | 3 | Re-planning logic stable, but inputs vary (traffic unpredictable, driver availability dynamic). |
| **Data Availability** | 3 | **Dispatch Console API "limited"** (per brief). If full route state + vehicle locations + driver hours available → score 5. Currently unclear. |
| **Time Sensitivity** | 5 | **Critical**: Mid-route decisions must be made in minutes (customer time windows closing, driver waiting for instruction). |
| **Risk of Error** | 2 | **High**: Missed time window → customer SLA breach. Overloaded driver → overtime cost or regulatory violation (driver hours limits). |
| **Codifiability** | 3 | **Medium**: Route optimization algorithms exist (vehicle routing problem, VRP), but require full system state. Dispatcher intuition supplements algorithm (e.g., "Driver A is fast, Driver B is reliable — assign urgent pickup to A"). |
| **COMPOSITE** | **3.0** | |

**Delegation Archetype**: **HUMAN-ONLY** (for Gate 2 scope)

**Rationale**:
- **Out of scope**: Gate 2 focuses on Customer Operations (ETA inquiries, billing disputes, exceptions). Dispatch adjustments are **Dispatch Operations**, not Customer Ops.
- **High complexity**: Real-time multi-constraint optimization with high stakes (SLA breach, cost overruns). Requires significant system integration (Dispatch Console API access, real-time vehicle tracking, driver hours tracking).
- **Agent potential (future)**: Agent could assist by:
  - Presenting vehicle locations + available capacity on map
  - Calculating route impact of adding new pickup ("Driver B is 15 min from pickup location, has 2 hours remaining, vehicle at 70% capacity")
  - Simulating alternative assignments ("Option A: Assign to Driver B, arrival 14:30, delays 1 downstream stop. Option B: Assign to Driver C, arrival 15:00, no downstream impact.")
- **Decision remains human**: Dispatcher chooses option based on customer priority, driver reliability, risk tolerance.

**Defer to Future Phase**: After ETA/Billing/Exception agents prove value, revisit dispatch adjustment support (Phase 4, Month 10+).

---

## 4. Delegation Suitability Matrix: Summary Table

| Task Cluster | Volume/Day | Composite Score | Delegation Archetype | Rationale (Summary) | Phase |
|---|---|---|---|---|---|
| **TC1.1**: Standard ETA Lookup | 400 | 4.8 | **FULLY AGENTIC** | Deterministic lookup, zero judgment, low risk. Ideal deflection target. | **Phase 1** |
| **TC1.2**: Precision ETA Calculation | 400 | 3.8 | **AGENT-LED WITH OVERSIGHT** | Algorithmic, but GPS API access required. Escalate if data stale. | **Phase 1** |
| **TC2.1**: Dispute Intake & Classification | 60 | 4.5 | **FULLY AGENTIC** | Pattern matching, zero judgment, low risk. Immediate acknowledgment improves CX. | **Phase 2** |
| **TC2.2**: Dispute Investigation | 60 | 4.5 | **FULLY AGENTIC** | Data aggregation across 4 systems. Agent 10x faster than human. Aurum T-1 lag handled gracefully. | **Phase 2** |
| **TC2.3**: Resolution Decision & Approval | 60 | 2.7 | **HUMAN-LED WITH AGENT SUPPORT** | Discretionary credit decision, financial risk, governance requirement. Agent recommends, human approves. | **Phase 2** |
| **TC3.1**: Low-Value Exception Triage | ~120 (est.) | 3.7 | **AGENT-LED WITH OVERSIGHT** | Heuristic-based for low-stakes cases. Escalate high-value, VIP, damage claims. Unblocks drivers. | **Phase 3** |
| **TC3.2**: High-Value Exception Decision | ~60 (est.) | 3.0 | **HUMAN-LED WITH AGENT SUPPORT** | VIP customer judgment, damage assessment, cost-benefit trade-off. Agent surfaces data, human decides. | **Phase 3** |
| **TC4.1**: Dispatch Re-Planning | 90 | 3.0 | **HUMAN-ONLY** (current scope) | Multi-constraint optimization, high stakes, limited API access. Defer to future phase. | **Phase 4+** |

**Total Addressable Volume** (Phases 1-3): 400 (ETA) + 60 (Billing) + 180 (Exceptions) = **640 cases/day** (88% of total 730)

**Expected Deflection** (Phases 1-3):
- ETA: 90% deflection = 360 cases/day fully agentic, 40 escalations
- Billing: 60% investigation time saved = 60 cases agent-accelerated, 60 human-approved
- Exceptions: 60% triage agentic = 108 cases agent-handled, 72 escalations

**Labor Hours Freed** (Phases 1-3): 98 hours/day (per Problem Statement, Section 2)

---

## 5. Justification of Archetype Assignments

### Why TC1.1 and TC1.2 (ETA Inquiries) Are NOT Both "Fully Agentic"

**Objection**: Both are ETA inquiries, both are algorithmic, why different archetypes?

**Answer**: 
- **TC1.1** (Standard Lookup) uses **existing system data** (scheduled window in CRM) → no API dependency, no calculation complexity → fully agentic
- **TC1.2** (Precision ETA) requires **GPS API access** (currently siloed) + **heuristic calculation** (stops remaining, traffic) → agent-led until architecture changes

**Key Distinction**: Data availability (dimension 3). TC1.1 scores 5/5 (data in CRM). TC1.2 scores 3/5 (GPS siloed). Once GPS API available, TC1.2 → fully agentic.

**Design Implication**: Phase 1 can deploy TC1.1 immediately (no API dependency). TC1.2 requires negotiation with Dispatch to expose GPS API → Phase 1b (API integration) before TC1.2 goes fully agentic.

---

### Why TC2.3 (Credit Decision) Is NOT "Agent-Led"

**Objection**: Agent can calculate credit amount (e.g., 50% split), why not agent-led?

**Answer**:
- **Financial risk**: Over-crediting cumulative cost (£50K+ if unchecked). Under-crediting churn risk (Hayes & Sons £10K+ receivables at risk).
- **Governance gap identified**: Sandra's "manual override" not logged in audit trail (email artefact internal note) → compliance risk if agent operates unsupervised
- **Policy ambiguity**: "Goodwill credit" discretionary, no documented threshold or criteria → agent would be guessing, not applying policy
- **Customer relationship context**: Credit decision depends on factors not in systems (e.g., account manager's intuition: "This customer is a complainer, don't over-credit" vs. "This customer is genuinely wronged, full credit to preserve relationship")

**Design Implication**: Agent can **recommend** (e.g., "Suggested £170, based on 50% split pattern for similar disputes"), but human must **approve** before credit applied. Approval logged in audit trail (fixes Sandra's gap).

**Alternative Considered**: "Agent-led with high oversight" (agent decides, human spot-checks 20%). **Rejected** because spot-checking doesn't prevent over-crediting in the 80% of cases not reviewed → financial risk too high. All credits require approval until policy codified.

---

### Why TC3.1 (Low-Value Exceptions) Is "Agent-Led" But TC3.2 (High-Value) Is "Human-Led"

**Objection**: Both are exception decisions, why different?

**Answer**:
- **Stakes**: TC3.1 (packages <£500, standard customers) → wrong decision costs £40-80 re-delivery. TC3.2 (packages >£500, VIP customers) → wrong decision costs customer relationship (churn risk = £50K-200K annual revenue loss per customer, estimated from credit limits).
- **Reversibility**: TC3.1 errors are correctable (customer calls back, we re-attempt delivery). TC3.2 errors are relationship-damaging (VIP customer loses trust, switches carriers).
- **Codifiability**: TC3.1 follows heuristic (value + tier + refusal reason → return-to-depot). TC3.2 requires judgment (customer relationship history, damage evidence assessment, cost-benefit intuition).

**Design Implication**: Agent can handle **routine triage** (TC3.1) autonomously, human spot-checks. Agent **cannot handle** **VIP/high-value** (TC3.2) → always escalate. This is a **delegation boundary** based on stakes, not complexity.

---

## 6. Anti-Pattern: "Everything Is Fully Agentic"

**What This Looks Like**:
- All 8 task clusters assigned "Fully Agentic"
- Rationale: "AI can do everything, just need oversight"
- No escalation triggers defined
- No governance controls (e.g., credit approval thresholds)

**Why This Fails**:
1. **TC2.3** (Credit Decision) fully agentic → unsupervised over-crediting → £50K+ financial loss in 6 months
2. **TC3.2** (High-Value Exceptions) fully agentic → VIP customer gets "return to depot" instruction → relationship lost, customer churns
3. **No audit trail** → compliance gap (already identified in Sandra's manual override) gets worse, not better
4. **Sarah Whitmore rejects design** → She's burned by 2 prior automation failures; "everything agentic" reads as reckless, not thoughtful

**How This Matrix Avoids Anti-Pattern**:
- **3 task clusters** assigned "Human-Led" or "Human-Only" (TC2.3, TC3.2, TC4.1) → 37.5% of clusters require human judgment
- **Explicit rationale** for each archetype (risk, governance, policy ambiguity, stakes)
- **Escalation triggers** defined for agent-led tasks (GPS stale, VIP customer, legal keywords)
- **Phase 4 defer** for dispatch adjustments → honest about scope limits

---

## 7. Constraints Driving Archetype Assignments

### Constraint 1: Aurum Batch-Only Architecture (T-1 Lag)

**Impact on TC2.2** (Dispute Investigation):
- Agent operates on yesterday's data (T-1 lag) → acceptable for most disputes (customer disputes last week's invoice)
- Edge case: Customer disputes today's invoice → data not yet in Aurum export → agent must wait or escalate
- **Design decision**: Archetype remains "Fully Agentic" because agent can **handle lag gracefully** (acknowledge dispute, promise tomorrow's investigation) vs. requiring real-time data

**If Aurum had real-time API**: TC2.2 score 5.0 (vs. current 4.5), but archetype unchanged (already fully agentic).

---

### Constraint 2: GPS Data Siloed in Dispatch Console

**Impact on TC1.2** (Precision ETA):
- Agent cannot query GPS directly → must coordinate with Dispatch (defeats deflection purpose)
- **Design decision**: Archetype "Agent-Led with Oversight" acknowledges GPS API is **prerequisite**. Until API available, agent escalates to human for GPS data.

**If Driver App GPS API available**: TC1.2 → "Fully Agentic" (score 4.5 → 5.0).

---

### Constraint 3: Goodwill Credit Policy Ambiguity

**Impact on TC2.3** (Credit Decision):
- No documented threshold (£200? £500? Unlimited?)
- No documented criteria (first offense 50%, repeat 100%? VIP full credit, standard partial?)
- Sandra's discretion not codified ("£170 = 50% split" — rationale inferred, not stated)
- **Design decision**: Archetype "Human-Led" until policy codified. Agent can recommend, but human must approve to prevent over-crediting.

**If policy codified**: TC2.3 could shift to "Agent-Led with High Oversight" (agent applies policy, human spot-checks 20%). But still not "Fully Agentic" due to financial risk.

---

## 8. Phased Rollout Aligned with Delegation Archetypes

| Phase | Task Clusters | Delegation Archetypes | Rationale | Success Metric |
|---|---|---|---|---|
| **Phase 1** (Months 1-3) | TC1.1, TC1.2 (ETA Inquiries) | Fully Agentic + Agent-Led | Highest volume, lowest risk, fastest ROI. Proves agentic value. | 85-90% ETA deflection, <30s response time |
| **Phase 2** (Months 4-6) | TC2.1, TC2.2, TC2.3 (Billing Disputes) | Fully Agentic (intake, investigation) + Human-Led (approval) | High complexity, high relationship impact. Agent accelerates, human governs. | Dispute resolution <48 hrs, audit compliance 100% |
| **Phase 3** (Months 7-9) | TC3.1, TC3.2 (Delivery Exceptions) | Agent-Led (triage) + Human-Led (high-value) | Unblocks dispatcher bottleneck. Agent handles routine, human handles VIP. | Driver wait time <2 min, Sandra's line not busy |
| **Phase 4+** (Months 10+) | TC4.1 (Dispatch Adjustments) | Human-Only (current) → potential Agent Support (future) | Out of initial scope. Requires Dispatch Console API access and real-time optimization. | Deferred |

**Rationale for Phasing**:
- **Phase 1**: Low-hanging fruit (ETA deflection) proves concept, builds trust with Sarah and Customer Ops team
- **Phase 2**: Higher complexity (billing disputes) demonstrates agent value in judgment-heavy work (investigation acceleration)
- **Phase 3**: Extends to dispatcher bottleneck (Sandra's line busy) — high organizational impact
- **Phase 4**: Defers highest-complexity work (dispatch optimization) until Phases 1-3 prove ROI and unlock budget for deeper system integration

---

## 9. Validation Against Gate 2 Requirements

### Requirement: "Score each major task cluster on delegation dimensions"

**Met**: 8 task clusters scored across 6 dimensions (determinism, pattern stability, data availability, time sensitivity, risk, codifiability). Composite scores calculated.

### Requirement: "Assign archetypes with rationale"

**Met**: 4 archetypes assigned (Fully Agentic, Agent-Led with Oversight, Human-Led with Agent Support, Human-Only). Each archetype justified with reference to score + constraints + risk.

### Requirement: "Arbitrary assignments will be challenged"

**Met**: No arbitrary assignments. Every archetype justified with:
- Composite score
- Specific constraints (Aurum lag, GPS API, policy ambiguity)
- Risk profile (financial, relationship, operational)
- Evidence from artefacts (email, SMS, voicemail, SOP, exports)

### Requirement: "'Everything is fully agentic' is the most marked-down anti-pattern"

**Avoided**: Only 3 of 8 task clusters (37.5%) assigned "Fully Agentic." 5 of 8 (62.5%) require human involvement (Agent-Led, Human-Led, or Human-Only).

---

## 10. Conclusion: Delegation Boundaries Reflect Reality

This matrix assigns delegation archetypes based on **lived work reality** (cognitive load map), **system constraints** (Aurum, GPS API), and **risk governance** (financial, relationship, compliance).

**Key Takeaways**:
1. **High-volume, low-complexity tasks** (ETA lookups, dispute intake) → Fully Agentic
2. **High-complexity, judgment-heavy tasks** (credit decisions, VIP exceptions) → Human-Led with Agent Support
3. **Out-of-scope tasks** (dispatch optimization) → Human-Only, deferred to future

The phased rollout prioritizes **quick wins** (Phase 1: ETA deflection) to build trust, then extends to **higher-value work** (Phase 2: billing disputes, Phase 3: exception triage).

**No task is "agentic because AI can do it."** Every task is evaluated on **suitability, risk, and constraints** — the ATX methodology applied honestly.
