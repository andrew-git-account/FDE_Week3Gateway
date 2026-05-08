# Domain Orientation: Apex Distribution Ltd Customer Operations

## Executive Summary

Apex Distribution Ltd is a mid-sized regional carrier facing cognitive load concentration in Customer Operations. This document provides domain orientation for assessing agentic transformation opportunities using ATX methodology. Analysis based on scenario brief, 5 operational artefacts, and batch export data from legacy billing system.

**Key Finding**: Customer Operations absorbs ~730 daily cases across 4 work streams with 35 staff. High-volume/low-complexity work (ETA inquiries) coexists with low-volume/high-complexity work (billing disputes) in an environment where documented SOPs diverge significantly from lived processes.

---

## 1. Industry Context: UK Regional Parcel Distribution

### Business Model
- **Segment**: Regional carrier (Midlands, South, East England)
- **Scale**: Mid-market (800 employees, 180 vehicles, ~3,500 deliveries/day)
- **Mix**: B2B (majority) and DTC parcels
- **Economics**: Thin margins (~3-8% net), scale-sensitive, high fixed costs

### Industry Characteristics
- **Peak sensitivity**: Volume spikes (Q4, promotional periods) stress capacity
- **Customer expectations**: Real-time tracking, tight delivery windows, instant ETA updates
- **Competitive pressure**: Large nationals (DPD, Hermes/Evri) and regionals compete on service quality, not just price
- **Regulatory**: Consumer Rights Act 2015, GDPR, carrier liability frameworks

### Typical Failure Modes in Distribution
1. **Last-mile volatility**: Traffic, weather, recipient unavailability, address errors
2. **Exception avalanche**: One delivery failure cascades (missed time window → re-delivery → dispute)
3. **Information lag**: GPS/tracking data not synchronized across systems → customer inquiries
4. **Billing complexity**: Fuel surcharges, dimensional weight, accessorial fees → disputes
5. **Dispatcher bottleneck**: Route optimization + exception handling + driver coordination overwhelms capacity during peaks

---

## 2. Apex Distribution: Business Profile

### Company Overview
- **Founded**: Not specified; mature operations (legacy billing system since 2008)
- **Headquarters**: Birmingham, UK
- **Coverage**: Midlands, South, East England
- **Fleet**: 180 vehicles (mix of vans, trucks for B2B pallets)
- **Daily volume**: ~3,500 deliveries
- **Workforce**: 800 total (drivers, warehouse, dispatch, customer ops, admin)

### Customer Base Analysis (from APEX_CUSTOMER_MASTER)
Sample data shows 6 customers, all B2B:
- **Contract types**: B2B_STANDARD (smaller accounts, RC-2024A) and B2B_VOLUME (larger accounts, RC-2023/2024B)
- **Credit limits**: £5K to £60K (Hayes & Sons at £25K, Severn Wholesale at £60K)
- **Account managers**: Concentrated (U-0089 manages 4 of 6 accounts in sample)
- **Status**: All ACTIVE (no churned accounts visible, but sample is survivorship-biased)

**Key observation**: Customer concentration risk. Hayes & Sons appears 3 times in disputes data and has £10,272 in open receivables (aged across 3 buckets). Relationship strain visible in email thread artefact.

### Financial Health Indicators (from APEX_AGED_RECEIVABLES)
- **Total open receivables (sample)**: £23,836 across 6 customers
- **Ageing profile**: 
  - 0-30 days: £21,817 (92% — healthy)
  - 31-60 days: £1,765 (7%)
  - 61-90 days: £255 (1%)
  - Over 90 days: £0
- **Dispute correlation**: C-04451 (Hayes & Sons) has aged 61-90 balance of £212, matches dispute D-2026-00318 from Feb 28

**Implication**: Collections are generally healthy, but disputes directly impact ageing. Friction in dispute resolution extends payment cycles.

---

## 3. Customer Operations: The Core Focus

### Organizational Structure
- **Function**: Customer Operations (35 people)
- **Reporting**: COO Sarah Whitmore (promoted internally 18 months ago, formerly Dispatch manager)
- **Mandate**: Handle post-dispatch customer touchpoints, exceptions, and billing issues

### The 4 Work Streams

| Work Stream | Daily Volume | Avg Handle Time | Total Labor Hours/Day | Complexity Profile |
|---|---|---|---|---|
| **Delivery Exceptions** | ~180 | 12 min | 36 hours | Medium-High: Dispatcher discretion, judgment calls, driver coordination |
| **ETA Inquiries** | ~400 | 4 min | 27 hours | Low: Mostly lookup, edge cases require driver contact |
| **Dispatch Adjustments** | ~90 | 18 min | 27 hours | High: Time-sensitive, route re-planning, driver swap logistics |
| **Billing Disputes** | ~60 | 28 min | 28 hours | High: Cross-system reconciliation, policy interpretation, legacy system constraints |
| **TOTAL** | **730** | **~10 min avg** | **118 hours/day** | |

**Capacity Analysis**:
- 35 FTE × 7.5 hours/day = 262.5 available hours/day
- Current load: 118 hours/day (45% of capacity)
- **Interpretation**: Significant headroom OR significant unaccounted work (meetings, training, rework, escalations, email/phone not tracked as "cases")

**ASSUMPTION**: Handle time data reflects case-close time, not total elapsed time including waits, coordination, and rework. Confidence: High. Test via: Ask Sarah if 12-minute exception handle time includes driver callback wait time.

---

## 4. System Landscape: Modern + Legacy Hybrid

### 4.1 Modern CRM (Salesforce-based)
- **Purpose**: Customer records, case history, communications
- **Interface**: REST APIs available
- **Data quality**: Assumed good for customer master, contact logs
- **Integration**: Likely integrates with Driver App and Dispatch Console via middleware

**ASSUMPTION**: CRM is system of record for customer interactions and case status. Confidence: High. Test via: Confirm with Sarah which system tracks case lifecycle (CRM vs. Dispatch Console).

### 4.2 Driver App (In-House iOS/Android)
- **Purpose**: GPS tracking, route navigation, scan-on-delivery, driver-to-dispatch messaging
- **Real-time data**: GPS pings, delivery confirmations
- **Interface**: Likely REST API for back-office systems to query driver status
- **Constraints**: Mobile network dependency (rural coverage gaps likely)

**Evidence from SMS artefact**: Driver's "last GPS ping was 10:48 in Watford" suggests GPS data is time-stamped and query-able, but not continuously streamed (or Customer Ops agent had to ask Dispatch for it, indicating information silo).

**ASSUMPTION**: Driver App pushes GPS updates at intervals (not real-time continuous), and Customer Ops does not have direct access to Driver App backend — must query Dispatch Console or ask dispatchers. Confidence: Medium. Test via: Ask Sarah if Customer Ops agents can query driver GPS directly or must ask Dispatch.

### 4.3 Dispatch Console (Java Desktop via Citrix)
- **Purpose**: Route planning, driver assignment, exception triage
- **Interface**: "Limited API surface" (per brief)
- **Architecture**: Desktop app deployed via Citrix — implies thick client, legacy Java stack, likely on-prem
- **Constraints**: Not web-accessible, limited automation potential

**Evidence from voicemail artefact**: Mark Petrov (driver) calls dispatch line directly, leaving voicemail. Sandra (dispatcher, referenced in email) has a phone line. This suggests voice/phone is primary driver-to-dispatch channel, not just the Driver App messaging.

**Evidence from SOP artefact**: SOP references "DispatchHub tablet" (retired Oct 2024), replaced by Driver App. SOP not updated. This reveals **documentation lag** — a key lived-vs-documented gap signal.

**ASSUMPTION**: Dispatch Console is the authoritative system for route status and driver assignment, but Customer Ops cannot modify routes directly — must request Dispatch team action. Confidence: High. Test via: Confirm with Sarah if Customer Ops has read-only or read-write access to Dispatch Console.

### 4.4 Aurum Billing (Legacy On-Prem Oracle, Since 2008)
**This is the critical constraint for agentic design.**

#### Architecture
- **Platform**: On-prem Oracle database
- **Age**: 18 years old (2008)
- **Interface**: **Batch-file exports only** — no real-time API, no webhooks
- **Export schedule**: Daily 02:00–04:00 GMT to CSV files
- **Modification process**: Manual ticket to Aurum support team, 48-hour turnaround

#### Data Export Catalogue

| File | Cadence | Lag | Schema |
|---|---|---|---|
| `APEX_BILL_DAILY_YYYYMMDD.csv` | Daily (T-1) | 1 day | Invoice header: INVOICE_NO, CUSTOMER_ID, CUSTOMER_NAME, INVOICE_DT, AMT_NET, AMT_FUEL_SURCH, AMT_VAT, AMT_GROSS, ROUTE_CODE, DEPOT |
| `APEX_FUEL_SURCH_YYYYMMDD.csv` | Daily (T-1) | 1 day | Surcharge line items: INVOICE_NO, ROUTE_CODE, FUEL_RATE_TIER, BASE_NET, FUEL_PCT, FUEL_AMT, CALC_TIMESTAMP, CALC_USER |
| `APEX_CREDITS_YYYYMMDD.csv` | Daily (T-1) | 1 day | Manual credits: CREDIT_ID, INVOICE_NO, CUSTOMER_ID, CREDIT_AMT, REASON_CODE, APPROVER_ID, AUDIT_REF, APPLIED_DT |
| `APEX_RECON_YYYYMMDD.csv` | Daily (T-2) | **2 days** | Reconciliation: RECON_ID, INVOICE_NO, EXPECTED_AMT, RECEIVED_AMT, VAR, AGEING_DAYS, FLAG |
| `APEX_DISPUTES_OPEN_YYYYMMDD.csv` | Daily (T-1) | 1 day | Disputes snapshot: DISPUTE_ID, INVOICE_NO, CUSTOMER_ID, OPEN_DT, DISPUTE_TYPE, DISPUTE_AMT, ASSIGNED_TO, STATUS, LAST_UPDT |
| `APEX_AGED_RECEIVABLES_YYYYMMDD.csv` | Weekly (Friday) | Up to 7 days | Ageing buckets: CUSTOMER_ID, CUSTOMER_NAME, AGE_0_30, AGE_31_60, AGE_61_90, AGE_OVER_90, TOTAL_OPEN |
| `APEX_CUSTOMER_MASTER_YYYYMMDD.csv` | Monthly (1st) | Up to 31 days | Customer master: CUSTOMER_ID, CUSTOMER_NAME, ACCT_OPEN_DT, CONTRACT_TYPE, RATE_CARD, CR_LIMIT, ACCT_MGR, STATUS |

#### Operational Constraints
1. **No real-time queries**: Cannot validate invoice amounts, fuel surcharge calculations, or credit status during customer call
2. **No write-back**: Cannot apply credits, adjust invoices, or flag disputes directly in Aurum
3. **Manual ticket workflow**: "Modifications to invoices require a manual ticket to the Aurum support team (typical turnaround 48 hours)"
4. **Schema volatility**: "Schema changes happen ~quarterly without prior notice" — breaks downstream integrations
5. **Reconciliation lag**: T-2 lag means payment reconciliation data is 48 hours stale (e.g., customer may have paid yesterday, but recon file won't show until tomorrow)

#### Fuel Surcharge Calculation (from APEX_FUEL_SURCH)
- **Tiered by route**: T1 (8.09%), T2 (8.15-10.04%), T3 (9.37-12.00%)
- **Applied to base net**: Percentage varies by route and date (likely linked to diesel price index)
- **Automatic calculation**: CALC_USER = SYS_BATCH, CALC_TIMESTAMP during nightly batch window
- **Not editable**: Per email artefact, "fuel surcharges are calculated automatically by route distance and aren't tied to delivery condition"

**Key insight from email artefact**: Customer dispute (Hayes & Sons) challenged £340 fuel surcharge on damaged pallet. Billing team responded that surcharge is route-based, not condition-based, and directed customer to Customer Ops for goodwill credit. Sandra (Customer Ops agent) applied £170 goodwill credit via "manual override" — **but no entry in credits audit log** per internal note. This reveals:
1. **Workaround behavior**: Sandra bypassed standard credit approval process
2. **Audit gap**: Manual override not logged in Aurum APEX_CREDITS export (or logged with lag)
3. **Policy ambiguity**: "Goodwill credit" is discretionary, not rule-bound

**ASSUMPTION**: Customer Ops agents have local authority to apply credits up to a threshold (likely £200-500) without Aurum ticket, but these credits may not sync to Aurum in real-time. Confidence: Medium. Test via: Ask Sarah what the goodwill credit approval threshold is and how credits are tracked.

---

## 5. Process Flows: Lived vs. Documented

### 5.1 Delivery Exception Handling

#### Documented Process (from SOP artefact, incomplete)
1. Driver notes refusal reason on DispatchHub tablet (obsolete — replaced by Driver App)
2. Confirm with DispatchHub whether to return-to-depot, hold, or re-attempt
3. If high-value (>£500), escalate to Duty Manager via dispatch console

**Gaps in SOP**:
- Section 4.3 "Damaged consignments" is incomplete: "TBD pending review of insurance protocol"
- SOP references retired system (DispatchHub)
- No guidance on who "Duty Manager" is or escalation criteria beyond £500 threshold

#### Lived Process (from voicemail artefact)
**Case**: Mark Petrov, route 042, at Cobham drop (Stein-Allen account, large B2B customer)

1. Driver encounters refusal: Pallet leaning, recipient claims damage, warehouse worker (not site manager) refuses to sign
2. Driver's judgment: "Looks fine to me, it's just been on the lorry" — **driver-dispatcher disagreement on damage assessment**
3. Driver tries to contact Sandra (dispatcher) — **line busy** (bottleneck signal)
4. Driver leaves voicemail on dispatch line, parks vehicle, blocks further deliveries ("I've got six more drops on this route")
5. Waits for callback

**Observed gaps**:
- **No self-service resolution**: Driver cannot proceed without dispatcher approval
- **Single point of failure**: Sandra's line busy → full route blockage
- **Judgment ambiguity**: Who decides if pallet is damaged — driver, recipient, dispatcher, or site manager? Recipient is "new warehouse guy" (inexperienced) and "site manager isn't here" (decision-maker absent)
- **Opportunity cost**: 6 deliveries blocked while driver waits

**Cognitive load map (micro-level)**:
1. **Perception/Assessment** (driver): Visual inspection of pallet — is it damaged? (Low-structure judgment)
2. **Authorization/Negotiation** (driver): Attempt to convince recipient — failed
3. **Escalation** (driver → dispatcher): Voicemail, wait
4. **Decision** (dispatcher): Return, leave, or override refusal? (Judgment call: customer relationship, inventory value, re-delivery cost)
5. **Instruction** (dispatcher → driver): Callback with decision
6. **Execution** (driver): Proceed per instruction

**Delegation suitability signals**:
- **Perception/Assessment**: Could agent assess damage from photo? Possibly, but recipient's refusal is a human judgment call, not just visual.
- **Decision**: Route-return has hard costs (~£40-80 based on distance + driver time); customer-relationship risk if large account; inventory risk if pallet is actually damaged. Dispatcher uses contextual knowledge (customer history, driver judgment reliability, account value).
- **Bottleneck**: Sandra's line busy → need for scalable decision support or triage queue

**ASSUMPTION**: Dispatcher discretion is based on unwritten heuristics (customer tier, driver experience, delivery value, re-delivery cost) not captured in SOP. Confidence: High. Test via: Ask Sandra to walk through 3 recent exception cases and articulate decision criteria.

---

### 5.2 ETA Inquiry Handling

#### Lived Process (from SMS artefact)
**Case**: Customer M.K. inquires about order AX-771-3344

1. Customer sends SMS: "Where is order #AX-771-3344?"
2. Agent looks up order, responds: "Out for delivery on route 028. ETA window is 13:00–17:00."
3. Customer pushes back: "That's a 4 hour window, can you tell me anything more specific?"
4. Agent: "One moment, checking with dispatch."
5. **5-minute gap** (11:19 → 11:24)
6. Agent: "Driver's last GPS ping was 10:48 in Watford. Best guess is your drop will be early afternoon, around 14:00–15:00. We don't have a tighter ETA than that — sorry."

**Observed workflow**:
- **First response**: Lookup in CRM (or Dispatch Console?) — order ID → route → scheduled ETA window (4 hours is poor customer experience)
- **Second response**: Agent must contact Dispatch (phone call? Slack? Dispatch Console query?) to get GPS data
- **Information silo**: Customer Ops agent does not have direct access to real-time driver location
- **Data lag**: GPS ping is 36 minutes old (10:48 → 11:24) — not real-time
- **Hedging language**: "Best guess" and "We don't have a tighter ETA" signals uncertainty and lack of system support

**Cognitive load map**:
1. **Lookup** (agent): Order ID → route, scheduled window (Low complexity, system-supported)
2. **Triage** (agent): Can I answer from system data, or do I need Dispatch input? (Judgment: customer expects precision)
3. **Coordination** (agent → Dispatch): Request GPS data (Async wait, 5 minutes)
4. **Interpretation** (agent): GPS ping + route knowledge → estimated time to customer address (Heuristic)
5. **Communication** (agent → customer): Hedged estimate (Soft skill: manage expectations)

**Delegation suitability signals**:
- **Lookup**: Fully automatable — agent should have direct access to GPS data
- **Triage**: Rule-bound — if scheduled window > 2 hours, escalate to GPS query; if < 2 hours, provide scheduled window
- **Interpretation**: Requires route knowledge (stops remaining, traffic, typical stop duration) — could be agent-computable if data available
- **Communication**: Template-able with dynamic data injection

**Volume × Value**:
- **Volume**: 400/day = highest volume stream
- **Handle time**: 4 min avg (but SMS artefact shows 11 min elapsed time for 2-message exchange)
- **Cognitive load**: Low per case, but cumulative (27 hours/day labor)
- **Customer impact**: High — ETA inquiries correlate with customer anxiety; poor ETA precision damages satisfaction

**ASSUMPTION**: 4-minute avg handle time includes only agent active time, not customer wait time or agent wait time for Dispatch callback. Confidence: High. Test via: Ask Sarah if handle time metrics include hold time and coordination waits.

---

### 5.3 Billing Dispute Handling

#### Lived Process (from email thread artefact)
**Case**: Hayes & Sons disputes INV-2026-04318 (£340 fuel surcharge on damaged delivery)

**Timeline**:
- **Day 1, 09:14**: Customer (Pete H.) emails billing@: "£340 fuel surcharge on damaged delivery — pallet unusable, disposed of half the consignment. Please remove surcharge and confirm credit."
- **Day 1, 16:48**: Billing team responds: "Fuel surcharges calculated automatically by route distance, not tied to delivery condition. Contact Customer Ops for goodwill credits."
- **Day 4, 11:02**: Customer escalates: "Called Customer Ops, was on hold for 22 minutes, got cut off. Second time this quarter. Who is your manager?"
- **Day 6, 15:30**: Customer Ops agent (Sandra) responds: "Applied £170 goodwill credit, you'll see it on next statement. Fuel surcharge can't be adjusted on individual invoices because of how Aurum works."
- **Day 9**: Internal note (not visible to customer): "No entry in credits audit log for this £170; Sandra applied it via manual override."

**Observed failure modes**:
1. **Misdirection**: Billing team (first responder) deflects to Customer Ops without acknowledging damage claim
2. **System constraint miscommunication**: "Fuel surcharges calculated automatically" is technically true but unhelpful — customer cares about fairness, not system design
3. **Customer Ops access bottleneck**: 22-minute hold time, call dropped (capacity or phone system issue?)
4. **Repeat issue**: Customer notes "second time this quarter" — pattern of fuel surcharge disputes on damaged deliveries
5. **Partial resolution**: Sandra applies £170 credit (half of £340) — **policy decision not explained to customer**
6. **Audit gap**: Manual override not logged in Aurum APEX_CREDITS export (or logged with lag)

**Cognitive load map**:
1. **Intake & Classification** (Billing team): Email → dispute type (fuel surcharge) → route to Customer Ops (Hand-off)
2. **Customer Outreach** (Customer): Phone call → hold → dropped (Failure)
3. **Case Investigation** (Sandra): 
   - Retrieve invoice data (INV-2026-04318 from Aurum export)
   - Cross-reference with delivery exception (was damage reported by driver?)
   - Assess customer relationship (Hayes & Sons is large account, £25K credit limit, recurring disputes)
   - Determine resolution: Policy says no fuel surcharge adjustment, but customer has valid grievance (damaged goods)
4. **Policy Interpretation** (Sandra): Discretionary goodwill credit (£170 = 50% of disputed amount) — **judgment call**
5. **Resolution Execution** (Sandra): Apply credit via "manual override" (bypasses Aurum ticket system)
6. **Communication** (Sandra → customer): Email with explanation of constraint ("can't adjust on individual invoices")

**Delegation suitability signals**:
- **Intake & Classification**: Automatable — email parsing, keyword matching ("fuel surcharge," "damaged," "credit")
- **Case Investigation**: Requires cross-system data (invoice + delivery exception + customer history) — agent could aggregate if APIs available
- **Policy Interpretation**: **Judgment-bound** — discretionary credit requires:
  - Customer relationship assessment (account value, churn risk, payment history)
  - Damage claim validation (driver report, recipient notes, photo evidence?)
  - Cost-benefit analysis (£170 goodwill vs. customer escalation/churn)
- **Resolution Execution**: Blocked by Aurum constraint — cannot automate without changing Aurum workflow or building parallel credit ledger
- **Communication**: Template-able with empathy phrasing

**Risk profile**:
- **Financial risk**: Goodwill credits accumulate (if not governed, agents may over-credit to resolve disputes quickly)
- **Audit risk**: Manual overrides not logged → compliance gap, potential for fraud
- **Customer relationship risk**: Misdirection and hold time damage trust; Hayes & Sons is visibly frustrated (£10K+ receivables at risk)

**ASSUMPTION**: "Manual override" refers to a local system (CRM or spreadsheet) where Customer Ops tracks credits, which are then manually ticketed to Aurum nightly or weekly. Confidence: Medium. Test via: Ask Sarah how Sandra applied the credit and how it syncs to Aurum.

---

### 5.4 Dispatch Adjustment Process

**No direct artefact provided**, but can infer from scenario brief and industry norms.

#### Typical Lived Process
1. **Trigger**: Mid-route event (new pickup request, vehicle breakdown, traffic delay, driver call-out)
2. **Impact assessment**: Dispatcher evaluates impact on remaining stops (time, capacity, customer commitments)
3. **Re-planning**: Assign pickup to different route, swap drivers, delay low-priority stops
4. **Driver coordination**: Contact affected drivers (via Driver App or phone), issue new instructions
5. **Customer notification**: If delivery window affected, notify customers (Customer Ops or automated?)

**Cognitive load characteristics**:
- **Time-sensitive**: "Tight time pressure" per brief — decisions made in minutes, not hours
- **Multi-constraint optimization**: Route distance, driver availability, vehicle capacity, customer priority, time windows
- **High coordination**: Dispatcher ↔ multiple drivers, Dispatcher ↔ Customer Ops (if customer notifications needed)
- **Judgment-heavy**: No perfect solution — trade-offs between on-time delivery, cost, customer satisfaction

**Delegation suitability signals**:
- **Re-planning**: Partially automatable — route optimization algorithms exist, but require:
  - Real-time vehicle location (Driver App GPS)
  - Real-time traffic data (Google Maps API, Waze)
  - Customer priority rules (SLA, account tier, delivery urgency)
  - Driver capacity data (hours remaining, vehicle capacity)
- **Decision**: Human oversight likely required — edge cases (e.g., VIP customer, high-value shipment) need judgment
- **Coordination**: Automatable if Driver App supports push notifications and two-way messaging

**Volume**: 90/day, 18 min avg = 27 hours/day labor

**ASSUMPTION**: Dispatch adjustments currently rely on dispatcher experience and mental models of route capacity, driver performance, and customer tolerance. Confidence: High. Test via: Ask Sarah how dispatchers decide which route gets a new pickup or how driver swaps are prioritized.

---

## 6. Failure Modes & Pain Points

### 6.1 Systemic Failure Modes

#### Aurum Billing Constraint Cascade
**Trigger**: Billing dispute arises
**Cascade**:
1. Customer contacts Billing team → deflected to Customer Ops (first delay)
2. Customer calls Customer Ops → hold time, potential dropped call (second delay)
3. Customer Ops investigates → must wait for next-day Aurum export if invoice not yet in batch (data lag)
4. Customer Ops applies goodwill credit → manual override, 48-hour Aurum ticket for official adjustment (third delay)
5. Customer waits for next statement to see credit (typically 7-30 days depending on billing cycle)

**Impact**: Hayes & Sons dispute (email artefact) took 6 days for partial resolution, 9+ days without full closure. Customer frustration visible ("Second time this quarter," "Who is your manager?").

**Root cause**: Aurum batch-only architecture creates information asymmetry — Customer Ops cannot query or modify billing data in real-time.

#### Dispatcher Bottleneck
**Trigger**: High exception volume or peak hours
**Symptoms**:
- Sandra's line busy (voicemail artefact)
- Drivers parked waiting for callback (opportunity cost: 6 deliveries blocked)
- ETA inquiry agents waiting for Dispatch GPS data (5-minute delay in SMS artefact)

**Root cause**: Dispatcher expertise concentrated in individuals (Sandra appears in both voicemail and email artefacts); decision-making is synchronous and unscalable.

#### Information Silos
**Evidence**:
- Customer Ops cannot access Driver App GPS directly (must ask Dispatch)
- Billing team cannot see delivery exceptions (deflects to Customer Ops)
- Dispute data in Aurum is point-in-time snapshot (T-1 lag), not transactional log

**Impact**: Multi-step coordination for simple queries; data staleness forces hedging ("best guess" in SMS artefact).

---

### 6.2 Operational Pain Points (Inferred)

#### Customer Ops Capacity vs. Load
- **Visible load**: 730 cases/day × ~10 min avg = 118 hours/day
- **Available capacity**: 35 FTE × 7.5 hours = 262.5 hours/day
- **Apparent headroom**: 55% unused capacity

**Red flags**:
1. Hold times (22 minutes in email artefact) suggest bottleneck, not excess capacity
2. Dropped calls suggest phone system or staffing issue
3. Sandra appears in 3 of 5 artefacts (voicemail, email, disputes export) — high-value employee, likely overloaded

**ASSUMPTION**: 55% "unused capacity" is actually consumed by untracked work (email triage, meetings, training, rework, escalations, phone waits). Confidence: High. Test via: Ask Sarah what percentage of Customer Ops time is spent on tracked cases vs. other work.

#### Repeat Disputes
Hayes & Sons has 3 open disputes in APEX_DISPUTES_OPEN:
- D-2026-00342: FUEL_SURCH_DAMAGE, £340 (INV-2026-04318, the email artefact case)
- D-2026-00337: REDELIVERY_FEE, £60
- D-2026-00318: FUEL_SURCH_DAMAGE, £212 (61-90 days aged)

**Pattern**: Fuel surcharge disputes tied to damaged deliveries are recurring (3 of 6 disputes in sample are this type).

**Implication**: Policy-process misalignment — fuel surcharges are applied regardless of delivery outcome, but customers perceive this as unfair when goods arrive damaged. Customer Ops applies goodwill credits reactively, but root cause (policy or communication) not addressed.

#### SOP Drift
- DispatchHub (retired Oct 2024) still referenced in SOP (last revised Oct 2023)
- Section 4.3 "Damaged consignments" incomplete ("TBD pending review of insurance protocol")

**Impact**: New hires onboarded with outdated SOP; agents improvise ("Sandra applied it via manual override"); inconsistent handling.

---

### 6.3 Stakeholder Context: Sarah Whitmore (COO)

**Background**:
- Promoted internally 18 months ago (mid-2024)
- Formerly Dispatch manager (5 years) — deep operational knowledge, limited exposure to AI/automation
- Sceptical of chatbots and consultants (burned twice: 2024 chatbot "customers hated," RPA billing recon "broke whenever Aurum schema changed")

**Pressures**:
- CEO mandate: "Look into" AI after hearing competitor saved £1.2M annualised on customer service
- Organizational skepticism: Two failed automation projects eroded trust
- Operational reality: Customer Ops is functioning but strained (hold times, repeat disputes, dispatcher bottleneck)

**Decision criteria (inferred)**:
- **Must work**: Not interested in PoCs or pilots that don't ship to production
- **Must not break**: Risk-averse after RPA schema-change failure — any solution must handle Aurum volatility
- **Must prove value**: £1.2M benchmark set by competitor (Apex is smaller, so proportional target likely £400-600K annualised savings)
- **Must fit current team**: 35-person Customer Ops team — solution should augment, not replace (redeployment possible, but mass layoffs unlikely given internal promotion culture)

**ASSUMPTION**: Sarah will challenge any design that requires Aurum API integration (she knows it doesn't exist) or that assumes chatbots can handle nuanced disputes (she's seen customers hate chatbots). Confidence: High. Test via: Frame agent design as "decision support for your team" not "chatbot replacement."

---

## 7. ATX Opportunity Hypothesis (Preliminary)

### High-Potential Work Streams (Volume × Cognitive Load)

| Work Stream | Volume | Complexity | Total Labor | Automation Potential | Constraints |
|---|---|---|---|---|---|
| **ETA Inquiries** | 400/day | Low | 27 hrs/day | **High** — mostly lookup + simple heuristics | Requires Driver App GPS API access |
| **Delivery Exceptions** | 180/day | Medium-High | 36 hrs/day | **Medium** — judgment-heavy, but patterns exist | Requires dispatcher heuristic codification |
| **Billing Disputes** | 60/day | High | 28 hrs/day | **Medium** — policy interpretation + cross-system data | **Blocked by Aurum constraint** — can assist investigation, but resolution requires manual ticket |
| **Dispatch Adjustments** | 90/day | High | 27 hrs/day | **Medium** — optimization algorithms exist, but real-time coordination complex | Requires Dispatch Console API (limited surface) |

### Delegation Archetype Hypotheses

#### ETA Inquiries → **Agent-Led with Oversight** (trending toward Fully Agentic)
- **Why**: Lookup-dominant, low risk, high volume
- **Agent role**: Query Driver App GPS, apply route/traffic heuristic, respond to customer with ETA estimate
- **Human oversight**: Escalate if GPS data stale (>30 min) or customer demands callback
- **Quick win**: Could reduce 400 cases/day to ~40 escalations/day (90% deflection)

#### Delivery Exceptions → **Human-Led with Agent Support**
- **Why**: Judgment-heavy (customer relationship, damage assessment, cost-benefit), but agent can aggregate data (customer history, driver notes, re-delivery cost)
- **Agent role**: Surface decision-supporting data (account value, past exceptions, driver reliability score, re-delivery cost estimate)
- **Human decision**: Dispatcher decides return/leave/override
- **Benefit**: Reduce Sandra's line-busy bottleneck by triaging low-stakes cases (e.g., "return to depot" is default if account value <£500 and no prior exceptions)

#### Billing Disputes → **Agent-Led Investigation + Human Resolution**
- **Why**: Investigation (cross-system data aggregation) is automatable; resolution (credit approval) requires judgment and is blocked by Aurum constraint
- **Agent role**: 
  - Parse dispute email/call
  - Retrieve invoice from Aurum export
  - Cross-reference delivery exception (was damage reported?)
  - Retrieve customer history (past disputes, payment behavior, account value)
  - Draft resolution recommendation (e.g., "Apply £170 goodwill credit — customer is high-value, damage claim valid per driver notes")
- **Human role**: Approve/modify recommendation, apply credit (manual override or Aurum ticket)
- **Benefit**: Reduce investigation time from 28 min to ~5 min; improve consistency (agent applies same policy logic across all cases)

#### Dispatch Adjustments → **Human-Only** (for Gate 2 scope)
- **Why**: Real-time, multi-constraint optimization with high stakes (customer SLA breach, driver overtime, vehicle capacity)
- **Constraint**: Dispatch Console API "limited" — unclear if agent can read route state or issue driver instructions
- **Defer**: Out of scope for initial agentic transformation; revisit after ETA/Exceptions/Disputes agents prove value

---

## 8. Key Assumptions Log

| ID | Assumption | Confidence | Test Via |
|---|---|---|---|
| A1 | Handle time metrics (4 min, 12 min, 18 min, 28 min) reflect agent active time, not total elapsed time including waits | High | Ask Sarah if metrics include hold time and coordination waits |
| A2 | Customer Ops agents cannot query Driver App GPS directly; must ask Dispatch team | Medium | Ask Sarah if Customer Ops has direct access to driver location data |
| A3 | Customer Ops agents have local authority to apply goodwill credits up to £200-500 threshold without Aurum ticket | Medium | Ask Sarah what the approval threshold is and how credits are tracked |
| A4 | "Manual override" refers to a local system (CRM or spreadsheet) where Customer Ops tracks credits, synced to Aurum nightly/weekly | Medium | Ask Sandra how she applied the £170 credit and how it reaches Aurum |
| A5 | Dispatcher discretion for exceptions is based on unwritten heuristics (customer tier, driver experience, delivery value, re-delivery cost) | High | Ask Sandra to walk through 3 recent exception cases and articulate decision criteria |
| A6 | 55% "unused capacity" (262.5 available hrs - 118 tracked hrs = 144.5 hrs) is consumed by untracked work (email, meetings, rework, escalations) | High | Ask Sarah what percentage of Customer Ops time is spent on tracked cases vs. other work |
| A7 | Dispatch Console is authoritative for route status; Customer Ops has read-only or no access (cannot modify routes) | High | Confirm with Sarah if Customer Ops can modify routes or must request Dispatch action |
| A8 | Fuel surcharge dispute pattern (3 of 6 disputes are FUEL_SURCH_DAMAGE) indicates policy-process misalignment, not isolated incidents | High | Ask Sarah if fuel surcharge on damaged goods is a known recurring issue and if policy change has been considered |

---

## 9. Next Steps for ATX Assessment

### Discovery Questions to Prioritize (for Live Clarification Round)
1. **Dispatcher heuristic codification**: "Sandra, when Mark called about the leaning pallet at Stein-Allen, what factors would make you decide to return-to-depot vs. leave-and-reattempt? Is there a pattern, or is it different every time?"
2. **Customer Ops GPS access**: "Does your Customer Ops team have direct access to driver GPS data, or do they have to call Dispatch to get it?"
3. **Goodwill credit governance**: "What's the approval threshold for goodwill credits? How do Sandra and her team track credits before they hit Aurum?"
4. **Capacity reality check**: "Your team handles 730 cases/day at ~10 min average, which is 118 hours. You have 35 people, which is 262 hours available. What's consuming the other 144 hours?"
5. **Fuel surcharge policy**: "Hayes & Sons has disputed fuel surcharges on damaged deliveries three times. Is this a known issue? Have you considered changing how fuel surcharges are communicated or applied when damage occurs?"

### Deliverable Prioritization
1. **Cognitive Load Map**: Focus on ETA Inquiries (high volume) and Billing Disputes (high complexity + visible pain)
2. **Delegation Suitability Matrix**: Score all 4 streams, but justify archetypes with reference to lived-process artefacts (voicemail, email, SMS)
3. **Volume × Value Analysis**: ETA Inquiries wins on volume; Billing Disputes wins on customer relationship risk; Delivery Exceptions is medium on both
4. **Agent Purpose Document**: Design for **ETA Inquiry Agent** (highest ROI, lowest risk, least constrained by Aurum)
5. **System/Data Inventory**: Explicitly address Aurum batch-export constraint; propose agent design that works with T-1 lag (investigation phase) and manual resolution (execution phase)
6. **Discovery Questions**: Frame as "questions whose answers would materially change the agent design scope or delegation level"

---

## 10. Domain Orientation Summary

**Apex Distribution is a mid-market regional carrier with a functioning but strained Customer Operations function.** The primary constraints are:
1. **Legacy billing system (Aurum)** with batch-only exports, no real-time API, 48-hour modification turnaround
2. **Dispatcher expertise bottleneck** (Sandra's line busy, drivers blocked, Customer Ops waiting for GPS data)
3. **Information silos** across CRM, Driver App, Dispatch Console, and Aurum
4. **Policy-process misalignment** (fuel surcharges on damaged goods → recurring disputes)
5. **SOP drift** (documentation lags operational reality by 12+ months)

**The highest-value agentic opportunity is ETA Inquiries** (400/day, low complexity, automatable with Driver App GPS access), followed by **Billing Dispute Investigation** (60/day, high complexity, agent can assist investigation even if Aurum blocks automated resolution).

**The anti-pattern to avoid is "everything is fully agentic."** Delivery Exceptions require dispatcher judgment (customer relationship, risk assessment); Billing Disputes require credit approval authority (governance + Aurum constraint). Agent designs must respect these delegation boundaries while providing scalable decision support.

**Sarah Whitmore will challenge designs that ignore Aurum constraints, assume chatbots can handle nuanced disputes, or require dispatcher replacement.** The winning design augments her team's capabilities, reduces coordination waits, and proves value incrementally (ETA deflection first, dispute investigation second, exception triage third).
