# ETA Inquiry Agent - Demo Application

Browser-based Python demonstration of the proposed ETA Inquiry Agent for Apex Distribution. Uses synthetic data to showcase agent capabilities, delegation archetypes, and escalation logic.

## Quick Start

### 1. Install Dependencies

```bash
cd demo_app
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### 3. Access Demo Views

- **Customer View**: http://localhost:5000/ - Simulate customer inquiries
- **Admin Panel**: http://localhost:5000/admin - View agent decision log
- **Comparison View**: http://localhost:5000/comparison - See baseline vs. agent metrics

## Demo Scenarios

Try these order IDs to see different agent behaviors:

### Scenario 1: Standard ETA Lookup (Fully Agentic)
**Order ID**: `AX-771-3344`
- **Expected**: Instant response (<1 sec) with scheduled ETA window
- **Delegation**: Fully Autonomous (green badge)
- **GPS Data**: Fresh (12 min old)
- **Demonstrates**: Standard lookup capability, fast response

### Scenario 2: Precision ETA with Fresh GPS (Agent-Led)
**Order ID**: `AX-771-3344` → Click "Need more specific time?"
- **Expected**: GPS-based calculation, confidence shown
- **Delegation**: Agent-Led (yellow badge) if GPS slightly stale
- **Demonstrates**: Precision ETA calculation, confidence scoring

### Scenario 3: GPS Stale - Escalation
**Order ID**: `AX-441-8821` → Click "Need more specific time?"
- **Expected**: Escalation due to GPS data >30 min stale (52 min)
- **Delegation**: Escalated to Human (red badge)
- **Demonstrates**: Escalation trigger (GPS staleness threshold)

### Scenario 4: Delivery Exception - Immediate Escalation
**Order ID**: `AX-996-7890`
- **Expected**: Immediate escalation (high-value exception)
- **Delegation**: Escalated to Human (red badge)
- **Package Value**: £1,250 (>£500 threshold)
- **Status**: EXCEPTION (Stein-Allen pallet refusal scenario)
- **Demonstrates**: High-value exception handling

### Scenario 5: Order Not Found
**Order ID**: `XX-999-9999`
- **Expected**: Error message, escalation option
- **Delegation**: Escalated to Human (red badge)
- **Demonstrates**: Order validation, graceful failure

## Features Demonstrated

### 1. Delegation Archetypes
- **Fully Agentic** (Green) - Agent decides and acts autonomously
- **Agent-Led** (Yellow) - Agent calculates but shows confidence limits
- **Human-Only** (Red) - Escalated due to trigger conditions

### 2. Escalation Triggers
- GPS data stale (>30 min threshold)
- Order not found in system
- Delivery exception status
- High-value order (>£500) in exception state
- Customer requests callback

### 3. Decision Transparency (Admin Panel)
- Real-time decision log with timestamps
- Response time tracking
- Escalation reason visibility
- Confidence scoring display
- Delegation level for each inquiry

### 4. Performance Comparison
- Baseline (human agent) vs. agent metrics
- Response time improvements (96% faster)
- ETA precision improvements (87% more precise)
- Deflection rate tracking (90% target)
- Cost savings visualization (£301K annual)

## Demo Walkthrough Script (5 Minutes)

### Minute 1: Introduction
1. Open Customer View (`http://localhost:5000/`)
2. Explain: "This demo uses synthetic data to showcase the ETA Inquiry Agent"
3. Show demo instructions box with test order IDs

### Minute 2: Fully Agentic Capability
1. Enter order ID: `AX-771-3344`
2. Click "Check Delivery Status"
3. Point out:
   - Response time (<1 sec)
   - Green "Fully Autonomous" badge
   - Clear ETA message
4. Explain: "This is what we expect for 90% of inquiries"

### Minute 3: Precision ETA (Agent-Led)
1. Click "Need more specific time?"
2. Point out:
   - GPS-based calculation
   - Yellow "Agent-Led" badge
   - Confidence score (HIGH/MEDIUM/LOW)
   - Calculation details expanded
3. Explain: "Agent shows GPS staleness and confidence level"

### Minute 4: Escalation Demonstration
1. Start new inquiry: Enter `AX-441-8821`
2. Click "Check Delivery Status" → shows scheduled window
3. Click "Need more specific time?"
4. Point out:
   - Red "Escalated to Human" badge
   - Escalation reason: GPS stale (52 min > 30 min threshold)
   - Clear explanation to customer
5. Explain: "Agent knows when it doesn't know - safety net"

### Minute 5: Admin Panel & Comparison
1. Switch to Admin Panel (`/admin`)
2. Show:
   - Decision log with all test inquiries
   - Escalation triggers summary
   - Deflection rate calculation
3. Switch to Comparison View (`/comparison`)
4. Show:
   - Side-by-side metrics table
   - Response time chart (8.5 min → 30 sec)
   - Deflection rate pie chart (90% autonomous)
   - Business case: £301K annual savings

## Technical Architecture

### Backend (Flask)
- **app.py** - Main Flask application with API routes
- **agent/order_validator.py** - Order ID extraction & validation
- **agent/eta_calculator.py** - ETA calculation logic (standard & precision)
- **agent/escalation_engine.py** - Escalation trigger detection

### Frontend (HTML/CSS/JS)
- **templates/index.html** - Customer inquiry interface
- **templates/admin.html** - Admin panel (decision log)
- **templates/comparison.html** - Comparison view with charts

### Data Layer (JSON)
- **data/mock_orders.json** - 8 sample orders
- **data/mock_routes.json** - 4 routes with GPS data

## Key Design Decisions

### 1. Mock Data (No Real Integrations)
- Uses pre-generated JSON files
- No CRM, Driver App, or Aurum Billing connections
- Demonstrates concept without system dependencies

### 2. GPS Staleness Threshold
- **30 minutes** - Agent operates autonomously if GPS <30 min old
- **>30 minutes** - Agent escalates (cannot provide confident ETA)
- Configurable threshold (not hardcoded in production)

### 3. Confidence Scoring
- **High (>90%)**: GPS fresh, calculation confident
- **Medium (70-90%)**: GPS slightly stale, calculation acceptable
- **Low (<70%)**: Escalate (GPS too stale)

### 4. In-Memory Decision Log
- Stores decisions in Python list (resets on server restart)
- Production would use database (PostgreSQL, MongoDB)
- Sufficient for demo purposes

## Customization Options

### Add More Test Orders
Edit `data/mock_orders.json` to add orders with different scenarios:
- Different GPS staleness (modify `timestamp` in routes)
- Different package values (escalation threshold testing)
- Different order statuses (OUT_FOR_DELIVERY, EXCEPTION, DELIVERED)

### Adjust Escalation Thresholds
In `agent/escalation_engine.py`:
- GPS staleness: Change `> 30` to different threshold
- Package value: Change `> 500` for high-value exceptions

### Modify Confidence Scoring
In `agent/eta_calculator.py`:
- Adjust confidence degradation formula
- Change ETA window (currently ±15 min)

## Production Considerations

This demo is **not production-ready**. For production deployment, you would need:

1. **Database Integration** - PostgreSQL/MySQL for orders, routes, GPS logs
2. **Real-time APIs** - CRM (Salesforce), Driver App, Dispatch Console
3. **Aurum Batch Processing** - Scheduled jobs for CSV import (T-1 lag handling)
4. **Authentication** - API keys, OAuth for customer verification
5. **Logging & Monitoring** - Structured logging, metrics, alerting
6. **Error Handling** - Retry logic, circuit breakers, fallback strategies
7. **Scalability** - Async processing (Celery), load balancing
8. **Testing** - Unit tests, integration tests, end-to-end tests

## Troubleshooting

### Port 5000 Already in Use
```bash
# Use different port
python app.py
# Then edit app.py: app.run(debug=True, port=5001)
```

### Module Not Found Errors
```bash
# Ensure you're in demo_app directory
cd demo_app

# Reinstall dependencies
pip install -r requirements.txt
```

### Cannot Find Mock Data Files
- Ensure `data/mock_orders.json` and `data/mock_routes.json` exist
- Check you're running `python app.py` from `demo_app/` directory

## Next Steps

After demo validation:
1. **User Testing**: Have Sarah Whitmore's team test with more scenarios
2. **Feedback Loop**: Collect escalation cases that should/shouldn't have escalated
3. **Threshold Tuning**: Adjust GPS staleness, confidence thresholds based on feedback
4. **Production Planning**: Design real system integrations (CRM, GPS API)
5. **Pilot Preparation**: Plan 2-month pilot with real data

## Contact

For questions about this demo or implementation details, see:
- **Agent Purpose Document**: `../Specification/06_Agent_Purpose_Document.md`
- **System Inventory**: `../Specification/07_System_Data_Inventory.md`
- **Demo Design**: `../Specification/10_Demo_Application_Design.md`
