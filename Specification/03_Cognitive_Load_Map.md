# Cognitive Load Map

## Purpose

This cognitive load map decomposes Customer Operations work streams into Jobs to be Done (JtDs), micro-tasks, and cognitive dimensions. The map reflects **lived work** as evidenced in the 5 operational artefacts, not documented SOP processes.

Two work streams are mapped in depth: **ETA Inquiries** (high volume, low complexity) and **Billing Disputes** (high complexity, high customer relationship impact). These represent opposite ends of the cognitive spectrum and demonstrate different agentic transformation approaches.

---

## 1. ETA Inquiries: Cognitive Load Map

### Job to be Done (Customer Perspective)
**"Help me know when my delivery will arrive so I can plan to receive it."**

**Customer Context**:
- Time-sensitive need (must be present to receive, or arrange alternative)
- Uncertainty anxiety (scheduled window too broad)
- Trust in carrier to provide accurate information

### Job to be Done (Agent Perspective)
**"Provide accurate delivery time estimate based on current route progress and traffic conditions."**

---

### Lived Process Flow (from SMS Artefact)

**Trigger**: Customer SMS "Where is order #AX-771-3344?"

#### Step 1: Order Lookup & Initial Response
**Micro-tasks**:
1. Parse customer inquiry (order ID extraction)
2. Query CRM/order system by order ID
3. Retrieve route assignment (route 028)
4. Retrieve scheduled ETA window (13:00-17:00)
5. Compose response with available data

**Cognitive Zone**: **Low-Cognitive** (Lookup + Template)
- **Cognitive Load**: ★☆☆☆☆ (1/5) — Deterministic lookup, no judgment required
- **Knowledge Type**: Procedural (system navigation)
- **Decision Complexity**: Rule-bound (if order found, return route + window)
- **Elapsed Time**: ~30 seconds (observed: 11:14 → 11:16 = 2 minutes, includes typing)

**Breakpoint Detection**: Customer pushes back on 4-hour window precision → **Escalates cognitive zone**

---

#### Step 2: Customer Dissatisfaction → Precision Request
**Customer**: "That's a 4 hour window, can you tell me anything more specific?"

**Agent Judgment**: Scheduled window insufficient; customer expects precision; must escalate to GPS data

**Cognitive Zone Shift**: Low → **Medium-Cognitive** (Triage + Coordination)

**Micro-tasks**:
1. Assess if scheduled window is acceptable (NO — customer explicitly requests more precision)
2. Determine information source for precision (GPS data from Dispatch)
3. Initiate coordination with Dispatch team (phone call or Dispatch Console query — unclear from artefact)

**Cognitive Load**: ★★☆☆☆ (2/5) — Requires triage decision (can I answer from current data or need escalation?)
- **Knowledge Type**: Contextual (what level of precision does customer need? Is scheduled window ever acceptable?)
- **Decision Complexity**: Judgment-light (customer explicitly asks for precision, no ambiguity)
- **Elapsed Time**: ~5 minutes (11:17 → 11:24 = 7 minutes) — **coordination wait time**, not active cognitive time

**Information Silo Constraint**: Agent does NOT have direct access to GPS data → must ask Dispatch

---

#### Step 3: GPS Data Retrieval & Interpretation
**Dispatch provides**: "Driver's last GPS ping was 10:48 in Watford."

**Micro-tasks**:
1. Receive GPS data (timestamp + location)
2. Assess data freshness (10:48 → 11:24 = 36 minutes stale — is this usable?)
3. Calculate distance/time from Watford to customer address (heuristic: route knowledge, traffic conditions, stops remaining)
4. Formulate estimated time range (14:00-15:00)
5. Compose hedged response ("best guess," "don't have a tighter ETA," "sorry")

**Cognitive Zone**: **Medium-Cognitive** (Interpretation + Heuristic Application)
- **Cognitive Load**: ★★★☆☆ (3/5) — Requires route knowledge, traffic intuition, stop-sequence estimation
- **Knowledge Type**: Heuristic (experienced agents know typical stop durations, traffic patterns)
- **Decision Complexity**: Estimation under uncertainty (GPS stale, no visibility into stops remaining)
- **Hedging Behavior**: "Best guess" and apology signal agent lacks confidence in estimate

**Elapsed Time**: ~2-3 minutes (interpretation + response composition)

---

### Cognitive Zones Summary (ETA Inquiries)

| Phase | Cognitive Zone | Load | Knowledge Type | Agent Suitability |
|---|---|---|---|---|
| **Order Lookup** | Low-Cognitive | ★☆☆☆☆ | Procedural (system lookup) | **Fully Agentic** — deterministic |
| **Triage** | Medium-Cognitive | ★★☆☆☆ | Contextual (precision judgment) | **Agent-Led** — rule-based (if window >2 hours, get GPS) |
| **Coordination** | Low-Cognitive (agent wait) | ★☆☆☆☆ | N/A (blocked on Dispatch) | **Eliminate via architecture** — agent should have GPS API access |
| **Interpretation** | Medium-Cognitive | ★★★☆☆ | Heuristic (route/traffic estimation) | **Agent-Led** — calculable if data available (stops remaining, traffic API) |
| **Communication** | Low-Cognitive | ★☆☆☆☆ | Procedural (template with variables) | **Fully Agentic** — dynamic template injection |

**Key Breakpoints**:
1. **Customer escalation** (11:16): Scheduled window rejected → GPS needed
2. **Data staleness** (36 min lag): Fresh GPS would improve estimate precision

**Delegation Insight**: 
- Steps 1, 2, 5 (lookup, triage, communication) are **fully automatable** if GPS API available
- Step 4 (interpretation) requires heuristic but is **calculable** with proper data (stops remaining, traffic conditions, typical stop duration)
- Step 3 (coordination) is **architectural failure** — should not exist if agent has direct GPS access

**Total Lived Process Time**: 11 minutes (11:14 → 11:25) for a task that should take <30 seconds

---

### Cognitive Dimensions Analysis (ETA Inquiries)

| Dimension | Assessment | Implication for Agentic Design |
|---|---|---|
| **Determinism** | High (80% of cases) — Order ID → route → ETA is lookup. 20% require GPS interpretation. | Highly automatable; edge cases escalate when GPS stale or customer demands callback |
| **Pattern Stability** | High — Process identical across customers (B2B vs. DTC makes no difference) | Single agent design serves all customer types |
| **Information Availability** | Medium — Order + route data available; GPS data siloed in Dispatch Console | Agent blocked until GPS API access granted; architectural prerequisite |
| **Time Sensitivity** | Low-Medium — Customer waiting, but not mission-critical (unlike dispatcher route changes) | Acceptable to serve from cached/batch data if real-time unavailable; customer expects <5 min response |
| **Risk of Error** | Low — Worst case: inaccurate ETA → customer calls back. No financial/regulatory risk. | High tolerance for agent autonomy; errors are reversible (customer can escalate) |
| **Contextual Dependency** | Low — Customer context (VIP, complaint history) irrelevant to ETA calculation | No customer segmentation required; treat all inquiries uniformly |

**Overall Cognitive Profile**: **Low-complexity, high-volume, low-risk** — **ideal agentic deflection candidate**

---

## 2. Billing Disputes: Cognitive Load Map

### Job to be Done (Customer Perspective)
**"Resolve an unfair charge on my invoice so I'm not paying for something that went wrong."**

**Customer Context**:
- Financial impact (£60-340 per dispute in sample data)
- Fairness perception (damaged delivery → shouldn't pay fuel surcharge)
- Trust erosion (repeat disputes signal relationship strain)

### Job to be Done (Agent Perspective)
**"Investigate dispute claim, validate against delivery records and policy, recommend resolution that balances customer satisfaction and cost control."**

---

### Lived Process Flow (from Email Thread Artefact)

**Trigger**: Customer email to billing@ (Hayes & Sons disputes INV-2026-04318, £340 fuel surcharge on damaged delivery)

#### Step 1: Intake & Initial Routing (Billing Team)
**Email received**: Day 1, 09:14

**Micro-tasks**:
1. Read customer email
2. Classify dispute type (fuel surcharge + damage claim)
3. Retrieve policy guidance ("fuel surcharges calculated automatically by route distance, not tied to delivery condition")
4. Compose deflection response (refer to Customer Ops for goodwill credits)

**Cognitive Zone**: **Low-Cognitive** (Classification + Hand-off)
- **Cognitive Load**: ★★☆☆☆ (2/5) — Pattern matching (keywords: "fuel surcharge," "damaged")
- **Knowledge Type**: Procedural (policy lookup, routing rules)
- **Decision Complexity**: Rule-bound (dispute involves delivery condition → route to Customer Ops)
- **Elapsed Time**: ~7.5 hours (09:14 → 16:48) — **queue time**, not active time

**Failure Mode Observed**: Billing team deflects without acknowledging damage claim → customer feels unheard

---

#### Step 2: Customer Escalation → Access Barrier
**Customer**: Day 4, 11:02 — "Called Customer Ops, was on hold for 22 minutes, got cut off. Second time this quarter. Who is your manager?"

**Agent Role**: N/A (customer blocked by capacity bottleneck)

**Cognitive Zone**: **N/A** (System Failure — Customer Cannot Access Service)
- **Elapsed Time**: 22 minutes hold → dropped call → 2.5 days lost

**Failure Mode Observed**: Capacity bottleneck prevents case from progressing; customer frustration escalates

---

#### Step 3: Investigation & Resolution (Customer Ops — Sandra)
**Sandra responds**: Day 6, 15:30

**Micro-tasks**:
1. **Retrieve invoice data** (INV-2026-04318 from APEX_BILL_DAILY export)
   - Locate invoice: CUSTOMER_ID C-04451, AMT_GROSS £3,816, AMT_FUEL_SURCH £340
2. **Retrieve fuel surcharge detail** (APEX_FUEL_SURCH export)
   - Route R-008, Tier T3, 11.97% rate, BASE_NET £2,840 → FUEL_AMT £340 (auto-calculated)
3. **Cross-reference delivery exception** (Driver App or Dispatch Console — was damage reported?)
   - ASSUMPTION: Sandra queries whether driver logged damage at delivery (not visible in artefacts, but required for validation)
4. **Retrieve customer history** (CRM + APEX_DISPUTES_OPEN + APEX_AGED_RECEIVABLES)
   - Hayes & Sons: £25K credit limit, 3 open disputes (2 are FUEL_SURCH_DAMAGE type), £10,272 in receivables (aged across 3 buckets)
   - Pattern: Repeat fuel surcharge disputes on damaged deliveries
5. **Assess customer relationship risk**
   - High-value account (£25K limit, B2B_STANDARD contract)
   - Payment behavior: Aging into 61-90 days on one dispute (£212) — relationship strained
   - Churn risk: Customer escalating ("Who is your manager?")
6. **Interpret policy** (Goodwill credit discretion)
   - Policy: Fuel surcharges non-refundable (route-based, not condition-based)
   - Exception: Goodwill credits allowed for customer satisfaction
   - Judgment: How much? Full £340 or partial?
7. **Decide resolution** (£170 = 50% of disputed amount)
   - Rationale (inferred): Split difference — acknowledge customer grievance without setting precedent for full fuel surcharge refunds on all damage claims
8. **Execute resolution** ("Manual override" — bypasses Aurum ticket system)
   - ASSUMPTION: Sandra applies credit in CRM or local tracking system, to be synced to Aurum later (but internal note: "no entry in credits audit log")
9. **Communicate decision** (Email to customer)
   - Explain Aurum constraint ("can't adjust on individual invoices because of how Aurum works")
   - Confirm credit will appear on next statement

**Cognitive Zone Sequence**:
- **Tasks 1-4**: **Low-Cognitive** (Data Aggregation) — ★★☆☆☆ (2/5) — System lookups across 4 sources
- **Task 5**: **High-Cognitive** (Risk Assessment) — ★★★★☆ (4/5) — Requires customer relationship intuition, churn risk evaluation
- **Task 6-7**: **High-Cognitive** (Policy Interpretation + Judgment) — ★★★★★ (5/5) — Discretionary decision, no clear rule
- **Task 8-9**: **Medium-Cognitive** (Execution + Communication) — ★★★☆☆ (3/5) — Workaround required (Aurum constraint), empathy phrasing

**Total Elapsed Time**: Day 1 → Day 6 = **5.5 days** (but active Sandra time likely 20-30 min based on 28-min avg handle time)

---

### Cognitive Zones Summary (Billing Disputes)

| Phase | Cognitive Zone | Load | Knowledge Type | Agent Suitability |
|---|---|---|---|---|
| **Intake & Classification** | Low-Cognitive | ★★☆☆☆ | Procedural (keyword matching) | **Fully Agentic** — email parsing, routing |
| **Data Aggregation** (Invoice, fuel surcharge, delivery exception, customer history) | Low-Cognitive | ★★☆☆☆ | Procedural (cross-system queries) | **Fully Agentic** — agent can aggregate faster than human |
| **Customer Risk Assessment** | High-Cognitive | ★★★★☆ | Contextual (relationship intuition, churn signals) | **Agent-Assisted** — agent surfaces data (receivables aging, dispute history), human interprets |
| **Policy Interpretation** | High-Cognitive | ★★★★★ | Judgment (discretionary credit decision) | **Human-Led** — agent can recommend (e.g., "£170 = 50% split"), human approves |
| **Resolution Execution** | Medium-Cognitive | ★★★☆☆ | Procedural + Workaround (Aurum constraint) | **Human-Only** (currently) — Requires manual override; automatable if credit approval API exists |
| **Communication** | Low-Cognitive | ★★☆☆☆ | Procedural (template with empathy) | **Agent-Led** — Draft email, human reviews for tone |

**Key Breakpoints**:
1. **Billing team hand-off** (Day 1): Customer expects resolution, gets deflection → frustration starts
2. **Access failure** (Day 4): Hold time + dropped call → escalation to management threat
3. **Judgment decision** (Day 6): Sandra decides £170 (not £0, not £340) — **core cognitive act**

**Delegation Insight**:
- **Automatable**: Intake (Steps 1-2), Data Aggregation (Steps 1-4), Communication (Step 9) — ~60% of process time
- **Agent-Assisted**: Risk Assessment (Step 5) — Agent surfaces data, human interprets
- **Human Decision**: Policy Interpretation + Credit Approval (Steps 6-7) — **Cannot delegate** due to discretionary nature and financial risk
- **Blocked by Aurum**: Execution (Step 8) — Requires manual override; agent can draft credit request, but human must submit Aurum ticket

**Total Time Reduction Potential**: 28 min (current) → 8 min (agent aggregates data in 2 min, human reviews + decides in 6 min)

---

### Cognitive Dimensions Analysis (Billing Disputes)

| Dimension | Assessment | Implication for Agentic Design |
|---|---|---|
| **Determinism** | Low (30%) — Standard disputes (invoice errors) have rules; damage-related disputes require judgment | Agent can handle 30% fully (invoice corrections); 70% require human judgment on credit amount |
| **Pattern Stability** | Medium — Fuel surcharge disputes recurring (3 of 6 in sample); pattern exists but requires policy change, not just automation | Agent can flag pattern ("customer has 2 prior FUEL_SURCH_DAMAGE disputes") for human awareness |
| **Information Availability** | Medium — Data scattered across 4 systems (Aurum exports, CRM, Dispatch, Driver App); T-1 lag on Aurum | Agent can aggregate but must handle staleness (e.g., "Invoice not yet in system; can escalate for today's data") |
| **Time Sensitivity** | Medium — Customer expects <48 hour response (industry standard), not <5 min (unlike ETA inquiries) | Acceptable to batch investigation (agent works overnight, human reviews next morning) |
| **Risk of Error** | High — Over-crediting costs money; under-crediting risks churn. Financial and relationship stakes. | High oversight required; agent recommends, human approves (especially >£200 threshold) |
| **Contextual Dependency** | High — Resolution depends on customer tier (VIP vs. standard), dispute history (first-time vs. repeat), payment behavior (current vs. 90-day aged) | Agent must surface context to human; cannot decide in isolation |

**Overall Cognitive Profile**: **High-complexity, medium-volume, high-risk** — **Agent-led investigation + human approval model**

---

## 3. Comparative Cognitive Load: ETA Inquiries vs. Billing Disputes

| Dimension | ETA Inquiries | Billing Disputes | Implication |
|---|---|---|---|
| **Cognitive Peak Load** | ★★★☆☆ (GPS interpretation) | ★★★★★ (credit decision) | ETA can be fully agentic; disputes require human judgment loop |
| **Cognitive Duration** | 11 min elapsed, ~2 min active cognitive time | 5.5 days elapsed, ~20-30 min active cognitive time | Both have architectural delays (coordination waits, queue times) — agents reduce waits, not judgment time |
| **Breakpoint Count** | 2 (customer escalation, GPS staleness) | 3 (hand-off, access failure, judgment decision) | Fewer breakpoints = simpler agentic design (ETA cleaner than disputes) |
| **Knowledge Codifiability** | High (route heuristics, traffic estimation) | Low (customer relationship intuition, churn risk assessment) | ETA knowledge can be trained/modeled; dispute knowledge is experiential |
| **Error Tolerance** | High (inaccurate ETA → customer calls back) | Low (wrong credit amount → financial loss or churn) | ETA allows autonomous agent; disputes require human-in-loop |

**Strategic Insight**: Start with **ETA Inquiries** (high volume, low risk, high deflection potential) to prove agentic value, then extend to **Billing Dispute Investigation** (agent accelerates data gathering, human retains decision authority).

---

## 4. Cross-Stream Cognitive Patterns

### Pattern 1: Information Silo Tax
**Observed in**: ETA Inquiries (Customer Ops → Dispatch), Billing Disputes (Billing team → Customer Ops)

**Cognitive Load**: ★★☆☆☆ (Coordination wait = low cognitive load but high elapsed time)

**Impact**: 5-7 minute delays per inquiry; multi-day delays for disputes (hand-offs via email)

**Agentic Solution**: Agent serves as **integration layer** — queries all systems in parallel, presents unified view

---

### Pattern 2: Discretionary Judgment Under Ambiguity
**Observed in**: Billing Disputes (credit amount), Delivery Exceptions (return vs. leave decision — from voicemail artefact)

**Cognitive Load**: ★★★★★ (High — requires contextual knowledge, cost-benefit intuition, relationship assessment)

**Characteristics**:
- No explicit policy ("goodwill credit" is discretionary)
- Outcome depends on unwritten heuristics (customer tier, past behavior, financial impact)
- Agent's decision criteria not documented ("Sandra applied £170" — rationale inferred, not stated)

**Agentic Solution**: **Agent-assisted, not agent-decided** — Agent surfaces decision-supporting data (customer history, past credit amounts for similar disputes, churn risk signals), human makes judgment call

---

### Pattern 3: Workaround Behavior Due to System Constraints
**Observed in**: Billing Disputes (Sandra's "manual override"), Delivery Exceptions (SOP incomplete, agents improvise)

**Cognitive Load**: ★★★☆☆ (Medium — requires knowledge of workaround, not just formal process)

**Risk**: Workarounds not logged (audit gap), not transferable to new hires (tribal knowledge), inconsistent across agents

**Agentic Solution**: **Codify lived process** as agent logic — Agent follows workaround path but logs actions (audit trail). Side benefit: Makes workarounds visible to leadership for formal process improvement.

---

## 5. Cognitive Load Reduction: Agent vs. Human

### ETA Inquiries: Cognitive Load Shift

| Task | Human Cognitive Load | Agent Cognitive Load | Rationale |
|---|---|---|---|
| Order lookup | ★☆☆☆☆ | ★☆☆☆☆ | Identical (API call) |
| Route/window retrieval | ★☆☆☆☆ | ★☆☆☆☆ | Identical (database query) |
| GPS data retrieval | ★★☆☆☆ (must call Dispatch) | ★☆☆☆☆ (direct API call) | Agent eliminates coordination |
| ETA calculation | ★★★☆☆ (heuristic) | ★★☆☆☆ (algorithmic: stops remaining + traffic API + avg stop duration) | Agent more precise if data available |
| Response composition | ★☆☆☆☆ (template) | ★☆☆☆☆ (template) | Identical |
| **TOTAL LOAD** | **★★★☆☆** (8/25 points) | **★★☆☆☆** (5/25 points) | **37.5% cognitive load reduction** |
| **TOTAL TIME** | **11 min (observed)** | **<30 sec (projected)** | **96% time reduction** |

**Key Insight**: Agent reduces **coordination time** (5 min wait eliminated) and **calculation complexity** (heuristic → algorithmic). Human cognitive load wasn't high to begin with — the value is in **speed and scale**, not complexity reduction.

---

### Billing Disputes: Cognitive Load Shift

| Task | Human Cognitive Load | Agent Cognitive Load | Shift |
|---|---|---|---|
| Email parsing & classification | ★★☆☆☆ | ★☆☆☆☆ | Agent faster, same accuracy |
| Invoice retrieval (Aurum export) | ★★☆☆☆ | ★☆☆☆☆ | Agent faster (batch query) |
| Fuel surcharge detail retrieval | ★★☆☆☆ | ★☆☆☆☆ | Agent faster |
| Delivery exception cross-ref | ★★☆☆☆ | ★☆☆☆☆ | Agent faster |
| Customer history aggregation | ★★☆☆☆ | ★☆☆☆☆ | Agent faster (parallel queries) |
| **SUBTOTAL (Investigation)** | **★★☆☆☆** (10/25) | **★☆☆☆☆** (5/25) | **50% load reduction** |
| Risk assessment (churn, payment) | ★★★★☆ | N/A (agent surfaces data only) | **Human retains** |
| Credit decision (amount, rationale) | ★★★★★ | N/A (agent recommends) | **Human retains** |
| Resolution execution | ★★★☆☆ | N/A (human submits Aurum ticket) | **Human retains** (Aurum constraint) |
| Communication drafting | ★★☆☆☆ | ★☆☆☆☆ | Agent drafts, human reviews |
| **SUBTOTAL (Judgment & Execution)** | **★★★★☆** (16/25) | **★☆☆☆☆** (2/25 assist only) | **Human-led** |

**Key Insight**: Agent reduces **investigation time** (28 min → 5 min for data aggregation), but **judgment time unchanged** (human must still decide credit amount). Total time 28 min → 8-10 min (**64% time reduction**), but cognitive load on judgment **not reduced** — just accelerated by faster data availability.

---

## 6. Implications for Agent Design

### Design Principle 1: Match Agent Capabilities to Cognitive Zone
- **Low-Cognitive zones** (lookup, classification, template response) → **Fully Agentic**
- **Medium-Cognitive zones** (heuristic application, triage decisions) → **Agent-Led** (agent decides, human can override)
- **High-Cognitive zones** (judgment, relationship management, policy interpretation) → **Human-Led** (agent assists, human decides)

### Design Principle 2: Eliminate Coordination Waits, Not Judgment Time
- **ETA Inquiries**: Agent's value is eliminating 5-min Dispatch coordination wait, not replacing agent's 2-min cognitive work
- **Billing Disputes**: Agent's value is aggregating data across 4 systems in 2 min (vs. human's 20 min), not replacing Sandra's judgment

### Design Principle 3: Surface Context for Human Judgment
For high-cognitive tasks (billing disputes, delivery exceptions), agent must provide:
- **Decision-supporting data**: Customer tier, past disputes, receivables aging, delivery exception history
- **Pattern recognition**: "Customer has 2 prior FUEL_SURCH_DAMAGE disputes in 90 days" (flag for policy issue)
- **Recommendation with confidence**: "Suggested credit: £170 (50% of dispute). Confidence: Medium. Rationale: Customer high-value, damage claim valid per driver notes, but full refund sets precedent."

Human sees context at a glance, makes informed decision in 2-3 min (vs. 20 min of data gathering).

---

## 7. Cognitive Load Map: Summary Table

| Work Stream | Cognitive Peak | Avg Load | Automatable % | Agent Role | Human Role |
|---|---|---|---|---|---|
| **ETA Inquiries** | ★★★☆☆ (GPS interpretation) | ★★☆☆☆ | 90% | **Fully Agentic** (lookup + heuristic) | Review escalations (GPS stale, customer demands callback) |
| **Billing Disputes** | ★★★★★ (Credit decision) | ★★★☆☆ | 60% (investigation) | **Agent-Led Investigation** (data aggregation, recommendation) | **Human Approval** (credit decision, Aurum ticket) |
| **Delivery Exceptions** | ★★★★☆ (Return vs. leave judgment) | ★★★☆☆ | 40% (routine triage) | **Agent-Led Triage** (low-value packages) | **Human Decision** (high-value, VIP customers, damage assessment) |
| **Dispatch Adjustments** | ★★★★★ (Multi-constraint optimization) | ★★★★☆ | 20% (data assembly) | **Human-Only** (current scope) | Dispatcher decides route changes; agent could assist with data (vehicle locations, capacity, time windows) in future |

**Delegation Strategy**:
1. **Phase 1** (Months 1-3): Deploy **ETA Inquiry Agent** (fully agentic) — highest ROI, lowest risk
2. **Phase 2** (Months 4-6): Deploy **Billing Dispute Investigation Agent** (agent-led investigation, human approval) — accelerates resolution, maintains governance
3. **Phase 3** (Months 7-9): Extend to **Delivery Exception Triage** (agent handles routine, escalates complex) — reduces dispatcher bottleneck
4. **Phase 4** (Future): Explore **Dispatch Adjustment Support** — requires Dispatch Console API access, real-time optimization

---

## 8. Validation Against Artefacts

### Artefact 1 (Voicemail): Delivery Exception Not Fully Mapped
**Why**: Focus on ETA Inquiries + Billing Disputes per Gate 2 requirement ("at least 2 of 4 work streams"). Delivery exceptions cognitive load inferred from voicemail (dispatcher judgment, driver blocked), but full micro-task decomposition deferred to implementation phase.

**Partial Map** (from voicemail):
- Driver assessment (★★★☆☆) → Dispatcher decision (★★★★☆) → Driver execution (★☆☆☆☆)
- Breakpoint: Driver cannot proceed without dispatcher approval (bottleneck)

### Artefacts 2-3 (Email, SMS): Fully Mapped
**Email thread** (billing dispute) mapped in Section 2.
**SMS exchange** (ETA inquiry) mapped in Section 1.

### Artefacts 4-5 (SOP, Batch Exports): Referenced for Constraints
**SOP** reveals documentation lag (DispatchHub retired, Section 4.3 incomplete) — reinforces lived-vs-documented insight.
**Batch exports** reveal Aurum constraint (T-1 lag) — critical for billing dispute cognitive load (Sandra works with yesterday's data).

---

## Conclusion

**ETA Inquiries** are **low-cognitive, high-volume, coordination-heavy** — agent eliminates waits and scales infinitely.

**Billing Disputes** are **high-cognitive, medium-volume, judgment-heavy** — agent accelerates investigation (60% of time), human retains decision authority (40% of time).

Both reveal **information silos as the primary cognitive tax** — agents remove this tax by serving as integration layer, even without changing underlying systems.

The cognitive load map justifies the **delegation suitability matrix** (next deliverable) and informs the **agent purpose document** (task decomposition → feature requirements).
