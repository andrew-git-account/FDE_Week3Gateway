# Demo Application - Quick Guide

## What This Demo Shows

This browser-based application demonstrates the ETA Inquiry Agent for Apex Distribution using **synthetic data** (no real system connections). It showcases:

✅ **Fully Agentic** capability - Instant ETA lookup (<1 sec)  
✅ **Agent-Led** capability - GPS-based precision ETA with confidence scoring  
✅ **Escalation Logic** - GPS stale, delivery exceptions, high-value orders  
✅ **Decision Transparency** - Real-time admin panel showing agent reasoning  
✅ **Performance Comparison** - 96% faster response, 90% deflection rate, £301K savings

## Quick Start

### Windows
```cmd
cd demo_app
start.bat
```

### Mac/Linux
```bash
cd demo_app
./start.sh
```

### Manual Start
```bash
cd demo_app
python app.py
```

Then open your browser to: **http://localhost:5000/**

## 5-Minute Demo Script

### 1. Customer View (2 minutes)

**Order AX-771-3344** - Standard lookup (Fully Agentic)
- Response time: <1 sec
- Green badge: "Fully Autonomous"
- Shows scheduled ETA window (13:00-17:00)

**Click "Need more specific time?"** - Precision ETA
- Calculates GPS-based ETA
- Shows calculation details (distance, stops, traffic)
- Confidence level displayed

**Order AX-441-8821** → Click "Need more specific time?" - Escalation
- GPS data is stale (>30 min)
- Red badge: "Escalated to Human"
- Agent explains why it cannot provide accurate ETA

**Order AX-996-7890** - High-value exception
- Immediate escalation (£1,250 package in EXCEPTION status)
- Demonstrates safety net for complex cases

### 2. Admin Panel (1 minute)

Navigate to: **http://localhost:5000/admin**

- Decision log shows all inquiries with timestamps
- Delegation level for each (Fully Agentic / Agent-Led / Human Only)
- Response times tracked
- Escalation reasons visible
- Auto-refreshes every 3 seconds

### 3. Comparison View (2 minutes)

Navigate to: **http://localhost:5000/comparison**

**Metrics Table:**
- Response time: 8.5 min → 30 sec (96% faster)
- ETA precision: 4-hour window → ±30 min (87% more precise)
- Deflection rate: 0% → 90%
- Daily labor: 73 hrs → 7 hrs (66 hrs freed)
- Annual savings: £301K

**Charts:**
- Response time bar chart
- Deflection rate pie chart (90% autonomous, 10% escalated)

**Live Stats:**
- Shows actual demo usage (total inquiries, deflections, escalations)

## Test Order IDs

| Order ID | Scenario | Expected Behavior |
|----------|----------|-------------------|
| AX-771-3344 | Standard + Fresh GPS | Fully Agentic (green badge) |
| AX-441-8821 | Stale GPS | Escalates on precision request |
| AX-996-7890 | High-value Exception | Immediate escalation (red badge) |
| AX-552-1234 | Standard order | Fully Agentic |
| XX-999-9999 | Order not found | Escalation with error message |

## Key Features Demonstrated

### 1. Delegation Transparency
Every inquiry shows:
- **Green badge** = Fully Agentic (agent decides autonomously)
- **Yellow badge** = Agent-Led (medium confidence, shows GPS staleness)
- **Red badge** = Escalated to Human (trigger conditions met)

### 2. Confidence Scoring
- **HIGH (>90%)** - GPS fresh, confident calculation
- **MEDIUM (70-90%)** - GPS slightly stale, acceptable but shows warning
- **LOW (<70%)** - Escalates (cannot provide confident ETA)

### 3. Escalation Triggers
- GPS data >30 min stale
- Order not found in system
- Delivery exception status
- High-value package (>£500) in exception state
- Customer requests callback ("speak with someone")

### 4. Real-Time Decision Log
Admin panel shows:
- Every inquiry logged with timestamp
- Action taken (Standard Lookup, Precision ETA, Escalation)
- Response time (milliseconds)
- Delegation level
- Escalation reason (if escalated)

## What This Demo Does NOT Do

❌ Connect to real CRM/Driver App/Aurum Billing  
❌ Use live GPS data  
❌ Process real customer inquiries  
❌ Persist data (in-memory only, resets on server restart)  
❌ Handle authentication/security  

**This is a proof-of-concept only.** For production, you would need:
- Real system integrations (CRM API, GPS API, Aurum batch processing)
- Database (PostgreSQL/MySQL)
- Authentication (OAuth, API keys)
- Monitoring and logging
- Scalability (async processing, load balancing)

## Addressing Sarah Whitmore's Concerns

**Sarah's Past Failures:**
1. **2024 Chatbot** - Customers hated it (black-box, couldn't escalate)
2. **RPA Billing** - Broke when Aurum schema changed (brittle)

**How This Demo Addresses Concerns:**

✅ **Not a Black-Box Chatbot**
- Admin panel shows every decision
- Escalation reasons transparent
- Confidence levels visible to customer

✅ **Safety Net Built-In**
- Agent knows when it doesn't know (GPS stale → escalate)
- High-value exceptions always escalate
- Customer can manually request human anytime

✅ **No Brittle RPA**
- Reads mock data, not brittle screen-scraping
- Production would use APIs where available, graceful fallbacks for Aurum batch lag

✅ **Low-Risk Proof**
- Runs standalone on laptop
- No disruption to live systems
- Sarah can test with her team before pilot

## Next Steps After Demo

1. **User Feedback** - Sarah's team tests with different scenarios
2. **Threshold Tuning** - Adjust GPS staleness, confidence thresholds
3. **Pilot Planning** - 2-month pilot with real data (Phase 1A)
4. **System Integration Design** - Plan CRM, GPS API, Aurum batch processing
5. **Decision Point** - If it doesn't work in 2 months, we stop (no sunk cost)

## Troubleshooting

**Port 5000 already in use?**
```bash
# Edit app.py, change last line:
app.run(debug=True, port=5001)
```

**Module not found?**
```bash
cd demo_app
python -m pip install -r requirements.txt
```

**Can't find mock data?**
- Check `data/mock_orders.json` exists
- Ensure running `python app.py` from `demo_app/` directory

## Demo Talking Points

**For Sarah (COO):**
- "This shows how the agent handles 90% of inquiries autonomously"
- "When GPS is stale, it escalates - no black-box decisions"
- "Admin panel lets you audit every decision in real-time"
- "£301K annual savings, 66 hours/day capacity freed"
- "2-month pilot, if it doesn't work, we stop"

**For Technical Team:**
- "Uses mock data (JSON files), no real integrations yet"
- "Escalation triggers configurable (GPS threshold, package value)"
- "Production would use CRM API, Driver App GPS API, Aurum batch processing"
- "Agent logic in Python modules (order_validator, eta_calculator, escalation_engine)"

**For Executive Sponsor:**
- "Competitor saved £1.2M - our target is £301K (ETA inquiries only)"
- "90% deflection rate frees capacity for growth absorption"
- "Response time: 8.5 min → 30 sec (96% improvement)"
- "Phase 1 proof point, Phase 2-3 expands to billing disputes and exceptions"

## Files Overview

```
demo_app/
├── app.py                  # Flask application (API routes)
├── requirements.txt        # Python dependencies
├── README.md              # Full documentation
├── DEMO_GUIDE.md          # This file
├── start.bat / start.sh   # Quick start scripts
├── agent/
│   ├── order_validator.py # Order ID extraction & validation
│   ├── eta_calculator.py  # ETA calculation (standard & precision)
│   └── escalation_engine.py # Escalation trigger detection
├── data/
│   ├── mock_orders.json   # 8 sample orders
│   └── mock_routes.json   # 4 routes with GPS data
└── templates/
    ├── index.html         # Customer inquiry interface
    ├── admin.html         # Admin panel (decision log)
    └── comparison.html    # Comparison view (metrics)
```

## Questions?

See full documentation:
- **README.md** - Complete setup and usage guide
- **Design Doc** - `../Specification/10_Demo_Application_Design.md`
- **Agent Purpose** - `../Specification/06_Agent_Purpose_Document.md`
