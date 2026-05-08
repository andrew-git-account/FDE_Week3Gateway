# System/Data Inventory

## Purpose

This inventory catalogs all systems, data sources, and integration points required for the agentic transformation of Apex Distribution Customer Operations. For each system, we document:
- What the agent needs to access
- What's currently available
- What's missing or risky
- How constraints (especially Aurum Billing batch-only architecture) affect agent design

**Critical Constraint**: Aurum Billing has **no real-time API**, batch-file exports only (T-1/T-2 lag). Agent designs must work within this constraint, not assume it away.

---

## 1. System Landscape Overview

### Architecture Diagram (Logical)

```
┌─────────────────────────────────────────────────────────────┐
│                     CUSTOMER CHANNELS                        │
│                                                               │
│   SMS  │  Email  │  Web Portal  │  Phone (IVR)              │
└───┬───────┬──────────┬──────────────┬──────────────────────┘
    │       │          │              │
    └───────┴──────────┴──────────────┘
                 │
         ┌───────▼────────┐
         │   ETA AGENT    │  ← Phase 1 (Primary Target)
         │                │
         │  • Order Lookup│
         │  • GPS Query   │
         │  • ETA Calc    │
         └────┬──────┬────┘
              │      │
    ┌─────────┼──────┼────────────┬─────────────────┐
    │         │      │            │                 │
┌───▼────┐ ┌──▼──────▼──┐  ┌────▼─────┐  ┌────────▼──────┐
│  CRM   │ │ Driver App │  │  Order   │  │ Traffic API   │
│(Sales- │ │  GPS API   │  │ Database │  │ (Google Maps) │
│ force) │ │            │  │          │  │               │
└────────┘ └────────────┘  └──────────┘  └───────────────┘
    │
    │ (Future: Phases 2-3)
    │
┌───▼──────────────────────────────────────────────────┐
│            BILLING DISPUTE AGENT (Phase 2)           │
│                                                       │
│  • Dispute Classification                            │
│  • Data Aggregation (Invoice, Customer History)     │
│  • Resolution Recommendation                         │
└───┬──────────────┬───────────┬────────────┬─────────┘
    │              │           │            │
┌───▼────┐  ┌──────▼───────┐ ┌▼──────┐  ┌─▼────────────┐
│ Aurum  │  │  Delivery    │ │  CRM  │  │ Driver App / │
│Billing │  │  Exception   │ │       │  │   Dispatch   │
│(Batch  │  │  Logs        │ │       │  │   Console    │
│ Export)│  │              │ │       │  │              │
└────────┘  └──────────────┘ └───────┘  └──────────────┘
    │
    │ T-1 Lag (02:00-04:00 GMT daily export)
    │
    ▼
  (No real-time API — batch CSV files only)
```

---

## 2. System Inventory: Detailed Assessment

### 2.1 CRM (Salesforce-Based)

**System Owner**: Customer Operations / IT  
**Purpose**: Customer records, order tracking, case history, communications

#### What the Agent Needs

**Phase 1** (ETA Inquiry Agent):
- **Read Access**:
  - Orders table: `order_id`, `customer_id`, `route_id`, `delivery_address`, `delivery_status`, `scheduled_eta_start`, `scheduled_eta_end`, `delivery_timestamp`, `recipient_name`
  - Customers table: `customer_id`, `customer_name`, `contact_phone`, `contact_email`, `contract_type`, `credit_limit`
  - Routes table: `route_id`, `route_code`, `driver_id`, `route_date`, `route_type`
- **Write Access**:
  - Cases table: Create new cases for agent interactions (logging), escalations

**Phase 2** (Billing Dispute Agent):
- **Read Access**:
  - Customer history: past cases, dispute frequency, payment behavior (aging)
  - Delivery exception logs (if stored in CRM): damage reports, refusals, re-deliveries
- **Write Access**:
  - Cases table: Billing dispute investigations, resolution recommendations

#### What's Available

- **REST API**: Confirmed in brief ("REST APIs available")
- **Assumed**: Salesforce standard objects (Account, Contact, Case, Custom Objects for Orders/Routes)
- **Authentication**: OAuth 2.0 (service account for agent)
- **Rate Limits**: Unknown (needs confirmation from IT) — Salesforce typically 100,000 API calls/day for Enterprise edition

#### What's Missing or Risky

| Gap | Impact | Mitigation |
|---|---|---|
| **Schema not documented** | Agent design assumes table names (`orders`, `customers`, `routes`) but actual CRM may use different names (e.g., `Delivery__c`, `Account`, `Contact`) | **Discovery**: Request CRM schema documentation from IT. Map actual table/field names to agent design requirements. |
| **GPS data not in CRM** | ETA agent needs driver location; CRM likely doesn't store GPS (stored in Driver App backend) | **Architectural**: Agent must integrate with Driver App GPS API directly (not via CRM). |
| **Delivery exception logs** | Brief doesn't specify where delivery exceptions (refusals, damage) are logged — CRM? Dispatch Console? Driver App? | **Discovery**: Ask Sarah/IT where delivery exceptions are recorded. If not in CRM, agent needs second integration point. |
| **Rate limit unknown** | If agent generates 400 ETA inquiries/day × 3 API calls each (order lookup, customer lookup, case logging) = 1,200 calls/day — well within typical Salesforce limits, but needs confirmation | **Discovery**: Confirm CRM rate limit with IT. If <10,000 calls/day, may need batch operations or caching. |

#### Data Quality Assumptions

| Assumption | Confidence | Test Via |
|---|---|---|
| **Order ID format stable** (`AX-771-3344` pattern) | High (observed in SMS artefact) | Grep CRM for order ID patterns; confirm with IT |
| **Customer phone/email always populated** (for SMS/email matching) | Medium (B2B customers likely have contact info, but DTC may be incomplete) | Query CRM: `SELECT COUNT(*) FROM orders WHERE contact_phone IS NULL OR contact_email IS NULL` |
| **Scheduled ETA window always populated** | Low (voicemail artefact shows SOP incomplete, may indicate data quality issues) | Query CRM: `SELECT COUNT(*) FROM orders WHERE delivery_status = 'OUT_FOR_DELIVERY' AND (scheduled_eta_start IS NULL OR scheduled_eta_end IS NULL)` |
| **Delivery status updated real-time** (driver scans package → CRM updated immediately) | Medium (Driver App likely syncs to CRM, but sync lag unknown) | Ask Sarah: "When a driver scans a delivery as complete, how quickly does CRM reflect that status?" |

---

### 2.2 Driver App (In-House iOS/Android)

**System Owner**: Dispatch Operations / IT  
**Purpose**: GPS tracking, route navigation, scan-on-delivery, driver-to-dispatch messaging

#### What the Agent Needs

**Phase 1** (ETA Inquiry Agent):
- **Read Access**:
  - Driver location (GPS): `driver_id`, `latitude`, `longitude`, `timestamp`, `location_name`
  - Route progress: `stops_completed`, `stops_remaining`
- **No write access required** (agent does not send instructions to drivers — that's Phase 3 scope)

**Phase 3** (Delivery Exception Triage Agent):
- **Read Access**:
  - Delivery exception logs: `order_id`, `exception_type`, `driver_notes`, `photo_url` (if driver uploads damage photos)
- **Write Access** (possibly):
  - Exception instructions: Agent tells driver "Return to depot" or "Leave at safe location" (requires Driver App to accept API commands, not just GPS queries)

#### What's Available

- **GPS data**: Confirmed in SMS artefact (agent queries GPS, receives "last ping 10:48 in Watford")
- **Assumed**: REST API for GPS queries (endpoint unknown, placeholder `/api/driver-location`)
- **Polling interval**: Unknown (SMS artefact shows 36-min staleness → suggests 15-30 min polling interval, not real-time)

#### What's Missing or Risky

| Gap | Impact | Mitigation |
|---|---|---|
| **GPS API endpoint not documented** | Agent design assumes REST API exists, but endpoint URL, authentication method, request/response format unknown | **Discovery**: Request Driver App API documentation from IT/Dispatch team. If no API exists, requires development (Phase 1 blocker). |
| **GPS polling interval too long** (15-30 min inferred from SMS artefact) | 36-min stale data → agent cannot provide accurate ETA → escalates to human (defeats deflection purpose) | **Discovery**: Ask IT what the GPS polling interval is. Request increase to 5-10 min polling for Phase 1. Trade-off: battery life vs. data freshness. |
| **Stops remaining not in GPS data** | ETA calculation requires `stops_remaining` to estimate time until customer delivery. If Driver App GPS only returns lat/lon + timestamp (no route progress), agent cannot calculate precision ETA. | **Discovery**: Confirm GPS API returns `stops_completed` and `stops_remaining`. If not, agent must query route table separately (less precise). |
| **GPS availability by driver** | Not all drivers may have GPS enabled (battery-saving mode, device offline, rural coverage gaps) | **Monitoring**: Track GPS availability rate (% of drivers with GPS <15 min fresh). If <90%, escalate to IT/Dispatch for device/network improvements. |
| **No API for exception logs** | Brief doesn't specify if Driver App stores delivery exceptions (refusals, damage) in API-queryable format | **Discovery**: Ask IT if Driver App has exception log API. If not, exceptions may be in Dispatch Console (limited API) or manual entry in CRM. |

#### Data Quality Assumptions

| Assumption | Confidence | Test Via |
|---|---|---|
| **GPS accuracy ±10 meters** | High (industry standard for mobile GPS) | Spot-check: Compare driver-reported location vs. GPS coordinates for known addresses |
| **GPS updates every 5-10 min** (target, not current) | Low (current is 15-30 min based on SMS artefact) | Request from IT: GPS polling interval configuration |
| **Stops remaining calculated automatically** | Medium (Driver App likely tracks scans → decrements stops remaining) | Query Driver App backend: Confirm `stops_remaining` field exists and is updated on each scan |

---

### 2.3 Dispatch Console (Java Desktop via Citrix)

**System Owner**: Dispatch Operations  
**Purpose**: Route planning, driver assignment, exception triage

#### What the Agent Needs

**Phase 1** (ETA Inquiry Agent):
- **Read Access** (minimal): Route status, driver assignment (already in CRM Routes table, so Dispatch Console may not be needed for Phase 1)

**Phase 3** (Delivery Exception Triage Agent):
- **Read Access**: Exception queue, dispatcher notes, priority flags
- **Write Access** (possibly): Agent assigns exceptions to drivers or marks as "return-to-depot" (requires Dispatch Console to accept API commands)

#### What's Available

- **"Limited API surface"** (per brief) — unclear what "limited" means
- **Assumed**: Read-only access to route status, driver locations (but GPS may be in Driver App backend, not Dispatch Console)

#### What's Missing or Risky

| Gap | Impact | Mitigation |
|---|---|---|
| **"Limited API surface" not defined** | Agent design for Phase 3 (exception triage) assumes Dispatch Console API can receive commands (e.g., "assign exception to Driver B"). If API is read-only, agent cannot execute decisions autonomously. | **Discovery**: Ask Sarah/Dispatch team what "limited API surface" means. Request API documentation. If write access unavailable, Phase 3 design shifts to "agent recommends, human executes via Dispatch Console UI." |
| **Citrix deployment** | Citrix (remote desktop) suggests thick client, not web-based → API may not exist (desktop apps typically don't expose REST APIs) | **Discovery**: Confirm if Dispatch Console has backend API (separate from UI). If no API, agent integration blocked → Phase 3 requires re-architecting (e.g., agent writes to CRM queue, dispatcher reads queue via Dispatch Console). |
| **Route optimization logic proprietary** | If agent needs to recommend route changes (Phase 3 scope), requires understanding of Dispatch Console's route optimization algorithm (vehicle capacity, time windows, driver hours) | **Discovery**: Ask Dispatch team if route optimization algorithm is documented. If proprietary/undocumented, agent cannot replicate logic → must defer to dispatcher judgment. |

#### Data Quality Assumptions

| Assumption | Confidence | Test Via |
|---|---|---|
| **Route status updated real-time** | High (dispatchers actively monitor routes) | Spot-check: Compare Dispatch Console route status vs. Driver App GPS (should be consistent) |
| **Exception queue is digital** (not manual voicemail, per artefact) | Low (voicemail artefact suggests exceptions handled via phone, not queue) | Ask Dispatch team: "How do you track exceptions — digital queue, spreadsheet, voicemail?" |

---

### 2.4 Aurum Billing (Legacy On-Prem Oracle, Since 2008)

**System Owner**: Finance / IT  
**Purpose**: Invoicing, fuel surcharge calculation, customer credit handling

**CRITICAL CONSTRAINT**: **No real-time API. Batch-file exports only. T-1/T-2 lag. 48-hour modification turnaround.**

#### What the Agent Needs

**Phase 2** (Billing Dispute Agent):
- **Read Access**:
  - Invoice header: `INVOICE_NO`, `CUSTOMER_ID`, `INVOICE_DT`, `AMT_NET`, `AMT_FUEL_SURCH`, `AMT_GROSS`, `ROUTE_CODE`
  - Fuel surcharge detail: `FUEL_RATE_TIER`, `FUEL_PCT`, `FUEL_AMT`
  - Credits applied: `CREDIT_ID`, `CREDIT_AMT`, `REASON_CODE`, `APPLIED_DT`, `APPROVER_ID`
  - Disputes: `DISPUTE_ID`, `DISPUTE_TYPE`, `DISPUTE_AMT`, `ASSIGNED_TO`, `STATUS`
  - Reconciliation: `EXPECTED_AMT`, `RECEIVED_AMT`, `VAR` (payment variance)
  - Aged receivables: `AGE_0_30`, `AGE_31_60`, `AGE_61_90`, `AGE_OVER_90`
  - Customer master: `CONTRACT_TYPE`, `RATE_CARD`, `CR_LIMIT`, `ACCT_MGR`
- **No write access** (cannot apply credits directly via API — must submit manual ticket)

#### What's Available

- **Batch CSV exports** (7 files, daily 02:00-04:00 GMT):
  - `APEX_BILL_DAILY_YYYYMMDD.csv` (T-1 lag: invoices from yesterday)
  - `APEX_FUEL_SURCH_YYYYMMDD.csv` (T-1 lag)
  - `APEX_CREDITS_YYYYMMDD.csv` (T-1 lag)
  - `APEX_RECON_YYYYMMDD.csv` (**T-2 lag**: reconciliation 24 hours behind invoice)
  - `APEX_DISPUTES_OPEN_YYYYMMDD.csv` (T-1 lag, point-in-time snapshot)
  - `APEX_AGED_RECEIVABLES_YYYYMMDD.csv` (weekly Friday)
  - `APEX_CUSTOMER_MASTER_YYYYMMDD.csv` (monthly 1st-of-month)
- **File location**: `/exports/aurum/` (presumably on shared file server accessible to agent infrastructure)

#### What's Missing or Risky

| Gap | Impact | Mitigation |
|---|---|---|
| **No real-time data** (T-1 lag) | If customer disputes invoice generated today, agent cannot retrieve invoice data until tomorrow's batch export → agent must tell customer "Your invoice is being processed, I'll have details tomorrow." | **Design**: Agent detects T-1 lag, provides explanation to customer, offers human escalation if urgent. No workaround possible without Aurum API (which doesn't exist). |
| **No write-back capability** | Agent cannot apply credits directly → must create manual ticket for Aurum support team (48-hour turnaround) → dispute resolution delayed | **Design**: Agent recommends credit amount, human approves, human submits Aurum ticket (or logs in CRM for batch ticketing). Agent's value is investigation acceleration (60%), not resolution automation (40%). |
| **Schema changes quarterly without notice** | "Schema changes happen ~quarterly without prior notice" (per brief) → agent CSV parsing breaks when column names change (e.g., `AMT_FUEL_SURCH` → `FUEL_SURCHARGE_AMT`) | **Monitoring**: Agent logs CSV parse errors; if >10% of files fail to parse, alert IT. Manual intervention required to update agent CSV parser. **Design**: Use flexible CSV parsing (column position + name matching) to reduce brittleness. |
| **Reconciliation lag (T-2)** | Payment reconciliation file lags 24 hours behind invoice → if customer says "I paid yesterday," agent cannot confirm payment until day after tomorrow | **Design**: Agent acknowledges lag: "Payment reconciliation updates daily. If you paid yesterday, it should appear in our system by tomorrow. For immediate confirmation, I'll connect you with Accounts Receivable." |
| **Audit gap (Sandra's manual override)** | Email artefact shows Sandra applied £170 credit via "manual override" not logged in `APEX_CREDITS` export → either credits logged with lag, or workaround bypasses Aurum entirely | **Discovery**: Ask Sarah/Sandra how "manual override" credits work. If bypassing Aurum → compliance risk. **Design**: Agent logs all credit recommendations in CRM (audit trail) even if Aurum doesn't capture them. |

#### Aurum Constraint Handling Strategy

**Principle**: Agent design **works within Aurum constraints**, not around them.

1. **Investigation Phase** (T-1 acceptable):
   - Agent queries yesterday's Aurum exports to retrieve invoice, fuel surcharge, credits, disputes
   - If customer disputes today's invoice → agent responds: "Your invoice from [date] is being processed. I'll have full details tomorrow morning. Would you like to speak with a specialist now, or is tomorrow acceptable?"
   - **Design decision**: Majority of disputes are for invoices 3-7 days old (customers receive invoice, review, then dispute) → T-1 lag acceptable for most cases

2. **Resolution Phase** (Human-Executed):
   - Agent recommends credit amount (e.g., "Suggested credit: £170, based on 50% split for similar disputes")
   - Human approves/modifies recommendation
   - Human submits Aurum ticket (manual process, 48-hour turnaround) OR applies "manual override" in CRM (faster but audit gap)
   - **Design decision**: Agent cannot automate resolution due to Aurum constraint, but can accelerate investigation (28 min → 8 min)

3. **Monitoring & Alerts**:
   - Agent monitors for "invoice not yet in Aurum export" cases → flags as "data lag" (not agent failure)
   - Weekly report: % of disputes where invoice data unavailable (T-1 lag) → informs Sarah of constraint impact

#### Data Quality Assumptions

| Assumption | Confidence | Test Via |
|---|---|---|
| **CSV files always generated** (no missed exports) | High (batch processes typically reliable) | Monitor: Check file existence daily; alert if file missing >24 hours |
| **CSV schema stable within quarter** | Medium (brief says "quarterly changes" but frequency unclear) | Monitor: Track CSV parse success rate; alert if <90% for 3 consecutive days |
| **Credits in `APEX_CREDITS` match CRM credits** | Low (email artefact shows Sandra's manual override not logged) | Reconciliation: Weekly join CRM credits vs. Aurum credits; flag mismatches for audit |
| **Dispute status updated daily** | High (`APEX_DISPUTES_OPEN` is T-1 snapshot) | Spot-check: Compare dispute status in CRM vs. Aurum export (should be consistent) |

---

### 2.5 Traffic API (Google Maps / Waze)

**System Owner**: External (Google / Waze)  
**Purpose**: Real-time traffic conditions, travel time estimation

#### What the Agent Needs

**Phase 1** (ETA Inquiry Agent):
- **API Call**: Distance Matrix API (driver location → customer address, with traffic)
- **Request**: Origins (lat/lon), Destinations (lat/lon), Departure time (now), Mode (driving)
- **Response**: Travel time (`duration_in_traffic`), Distance (`distance`), Traffic conditions (inferred from duration vs. duration_in_traffic)

#### What's Available

- **Google Maps Distance Matrix API**: Public API, pay-per-use ($5-10 per 1,000 requests for Standard tier)
- **Waze Traffic API**: Alternative, similar pricing
- **Authentication**: API key (stored in secrets manager)

#### What's Missing or Risky

| Gap | Impact | Mitigation |
|---|---|---|
| **API cost unknown** | 400 ETA inquiries/day × 40% precision requests = 160 traffic API calls/day × 250 work days = 40,000 calls/year × $0.005 = **$200/year** (negligible, but needs budget approval) | **Discovery**: Confirm budget approval for Traffic API cost with Sarah/Finance. |
| **API rate limits** | Google Maps free tier: 40,000 requests/month (1,333/day). Agent needs 160/day → within limits. But if volume spikes (Q4, promos), may exceed. | **Monitoring**: Track API usage; alert if approaching 80% of monthly quota. Upgrade to paid tier if needed. |
| **API availability <100%** | If Traffic API unavailable, agent cannot provide traffic-adjusted ETA → falls back to non-traffic distance (acceptable degradation) | **Design**: Agent calls Traffic API with 3-sec timeout; if timeout, use Google Maps non-traffic distance + warn customer "Traffic data unavailable, estimate based on typical conditions." |

#### Data Quality Assumptions

| Assumption | Confidence | Test Via |
|---|---|---|
| **Traffic data covers UK service area** (Midlands, South, East England) | High (Google Maps has comprehensive UK coverage) | Spot-check: Query Traffic API for sample addresses in service area; confirm traffic data returned |
| **Traffic data updated every 5 min** | High (industry standard for traffic APIs) | Google Maps documentation confirms 5-min refresh interval |

---

## 3. Data Flow Diagrams

### 3.1 ETA Inquiry Agent (Phase 1) — Data Flow

```
Customer Inquiry (SMS)
   │
   ▼
┌──────────────────┐
│   ETA AGENT      │
└────┬─────────────┘
     │
     │ (1) Parse order ID
     │
     ▼
┌──────────────────┐     ┌─────────────────┐
│  CRM (Orders)    │────▶│ order_id        │
│                  │     │ route_id        │
│                  │     │ scheduled_eta   │
│                  │     │ delivery_status │
└──────────────────┘     └─────────────────┘
     │
     │ (2) If customer requests precision ETA
     │
     ▼
┌──────────────────┐     ┌─────────────────┐
│ Driver App GPS   │────▶│ driver_location │
│ API              │     │ stops_remaining │
│                  │     │ timestamp       │
└──────────────────┘     └─────────────────┘
     │
     │ (3) Calculate ETA
     │
     ▼
┌──────────────────┐     ┌─────────────────┐
│ Traffic API      │────▶│ travel_time     │
│ (Google Maps)    │     │ traffic_cond    │
└──────────────────┘     └─────────────────┘
     │
     │ (4) Compose response
     │
     ▼
┌──────────────────┐
│ CRM (Cases)      │◀──── Log interaction
│                  │
└──────────────────┘
     │
     ▼
Customer Response (SMS)
```

**Data Sources**: 3 (CRM, Driver App GPS, Traffic API)  
**Data Writes**: 1 (CRM Cases for logging)  
**External Dependencies**: 2 (Driver App GPS, Traffic API)

---

### 3.2 Billing Dispute Agent (Phase 2) — Data Flow

```
Customer Dispute (Email)
   │
   ▼
┌──────────────────┐
│ BILLING AGENT    │
└────┬─────────────┘
     │
     │ (1) Parse dispute type + invoice number
     │
     ▼
┌──────────────────┐     ┌─────────────────┐
│ Aurum Exports    │────▶│ Invoice data    │
│ (CSV files)      │     │ Fuel surcharge  │
│                  │     │ Credits applied │
│                  │     │ Disputes open   │
│                  │     │ Receivables     │
└──────────────────┘     └─────────────────┘
     │                         (T-1 lag)
     │
     │ (2) Cross-reference delivery exception
     │
     ▼
┌──────────────────┐     ┌─────────────────┐
│ Driver App /     │────▶│ Damage reported?│
│ Dispatch Console │     │ Refusal reason? │
│                  │     │ Driver notes    │
└──────────────────┘     └─────────────────┘
     │
     │ (3) Retrieve customer history
     │
     ▼
┌──────────────────┐     ┌─────────────────┐
│ CRM (Cases)      │────▶│ Past disputes   │
│                  │     │ Payment behavior│
│                  │     │ Account value   │
└──────────────────┘     └─────────────────┘
     │
     │ (4) Generate resolution recommendation
     │
     ▼
┌──────────────────┐
│ CRM (Cases)      │◀──── Log investigation
│                  │      + recommendation
└──────────────────┘
     │
     ▼
Human Approval
     │
     ▼
Manual Aurum Ticket (48h turnaround)
```

**Data Sources**: 3 (Aurum exports, Driver App/Dispatch Console, CRM)  
**Data Writes**: 1 (CRM Cases)  
**External Dependencies**: 1 (Aurum batch exports, T-1 lag)  
**Human-in-Loop**: Yes (approval + Aurum ticket submission)

---

## 4. Missing Data & Integration Gaps

### Priority 1: Blockers (Must Resolve for Phase 1)

| Gap | System | Impact | Discovery Question | Mitigation if Unavailable |
|---|---|---|---|---|
| **Driver App GPS API** | Driver App | ETA agent cannot calculate precision ETA (only scheduled window) | "Does Driver App have a REST API for querying driver GPS location? What's the endpoint URL and authentication method?" | Phase 1A proceeds with scheduled window only (50% deflection vs. 90% target). Negotiate GPS API access for Phase 1B. |
| **GPS polling interval** | Driver App | If >30 min, most GPS data stale → agent escalates → low deflection | "What is the GPS polling interval? Can it be increased to 5-10 min for Customer Ops use case?" | Accept 15-30 min polling for Phase 1, budget for device/network upgrades in Phase 1B. |
| **CRM schema** | CRM | Agent assumes table/field names; if wrong, agent cannot query data | "Can IT provide CRM schema documentation (table names, field names, data types)?" | Manual schema discovery (query CRM via Salesforce Workbench, map to agent requirements). |

### Priority 2: Important (Should Resolve for Phase 2)

| Gap | System | Impact | Discovery Question | Mitigation if Unavailable |
|---|---|---|---|---|
| **Delivery exception logs location** | Driver App / Dispatch Console / CRM | Billing dispute agent cannot cross-reference damage claims without exception data | "Where are delivery exceptions (refusals, damage) logged — Driver App, Dispatch Console, or CRM?" | If not in any system, billing agent relies on customer claim only (no validation against driver notes). |
| **Aurum credit reconciliation** | Aurum / CRM | Sandra's "manual override" not in Aurum export → compliance gap | "How does Sandra apply goodwill credits? Are they logged in Aurum, CRM, or spreadsheet?" | Agent logs all credit recommendations in CRM (audit trail), even if Aurum doesn't capture. Weekly reconciliation (CRM vs. Aurum credits). |
| **Dispatch Console API** | Dispatch Console | Exception triage agent (Phase 3) cannot read exception queue or write decisions | "What does 'limited API surface' mean for Dispatch Console? Can agent read exception queue and write decisions?" | If no API, Phase 3 shifts to "agent recommends, dispatcher executes via UI" (lower automation). |

### Priority 3: Nice-to-Have (Improves Performance)

| Gap | System | Impact | Discovery Question | Mitigation if Unavailable |
|---|---|---|---|---|
| **Real-time CRM sync latency** | CRM | If driver scans delivery but CRM updates 5 min later, agent may provide stale status | "When driver scans delivery, how quickly does CRM reflect updated status?" | Acceptable if <5 min lag; if >5 min, agent warns customer "Status as of [timestamp]." |
| **Traffic API redundancy** | Traffic API | If Google Maps unavailable, agent falls back to non-traffic distance (less accurate) | N/A (external API) | Fallback to non-traffic distance is acceptable; monitor API availability weekly. |
| **Aurum schema change alerts** | Aurum | If schema changes without notice, agent CSV parsing breaks | "Can IT provide advance notice (email, Slack) when Aurum schema changes?" | If no alerts, agent monitors CSV parse success rate; alerts if <90% for 3 days. |

---

## 5. Data Quality Assessment

### 5.1 CRM Data Quality

**Assessment Method**: SQL queries on CRM database (if accessible) or Salesforce Data Loader export

| Field | Completeness Target | Quality Issue | Impact | Mitigation |
|---|---|---|---|---|
| `orders.contact_phone` | >95% populated | B2B customers likely complete; DTC may be missing | Agent cannot match SMS sender to order → security check fails → escalates | Query: `SELECT COUNT(*) FROM orders WHERE contact_phone IS NULL`. If >5%, request data cleanup initiative. |
| `orders.scheduled_eta_start` | >98% populated | SOP incomplete (voicemail artefact) suggests data entry gaps | Agent cannot provide scheduled window → escalates | Query: `SELECT COUNT(*) FROM orders WHERE delivery_status = 'OUT_FOR_DELIVERY' AND scheduled_eta_start IS NULL`. If >2%, flag as data quality issue for Dispatch team. |
| `orders.delivery_status` | 100% populated (should be non-null) | If null or invalid enum value, agent cannot determine order stage | Agent cannot process inquiry → escalates | Validate: `SELECT DISTINCT delivery_status FROM orders` — confirm only valid enum values. |

### 5.2 Aurum Billing Data Quality

**Assessment Method**: Parse CSV files, check for consistency across files

| File | Quality Issue | Impact | Mitigation |
|---|---|---|---|
| `APEX_CREDITS` | Sandra's manual override not logged (email artefact) | Audit gap, potential compliance risk | **Discovery**: Confirm with Sandra how credits are logged. **Design**: Agent logs all recommendations in CRM, weekly reconciliation CRM vs. Aurum. |
| `APEX_RECON` | T-2 lag (24 hours behind invoice) | Customer says "I paid yesterday," agent cannot confirm | **Design**: Agent acknowledges lag, offers human escalation for immediate confirmation. |
| `APEX_DISPUTES_OPEN` | Point-in-time snapshot (not transactional log) | If dispute status changes mid-day, agent works with stale data until next export | **Acceptable**: T-1 lag is constraint; agent notes timestamp: "Dispute status as of [export date]." |

### 5.3 Driver App GPS Data Quality

**Assessment Method**: Spot-check GPS coordinates vs. known addresses

| Metric | Target | Current (Inferred) | Mitigation |
|---|---|---|---|
| **GPS accuracy** | ±10 meters | Unknown (assumed standard mobile GPS) | Spot-check: Compare driver-reported location vs. GPS for sample deliveries. |
| **GPS freshness (p50)** | <10 min | 15-30 min (inferred from SMS artefact: 36 min staleness) | **Discovery**: Request GPS polling interval increase to 5-10 min. |
| **GPS availability** | >95% of drivers | Unknown | Monitor: Track % of drivers with GPS <15 min fresh. Alert if <90%. |

---

## 6. System Integration Risk Matrix

| Integration | Phase | Risk Level | Failure Mode | Mitigation |
|---|---|---|---|---|
| **CRM ↔ Agent** | Phase 1 | **LOW** | CRM API unavailable → agent cannot function | Critical dependency; CRM has >99.5% uptime (Salesforce SLA). Monitor API availability; escalate all inquiries if CRM down >5 min. |
| **Driver App GPS ↔ Agent** | Phase 1 | **MEDIUM** | GPS API unavailable → agent falls back to scheduled window (graceful degradation) | Non-critical for Phase 1A (scheduled window only). Critical for Phase 1B (precision ETA). Fallback: provide scheduled window + explanation. |
| **Traffic API ↔ Agent** | Phase 1 | **LOW** | Traffic API unavailable → agent uses non-traffic distance | External API, 99% uptime. Fallback acceptable (ETA accuracy drops slightly). Monitor API availability weekly. |
| **Aurum Exports ↔ Agent** | Phase 2 | **MEDIUM** | CSV file missing or schema changed → agent cannot investigate disputes | Batch process, typically reliable. **Monitoring**: Check file existence daily; alert if missing. **Schema changes**: Weekly parse success rate; alert if <90%. |
| **Dispatch Console ↔ Agent** | Phase 3 | **HIGH** | "Limited API" may not support agent write operations → agent cannot triage exceptions autonomously | **Discovery Priority 2**: Confirm API capabilities. If no write access, Phase 3 design shifts to "agent recommends, dispatcher executes." |

---

## 7. Infrastructure Requirements

### 7.1 Agent Hosting

**Deployment Model**: Cloud-hosted (AWS/Azure/GCP) or on-prem (if Apex has strict data residency requirements)

**Compute Requirements**:
- **Phase 1**: 2-4 vCPU, 8 GB RAM (handles 10 concurrent ETA inquiries, peak load)
- **Phase 2**: +2 vCPU, +4 GB RAM (billing dispute investigation is memory-intensive — loads multiple CSV files)
- **Scaling**: Horizontal (stateless agent, can deploy multiple instances behind load balancer)

**Storage Requirements**:
- **Aurum CSV files**: 7 files × 250 days/year (daily exports, 1-year retention) × 5 MB/file (estimated) = 8.75 GB/year
- **CRM case logs**: 400 ETA inquiries/day × 250 days × 1 KB/case = 100 MB/year
- **Total**: <10 GB (negligible)

**Network Requirements**:
- **Bandwidth**: 1 Mbps sustained (agent sends/receives SMS, API calls)
- **Latency**: <100 ms to CRM, <200 ms to Driver App GPS (on-prem or cloud-hosted)
- **Firewall**: Outbound HTTPS (443) to Traffic API (Google Maps), SMS gateway

### 7.2 Data Pipeline (Aurum CSV Ingestion)

**Process**:
1. Daily cron job (04:30 GMT, after Aurum export completes) fetches CSV files from `/exports/aurum/`
2. Parse CSV → validate schema (detect column name changes)
3. Load into agent database (PostgreSQL or MySQL — normalized tables mirroring Aurum schema)
4. Agent queries agent database (not CSV files directly) for billing dispute investigation

**Why Database, Not CSV**: Agent needs to JOIN across files (e.g., invoice + fuel surcharge + disputes). CSV files are denormalized; database allows efficient queries.

**Failure Handling**:
- If CSV missing → alert IT, agent uses yesterday's data (T-2 lag instead of T-1)
- If schema changed → alert IT, manual intervention to update CSV parser

---

## 8. Security & Compliance

### 8.1 Authentication & Authorization

| System | Auth Method | Agent Credentials | Rotation Policy |
|---|---|---|---|
| **CRM (Salesforce)** | OAuth 2.0 | Service account with scopes: `orders.read`, `customers.read`, `cases.write` | Access token refreshed every 12 hours, service account password rotated quarterly |
| **Driver App GPS API** | Bearer token (assumed) | API token stored in secrets manager (AWS Secrets Manager / Azure Key Vault) | Rotated quarterly, never logged |
| **Traffic API (Google Maps)** | API key | API key stored in secrets manager | Rotated annually |
| **SMS Gateway** | API key | API key stored in secrets manager | Rotated quarterly |

### 8.2 Data Privacy (GDPR Compliance)

**PII Handling**:
- Agent logs case interactions to CRM: Include `customer_id` (internal), NOT `customer_name`, `phone`, `email` (unless required for audit)
- SMS/email responses: Do NOT include sensitive info (payment details, full address) — only order status, ETA
- GPS data: Driver location is PII (identifies individual's location) — do NOT log GPS coordinates, only `location_name` (city-level granularity)

**Data Retention**:
- CRM case logs: Retained per Apex's data retention policy (assumed 7 years for financial/regulatory compliance)
- Aurum CSV files: Retained 1 year (agent database mirrors Aurum, so CSV files not needed beyond 1 year)
- Agent logs (debug/error): Retained 90 days

### 8.3 Security Vulnerabilities

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Credential leakage** (API tokens in logs) | Low | High (unauthorized access to CRM, GPS data) | Never log credentials; store in secrets manager; rotate quarterly |
| **SQL injection** (CRM queries) | Low | High (data breach, unauthorized access) | Use parameterized queries (ORM), not string concatenation |
| **Cross-customer data leak** (customer A sees customer B's order) | Medium | High (GDPR violation, customer trust) | Enforce customer identity verification (SMS phone matches order phone, email matches order email) |
| **DDoS (spam inquiries)** | Medium | Medium (agent overload, increased costs) | Rate limit: 5 inquiries/hour per order ID; if exceeded, escalate to human |

---

## 9. Conclusion

This system/data inventory reveals:

1. **CRM (Salesforce)** is the primary integration point — REST API available, schema needs documentation
2. **Driver App GPS API** is critical for Phase 1B (precision ETA) — API access must be negotiated with Dispatch/IT
3. **Aurum Billing batch-only constraint** is non-negotiable — agent design for Phase 2 must work with T-1 lag, no workaround
4. **Dispatch Console "limited API"** is a Phase 3 blocker — discovery required to determine if agent can write decisions

**Integration Priorities**:
1. **Phase 1A** (Month 1-2): CRM only (scheduled window ETA) — **LOW RISK**, no new integrations
2. **Phase 1B** (Month 3): +Driver App GPS API, +Traffic API — **MEDIUM RISK**, requires GPS API negotiation
3. **Phase 2** (Months 4-6): +Aurum CSV ingestion pipeline — **MEDIUM RISK**, schema volatility requires monitoring
4. **Phase 3** (Months 7-9): +Dispatch Console API — **HIGH RISK**, API capabilities unknown

**Missing Data** (Discovery Questions for Sarah):
- Driver App GPS API endpoint, authentication, polling interval
- Delivery exception logs location (Driver App, Dispatch Console, CRM?)
- Aurum credit reconciliation (how does Sandra's "manual override" work?)
- Dispatch Console API capabilities (read-only or write access?)

**System Constraints Acknowledged**:
- Aurum T-1 lag is accepted, not hand-waved
- GPS staleness (15-30 min) is monitored, mitigation planned (polling interval increase)
- Dispatch Console "limited API" may block Phase 3 full automation — prepared to shift to "agent recommends, human executes"

**This inventory is honest about what's available, what's missing, and what's risky** — the ATX methodology applied to system integration.
