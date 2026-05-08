# Demo Application Design: ETA Inquiry Agent Prototype

## Purpose

Browser-based Python demonstration application showcasing the proposed ETA Inquiry Agent for Apex Distribution. The demo uses **synthetic data** (no real system integrations) to illustrate:

1. **Fully Agentic** capability (standard ETA lookup)
2. **Agent-Led with Oversight** capability (precision ETA calculation)
3. **Escalation handling** (order not found, GPS stale, customer demands callback)
4. **Decision transparency** (show agent logic, confidence levels, delegation boundaries)
5. **Performance comparison** (agent response time vs. baseline human handling)

---

## Demo Scenarios

### Scenario 1: Standard ETA Lookup (Fully Agentic)
**User Action**: Customer enters order ID `AX-771-3344`  
**Agent Response**: 
- Instant lookup (<1 sec)
- "Your order #AX-771-3344 is out for delivery on route 028. Scheduled delivery window: 13:00-17:00 today."
- **UI Shows**: Green indicator "Fully Autonomous", no human intervention required

### Scenario 2: Precision ETA Calculation (Agent-Led)
**User Action**: Customer clicks "Need more specific time"  
**Agent Response**:
- Queries mock GPS data (driver location: Watford, 10:48 AM)
- Calculates: 3 stops remaining × 15 min + 28 min travel time + 10 min traffic buffer = 83 min
- "Based on current driver location (Watford, last updated 36 min ago), estimated delivery: 14:00-14:30."
- **UI Shows**: Yellow indicator "GPS data staleness: 36 min (acceptable threshold <30 min exceeded, medium confidence)", option to "Escalate to human"

### Scenario 3: Escalation - GPS Stale
**User Action**: Customer enters order ID `AX-441-8821`  
**Agent Response**:
- GPS data is 52 minutes stale (exceeds 30-min threshold)
- "I'm unable to provide a precise ETA due to outdated location data (last updated 52 min ago). Connecting you with a specialist who can contact the driver directly. Hold time: ~2 minutes."
- **UI Shows**: Red indicator "Escalation triggered: GPS staleness >30 min", routes to human queue

### Scenario 4: Escalation - Order Not Found
**User Action**: Customer enters order ID `XX-999-9999`  
**Agent Response**:
- "I couldn't find order XX-999-9999. Please check the order number and try again. Reply 'AGENT' if you need assistance."
- **UI Shows**: Orange indicator "Order validation failed", option to escalate

### Scenario 5: Side-by-Side Comparison
**UI Feature**: Split screen showing:
- **Left**: Current state (human agent) — 4-11 min response time, 4-hour ETA window
- **Right**: Agent state — <30 sec response time, ±30 min ETA window
- Deflection rate: 90% (360/400 cases handled autonomously)

---

## Technical Architecture

### Tech Stack
- **Backend**: Flask (Python 3.9+)
- **Frontend**: HTML5, CSS3 (Tailwind CSS), Vanilla JavaScript
- **Data Layer**: SQLite (mock orders, routes, GPS data)
- **AI Integration**: Optional Claude API for NLP (or hardcoded rule-based logic for demo simplicity)
- **Deployment**: Local dev server (`flask run`) — no cloud dependencies

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser (Customer View)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ ETA Inquiry  │  │ Admin Panel  │  │ Comparison   │      │
│  │ Form         │  │ (Agent Logic)│  │ View         │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │ HTTP/JSON
┌─────────────────────────────────────────────────────────────┐
│                   Flask Backend (Python)                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Routes:                                              │  │
│  │  - POST /api/inquire (process order ID)              │  │
│  │  - POST /api/precision-eta (GPS calculation)         │  │
│  │  - POST /api/escalate (human handoff)                │  │
│  │  - GET /api/demo-stats (metrics for comparison)      │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Agent Logic Engine:                                  │  │
│  │  - Order ID extraction & validation                   │  │
│  │  - ETA calculation (distance, traffic, stops)        │  │
│  │  - Escalation trigger detection                      │  │
│  │  - Confidence scoring                                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │ SQLite queries
┌─────────────────────────────────────────────────────────────┐
│                    Mock Data Layer (SQLite)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ orders.db    │  │ routes.db    │  │ gps_logs.db  │      │
│  │ (400 orders) │  │ (28 routes)  │  │ (GPS pings)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## File Structure

```
demo_app/
├── app.py                          # Flask application entry point
├── requirements.txt                # Python dependencies
├── README.md                       # Setup and run instructions
├── data/
│   ├── mock_orders.json           # 400 sample orders (pre-generated)
│   ├── mock_routes.json           # 28 routes with driver assignments
│   ├── mock_gps.json              # GPS pings (timestamped locations)
│   └── init_db.py                 # Script to populate SQLite from JSON
├── agent/
│   ├── __init__.py
│   ├── eta_calculator.py          # ETA calculation logic
│   ├── escalation_engine.py       # Escalation trigger detection
│   └── order_validator.py         # Order ID extraction & validation
├── static/
│   ├── css/
│   │   └── styles.css             # Custom styles (Tailwind-based)
│   └── js/
│       ├── inquiry_form.js        # Customer inquiry UI logic
│       └── admin_panel.js         # Admin panel (agent decision transparency)
└── templates/
    ├── index.html                 # Customer inquiry page
    ├── admin.html                 # Admin panel (decision log viewer)
    └── comparison.html            # Side-by-side comparison view
```

---

## Key Features

### 1. Customer Inquiry Interface (`index.html`)
**UI Components**:
- **Input**: Order ID text field (e.g., `AX-771-3344`)
- **Primary Action**: "Check Delivery Status" button
- **Response Area**: 
  - Agent response message (styled like SMS bubble)
  - Response time indicator (e.g., "Responded in 0.8 sec")
  - Delegation archetype badge (Green: Fully Autonomous, Yellow: Agent-Led, Red: Escalated)
- **Secondary Action**: "Need more specific time?" button (triggers precision ETA)
- **Escalation Option**: "Speak with someone" button (visible after escalation trigger)

**Example Flow**:
```
User enters: AX-771-3344
Agent (0.8 sec): "Your order is on route 028. Scheduled: 13:00-17:00."
[Badge: Fully Autonomous ✓]
[Button: Need more specific time?]

User clicks: "Need more specific time?"
Agent (1.2 sec): "Driver is in Watford (GPS 36 min old). Estimated: 14:00-14:30. Confidence: Medium."
[Badge: Agent-Led (GPS staleness) ⚠️]
[Button: Speak with someone]
```

### 2. Admin Panel (`admin.html`)
**Purpose**: Show agent decision-making transparency (for stakeholders like Sarah Whitmore)

**UI Components**:
- **Decision Log Table**: 
  | Timestamp | Order ID | Action Taken | Delegation Level | Response Time | Escalated? |
  |-----------|----------|--------------|------------------|---------------|------------|
  | 11:14:32  | AX-771-3344 | Standard lookup | Fully Agentic | 0.8 sec | No |
  | 11:15:01  | AX-441-8821 | GPS query | Agent-Led | 1.2 sec | Yes (GPS stale) |

- **Escalation Triggers Summary**: 
  - GPS stale (>30 min): 12 cases today
  - Order not found: 3 cases today
  - Customer demanded callback: 5 cases today

- **Confidence Distribution**: 
  - High confidence (>90%): 340 cases (85%)
  - Medium confidence (70-90%): 48 cases (12%)
  - Low confidence (<70% → escalated): 12 cases (3%)

### 3. Comparison View (`comparison.html`)
**Purpose**: Show business case (baseline vs. agent)

**UI Layout**: Split-screen comparison

| Metric | Current (Human Agent) | With Agent | Improvement |
|--------|----------------------|------------|-------------|
| **Response Time (p50)** | 4-11 min | <30 sec | **96% faster** |
| **Response Time (p95)** | 15-20 min | <2 min | **90% faster** |
| **ETA Precision** | 4-hour window | ±30 min window | **87% more precise** |
| **Deflection Rate** | 0% (all human-handled) | 90% (360/400) | **66 hrs/day freed** |
| **Escalation Rate** | N/A | 10% (40/400) | 40 cases to human |
| **Customer Satisfaction** | Unknown (baseline) | 4.2/5 (simulated) | +0.2 vs. industry avg |

**Visual**: Bar charts comparing response times, pie chart showing deflection vs. escalation

---

## Mock Data Schema

### orders.json (400 sample orders)
```json
{
  "order_id": "AX-771-3344",
  "customer_name": "M.K.",
  "customer_phone": "+44 7700 900123",
  "delivery_address": "45 High Street, London NW1 2BX",
  "route_id": "028",
  "scheduled_eta_start": "13:00",
  "scheduled_eta_end": "17:00",
  "order_status": "OUT_FOR_DELIVERY",
  "package_value": 120.50,
  "created_at": "2026-05-05T08:23:00Z"
}
```

### routes.json (28 routes)
```json
{
  "route_id": "028",
  "route_code": "028",
  "driver_id": "DRV-042",
  "driver_name": "Mark Petrov",
  "vehicle_id": "VEH-128",
  "depot": "Birmingham East",
  "total_stops": 12,
  "completed_stops": 8,
  "remaining_stops": 4,
  "current_location": {
    "lat": 51.6575,
    "lon": -0.3961,
    "location_name": "Watford",
    "timestamp": "2026-05-06T10:48:00Z"
  }
}
```

### gps_logs.json (GPS pings)
```json
{
  "route_id": "028",
  "timestamp": "2026-05-06T10:48:00Z",
  "lat": 51.6575,
  "lon": -0.3961,
  "location_name": "Watford",
  "speed_mph": 35,
  "heading": 142
}
```

---

## Agent Logic Implementation

### ETA Calculation Algorithm (`agent/eta_calculator.py`)

```python
def calculate_precision_eta(order_id: str) -> dict:
    """
    Calculate precision ETA based on GPS location, traffic, remaining stops.
    Returns: {
        'eta_start': datetime,
        'eta_end': datetime,
        'confidence': float (0-1),
        'gps_staleness_min': int,
        'escalation_triggered': bool,
        'escalation_reason': str or None
    }
    """
    order = get_order(order_id)
    route = get_route(order['route_id'])
    latest_gps = get_latest_gps(route['route_id'])
    
    # Check GPS staleness
    gps_age_min = (datetime.now() - latest_gps['timestamp']).seconds // 60
    
    if gps_age_min > 30:
        return {
            'escalation_triggered': True,
            'escalation_reason': f'GPS data stale ({gps_age_min} min > 30 min threshold)',
            'confidence': 0.0
        }
    
    # Calculate travel time from current location to delivery address
    distance_km = haversine_distance(
        latest_gps['lat'], latest_gps['lon'],
        order['delivery_address_lat'], order['delivery_address_lon']
    )
    
    # Traffic API simulation (mock: add 10-20% buffer)
    traffic_multiplier = 1.15  # Moderate traffic
    travel_time_min = (distance_km / 50) * 60 * traffic_multiplier  # 50 km/h avg city speed
    
    # Add stop duration (remaining stops × 15 min avg)
    stop_duration_min = route['remaining_stops'] * 15
    
    # Total ETA = travel time + stop duration
    total_eta_min = travel_time_min + stop_duration_min
    
    eta_start = datetime.now() + timedelta(minutes=total_eta_min - 15)  # ±15 min window
    eta_end = datetime.now() + timedelta(minutes=total_eta_min + 15)
    
    # Confidence scoring
    confidence = 0.95 - (gps_age_min / 30) * 0.25  # Degrade confidence as GPS ages
    
    return {
        'eta_start': eta_start,
        'eta_end': eta_end,
        'confidence': confidence,
        'gps_staleness_min': gps_age_min,
        'escalation_triggered': False,
        'calculation_details': {
            'distance_km': distance_km,
            'travel_time_min': travel_time_min,
            'stop_duration_min': stop_duration_min,
            'traffic_multiplier': traffic_multiplier
        }
    }
```

### Escalation Trigger Detection (`agent/escalation_engine.py`)

```python
def check_escalation_triggers(order_id: str, user_message: str = None) -> dict:
    """
    Check if inquiry should be escalated to human.
    Returns: {'escalate': bool, 'reason': str, 'priority': str}
    """
    triggers = []
    
    # Trigger 1: Order not found
    order = get_order(order_id)
    if not order:
        return {
            'escalate': True,
            'reason': 'Order ID not found in system',
            'priority': 'MEDIUM'
        }
    
    # Trigger 2: GPS stale (>30 min)
    route = get_route(order['route_id'])
    latest_gps = get_latest_gps(route['route_id'])
    gps_age_min = (datetime.now() - latest_gps['timestamp']).seconds // 60
    
    if gps_age_min > 30:
        triggers.append({
            'type': 'GPS_STALE',
            'detail': f'{gps_age_min} min > 30 min threshold',
            'priority': 'HIGH'
        })
    
    # Trigger 3: Customer demands callback (NLP detection)
    if user_message and any(keyword in user_message.lower() for keyword in 
                            ['speak', 'call me', 'talk to someone', 'agent', 'human']):
        triggers.append({
            'type': 'CALLBACK_REQUESTED',
            'detail': 'Customer explicitly requested human contact',
            'priority': 'HIGH'
        })
    
    # Trigger 4: High-value order + ambiguous status
    if order['package_value'] > 500 and order['order_status'] == 'EXCEPTION':
        triggers.append({
            'type': 'HIGH_VALUE_EXCEPTION',
            'detail': f'£{order["package_value"]} package in exception state',
            'priority': 'URGENT'
        })
    
    if triggers:
        return {
            'escalate': True,
            'reason': triggers[0]['type'],
            'priority': triggers[0]['priority'],
            'all_triggers': triggers
        }
    
    return {'escalate': False, 'reason': None, 'priority': None}
```

---

## Demo Deployment

### Setup Instructions

1. **Install Python dependencies**:
   ```bash
   cd demo_app
   pip install -r requirements.txt
   ```

2. **Initialize mock database**:
   ```bash
   python data/init_db.py
   ```
   This populates SQLite with 400 mock orders, 28 routes, and GPS pings.

3. **Run Flask development server**:
   ```bash
   flask run
   ```
   Opens on `http://localhost:5000`

4. **Access demo views**:
   - Customer inquiry: `http://localhost:5000/`
   - Admin panel: `http://localhost:5000/admin`
   - Comparison view: `http://localhost:5000/comparison`

### Demo Script (5-Minute Walkthrough)

**Minute 0-1: Introduction**
> "This is a working demo of the ETA Inquiry Agent for Apex Distribution. It uses synthetic data—no real system integrations—to show how the agent would handle customer inquiries."

**Minute 1-2: Scenario 1 (Fully Agentic)**
> "Let's simulate a customer asking 'Where is my order?' I'll enter order AX-771-3344..."
> [Agent responds in <1 sec with scheduled window]
> "Notice the green badge: Fully Autonomous. No human intervention needed. This is what we expect for 90% of inquiries."

**Minute 2-3: Scenario 2 (Precision ETA)**
> "Now the customer wants a more specific time. I'll click 'Need more specific time?'..."
> [Agent queries GPS, calculates, shows 14:00-14:30]
> "Yellow badge: Agent-Led. The GPS data is 36 minutes old—acceptable but not ideal. Agent shows medium confidence. Customer can escalate if unsatisfied."

**Minute 3-4: Scenario 3 (Escalation)**
> "Let's try an order where GPS is too stale. Order AX-441-8821..."
> [Agent detects GPS >30 min stale, escalates]
> "Red badge: Escalation triggered. Agent explains why it can't provide accurate ETA and routes to human queue. This is the 10% we expect to escalate."

**Minute 4-5: Admin Panel & Comparison**
> "Here's the admin panel where Sarah can see agent decisions in real-time. Each inquiry logged with delegation level, response time, escalation reason."
> [Switch to comparison view]
> "Side-by-side: current state (4-11 min, 4-hour window) vs. agent (30 sec, ±30 min window). This is where the £301K annual savings comes from—deflecting 90% of inquiries at 10x faster response."

---

## Key Demonstration Points

### 1. Delegation Transparency
- Every agent decision shows which archetype applied (Fully Agentic, Agent-Led, Human-Only)
- Decision rationale visible in admin panel (why escalated, what triggered it)
- Sarah can audit agent behavior post-interaction

### 2. Escalation Governance
- Clear escalation triggers (GPS stale, order not found, callback requested)
- Escalations include context (agent's partial analysis, customer request, data quality issue)
- Human receives prepared summary, not cold handoff

### 3. Confidence Scoring
- Agent communicates uncertainty (High/Medium/Low confidence)
- Confidence degrades with GPS staleness, missing data
- Customer sees "medium confidence" → option to escalate proactively

### 4. Performance vs. Baseline
- Live metrics: response time, deflection rate, escalation rate
- Comparison view validates business case (£301K savings, 66 hrs/day freed)
- Sarah sees "prove it works" data in real-time

### 5. No Integration Complexity
- Demo runs standalone (no CRM, Driver App, Aurum dependencies)
- Proves concept before expensive system integration
- Low-risk proof-of-concept Sarah can test with her team

---

## Technical Requirements

### Python Dependencies (`requirements.txt`)
```
Flask==3.0.0
Flask-CORS==4.0.0
geopy==2.4.1           # For distance calculations (haversine)
python-dateutil==2.8.2 # For datetime parsing
```

### Optional Enhancements (Phase 2)
- **Claude API Integration**: Use Claude Haiku for NLP (order ID extraction, intent detection)
- **WebSocket**: Real-time updates when driver location changes
- **Multi-Channel**: Simulate SMS, email, web portal channels in one interface
- **Analytics Dashboard**: Plot deflection rate, response time trends over simulated 7-day period

---

## Success Criteria for Demo

Demo is successful if it demonstrates:
1. **Agent handles 90% of inquiries autonomously** (standard lookup + precision ETA)
2. **Escalation triggers work correctly** (GPS stale, order not found, callback requested)
3. **Decision transparency** (admin panel shows agent reasoning)
4. **Response time improvement** (<30 sec vs. 4-11 min baseline)
5. **Delegation archetypes visible** (Fully Agentic, Agent-Led, Escalated)
6. **No real system dependencies** (standalone, runs on laptop)

Sarah Whitmore's key concern (from scenario): *"I've watched two prior automation initiatives fail. I'm skeptical of chatbots, but open to something that actually works."*

**Demo addresses this**:
- Shows transparent decision-making (not black-box chatbot)
- Demonstrates escalation safety net (agent knows when it doesn't know)
- Proves performance improvement with synthetic data (de-risks before real integration)
- Runs standalone (no disruption to live systems during pilot)

---

## Next Steps (Implementation Plan)

1. **Create project structure** (`demo_app/` directory)
2. **Generate mock data** (400 orders, 28 routes, GPS logs)
3. **Build Flask backend** (routes, agent logic, SQLite queries)
4. **Build frontend UI** (inquiry form, admin panel, comparison view)
5. **Test demo scenarios** (standard lookup, precision ETA, escalations)
6. **Write README** (setup instructions, demo script)
7. **Package for handoff** (zip file, or GitHub repo link)

**Estimated Build Time**: 4-6 hours for working demo  
**Tech Skill Required**: Intermediate Python (Flask), basic HTML/CSS/JS

This demo becomes **Deliverable #8** (optional, not required by Gate 2) but demonstrates FDE principle: *"Show, don't just tell."* Sarah can interact with the agent, see escalations in action, and validate the business case with her own test queries.
