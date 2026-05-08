# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Context

This is an FDE (Full-Delivery Engineer) learning program repository for Week 3. The participant (Andrzej Bihun, Business Analyst) is working through an AI-native engagement simulation focused on building agentic solutions.

### Program Structure
- **Week 2 Completed**: Specifications for Apex Distribution ETA Inquiry Agent in `Specification/` folder
- **Week 3 Current**: End-to-end AI-native engagement simulation (MedFlex healthcare staffing scenario)
- **Demo Application**: Working Python/Flask prototype in `demo_app/` demonstrating Week 2 work

### Key Objectives for Week 3
1. Execute complete FDE engagement: discovery → specification → build-loop correction → stakeholder management
2. Produce 9 deliverables under timed exam conditions (Friday 13:30-17:00 CET)
3. Design AI-native solutions (agents as primary mechanism, not bolt-on features)
4. Diagnose build-loop failures with accurate classification
5. Handle client pushback professionally with scope discipline

## Running the Demo Application

### Quick Start
```bash
cd demo_app
pip install -r requirements.txt
python app.py
```

The application runs on `http://localhost:5000` with three views:
- **Customer View**: `/` - Simulate customer inquiries
- **Admin Panel**: `/admin` - View agent decision log
- **Comparison View**: `/comparison` - Baseline vs agent metrics

### Test Scenarios
Use these order IDs to demonstrate different agent behaviors:
- `AX-771-3344` - Standard ETA lookup (Fully Agentic)
- `AX-771-3344` → "Need more specific time?" - Precision ETA (Agent-Led)
- `AX-441-8821` → "Need more specific time?" - GPS stale escalation (52 min)
- `AX-996-7890` - High-value exception (£1,250 package)
- `XX-999-9999` - Order not found error

### Demo Application Architecture
```
demo_app/
├── app.py                    # Flask application (main routes)
├── agent/
│   ├── order_validator.py    # Order ID extraction & validation
│   ├── eta_calculator.py     # ETA calculation logic
│   └── escalation_engine.py  # Escalation trigger detection
├── templates/                # HTML views
├── data/                     # Mock JSON data (orders, routes)
└── requirements.txt          # Python dependencies
```

**Key Design Principle**: Demo uses mock data (no real system integrations) to prove agent concept before expensive integration work.

## Week 2 Specification Structure

The `Specification/` folder contains the completed Gate 2 deliverables for Apex Distribution:

### Core Deliverables
1. **Agent Purpose Document** (`06_Agent_Purpose_Document.md`) - Primary specification for ETA Inquiry Agent
   - Activity catalog with 6 activities (order validation, ETA calculation, escalation)
   - Autonomy matrix defining delegation levels
   - Escalation triggers (GPS stale >30 min, order not found, customer demands callback)
   - Success metrics: 90% deflection rate, <30 sec response time, >90% ETA accuracy

2. **Cognitive Load Map** (`03_Cognitive_Load_Map.md`) - Task decomposition showing:
   - ETA Inquiries: low-cognitive, high-volume (400/day, 73 hrs/day)
   - Billing Disputes: high-cognitive, judgment-heavy

3. **Delegation Suitability Matrix** (`04_Delegation_Suitability_Matrix.md`) - 8 task clusters scored:
   - 4/8 Fully Agentic (standard ETA lookup, dispute intake, low-value exceptions)
   - 2/8 Agent-Led (precision ETA with GPS staleness risk)
   - 2/8 Human-Led (credit decisions, dispatch optimization)

4. **Volume × Value Analysis** (`05_Volume_Value_Analysis.md`) - Business case:
   - ETA Inquiries: 73 hrs/day, £301K annual savings, 66 hrs/day capacity freed

5. **System Data Inventory** (`07_System_Data_Inventory.md`) - Integration landscape:
   - CRM (Salesforce), Driver App GPS API, Dispatch Console, Aurum Billing
   - Critical constraint: Aurum batch-only (T-1 lag, no real-time API)

### Submission Document
- `Gate2-Andrzej-Bihun.md` - Consolidated 3,642-line submission with all 7 deliverables
- `SUBMISSION_SUMMARY.md` - Overview of deliverables and demo status

## Week 3 Program Materials

The `FDE/Week 3/` folder contains:
- `README.md` - Complete Week 3 schedule, deliverables, and requirements
- `Week3_findings.md` - Participant's analysis and action items (created in this session)

### Critical Week 3 References
Located in `FDE/Reference/`:
- `spec-ambiguity-vs-builder-mistakes.md` - Build-loop diagnostic taxonomy (MUST READ before Wednesday)
- `production-spec-checklist.md` - Specification quality checklist
- `discovery-questioning-patterns.md` - Discovery session preparation
- `integration-spec-template.md` - Template for capability specs

## FDE Methodology (ATX Framework)

The specifications follow the ATX (Agent Task eXecution) framework used throughout the program:

### Key ATX Concepts
1. **Delegation Archetypes**:
   - **Fully Agentic**: Agent decides and acts autonomously (green indicator)
   - **Agent-Led with Oversight**: Agent calculates with confidence scoring (yellow indicator)
   - **Human-Led with Agent Support**: Human decides, agent assists (red indicator)

2. **Cognitive Load Mapping**: Decompose tasks into atomic activities, assess:
   - Cognitive complexity (pattern recognition vs procedural lookup)
   - Decision frequency and velocity
   - Error consequence and reversibility

3. **Volume × Value Analysis**: Prioritize opportunities by:
   - Volume metric: Daily labor hours consumed
   - Value composite: Customer Experience + Revenue Protection + Operational Risk + Scalability

4. **Buildability Standards**: Specifications must include:
   - Entity definitions (tables, columns, types, constraints)
   - State machines (status transitions, validation rules)
   - API contracts (request/response formats)
   - Error handling for all failure modes
   - Escalation patterns with explicit triggers

## Working with Specifications

### When Creating New Capability Specs
Follow the structure in `06_Agent_Purpose_Document.md`:

1. **Purpose Section**: Job to be done, customer problem, business problem
2. **Scope**: In-scope capabilities, explicitly call out what's OUT of scope
3. **Success Metrics**: Lagging indicators (business outcomes) + leading indicators (operational health)
4. **Activity Catalog**: Each activity with:
   - Trigger conditions
   - Input/output formats
   - Process steps (with code/query examples)
   - Error handling with specific failure scenarios
   - Acceptance criteria
5. **Autonomy Matrix**: For each activity, define autonomy level and human involvement
6. **Escalation Triggers**: Conditions requiring human handoff with customer experience
7. **Failure Modes & Mitigation**: Scenario → Root Cause → Customer Impact → Detection → Mitigation
8. **Data/System Dependencies**: Integration requirements, API contracts, schema definitions
9. **Non-Functional Requirements**: Performance, scalability, security, audit/compliance

### Build-Loop Diagnosis Categories
When analyzing build output (Week 3 Deliverable #5, #9):
- **Spec gap**: Ambiguity in spec requires revision
- **Builder misread**: Builder misinterpreted clear spec (direct correction)
- **Unjustified implementation choice**: Builder added features not in spec (removal request)
- **Test/environment issue**: Build is correct, test or environment is wrong
- **Legitimate unknown**: Builder correctly surfaced unclear requirement

### Anti-Patterns to Avoid
Based on Week 2 and Week 3 program guidance:
1. **"Everything is fully agentic"** - Only assign Fully Agentic where justified (Week 2 achieved 50% ratio)
2. **AI-as-a-feature on traditional systems** - Agents must be the mechanism, not sprinkled LLM calls
3. **Generic consulting templates** - Ground everything in specific artefacts and constraints
4. **Ignoring system constraints** - Aurum batch-only, GPS API availability, CRM dependencies
5. **Defensive spec reflection** - Honest diagnosis of build failures scores higher than defensive justification
6. **No ADR trade-offs** - Architecture decisions must name alternatives and consequences

## Development Commands

### Demo Application
```bash
# Install dependencies
cd demo_app
pip install -r requirements.txt

# Run development server
python app.py

# Application runs on http://localhost:5000
# No separate test commands - demo uses mock data
```

### Python Environment
- Python 3.13.0 installed
- Flask 3.0.0 web framework
- Flask-CORS for cross-origin requests
- geopy for distance calculations (haversine formula)
- python-dateutil for datetime parsing

## Architecture Notes

### Apex Distribution ETA Inquiry Agent (Week 2)
**Problem**: 400 ETA inquiries/day consuming 73 hours (28% of Customer Ops capacity), 4-11 min response time with 4-hour ETA windows.

**Solution**: AI-native agent that:
- Provides <30 sec response time with ±30 min ETA windows
- Deflects 90% of inquiries (360/400) autonomously
- Frees 66 hrs/day (8.8 FTE) capacity
- Calculates precision ETAs using GPS + traffic data
- Escalates when GPS >30 min stale or exceptions detected

**Key Architectural Decisions**:
1. **GPS Staleness Threshold**: 30 minutes (agent autonomous if <30 min, escalates if >30 min)
2. **Confidence Scoring**: HIGH (>90%), MEDIUM (70-90%), LOW (<70% → escalate)
3. **Escalation Reasons**: GPS_STALE, GPS_UNAVAILABLE, ORDER_NOT_FOUND, CUSTOMER_MISMATCH, DATA_INCONSISTENCY, EXCEPTION_INQUIRY, CALLBACK_REQUESTED
4. **Phased Rollout**: Phase 1A (scheduled window only), Phase 1B (add precision ETA), Phase 1C (proactive updates)

**System Constraints**:
- Aurum Billing: Batch-only, T-1 lag, no real-time API, 48h modification turnaround
- GPS Data: Driver App backend with <15 min polling target (currently ~30 min)
- CRM: Salesforce with read/write access (orders, customers, routes, cases)

### Demo Application (Mock Implementation)
- Uses JSON files instead of real database (mock_orders.json, mock_routes.json)
- In-memory decision log (resets on server restart)
- Simulates GPS staleness (timestamps in mock data)
- Demonstrates all 3 delegation archetypes visually (green/yellow/red badges)

## Week 3 Deliverables Reference

When working on Week 3 Gate 3 deliverables:

### D#1: Problem Framing & Success Metrics
- What is actually broken (not just stated request)
- Measurable outcomes for all stakeholder groups

### D#2: Engagement Intake & Scope
- Business context, stakeholder map, constraints, risks
- MVP scope definition with explicit OUT-of-scope items

### D#3: Agentic Solution Architecture
- Which workflows become agentic, at what delegation levels
- Minimum 2 ADRs with alternatives considered, trade-offs, consequences, why revisitable

### D#4: Two Production-Grade Capability Specifications
- Precise enough for Claude Code to build from (buildability standard from Week 2)
- Shared entities consistent across both specs
- Where ambiguity unavoidable, state as assumption with confidence level
- This is the heaviest deliverable (expect ~50% of 3.5h exam time)

### D#5: Build-Loop Response Memo
- Reference Wednesday's Cascade Public Libraries fixture
- Classify what went wrong (spec gap / builder misread / unjustified addition / test issue)
- Write corrective response in appropriate tone

### D#6: Client Feedback Response
- Address CEO pushback professionally
- Hold boundaries without alienating
- Neither capitulate nor stonewall

### D#7: Validation Plan
- How to verify agentic system works before production

### D#8: Reflection Document
- Process improvements, lessons learned

### D#9: Self-Spec Build-Loop Reflection (1 page)
- Take ONE spec from D#4, run through Claude Code
- Graded on diagnosis honesty, NOT code correctness
- Broken build with honest diagnosis > working code by accident

## Important Dates & Timing (Week 3)

- **Wednesday 09:00 CET**: Submit build-loop classification prediction
- **Wednesday morning**: Coach-led build-review walkthrough (Coffee Subscription fixture)
- **Wednesday EOD**: Submit Cascade Public Libraries fixture diagnosis
- **Thursday 09:00 CET**: Gate 3 scenario released (MedFlex)
- **Thursday 09:30-10:30 CET**: Live discovery session (simulated client)
- **Thursday 23:59 CET**: Interim submission (D#1-D#3 rough drafts)
- **Friday 09:00 CET**: Receive CEO pushback email
- **Friday 13:30-17:00 CET**: TIMED GATE 3 EXAM (3.5 hours)
- **Friday 17:00 SHARP**: Submission cutoff
- **Friday 17:50-19:00 CET**: 10-minute verbal defense

## File Navigation Tips

### To understand the business domain:
Read `Specification/01_Domain_Orientation.md` and `02_Problem_Statement_and_Success_Metrics.md`

### To understand the agent specification:
Read `Specification/06_Agent_Purpose_Document.md` (primary) and `10_Demo_Application_Design.md`

### To understand Week 2 deliverables:
Read `Specification/SUBMISSION_SUMMARY.md` or the consolidated `Gate2-Andrzej-Bihun.md`

### To understand Week 3 requirements:
Read `FDE/Week 3/README.md` (complete 152-line guide) and `Week3_findings.md` (participant analysis)

### To understand FDE methodology:
Read `FDE/Reference/atx/atx-concepts.md` and `FDE/Week 2/references/atx-*.md` files

### To prepare for build-loop diagnosis:
Read `FDE/Reference/spec-ambiguity-vs-builder-mistakes.md` (CRITICAL before Wednesday)

## Session-Specific Reminders

- This is a learning environment - focus is on skill demonstration, not production deployment
- Specifications should be buildable but don't need production-grade security/scaling for demos
- Week 3 focuses on AI-native design (agents as mechanism) vs traditional software with AI features
- Honest diagnosis of failures is valued over perfect outcomes
- Scope discipline matters - explicitly call out what's OUT of scope and why
- Client stakeholder management is part of the evaluation (professional pushback handling)

## Contact & Support

For FDE program questions, participant should:
- Check Teams General channel for exact physical dates for virtual days
- Confirm verbal defense slot with coach on Friday
- Ask squad lead about submission format/location
- Reference Week 3 README for any schedule or requirement clarifications
