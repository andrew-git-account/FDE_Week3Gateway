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

The specifications follow the ATX (Agent Task eXecution) framework - a structured methodology for deciding what work AI agents should do, how autonomous they should be, and whether it's economically worth it.

### The Three Ways to Scale Work
1. **Traditional Software** - Fixed rules, fast but can't handle unexpected situations
2. **Hiring More People** - Flexible but expensive, slow to scale, coordination overhead
3. **Digital Labour (AI Agents)** - NEW! Software speed + human-like reasoning (what ATX is about)

**Key insight**: Agents are statistical (probabilistic), not deterministic. They need guardrails, testing, supervision - like managing a workforce, not just deploying code.

### The ATX Process (4 Steps)

**Step 1: Discovery - Find Pain Points**
- Ask real workers (not just managers): What takes most of your day? What requires lots of back-and-forth?
- Output: List of painful, time-consuming tasks with volume estimates

**Step 2: Cognitive Load Mapping - Break Down the Work**
- Identify "Jobs to be Done" (cognitive contracts with outcomes, not just tasks)
- Map Cognitive Zones (understanding → data gathering → diagnosis → decision → action)
- Find Breakpoints (where control shifts: customer → agent, agent → human, rules → judgment)
- Output: Map showing where thinking happens and where handoffs occur

**Step 3: Delegation Qualification - Decide Who Does What**

Score each task on 7 dimensions, then assign to archetype:

| Archetype | When to Use | Example |
|-----------|-------------|---------|
| **🟢 Fully Agentic** | High volume, structured, reversible, well-governed | Standard ETA lookup |
| **🟡 Agent-Led + Human Oversight** | High volume but needs human backstop | Precision ETA with GPS risk |
| **🟠 Human-Led + Agent Support** | Complex analysis, agent synthesizes, human decides | Billing dispute investigation |
| **🔴 Human-Led + Automation Support** | Agent does rote tasks, human keeps control | Data entry with verification |
| **⚫ Human Only** | Ethics, tacit knowledge, irreversible | Firing decisions, negotiations |

**Anti-pattern**: NOT everything should be "Fully Agentic"! Good ATX work shows mixed archetypes (Week 2 example: 50% fully agentic, 25% agent-led, 25% human-led)

**Step 4: Prioritization - Pick Winners**
- Plot tasks on Volume × Value grid (high volume + high reasoning = prime agent territory)
- Calculate economics: `Annual saving = Human cost - Agent cost`
- Only proceed if payback ≤ 18 months and Year 1 ROI > 0%
- Sequence into waves so early wins finance later investments

### ATX Scoring Dimensions

| Dimension | Good for Agents | Bad for Agents |
|-----------|-----------------|----------------|
| **Input Structure** | Structured data | Messy, ambiguous |
| **Decision Determinism** | Follows patterns | Needs judgment |
| **Tool Coverage** | APIs available | Systems inaccessible |
| **Context Complexity** | Explicit rules | Tribal knowledge |
| **Exception Rate** | Rare edge cases | Frequent surprises |
| **Latency** | Can wait seconds | Needs instant response |
| **Risk/Compliance** | Low consequence, reversible | Irreversible, regulated |

### Key ATX Principles

1. **Start from LIVED work, not SOPs** - Real work ≠ documented processes; shadow people, review transcripts
2. **Owned agents, not rented** - Pre-built SaaS agents = vendor lock-in; own the orchestration logic, boundaries, prompts
3. **Platform thinking (compounding)** - Build reusable integrations; each new agent becomes cheaper
4. **Cognitive work, not processes** - Target interpretation, judgment, exception handling (gaps between processes)
5. **Economics must close BEFORE production** - Token cost is both cost measure AND governance instrument

### Buildability Standards

Specifications must include:
- Entity definitions (tables, columns, types, constraints)
- State machines (status transitions, validation rules)
- API contracts (request/response formats with examples)
- Error handling for all failure modes (not just happy path)
- Escalation patterns with explicit triggers
- Worked examples for calculations/transformations
- Edge cases listed explicitly
- Production readiness: logging, metrics, alerts, concurrency, security

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

### Quick Reference: Specification Template Structure

Use this structure for Friday D#4 (two capability specs):

```markdown
# Capability Spec: [Name]

## Constraints (Read First!)
✅ DO: [specific actions]
❌ DO NOT: [forbidden actions]

## Requirement: [Name]

### Description
[Concrete actions only - no abstract words]

### Examples (Worked)
- Input: [case 1] → Output: [expected 1]
- Input: [edge case] → Output: [expected 2]  
- Input: [invalid] → Output: [error message]

### Edge Cases
- ✅ Happy path: [...]
- ⚠️ Empty/null input: [...]
- ⚠️ Concurrent requests: [...]
- ⚠️ Invalid values: [...]

### Error Handling
| Failure Mode | Response | Example |
|--------------|----------|---------|
| API timeout (>5s) | Escalate | "Unable to verify..." |
| Network error | Retry 3x, escalate | [...] |

### Process Steps
1. [Step with code/query example]
2. [Step with validation]
3. [Step with error handling]

### Validation Rules
- Input: [validation criteria]
- Output: [format requirements]

### Observability
- Log: [what gets logged]
- Metrics: [what gets tracked]
- Alerts: [when to alert]

### Acceptance Criteria
- [ ] Accuracy: [measurable target]
- [ ] Performance: [response time]
- [ ] Error handling: [all modes covered]
```

**Time per spec**: ~45 minutes × 2 = 90 minutes total

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

## Build-Loop Diagnosis Framework (Critical for Week 3)

### The 4 Categories of Build Failures

When AI builds don't match expectations, diagnose which category before fixing:

**Category 1: Spec Ambiguity** (YOU caused it)
- **Signal**: AI's code matches spec as written, but not your intent
- **Example**: "Validate address" → AI checks format, you meant USPS API geocoding
- **Fix**: Rewrite the spec to be precise, add worked examples
- **Red flags**: Words like "valid," "appropriate," "handle," "check," "reasonable"

**Category 2: Builder Misread** (AI caused it)
- **Signal**: AI's code contradicts explicit spec statements
- **Example**: Spec says "approval BEFORE payment," AI processes payment first
- **Fix**: Re-prompt with relevant spec section highlighted, don't change spec
- **Detection**: "Wait, did you read the part about...?"

**Category 3: Test Problem** (Test caused it)
- **Signal**: Code matches spec, test expectation is wrong
- **Example**: Spec says "round half up," test expects floor behavior
- **Fix**: Update the test, not the code or spec

**Category 4: Design Gap** (Spec incomplete)
- **Signal**: Build is "correct" but obviously incomplete for production
- **Example**: Spec described happy path, forgot error handling for API failures
- **Fix**: Add missing requirement (error handling, concurrency, logging) to spec
- **Common gaps**: Error handling, validation, observability, concurrency control

### Diagnostic Decision Tree

```
Does AI's code match spec AS WRITTEN?
├─ YES → Does it match your INTENT?
│         ├─ YES → ✅ Pass (no problem)
│         └─ NO → 🟡 Category 1: Spec Ambiguity
│                    Fix: Rewrite spec
└─ NO → Is AI's choice reasonable?
        ├─ YES → Is difference meaningful?
        │         ├─ YES → 🟡 Category 1: Spec Ambiguity  
        │         │         Fix: Clarify spec
        │         └─ NO → ✅ Acceptable variation
        └─ NO → Does spec address this?
                ├─ YES → 🔴 Category 2: Builder Misread
                │         Fix: Re-prompt AI
                └─ NO → 🟣 Category 4: Design Gap
                          Fix: Add to spec
```

### Specification Verification Checklist (Before Building)

**To prevent spec ambiguity**:
- [ ] Scan for red flag words (valid, appropriate, handle, check, reasonable)
- [ ] Add 3 worked examples for every calculation/transformation
- [ ] Use "Explain to 5-year-old" test (can you describe it concretely?)
- [ ] Replace abstract words with specific actions

**To prevent builder misreads**:
- [ ] Extract all constraints to top of spec (bold, prominent)
- [ ] Add "DO NOT" statements for critical requirements
- [ ] Use visual hierarchy (bold, numbered lists, code blocks)
- [ ] Make specs scannable (key info visible in 30-second skim)

**To prevent test problems**:
- [ ] Write test cases FROM spec examples (not from memory)
- [ ] List all edge cases in spec explicitly
- [ ] Have someone else write tests from your spec (catches ambiguity)

**To prevent design gaps**:
- [ ] Run "Production Readiness Checklist" (8 questions):
  1. Error handling - what if API fails?
  2. Validation - what if input is null/empty/malformed?
  3. Concurrency - what if two requests happen simultaneously?
  4. Observability - how do we debug in production?
  5. Performance - what if 1000 requests at once?
  6. Security - can unauthorized users access?
  7. Compliance - does this need audit trail?
  8. Rollback - what if we need to undo?
- [ ] Check happy path vs error path ratio (should be ~50/50, not 80/20)
- [ ] Brainstorm 5 failure modes for each external dependency
- [ ] Add cross-cutting concerns (logging, metrics, alerts)

## Week 3 Deliverables Reference

### Deliverable Time Budget (Friday 13:30-17:00, 210 minutes total)

| # | Deliverable | Time | Strategy |
|---|-------------|------|----------|
| **D#1** | Problem framing & success metrics | 20 min | Revise Thursday draft against Marcus feedback |
| **D#2** | Engagement intake & scope | 20 min | Revise Thursday draft, add scope boundaries |
| **D#3** | Agentic architecture + ≥2 ADRs | 30 min | Revise Thursday draft, ensure ADRs have real trade-offs |
| **D#4** | **Two capability specs** | **90 min** | **Heaviest!** Apply verification checklist |
| **D#5** | Build-loop response memo | 15 min | Use Wednesday Cascade diagnosis |
| **D#6** | Client feedback response | 20 min | Address each Marcus point concretely |
| **D#7** | Validation plan | 10 min | Testing strategy before production |
| **D#8** | Reflection | 10 min | Lessons learned, process improvements |
| **D#9** | Self-spec build-loop reflection | 15 min | Run ONE D#4 spec through Claude Code |
| | **TOTAL** | **230 min** | *You have 210 min - work fast!* |

### D#1: Problem Framing & Success Metrics
- What is actually broken (not just stated request)
- Measurable outcomes for all stakeholder groups (MedFlex, hospitals, nurses)
- "10x without 10x-ing" is not a technical requirement - figure out what it demands

### D#2: Engagement Intake & Scope
- Business context, stakeholder map, constraints, risks
- MVP scope definition with explicit OUT-of-scope items and WHY
- Two failed AI projects context (chatbot, recommendation engine)

### D#3: Agentic Solution Architecture
- Which workflows become agentic, at what delegation levels
- **Minimum 2 ADRs** with:
  - Alternatives considered (not just "we chose X")
  - Trade-off analysis (consequences of each option)
  - Why decision could be revisited (under what conditions)
- Avoid "justification theater" - real trade-offs only

### D#4: Two Production-Grade Capability Specifications ⚠️ CRITICAL
- **90 minutes = 43% of exam time** - this is the heaviest deliverable
- Precise enough for Claude Code to build from (buildability standard from Week 2)
- Shared entities consistent across both specs
- Where ambiguity unavoidable, state as assumption with confidence level
- Apply verification checklist:
  - [ ] No red flag words (valid, appropriate, handle)
  - [ ] 3+ worked examples per calculation
  - [ ] Constraints extracted to top
  - [ ] DO/DO NOT statements for critical requirements
  - [ ] Production readiness: error handling, validation, logging, etc.
  - [ ] Edge cases listed explicitly
  - [ ] API failure modes covered (timeout, 500, 429, 401, partial response)
  - [ ] Happy path vs error path balanced (~50/50)

### D#5: Build-Loop Response Memo
- Reference Wednesday's Cascade Public Libraries fixture diagnosis
- Classify what went wrong (spec gap / builder misread / unjustified addition / test issue)
- Write corrective response in appropriate tone for each category:
  - Spec ambiguity → rewrite spec
  - Builder misread → re-prompt with spec quoted
  - Test problem → fix test
  - Design gap → add missing requirement

### D#6: Client Feedback Response
- Address Marcus Reyes CEO pushback professionally
- Hold boundaries without alienating (neither cave nor stonewall)
- For each pushback point: concede with concrete alternative OR hold scope with reasoning
- "Yes, 6 weeks!" = capitulation (failure mode)
- Stonewalling = failure mode
- Honest replanning with scope discipline = success

### D#7: Validation Plan
- How to verify agentic system works before production
- What to test, how to measure success
- Acceptance criteria

### D#8: Reflection Document
- Process improvements, lessons learned
- What would you do differently?
- What did you learn about your own process?

### D#9: Self-Spec Build-Loop Reflection (1 page) ⚠️ CRITICAL
- Take ONE spec from D#4, run through Claude Code under exam conditions
- Write 1-page reflection: what it built, what it asked, what you'd change
- **Graded on diagnosis honesty, NOT code correctness**
- **Broken build + honest diagnosis > working code by accident**
- Avoid defensive reading: "Claude mostly got it right" when it clearly didn't
- Good example: "Claude built X because my spec failed to distinguish Y from Z; I'd add worked example for case A"

## Week 3 Schedule & Critical Timing

### Monday (Virtual Day 1)
**Coach delivers**: 1h orientation + calendar confirmation (Teams General)  
**You do**: Read `spec-ambiguity-vs-builder-mistakes.md` end-to-end, audit Week 2 specs

### Tuesday (Virtual Day 2)
**You do**: Production-spec-checklist audit, review `discovery-questioning-patterns.md`

### Wednesday (Virtual Day 3) - Build-Loop Diagnosis Day

**09:00 CET - You deliver**: One-line classification prediction to critique pool
```
"The hardest part of build-loop diagnosis for me will be ___."
```
Examples: "...distinguishing spec ambiguity from builder misreads" OR "...catching design gaps I forgot to specify" OR "...avoiding defensive reading when diagnosing my own spec"

**09:00-10:30 CET - Coach delivers**: Live walkthrough on Coffee Subscription Credit Handler fixture (90 min), demonstrates all 5 categories + tone/response

**Afternoon - Coach delivers**: Cascade Public Libraries Hold Queue fixture release

**Afternoon - You do**: Solo diagnosis exercise on Cascade fixture

**EOD Wednesday - You deliver**: Cascade diagnosis to squad lead (NOT graded, feeds Friday D#5)

### Thursday (Virtual Day 4) - Discovery & Initial Design

**09:00 CET - Coach delivers**: Gate 3 scenario pack (`Gate3-Participant-Pack.md`) - MedFlex healthcare staffing

**You do**: Read scenario end-to-end BEFORE discovery call

**09:30-10:30 CET - Coach delivers**: Plays MedFlex stakeholder in live simulated discovery (60 min)

**You do**: Ask questions, take notes, extract requirements, notice inconsistencies

**Afternoon - You do**: Draft D#1 (problem framing), D#2 (intake & scope), D#3 (architecture + ADRs) - rough drafts OK

**23:59 CET Thursday - You deliver**: Interim D#1-D#3 to squad lead (NOT GRADED - triggers CEO feedback generator)

### Friday (Virtual Day 5) - Gate 3 Exam Day ⚠️

**09:00 CET - Coach delivers**: Personalized Marcus Reyes (CEO) email with pushback tailored to YOUR Thursday submission

**09:00-13:30 CET (4.5h) - You do**: UNTIMED PREPARATION ⚠️
- **THIS IS NOT THE EXAM YET**
- Read Marcus's pushback carefully
- Decide which points to concede vs hold scope
- Plan D#6 response strategy
- Refine D#1-D#3 thinking against discovery + pushback
- **DO NOT finalize deliverables** - this is thinking time

**13:30-17:00 CET (3.5h) - You do**: TIMED GATE 3 EXAM ⏱️
- Produce all 9 deliverables (final, polished, complete)
- D#4 (two specs) = 90 min (heaviest deliverable)
- Everything else = 120 min
- Work efficiently - total time = 230 min, you have 210 min

**17:00 CET SHARP - You deliver**: Single markdown folder with all 9 deliverables
- ⚠️ **NOT EOD - 17:00 SHARP**
- Anything not submitted by 17:00 is NOT graded

**17:50-19:00 CET - Coach delivers**: 10-minute verbal defense (your specific slot confirmed by coach)
- Coach probes one architectural decision + one weakness
- "The CEO's two failed AI projects - how is yours different?"
- "What kills this in production?"

### Following Monday (Week 4)
**Coach delivers**: Gate 3 results and feedback

---

## Common Timing Mistakes to Avoid

❌ **WRONG**: "Friday 09:00-17:00 is the exam (8 hours)"  
✅ **RIGHT**: 09:00-13:30 = prep time, 13:30-17:00 = exam time (3.5h)

❌ **WRONG**: "I'll submit Friday EOD"  
✅ **RIGHT**: "17:00 SHARP - no extensions"

❌ **WRONG**: "Thursday 23:59 D#1-D#3 must be perfect"  
✅ **RIGHT**: "Rough drafts fine - just input for CEO feedback"

❌ **WRONG**: "Wednesday Cascade is a Gate 3 deliverable"  
✅ **RIGHT**: "Not a deliverable, but I'll reuse diagnosis for Friday D#5"

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

## Critical Success Factors for Week 3

### What Coaches Look For

✅ **Genuinely AI-native solution**
- Agents are the mechanism, not a feature label on traditional systems
- Coach will ask: "Show me the agent decision - where reasoning determines an outcome a rule-based system couldn't"
- NOT: Deterministic matcher with LLM call sprinkled on top

✅ **Accurate build-loop diagnosis**
- Classify signals correctly (spec gap vs builder misread vs test issue vs design gap)
- Write right response in right tone for each category
- Go beyond surface signal (test fails) to read spec alongside code (test reflects real spec gap)

✅ **Problem framing addresses real problem**
- Not just stated request ("10x without 10x-ing" is not a technical requirement)
- What does it actually demand of architecture?

✅ **Honest self-spec build-loop reflection**
- Spec producing broken build but diagnosed precisely > working code by accident
- Graded on diagnosis quality, not build correctness
- Avoid defensive reading: "Claude mostly got it right" when it clearly missed the point

✅ **Professional client feedback response**
- Hold boundary without alienating (neither cave nor stonewall)
- Scope discipline with honest replanning
- Address each pushback point concretely

✅ **Specifications enable near-autonomous build**
- AI agent shouldn't need to guess at intent
- Where ambiguity unavoidable, name it as assumption with confidence level
- Production readiness checklist covered

### Common Week 3 Failure Modes

❌ **AI-as-a-feature on traditional matching** - Deterministic matcher with LLM, not AI-native

❌ **Build-loop diagnostic stops at first impression** - Names surface signal without reading spec + code together

❌ **Client feedback appeased, not addressed** - "Yes CEO, 6 weeks!" = capitulation that breaks at week 4

❌ **Self-spec reflection defends instead of diagnoses** - Bluffing when Claude clearly missed the point

❌ **No ADR trade-off analysis** - "We chose X because it's right" without alternatives/consequences = theater

### Pre-Exam Preparation Checklist

**Before Wednesday 09:00**:
- [ ] Read `spec-ambiguity-vs-builder-mistakes.md` end-to-end
- [ ] Submit classification prediction: "The hardest part... will be ___"
- [ ] Audit one Week 2 activity for ambiguous requirements

**Before Thursday 09:30**:
- [ ] Read `discovery-questioning-patterns.md`
- [ ] Prepare question templates for discovery session
- [ ] Note-taking system ready

**Before Friday 09:00**:
- [ ] Markdown folder structure ready for 9 deliverables
- [ ] Claude Code tested and working (for D#9)
- [ ] Week 2 specs available for reference
- [ ] Verification checklist printed/available

**Before Friday 13:30** (use 09:00-13:30 prep time):
- [ ] Marcus pushback read and annotated
- [ ] D#6 strategy planned (concede vs hold scope points)
- [ ] D#1-D#3 refined against discovery + pushback
- [ ] D#4 outline prepared (two specs structure)

## Session-Specific Reminders

- This is a learning environment - focus is on skill demonstration, not production deployment
- Week 3 focuses on AI-native design (agents as mechanism) vs traditional software with AI features
- Honest diagnosis of failures is valued over perfect outcomes
- Scope discipline matters - explicitly call out what's OUT of scope and why
- Client stakeholder management is part of the evaluation (professional pushback handling)
- Time management is critical - D#4 (90 min) is 43% of exam time, plan accordingly

## Contact & Support

For FDE program questions, participant should:
- Check Teams General channel for exact physical dates for virtual days
- Confirm verbal defense slot with coach on Friday
- Ask squad lead about submission format/location
- Reference Week 3 README for any schedule or requirement clarifications
