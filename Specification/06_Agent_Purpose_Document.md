# Agent Purpose Document: ETA Inquiry Agent

## Document Status
- **Version**: 1.0 (Gate 2 Submission)
- **Target Implementation**: Phase 1 (Months 1-3)
- **Buildability**: This document is written to enable an AI coding agent to begin building with minimal clarifying questions

---

## 1. Agent Purpose

### Primary Job to be Done
**"Provide accurate delivery time estimates to customers instantly, eliminating coordination delays and freeing Customer Operations capacity for higher-value work."**

### Customer Problem Solved
Customers asking "Where is my delivery?" currently wait 4-11 minutes for imprecise ETA estimates (4-hour windows). Agent provides <30-second response with precision estimates (±30 min windows) based on real-time driver location and traffic data.

### Business Problem Solved
ETA inquiries consume 73 hours/day (28% of Customer Ops capacity) for low-complexity lookup work. Agent deflects 90% of inquiries (360/400 cases/day), freeing 66 hours/day (8.8 FTE equivalent) for growth absorption or redeployment to billing disputes.

---

## 2. Scope

### In-Scope Capabilities

1. **Standard ETA Lookup** (Fully Agentic)
   - Input: Customer provides order ID (via SMS, email, web portal, or phone IVR)
   - Process: Query order system → retrieve route + scheduled ETA window
   - Output: "Your order #AX-771-3344 is out for delivery on route 028. Scheduled delivery window: 13:00-17:00 today."
   - Volume: 400 inquiries/day
   - Success Criteria: Response time <30 seconds, accuracy >98%

2. **Precision ETA Calculation** (Agent-Led, trending toward Fully Agentic)
   - Input: Customer requests more specific time after receiving scheduled window
   - Process: 
     - Query Driver App GPS API for driver's current location + timestamp
     - Assess GPS data freshness (if >30 min stale → escalate)
     - Calculate distance/time from driver location to customer address
     - Query traffic API (Google Maps/Waze) for current traffic conditions
     - Apply heuristic: Stops remaining × avg stop duration (15 min) + travel time + traffic buffer
     - Generate ETA estimate with ±30 min window
   - Output: "Based on current driver location (Watford), your delivery is estimated between 14:00-14:30 today. Traffic conditions: moderate."
   - Volume: ~160 inquiries/day (estimated 40% of customers request precision after initial response)
   - Success Criteria: Response time <2 min, ETA accuracy >90% (±30 min tolerance), escalation rate <10%

3. **Multi-Channel Support**
   - SMS (current primary channel, per artefact)
   - Email (current secondary channel)
   - Web portal (self-service, future)
   - Phone IVR (voice input → transcribe → agent processes, future Phase 1b)

4. **Escalation Handling**
   - Detect escalation triggers (GPS stale, customer demands callback, order not found)
   - Route to human agent with context summary
   - Provide hold instruction to customer: "I'm connecting you with a specialist. Hold time: ~2 minutes."

### Out-of-Scope (Deferred to Future Phases)

1. **Proactive ETA Updates**: Agent monitors delivery progress, sends unsolicited updates ("Your delivery is 30 min away") → Phase 1b (Month 4)
2. **Delivery Instructions**: Customer requests delivery time change or leave-at-door instructions → Requires Dispatch Console write access, Phase 2
3. **Exception Inquiries**: "Why was my delivery missed yesterday?" → Different job to be done (exception investigation, not ETA), Phase 3
4. **Multi-Lingual Support**: Non-English inquiries → Phase 1b (if customer base requires)
5. **Voice Channel (Conversational)**: Phone calls with conversational agent (not just IVR) → Phase 2 (requires speech synthesis + multi-turn dialog)

---

## 3. Success Metrics & KPIs

### Lagging Indicators (Business Outcomes, Monthly Review)

| Metric | Baseline | 3-Month Target | 6-Month Target | Measurement Method |
|---|---|---|---|---|
| **Deflection Rate** | 0% (all human-handled) | 80-85% | 90% | Agent-resolved / Total ETA inquiries |
| **Response Time (p50)** | 4-11 min | <30 sec | <15 sec | Timestamp: inquiry received → first response |
| **Response Time (p95)** | 15-20 min (est.) | <2 min | <1 min | Timestamp: inquiry received → first response |
| **ETA Accuracy** | Unknown (baseline needed) | >90% (±30 min) | >95% (±30 min) | Spot-check: agent ETA vs. actual delivery time |
| **Customer Satisfaction (CSAT)** | Unknown (baseline needed) | >4.0/5 | >4.3/5 | Post-interaction survey (10% sample) |
| **Escalation Rate** | N/A | 10-15% | <10% | Agent escalations / Agent-handled inquiries |
| **Repeat Inquiry Rate** | Unknown (baseline needed) | <15% (same order <24h) | <10% | CRM: duplicate order IDs within 24h |

### Leading Indicators (Operational Health, Weekly Review)

| Metric | Target | Alert Threshold | Measurement Method |
|---|---|---|---|
| **Agent Utilization Rate** | >80% | <70% for 2 consecutive weeks | Eligible cases routed to agent / Total eligible cases |
| **GPS Data Freshness** | <15 min (median) | >30 min for >20% of queries | Timestamp: GPS ping → query time |
| **Agent Response Time (p95)** | <5 sec (compute time) | >10 sec | Agent processing time (excludes API latency) |
| **API Availability** (Driver App GPS) | >99.5% | <98% for 24h | Successful API calls / Total API calls |
| **API Availability** (Traffic API) | >99% | <95% for 24h | Successful API calls / Total API calls |
| **Escalation Precision** | >85% | <75% for 2 consecutive weeks | Human review: escalations that needed escalation / Total escalations |
| **Escalation Recall** | >95% | <90% (indicates agent over-confident) | Spot-check: cases that should have escalated but didn't / Sample size |

---

## 4. Activity Catalog

### Activity 1: Order ID Extraction & Validation

**Trigger**: Customer inquiry received (SMS, email, web portal)

**Input**: 
- Raw customer message text (e.g., "Where is order #AX-771-3344?" or "AX-771-3344 status")
- Channel metadata (SMS sender phone, email sender address, web portal user ID)

**Process**:
1. Parse message using regex patterns:
   - Pattern 1: `#?[A-Z]{2}-\d{3}-\d{4}` (e.g., #AX-771-3344, AX-771-3344)
   - Pattern 2: Order ID in subject line (email) or first line (SMS)
   - Pattern 3: Fuzzy match if malformed (e.g., "AX 771 3344" → normalize to "AX-771-3344")
2. Validate order ID exists in order system (CRM database query)
3. Cross-reference customer identity (SMS phone number or email address matches order customer contact)

**Output**:
- **Success**: order_id (string), order_status (enum), route_id (string), customer_id (string)
- **Failure**: order_not_found (escalation trigger) OR customer_mismatch (security: customer inquiring about someone else's order)

**Error Handling**:
- Order ID not found → Response: "I couldn't find order [order_id]. Please check the order number and try again, or reply 'AGENT' to speak with someone."
- Customer mismatch (SMS phone doesn't match order phone) → Response: "For security, I can only provide order details to the phone number on file. Please call 0800-XXX-XXXX to verify."
- Ambiguous parse (multiple order IDs in message) → Response: "I found multiple order numbers in your message. Which order are you asking about: [list]?"

**Edge Cases**:
- Customer provides tracking number (not order ID) → Lookup tracking_number → order_id mapping table
- Customer provides partial ID ("771-3344" missing prefix) → Attempt fuzzy match; if ambiguous, ask clarification

**Acceptance Criteria**:
- Extracts order ID correctly from 95% of well-formed inquiries
- Handles malformed IDs (spaces, missing prefix) with >80% success
- Security: Never discloses order details to non-matching customer contact

---

### Activity 2: Route & Scheduled ETA Retrieval

**Trigger**: Order ID validated (Activity 1 success)

**Input**: order_id (string)

**Process**:
1. Query order database:
   ```sql
   SELECT order_id, route_id, scheduled_eta_start, scheduled_eta_end, delivery_address, delivery_status
   FROM orders
   WHERE order_id = :order_id
   ```
2. Join with route table:
   ```sql
   SELECT route.route_code, route.depot, route.driver_id, route.vehicle_id
   FROM routes AS route
   WHERE route.route_id = :route_id AND route.date = CURRENT_DATE
   ```
3. Format scheduled ETA window:
   - If scheduled_eta_start and scheduled_eta_end exist → "Scheduled delivery window: [HH:MM]-[HH:MM] today."
   - If only date available (no time window) → "Scheduled delivery: today. I can check driver progress for a more specific time — would you like that?"
   - If delivery_status = "DELIVERED" → "Your order was delivered at [timestamp]. Signed by: [recipient_name]."
   - If delivery_status = "OUT_FOR_DELIVERY" → Proceed to Activity 3 (GPS-based ETA)
   - If delivery_status = "CANCELLED" or "RETURNED" → Escalate to human (exception inquiry, out of scope)

**Output**:
- route_code (string), scheduled_eta_start (time), scheduled_eta_end (time), delivery_status (enum), driver_id (string)

**Error Handling**:
- Route not found (order assigned to route but route data missing) → Escalate: "I'm unable to locate your delivery route. Connecting you with a specialist."
- Scheduled ETA missing (data quality issue) → Fallback: "Your order is scheduled for delivery today. I can check the driver's current location for a specific time — would you like that?"

**Acceptance Criteria**:
- Retrieves route + scheduled ETA for >99% of orders with delivery_status = "OUT_FOR_DELIVERY"
- Handles delivered orders correctly (returns delivery timestamp, does not proceed to GPS query)
- Detects exceptions (cancelled, returned) and escalates

---

### Activity 3: GPS Data Retrieval & Freshness Assessment

**Trigger**: Customer requests precision ETA (after receiving scheduled window) OR scheduled window >3 hours

**Input**: route_id (string), driver_id (string), current_time (timestamp)

**Process**:
1. Call Driver App GPS API:
   ```http
   GET /api/driver-location
   Headers: Authorization: Bearer {api_token}
   Query: driver_id={driver_id}&route_id={route_id}
   Response: {
     "driver_id": "D-042",
     "route_id": "R-028",
     "latitude": 51.6577,
     "longitude": -0.3961,
     "timestamp": "2026-04-14T10:48:33Z",
     "location_name": "Watford",
     "stops_completed": 8,
     "stops_remaining": 14
   }
   ```
2. Assess GPS data freshness:
   - Calculate staleness: current_time - gps_timestamp
   - If staleness < 15 min → FRESH (proceed to Activity 4)
   - If 15 min ≤ staleness < 30 min → MODERATE (proceed to Activity 4, but flag low confidence)
   - If staleness ≥ 30 min → STALE (escalate to human)

**Output**:
- gps_latitude (float), gps_longitude (float), gps_timestamp (datetime), location_name (string), stops_remaining (int), freshness (enum: FRESH|MODERATE|STALE)

**Error Handling**:
- GPS API unavailable (timeout, 5xx error) → Escalate: "I'm unable to reach the driver tracking system. Connecting you with a specialist who can call the driver directly."
- GPS data not available for driver (driver hasn't enabled GPS, or device offline) → Escalate: "Driver location data is currently unavailable. A specialist will contact you within 30 minutes with an update."
- Staleness ≥ 30 min → Response: "Driver's last known location was [location_name] at [time], but the data is now [staleness] minutes old. For a current update, I'll connect you with dispatch."

**Edge Cases**:
- GPS coordinates outside expected service area (lat/lon validation) → Escalate (data quality issue or driver off-route)
- Stops_remaining = 0 but delivery_status ≠ "DELIVERED" → Escalate (data inconsistency: route complete but order not marked delivered)

**Acceptance Criteria**:
- Retrieves GPS data for >95% of active drivers
- Detects stale data (≥30 min) and escalates rather than providing low-confidence estimate
- API timeout handled gracefully (<5 sec timeout, escalates if exceeded)

---

### Activity 4: Precision ETA Calculation

**Trigger**: GPS data retrieved with freshness = FRESH or MODERATE (Activity 3 success)

**Input**:
- gps_latitude (float), gps_longitude (float), stops_remaining (int)
- delivery_address (string), customer_latitude (float), customer_longitude (float)
- route_id (string), current_time (timestamp)

**Process**:
1. **Distance Calculation** (Driver → Customer Address):
   - Call Google Maps Distance Matrix API:
     ```http
     GET /maps/api/distancematrix/json
     Query: origins={gps_lat},{gps_lon}&destinations={customer_lat},{customer_lon}&mode=driving&departure_time=now
     Response: {
       "rows": [{
         "elements": [{
           "distance": {"value": 12400, "text": "12.4 km"},
           "duration": {"value": 1260, "text": "21 mins"},
           "duration_in_traffic": {"value": 1680, "text": "28 mins"}
         }]
       }]
     }
     ```
   - Extract: travel_time_sec = duration_in_traffic.value

2. **Stop Duration Estimation**:
   - Heuristic: avg_stop_duration = 15 minutes (industry standard for B2B deliveries)
   - Total stop time: stops_remaining × avg_stop_duration × 60 (convert to seconds)
   - Adjustment: If route_type = "DTC" (residential), avg_stop_duration = 5 min (faster drop-off)

3. **ETA Calculation**:
   - base_eta = current_time + (stops_remaining × avg_stop_duration_sec) + travel_time_sec
   - Add buffer: ±15 min (accounts for unforeseen delays: traffic, parking, recipient delays)
   - eta_window_start = base_eta - 900 (15 min in seconds)
   - eta_window_end = base_eta + 900
   - Format: "14:00-14:30" (round to nearest 5-minute increment for readability)

4. **Confidence Assessment**:
   - If freshness = FRESH AND traffic = "light" → confidence = HIGH
   - If freshness = MODERATE OR traffic = "heavy" → confidence = MEDIUM
   - If stops_remaining > 10 → confidence = MEDIUM (many stops = higher uncertainty)

**Output**:
- eta_window_start (time), eta_window_end (time), confidence (enum: HIGH|MEDIUM), traffic_conditions (string)

**Error Handling**:
- Traffic API unavailable → Fallback to non-traffic distance (duration.value, not duration_in_traffic.value) + warn customer: "Traffic data unavailable; estimate based on typical conditions."
- Customer address not geocoded (lat/lon missing) → Escalate: "I need to verify your delivery address. Connecting you with a specialist."
- ETA calculation results in past time (e.g., driver closer than expected) → Override: "Your delivery is imminent — driver is nearby. Estimated arrival: within 15 minutes."

**Edge Cases**:
- Driver location is AFTER customer address on route (GPS data suggests driver passed customer but delivery not marked complete) → Escalate (data inconsistency)
- Stops_remaining = 1 but customer is not the last stop on route → Estimate uncertain (don't know customer's position in sequence); downgrade confidence to MEDIUM

**Acceptance Criteria**:
- ETA accuracy >90% (±30 min tolerance) when freshness = FRESH
- ETA accuracy >80% (±30 min tolerance) when freshness = MODERATE
- Traffic conditions factored into estimate (uses duration_in_traffic, not duration)
- Confidence level accurately reflects data quality (no HIGH confidence on STALE data)

---

### Activity 5: Response Composition & Delivery

**Trigger**: ETA calculated (Activity 4 success) OR scheduled window retrieved (Activity 2 success)

**Input**:
- order_id (string), route_code (string)
- scheduled_eta_start (time), scheduled_eta_end (time) [if Activity 2 only]
- eta_window_start (time), eta_window_end (time), confidence (enum), traffic_conditions (string) [if Activity 4 completed]
- customer_channel (enum: SMS|EMAIL|WEB)

**Process**:
1. **Select Response Template**:
   - **Template A** (Scheduled Window Only):
     - "Your order #{order_id} is out for delivery on route {route_code}. Scheduled delivery window: {scheduled_eta_start}-{scheduled_eta_end} today. Reply 'MORE' for a more specific time based on driver location."
   - **Template B** (Precision ETA, HIGH Confidence):
     - "Based on current driver location ({location_name}), your order #{order_id} is estimated for delivery between {eta_window_start}-{eta_window_end} today. Traffic conditions: {traffic_conditions}. We'll notify you when the driver is nearby."
   - **Template C** (Precision ETA, MEDIUM Confidence):
     - "Based on driver location as of {gps_time}, your order #{order_id} is estimated for delivery between {eta_window_start}-{eta_window_end} today. Traffic conditions: {traffic_conditions}. This is an estimate; actual time may vary. Reply 'AGENT' to speak with someone for a live update."
   - **Template D** (Delivered):
     - "Your order #{order_id} was delivered at {delivery_timestamp}. Signed by: {recipient_name}. Reply 'ISSUE' if there's a problem."

2. **Channel-Specific Formatting**:
   - **SMS**: Plain text, <160 characters if possible (for single-message delivery), use abbreviations if needed
   - **Email**: HTML formatted, include order details table (order #, items, delivery address), trackable link to web portal
   - **Web Portal**: Structured JSON response with map widget (show driver location + customer address), ETA countdown timer

3. **Logging & Audit Trail**:
   - Log to CRM:
     ```json
     {
       "case_id": "ETA-2026-04-14-003344",
       "order_id": "AX-771-3344",
       "customer_id": "C-04451",
       "inquiry_timestamp": "2026-04-14T11:14:22Z",
       "response_timestamp": "2026-04-14T11:14:48Z",
       "response_type": "PRECISION_ETA",
       "eta_provided": "14:00-14:30",
       "confidence": "HIGH",
       "agent_handled": true,
       "escalated": false
     }
     ```
   - Log GPS query for accuracy spot-check (store: gps_timestamp, eta_provided, actual_delivery_time [backfilled after delivery])

**Output**:
- Response message sent to customer (SMS, email, or web portal)
- Case logged in CRM

**Error Handling**:
- SMS delivery failure (phone number invalid, carrier error) → Retry once; if fails, escalate to email fallback (if email on file)
- Email delivery failure (bounce, invalid address) → Log error, attempt SMS fallback
- Response too long for SMS (>160 characters after formatting) → Split into multi-part SMS OR shorten using abbreviations ("est." instead of "estimated")

**Acceptance Criteria**:
- Response delivered to customer <30 sec after inquiry received (p50), <2 min (p95)
- Template selection matches confidence level (no HIGH confidence claims on MODERATE data)
- All interactions logged to CRM for audit + accuracy spot-check
- Multi-channel support (SMS, email, web) with appropriate formatting

---

### Activity 6: Escalation to Human Agent

**Trigger**: Any escalation condition met (GPS stale, order not found, customer demands callback, data inconsistency)

**Input**:
- order_id (string), customer_id (string), escalation_reason (enum)
- context_summary (string: brief description of what agent attempted and why escalation needed)

**Process**:
1. Create CRM case:
   - Case type: "ETA_INQUIRY_ESCALATION"
   - Priority: MEDIUM (unless customer explicitly demands urgency → HIGH)
   - Assigned to: Customer Ops queue (round-robin assignment)
2. Provide context summary to human agent:
   ```
   Case: ETA-2026-04-14-003344 (escalated from agent)
   Customer: Hayes & Sons Ltd (C-04451), Phone: +44-XXX
   Order: #AX-771-3344, Route: R-028
   Escalation Reason: GPS_STALE (last ping 42 min ago)
   Customer Message: "Where is order #AX-771-3344?"
   Agent Actions Taken: Retrieved order + route, attempted GPS query, detected stale data
   Recommended Next Step: Contact driver directly via radio/phone for live location update
   ```
3. Send hold message to customer:
   - "I'm connecting you with a specialist for a live update. Hold time: ~2 minutes. They'll reach out via [SMS/call]."

**Output**:
- CRM case created, assigned to human agent
- Customer notified of escalation + hold time

**Error Handling**:
- CRM case creation fails (API error) → Log to error queue, send fallback SMS to customer: "Technical issue. Please call 0800-XXX-XXXX. Reference: [order_id]."

**Escalation Reasons** (enum):
- GPS_STALE: GPS data >30 min old
- GPS_UNAVAILABLE: Driver App GPS API timeout or driver location not available
- ORDER_NOT_FOUND: Order ID not in system
- CUSTOMER_MISMATCH: Security check failed (customer inquiring about order not linked to their contact)
- DATA_INCONSISTENCY: Conflicting data (e.g., driver past customer address but delivery not marked complete)
- EXCEPTION_INQUIRY: Customer asking about exception (missed delivery, damage) not just ETA
- CUSTOMER_DEMANDS_CALLBACK: Customer explicitly requests human (keywords: "agent," "person," "call me," "speak to someone")

**Acceptance Criteria**:
- Escalation creates CRM case with full context summary (human agent doesn't need to re-query)
- Customer receives hold message with estimated wait time (<5 min p95)
- Escalation reason logged for analysis (monitor patterns: if GPS_STALE is >20% of escalations, GPS data infrastructure needs improvement)

---

## 5. Autonomy Matrix

**Definition**: For each activity, defines the level of autonomy (agent decides alone, agent proposes + human approves, human decides).

| Activity | Autonomy Level | Human Involvement | Rationale |
|---|---|---|---|
| **Activity 1**: Order ID Extraction | **Fully Autonomous** | None (spot-check 5% weekly) | Deterministic parsing + validation. Errors caught by "order not found" response. |
| **Activity 2**: Route & Scheduled ETA Retrieval | **Fully Autonomous** | None | Database lookup, zero judgment. Errors (missing data) trigger escalation. |
| **Activity 3**: GPS Data Retrieval | **Fully Autonomous** | None | API call + staleness check. Stale data triggers escalation (human decides next step). |
| **Activity 4**: Precision ETA Calculation | **Autonomous with Oversight** | Spot-check 10% weekly for accuracy | Algorithm-based (not judgment), but accuracy depends on data quality (GPS freshness, traffic API). Human reviews accuracy metrics weekly; if <90%, agent logic tuned. |
| **Activity 5**: Response Composition | **Fully Autonomous** | None (templates pre-approved) | Template selection based on confidence level. Human reviewed templates during design phase. |
| **Activity 6**: Escalation | **Fully Autonomous** | Human handles escalated case | Agent decides when to escalate (triggers defined). Human takes over after escalation. |

**Override Mechanism**:
- Human agents can **always** take over from agent mid-interaction (customer replies "AGENT" → immediate escalation)
- During rollout (first 4 weeks), human agents review 20% of agent interactions daily → identify edge cases → tune agent logic

**Governance**:
- **Response templates**: Pre-approved by Customer Ops lead + Sarah Whitmore (cannot be changed by agent without approval)
- **Escalation triggers**: Defined in this document; changes require approval (prevent agent from becoming over-confident and reducing escalations inappropriately)

---

## 6. Escalation Triggers

**Escalation Trigger Matrix**: When agent must hand off to human

| Trigger | Condition | Customer Experience | Human Action |
|---|---|---|---|
| **GPS Stale** | GPS timestamp >30 min old | "Driver location data is outdated. Connecting you with dispatch for a live update." | Contact driver via radio/phone, provide live location update |
| **GPS Unavailable** | Driver App GPS API timeout (>5 sec) or driver location not available | "Unable to reach driver tracking system. Specialist will call you within 30 min." | Investigate GPS system issue, contact driver directly |
| **Order Not Found** | Order ID not in database | "Couldn't find order [order_id]. Please check number, or reply 'AGENT' to verify." | Manual lookup (customer may have provided tracking # instead of order ID, or order from different carrier) |
| **Customer Mismatch** | SMS phone / email doesn't match order customer contact | "For security, I can only provide details to the phone/email on file. Call 0800-XXX to verify." | Security verification (customer may be authorized recipient not on order, e.g., office manager) |
| **Data Inconsistency** | Driver past customer address but delivery not marked complete, or stops_remaining = 0 but delivery_status ≠ DELIVERED | "I'm seeing conflicting data for your order. Connecting you with a specialist." | Investigate data quality issue, contact driver to confirm status |
| **Exception Inquiry** | Customer message contains keywords: "missed," "damaged," "wrong address," "refused," "complaint" | "I see you have a concern about your delivery. Connecting you with a specialist who can help." | Exception handling (out of scope for ETA agent), reassign to exception queue |
| **Customer Demands Callback** | Customer message contains keywords: "agent," "person," "human," "call me," "speak to someone" | "Connecting you with a specialist. Hold time: ~2 minutes." | Human agent handles inquiry (customer preference for human interaction) |
| **Repeat Inquiry (same order, <2 hours)** | Same order ID + customer contact within 2 hours of prior inquiry | "I provided an ETA for this order at [prior_time]. Has something changed? Reply 'YES' for a specialist, or 'UPDATE' for latest ETA." | If customer confirms issue ("YES"), escalate. If just wants update ("UPDATE"), provide latest ETA but flag for accuracy review (agent's prior ETA may have been wrong). |

**Escalation Rate Target**: 10-15% in Months 1-3 (higher during rollout as edge cases discovered), <10% by Month 6

---

## 7. Failure Modes & Mitigation

### Failure Mode 1: Inaccurate ETA (Agent Overconfident)

**Scenario**: Agent provides "HIGH confidence" ETA of 14:00-14:30, but delivery doesn't occur until 16:00 (90 min late)

**Root Cause**:
- GPS data was FRESH but driver encountered unplanned delay (accident, traffic jam not reflected in traffic API, long stop duration at prior customer)
- Agent's avg_stop_duration heuristic (15 min) underestimated actual stop duration (e.g., large B2B delivery requiring unloading, signature, inspection)

**Customer Impact**:
- Customer planned to receive delivery, was not present at 16:00 → missed delivery
- Customer frustrated, calls to complain ("you told me 14:00!")
- Repeat contact (customer calls back asking "where is it NOW?")

**Detection**:
- Weekly accuracy spot-check: Compare agent-provided ETA vs. actual delivery time (logged in CRM)
- If accuracy <90% for 2 consecutive weeks → investigate

**Mitigation**:
1. **Widen ETA window** for lower confidence:
   - HIGH confidence: ±15 min window (current)
   - MEDIUM confidence: ±30 min window (vs. current ±15 min)
   - If stops_remaining >10: automatically downgrade to MEDIUM confidence (many stops = higher uncertainty)
2. **Adjust avg_stop_duration** by route type:
   - Current: 15 min (B2B)
   - If route_type = "DTC" (residential): 5 min
   - If customer_type = "LARGE_B2B" (e.g., warehouse): 25 min (longer unload time)
3. **Real-time traffic monitoring**: If traffic API shows sudden "heavy" traffic after ETA provided, proactively message customer: "Traffic update: Delivery may be delayed by 20-30 min. Updated ETA: 14:30-15:00."
4. **Confidence calibration**: If agent's HIGH confidence ETAs are <95% accurate, retrain confidence threshold (require GPS <10 min fresh for HIGH, not <15 min)

**Residual Risk**: Medium — Cannot eliminate all inaccuracies (unpredictable delays), but can reduce frequency and improve customer communication

---

### Failure Mode 2: GPS Data Stale (Excessive Escalations)

**Scenario**: 40% of precision ETA requests trigger GPS_STALE escalation (>30 min old data) → overwhelms human agents, defeats deflection purpose

**Root Cause**:
- Driver App GPS polling interval too long (e.g., updates every 30 min instead of every 5 min)
- Mobile network coverage gaps (driver in rural area, GPS not transmitted)
- Driver device battery-saving mode (disables GPS)

**Customer Impact**:
- Customer waits 2-11 min for human agent (vs. <30 sec for agent response)
- Customer experience no better than pre-agent baseline

**Detection**:
- Escalation rate monitoring: If GPS_STALE >20% of escalations for 2 consecutive weeks → investigate

**Mitigation**:
1. **Negotiate GPS polling interval** with Dispatch/IT:
   - Current: Unknown (assumed 15-30 min based on SMS artefact: 36 min staleness)
   - Target: 5-10 min polling interval
   - Trade-off: Battery life vs. data freshness (may require driver device upgrades or vehicle charging docks)
2. **Adjust staleness threshold** based on route progress:
   - If stops_remaining >5 (driver far from customer): accept GPS up to 30 min stale (lower precision, but still useful)
   - If stops_remaining ≤3 (driver near customer): require GPS <15 min stale (precision critical)
3. **Fallback to scheduled window** with explanation:
   - If GPS stale: "Driver location data is [staleness] min old. Based on scheduled route, your delivery is expected between [scheduled_eta_start]-[scheduled_eta_end]. For a live update, reply 'AGENT'."
   - Avoids escalation for every stale GPS case; customer can self-select whether scheduled window is acceptable
4. **Driver incentives**: Encourage drivers to keep GPS enabled (gamification: "GPS uptime score" affects driver performance bonus)

**Residual Risk**: Medium — GPS staleness partially infrastructure-dependent (mobile network coverage), cannot fully control

---

### Failure Mode 3: Customer Dissatisfaction with Agent Interaction (Prefers Human)

**Scenario**: Customer receives agent response, but replies "I want to speak to a person" — feels agent is impersonal or doesn't trust agent's ETA

**Root Cause**:
- Customer preference for human interaction (especially older demographics, high-value B2B customers)
- Agent response tone perceived as robotic (lacks empathy, doesn't acknowledge frustration)
- Customer has prior bad experience with automation (chatbot, IVR) and distrusts AI

**Customer Impact**:
- Customer escalates to human agent (defeats deflection purpose for this customer)
- Customer satisfaction drops if agent doesn't quickly recognize "I want a person" and escalates

**Detection**:
- CSAT surveys: If agent interactions score <4.0/5 for 2 consecutive weeks → investigate sentiment
- Escalation analysis: If "CUSTOMER_DEMANDS_CALLBACK" is >15% of escalations → tone/trust issue

**Mitigation**:
1. **Immediate escalation on keywords**: If customer message contains "agent," "person," "human," "call me," "speak to someone" → escalate immediately, no friction
2. **Empathy in templates**: Revise templates to acknowledge customer emotion:
   - Before: "Your order is estimated for delivery between 14:00-14:30."
   - After: "I understand you're waiting for your delivery. Based on current driver location, it's estimated between 14:00-14:30. I'll notify you when the driver is nearby."
3. **Opt-out mechanism**: Allow customers to opt out of agent interactions:
   - SMS: Reply "NOAGENT" → future inquiries routed directly to human queue
   - Web portal: Toggle setting "Always connect me with a person"
4. **VIP customer segmentation**: Identify high-value customers (contract_type = "B2B_VOLUME", credit_limit >£50K) → automatically route to human agent (no agent interaction)
   - Trade-off: Lower deflection rate, but preserves VIP customer satisfaction

**Residual Risk**: Low-Medium — Some customers will always prefer human; agent should make escalation frictionless

---

### Failure Mode 4: Agent Over-Escalates (False Positives)

**Scenario**: Agent escalates 25% of inquiries (vs. target 10-15%) due to overly conservative escalation triggers (e.g., GPS 25 min stale → escalate, but 25 min is still usable)

**Root Cause**:
- Escalation triggers too strict (30-min staleness threshold too low)
- Agent interprets ambiguous customer messages as exception inquiries (false positive on keyword matching)

**Customer Impact**:
- Customer routed to human agent unnecessarily → longer wait time (human agents busy handling escalations)
- Defeats deflection purpose

**Detection**:
- **Escalation precision metric**: Human agents review escalations weekly; mark as "needed escalation" or "could have been handled by agent"
- If precision <85% for 2 consecutive weeks → escalation triggers too loose

**Mitigation**:
1. **Relax staleness threshold** based on route progress (as described in Failure Mode 2)
2. **Improve keyword matching** for exception inquiries:
   - Before: Any message containing "missed" → escalate (exception inquiry)
   - After: "missed" + "delivery" in same sentence → escalate; "missed" + "you" (e.g., "I missed your last message") → do NOT escalate
3. **A/B test escalation thresholds**: Randomly assign 20% of inquiries to relaxed thresholds (e.g., 45-min staleness OK) → measure accuracy impact → adjust thresholds if no accuracy drop

**Residual Risk**: Low — Escalation precision tunable via threshold adjustment

---

### Failure Mode 5: System Integration Failure (GPS API Unavailable)

**Scenario**: Driver App GPS API experiences outage (service down, network issue, API rate limit exceeded) → 100% of precision ETA requests fail → all escalate to human

**Root Cause**:
- GPS API infrastructure not highly available (no redundancy, SLA <99%)
- API rate limit too low (agent exceeds quota during peak hours)
- Network partition (agent can reach CRM but not Driver App backend)

**Customer Impact**:
- Agent provides scheduled window only (falls back gracefully), but customer expects precision → customer frustration
- Escalation spike → human agents overwhelmed

**Detection**:
- **API availability monitoring**: Alert if GPS API availability <98% for 1 hour
- **Escalation spike detection**: Alert if escalations >30% for 1 hour (vs. baseline 10-15%)

**Mitigation**:
1. **Graceful degradation**:
   - If GPS API unavailable, agent provides scheduled window + explanation: "Driver location system is temporarily unavailable. Your delivery is scheduled between [scheduled_eta_start]-[scheduled_eta_end]. I'll provide an update as soon as the system is back online."
   - Do NOT escalate on every GPS API failure; only escalate if customer explicitly requests callback
2. **API SLA negotiation**:
   - Current: Unknown (GPS API availability SLA not documented in artefacts)
   - Target: 99.5% availability, 5-sec timeout, 1000 requests/min rate limit
3. **Redundancy**:
   - If Driver App GPS unavailable, fallback to Dispatch Console GPS query (if API exists) → secondary data source
4. **Caching**:
   - Cache last-known GPS location for 10 min → if API unavailable, use cached location + warn customer "based on last known location [time]"

**Residual Risk**: Medium — System availability partially outside agent's control; graceful degradation reduces customer impact

---

## 8. Data & System Dependencies

### Required System Integrations

| System | Purpose | API/Access Method | Data Latency | Availability Requirement | Failure Handling |
|---|---|---|---|---|---|
| **CRM (Salesforce)** | Order lookup, customer contact, case logging | REST API (read/write) | Real-time | >99.5% | Critical — if CRM unavailable, agent cannot function. Escalate all inquiries to phone queue with apology message. |
| **Driver App (GPS Backend)** | Driver location, route progress | REST API (read-only) | <15 min (target 5-10 min polling) | >99% | High — if unavailable, fallback to scheduled window (graceful degradation). |
| **Traffic API (Google Maps / Waze)** | Traffic conditions, travel time | REST API (read-only) | Real-time | >99% | Medium — if unavailable, fallback to non-traffic distance calculation (warn customer). |
| **Order Database** | Order details, route assignment, delivery status | SQL query (read-only) | Real-time | >99.5% | Critical — if unavailable, agent cannot function. Escalate all inquiries. |
| **Route Database** | Route details, driver assignment | SQL query (read-only) | Real-time | >99.5% | High — if unavailable, agent can still provide order-level ETA (scheduled window), but cannot calculate precision ETA. |

### Data Schema Requirements

**CRM Orders Table** (read access):
```sql
CREATE TABLE orders (
  order_id VARCHAR(20) PRIMARY KEY,  -- e.g., "AX-771-3344"
  customer_id VARCHAR(20) NOT NULL,  -- FK to customers table
  route_id VARCHAR(20),              -- FK to routes table, nullable if not yet assigned
  delivery_address TEXT NOT NULL,
  delivery_latitude DECIMAL(10, 7),  -- geocoded address
  delivery_longitude DECIMAL(10, 7),
  scheduled_eta_start TIME,          -- scheduled delivery window start
  scheduled_eta_end TIME,            -- scheduled delivery window end
  delivery_status ENUM('PENDING', 'OUT_FOR_DELIVERY', 'DELIVERED', 'CANCELLED', 'RETURNED'),
  delivery_timestamp TIMESTAMP,      -- actual delivery time (null until delivered)
  recipient_name VARCHAR(100),       -- who signed for delivery
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_order_customer ON orders(customer_id);
CREATE INDEX idx_order_route ON orders(route_id);
CREATE INDEX idx_order_status ON orders(delivery_status);
```

**CRM Customers Table** (read access):
```sql
CREATE TABLE customers (
  customer_id VARCHAR(20) PRIMARY KEY,
  customer_name VARCHAR(200) NOT NULL,
  contact_phone VARCHAR(20),         -- for SMS channel matching
  contact_email VARCHAR(200),        -- for email channel matching
  contract_type ENUM('B2B_STANDARD', 'B2B_VOLUME', 'DTC'),
  credit_limit DECIMAL(10, 2),
  account_manager_id VARCHAR(20),
  status ENUM('ACTIVE', 'INACTIVE', 'CHURNED')
);
```

**Routes Table** (read access):
```sql
CREATE TABLE routes (
  route_id VARCHAR(20) PRIMARY KEY,
  route_code VARCHAR(10) NOT NULL,   -- e.g., "R-028"
  route_date DATE NOT NULL,
  driver_id VARCHAR(20),              -- FK to drivers table
  vehicle_id VARCHAR(20),
  depot VARCHAR(50),
  route_type ENUM('B2B', 'DTC'),
  total_stops INT,
  completed_stops INT,
  status ENUM('PLANNED', 'IN_PROGRESS', 'COMPLETED')
);
```

**Driver App GPS API** (read-only REST endpoint):
```http
GET /api/driver-location?driver_id={driver_id}&route_id={route_id}
Authorization: Bearer {api_token}
Response 200 OK:
{
  "driver_id": "D-042",
  "route_id": "R-028",
  "latitude": 51.6577,
  "longitude": -0.3961,
  "timestamp": "2026-04-14T10:48:33Z",
  "location_name": "Watford",
  "stops_completed": 8,
  "stops_remaining": 14,
  "vehicle_id": "V-180"
}
Response 404: {"error": "Driver location not available"}
Response 500: {"error": "GPS system unavailable"}
```

**CRM Cases Table** (write access for logging):
```sql
CREATE TABLE cases (
  case_id VARCHAR(30) PRIMARY KEY,   -- e.g., "ETA-2026-04-14-003344"
  order_id VARCHAR(20),               -- FK to orders table
  customer_id VARCHAR(20),            -- FK to customers table
  case_type ENUM('ETA_INQUIRY', 'ETA_INQUIRY_ESCALATION', 'BILLING_DISPUTE', 'DELIVERY_EXCEPTION'),
  inquiry_timestamp TIMESTAMP,
  response_timestamp TIMESTAMP,
  response_type ENUM('SCHEDULED_WINDOW', 'PRECISION_ETA', 'DELIVERED_STATUS', 'ESCALATED'),
  eta_provided VARCHAR(20),           -- e.g., "14:00-14:30"
  confidence ENUM('HIGH', 'MEDIUM', 'LOW'),
  agent_handled BOOLEAN,              -- true if agent handled, false if human
  escalated BOOLEAN,
  escalation_reason ENUM('GPS_STALE', 'GPS_UNAVAILABLE', 'ORDER_NOT_FOUND', 'CUSTOMER_MISMATCH', 'DATA_INCONSISTENCY', 'EXCEPTION_INQUIRY', 'CUSTOMER_DEMANDS_CALLBACK'),
  actual_delivery_time TIMESTAMP,     -- backfilled after delivery for accuracy spot-check
  eta_accuracy_sec INT,               -- difference between eta_provided (midpoint) and actual_delivery_time, in seconds
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_case_order ON cases(order_id);
CREATE INDEX idx_case_customer ON cases(customer_id);
CREATE INDEX idx_case_timestamp ON cases(inquiry_timestamp);
```

---

## 9. Non-Functional Requirements

### Performance

| Metric | Target | Constraint |
|---|---|---|
| **Response Time (p50)** | <30 sec (end-to-end: inquiry received → response sent) | Includes API latency (GPS, traffic), calculation time, message delivery |
| **Response Time (p95)** | <2 min | Allows for traffic API retries, GPS staleness re-checks |
| **Agent Compute Time** | <5 sec (p95) | Excludes external API latency (out of agent's control) |
| **Throughput** | 10 concurrent inquiries/sec (peak load) | Estimated: 400 inquiries/day = 0.005 inquiries/sec avg; peak 10x = 0.05 inquiries/sec. But buffer for 100x peak (Q4, promo periods) = 5 inquiries/sec sustained, 10 burst. |
| **API Timeout** | 5 sec (GPS API), 3 sec (Traffic API) | Escalate if timeout exceeded (don't wait indefinitely) |

### Scalability

- **Horizontal scaling**: Agent must be stateless (no session memory) → can deploy multiple instances behind load balancer
- **Database connection pooling**: CRM queries must use connection pool (max 100 connections per instance)
- **API rate limit management**: GPS API and Traffic API have rate limits → agent must respect limits, queue requests if needed (but prefer escalation if queue >2 min)

### Availability

- **Agent uptime**: >99% (target 99.5%) — measured as "agent response vs. escalation due to agent failure (not data failure)"
- **Dependency failures**: Agent must handle gracefully (provide scheduled window if GPS unavailable, escalate if CRM unavailable)

### Security

1. **Customer Identity Verification**:
   - SMS: Customer phone number must match order contact_phone (no cross-customer data leakage)
   - Email: Customer email must match order contact_email
   - Web portal: User must be authenticated (session token valid) and customer_id matches order
   - **If mismatch**: Do NOT provide order details; escalate with security message

2. **Data Privacy** (GDPR Compliance):
   - Agent must NOT log personally identifiable information (PII) beyond what's required for audit trail
   - CRM case logs: Include customer_id (internal), NOT customer name, address, phone (unless explicitly required for audit)
   - SMS/email responses: Do NOT include sensitive info (credit card, payment details) — only order status, ETA

3. **API Authentication**:
   - GPS API: Bearer token (rotated quarterly, stored in secrets manager, never logged)
   - Traffic API: API key (rotated annually, stored in secrets manager)
   - CRM: OAuth 2.0 (service account with read/write scopes: orders.read, customers.read, cases.write)

4. **Rate Limiting** (DDoS Protection):
   - Per-customer rate limit: 5 inquiries/hour for same order_id (prevents spam/abuse)
   - If exceeded: "You've reached the inquiry limit for this order. For immediate assistance, call 0800-XXX-XXXX."

### Audit & Compliance

- **Audit Trail**: All agent interactions logged to CRM (inquiry, response, escalation, API calls, timestamps)
- **Accuracy Spot-Check**: 10% of agent-provided ETAs sampled weekly, compared to actual delivery time → accuracy metric calculated
- **Human Review**: 5% of agent interactions reviewed weekly by Customer Ops team lead → identify edge cases, tune agent logic

---

## 10. Implementation Phases

### Phase 1A: MVP (Months 1-2)

**Scope**: Standard ETA Lookup (Activity 1, 2, 5) — Scheduled Window Only

**Deliverables**:
- Agent handles SMS inquiries (single channel)
- Provides order lookup + scheduled ETA window
- Logs interactions to CRM
- Escalates if order not found or customer mismatch

**Success Criteria**:
- 50% deflection rate (200/400 inquiries/day agent-handled)
- Response time <1 min (p50)
- CSAT >3.8/5

**Risk**: Low — No GPS API dependency, no precision calculation complexity

---

### Phase 1B: Full Feature Set (Month 3)

**Scope**: Add Precision ETA Calculation (Activities 3, 4) + Multi-Channel (Email, Web Portal)

**Deliverables**:
- GPS API integration (Driver App backend)
- Traffic API integration (Google Maps)
- Precision ETA calculation (stops remaining, traffic-adjusted)
- Email + web portal support

**Success Criteria**:
- 85% deflection rate (340/400 inquiries/day agent-handled)
- Response time <30 sec (p50), <2 min (p95)
- ETA accuracy >90% (±30 min tolerance)
- CSAT >4.0/5

**Risk**: Medium — GPS API dependency (requires Dispatch team approval + API access)

---

### Phase 1C: Optimization (Month 4)

**Scope**: Proactive ETA Updates (Out of Scope for Gate 2, but planned)

**Deliverables**:
- Agent monitors delivery progress, sends unsolicited updates ("Your delivery is 30 min away")
- Reduces inbound inquiries (customer notified before they call)

**Success Criteria**:
- 95% deflection rate (380/400 inquiries/day agent-handled)
- 20% reduction in inbound inquiry volume (customers don't need to ask because they're proactively notified)

**Risk**: Low — Builds on Phase 1B infrastructure

---

## 11. Buildability Checklist

This document is precise enough for an AI coding agent to build from if:

- [x] **Entity definitions complete**: order, customer, route, case (tables, columns, types, constraints defined)
- [x] **State machines defined**: order delivery_status (PENDING → OUT_FOR_DELIVERY → DELIVERED), case status, escalation flow
- [x] **Validation rules explicit**: Order ID regex patterns, GPS staleness thresholds (15 min, 30 min), rate limits (5 inquiries/hour/order)
- [x] **API contracts specified**: GPS API request/response format, Traffic API request/response, CRM case logging format
- [x] **Error handling complete**: All failure modes documented (GPS unavailable, order not found, customer mismatch, data inconsistency), escalation triggers defined
- [x] **Integration constraints explicit**: Aurum not relevant (ETA agent doesn't touch billing), GPS API is blocker (Phase 1A works without it, Phase 1B requires it)
- [x] **Escalation patterns defined**: 7 escalation reasons, escalation process (create CRM case, notify customer, hold message)
- [x] **Success metrics testable**: Deflection rate >85%, response time <30 sec, ETA accuracy >90%, CSAT >4.0/5 (all measurable)

**Buildability Score**: **9/10** — An AI coding agent can begin building with high confidence. Missing: Exact CRM table names (assumed "orders," "customers," "routes," "cases" but may differ), exact GPS API endpoint URL (placeholder "/api/driver-location").

**Next Step for Coding Agent**: Confirm CRM table names + GPS API endpoint with Sarah/IT team, then proceed to Activity 1 implementation (order ID extraction + validation).

---

## 12. Conclusion

This Agent Purpose Document defines the **ETA Inquiry Agent** as a **fully agentic** (for standard lookups) and **agent-led** (for precision ETAs) solution to deflect 90% of ETA inquiries (360/400 cases/day), freeing 66 hours/day (8.8 FTE equivalent) for Customer Operations.

The agent is designed to:
- **Operate autonomously** within well-defined guardrails (escalation triggers)
- **Handle GPS/Traffic API failures gracefully** (fallback to scheduled window, not blind escalation)
- **Maintain governance** (audit trail, accuracy spot-checks, human oversight)
- **Respect constraints** (GPS API dependency, Aurum not involved, customer security verification)

**Implementation is phased** (1A: scheduled window only, 1B: precision ETAs, 1C: proactive updates) to prove value quickly (Phase 1A: 2 months) while building toward full capability (Phase 1B: Month 3).

**Success is measurable**: Deflection rate, response time, ETA accuracy, CSAT — all tracked weekly, reviewed monthly, benchmarked against competitor results (£1.2M savings, proportional target £600K by Year 2).

This document is **ready for handoff to implementation team** (internal or vendor) and **buildable by AI coding agent** with minimal clarifying questions.
