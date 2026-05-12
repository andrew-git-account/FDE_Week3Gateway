# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Context

This is an FDE (Full-Delivery Engineer) learning program repository for Week 3. The participant (Andrzej Bihun, Business Analyst) is working through an AI-native engagement simulation focused on building agentic solutions.

### Program Structure
- **Week 2**: Completed — Gate 2 deliverables archived and removed from this repo
- **Week 3 Current**: End-to-end AI-native engagement simulation (MedFlex healthcare staffing scenario)
- **Gate 3 Scenario**: `FDE/Week 3/Gate3-Participant-Pack.md` — released Thursday 09:00 CET

### Current Status (Thursday Week 3)
- ✅ Gate 3 scenario pack received and read
- ✅ Discovery role-play with Marcus Reyes completed (09:30-10:30 CET)
- ✅ W3D3 Build-loop exercise submitted: `Deliverables/Build-loop-exercise-outcome-Andrzej_Bihun.md`
- **ACTIVE NOW**: Draft D#1, D#2, D#3 for Thursday 23:59 CET interim submission
- **FRIDAY**: Exam 13:30-17:00 CET, verbal defense 17:50-19:00 CET

### Key Objectives for Week 3
1. Execute complete FDE engagement: discovery → specification → build-loop correction → stakeholder management
2. Produce 9 deliverables under timed exam conditions (Friday 13:30-17:00 CET)
3. Design AI-native solutions (agents as primary mechanism, not bolt-on features)
4. Diagnose build-loop failures with accurate classification
5. Handle client pushback professionally with scope discipline

---

## The MedFlex Scenario (Gate 3)

> **MedFlex** — healthcare staffing agency, 200 employees, 5-state US region. B2B with hospital systems and B2C with travel nurses.

### Current Operations
- Hospitals submit shift requests via email, portal, or phone
- **8 coordinators manually match nurses to shifts** based on credentials, proximity, availability, hospital preferences, nurse preferences
- **Compliance verification** — license checks, background, training certifications — done manually against state regulatory databases
- ~120 shift-matching decisions per coordinator per day
- **Average time to fill: 4.2 hours.** Target: under 1 hour
- **Mismatch rate** (wrong credentials for facility type): 7%
- **No-show rate**: 12%

### Stakeholder — Marcus Reyes, CEO
- Just closed Series B; board wants significant growth in 24 months
- **Two failed AI projects**: chatbot hospital staff rejected; recommendation engine nobody used
- Background: operations + growth, not engineering
- Tone: confident, time-pressured, results-oriented
- Respects FDEs who challenge framing with substance
- Engagement framing: *"10x the business without 10x-ing the coordinators"* in 8 weeks

### Known Contradictions from Discovery (catch and flag)
1. *"Our app is the source of truth for nurse availability"* vs *"When a nurse calls in sick they call Kim, and Kim updates the schedule by hand"*
2. *"All credentials are verified before the nurse joins our roster"* vs *"When a credential lapses we get a state regulatory ping and we re-verify within a week"*
3. *"The 7% mismatch rate is hospital-flagged dissatisfaction"* vs *"We have a quality score. Trust me, it's reliable"* (when asked how agent should determine quality)

### Explicit Out-of-Scope (do not include in Gate 3 designs)
- Building a hospital-facing portal for shift submission (they use existing channels)
- Building a nurse-facing mobile app (they use phone/SMS/email today)
- Pricing engine / margin optimisation
- Continuing-education renewal automation for nurses (not in v1)

### Key People Referenced (not available in discovery)
- **Kim** — senior coordinator (operational detail)
- **Aaron** — IT (system internals)
- **Linda** — compliance (regulatory specifics)

---

## Week 3 Deliverables Reference

### Deliverable Time Budget (Friday 13:30-17:00, 210 minutes total)

| # | File | Time | Strategy |
|---|------|------|----------|
| **D#1** | `01-problem-framing.md` | 20 min | Revise Thursday draft against Marcus feedback |
| **D#2** | `02-intake-scope.md` | 20 min | Revise Thursday draft, add scope boundaries |
| **D#3** | `03-architecture.md` | 30 min | Revise Thursday draft, ensure ADRs have real trade-offs |
| **D#4** | `04a-capability-spec-<name>.md` + `04b-...` | **90 min** | **Heaviest!** Apply verification checklist |
| **D#5** | `05-build-loop-response.md` | 15 min | Reference Cascade diagnosis from `Deliverables/` |
| **D#6** | `06-client-feedback.md` | 20 min | Address each Marcus pushback point concretely |
| **D#7** | `07-validation-plan.md` | 10 min | Failure modes + mitigation, compliance risk |
| **D#8** | `08-reflection.md` | 10 min | Specific lessons, not generic |
| **D#9** | `09-self-spec-reflection.md` | 15 min | Run ONE D#4 spec through Claude Code, diagnose honestly |
| | **TOTAL** | **230 min** | You have 210 min — work fast |

### D#1: Problem Framing & Success Metrics
- "10x without 10x-ing" decoded into architectural requirements (e.g., "agent must hold N concurrent coordinator decisions/min")
- Measurable success metrics for MedFlex, hospitals, nurses
- What does it actually demand of architecture (not just a label)

### D#2: Engagement Intake & Scope
- Business context, stakeholder map (Marcus, Kim, Aaron, Linda), constraints, risks
- MVP scope definition with **concrete out-of-scope list with rationale** (interpret for your engagement, don't lift Gate3 pack verbatim)
- Address two failed AI projects explicitly

### D#3: Agentic Solution Architecture
- Specific agent decision points where contextual reasoning determines outcomes a rule-based system couldn't reach
- Delegation archetypes per workflow
- **Minimum 2 ADRs** with:
  - Alternatives considered (not just "we chose X")
  - Trade-off analysis (consequences of each option)
  - Why decision could be revisited (under what conditions)
- Avoid "justification theater" — real trade-offs only

### D#4: Two Production-Grade Capability Specifications (CRITICAL — 43% of exam time)
- Precise enough for Claude Code to build from without guessing at intent
- Shared entities consistent across both specs (one glossary)
- Worked examples for edge cases; marked assumptions with confidence levels
- Verification checklist:
  - [ ] No red flag words (valid, appropriate, handle)
  - [ ] 3+ worked examples per calculation
  - [ ] Constraints extracted to top with DO/DO NOT statements
  - [ ] Production readiness: error handling, validation, logging, concurrency
  - [ ] Edge cases listed explicitly
  - [ ] API failure modes covered (timeout, 500, 429, 401, partial response)
  - [ ] Happy path vs error path balanced (~50/50)

### D#5: Build-Loop Response Memo
- References Cascade Public Libraries fixture (`Deliverables/Build-loop-exercise-outcome-Andrzej_Bihun.md`)
- Each of 8 signals classified with response in correct tone per category
- Read spec alongside code — don't stop at first impression
- Tones: spec ambiguity ("I should have..."), builder misread (re-prompt, professional), unjustified choice (appreciate + reject + redirect), test problem (fix test), legitimate clarification (appreciate + revise + confirm)

### D#6: Client Feedback Response
- Friday morning's Marcus pushback memo loaded; each point addressed concretely
- Hold scope discipline: if you cave, name what gets cut; if you decline, propose concrete alternative
- "Yes, 6 weeks!" = capitulation (fail); stonewalling = fail; honest replanning = success

### D#7: Validation Plan
- Accuracy + edge cases + failure modes + compliance risk
- State portal rate limits, regulatory drift, model accuracy drift, single-points-of-failure — all named with mitigation

### D#8: Reflection Document
- Specific, not generic; honest assessment of what would change with more time

### D#9: Self-Spec Build-Loop Reflection (1 page) — CRITICAL
- Run ONE spec from D#4 through Claude Code under exam conditions
- Reflect: (a) what Claude built and whether it matches intent, (b) what questions it asked, (c) diagnosis of each gap, (d) what you'd change in 30 more minutes
- **Graded on diagnosis honesty, NOT code correctness**
- Broken build + honest diagnosis > working code by accident
- Avoid: "Claude mostly got it right" when it clearly didn't

---

## Friday Exam Flow (Gate3 pack §9 guidance)

- **0–20 min** — Re-read Thursday D#1-D#3 drafts + Marcus pushback memo; list what changed
- **20–60 min** — D#4 (capability specs) — don't skimp
- **60–90 min** — D#5 (build-loop response) — Cascade fixture, classify 8 signals
- **90–120 min** — D#6 (client feedback) + D#3 finalisation (update ADRs if pushback exposed weakness)
- **120–145 min** — D#7 (validation plan) + D#2 finalisation
- **145–175 min** — D#9 (self-spec reflection, 30 min clock)
- **175–195 min** — D#8 (reflection) + D#1 polish
- **195–210 min** — Final pass: hunt for AI-as-feature drift, cross-spec inconsistency, "mostly got it right" in #9, missing out-of-scope in #2, happy-path-only validation in #7

**Final pass priority: triage weakest deliverable, not polish the strongest.**

---

## Common Timing Mistakes to Avoid

❌ **WRONG**: "Friday 09:00-17:00 is the exam (8 hours)"
✅ **RIGHT**: 09:00-13:30 = prep time, 13:30-17:00 = exam time (3.5h)

❌ **WRONG**: "I'll submit Friday EOD"
✅ **RIGHT**: 17:00 SHARP — no extensions

❌ **WRONG**: "Thursday 23:59 D#1-D#3 must be perfect"
✅ **RIGHT**: Rough drafts fine — just input for CEO feedback generator

---

## W3D3 Build-Loop Exercise (Reference for D#5)

**File**: `FDE/Week 3/W3D3-BuildLoop-Exercise.md`
**Submitted**: ✅ `Deliverables/Build-loop-exercise-outcome-Andrzej_Bihun.md`

**Results**:
- 8/8 classifications correct (100% accuracy)
- Signals 3 & 6: Both unjustified implementation choices (return reminder, paused notification)
- Signal 7: Spec gap (R12 Note created ambiguity)
- Signal 8: Legitimate clarification request (Academic + Accessibility intersection)
- Key learning: When spec flags uncertainty (Assumptions, Notes), own it as spec ambiguity even if wording seemed clear

**The 8 signals** (for D#5 reference):
1. `notification_deadline.py` — 72-hour expiration logic (trap in R3: missing "if unclaimed" check)
2. `accessibility_priority.py` — Priority weight (NEW file builder added — unjustified)
3. `auto_checkout_handler.py` — Return reminder (unjustified implementation choice)
4. `test_overdrive_refresh.py` — Date-bound test fixture (fails in 2026 — test/environment issue)
5. `place_hold.py` — Duplicate hold rejection
6. `paused_holds.py` — Paused hold notification (unjustified implementation choice)
7. `sms_notification.py` — SMS-only vs dual-channel (spec gap)
8. Builder question — Academic + Accessibility intersection (legitimate clarification)

---

## Build-Loop Diagnosis Framework

### The 5 Categories

**Category 1: Spec Ambiguity** (YOU caused it)
- Signal: AI's code matches spec as written, but not your intent
- Fix: Rewrite spec to be precise, add worked examples
- Red flags: "valid," "appropriate," "handle," "check," "reasonable"

**Category 2: Builder Misread** (AI caused it)
- Signal: AI's code contradicts explicit spec statements
- Fix: Re-prompt with relevant spec section highlighted, don't change spec

**Category 3: Test/Environment Problem** (Test caused it)
- Signal: Code matches spec, test expectation is wrong
- Fix: Update the test, not the code or spec

**Category 4: Design Gap** (Spec incomplete)
- Signal: Build is "correct" but obviously incomplete for production
- Fix: Add missing requirement (error handling, concurrency, logging) to spec

**Category 5: Legitimate Clarification Request** (Expected behavior)
- Signal: Builder asks about genuine spec intersection gap
- Response: Appreciate + revise spec + confirm (reinforce correct behavior)

### Diagnostic Decision Tree

```
Does AI's code match spec AS WRITTEN?
├─ YES → Does it match your INTENT?
│         ├─ YES → Pass (no problem)
│         └─ NO → Cat 1: Spec Ambiguity — rewrite spec
└─ NO → Is AI's choice reasonable?
        ├─ YES → Is difference meaningful?
        │         ├─ YES → Cat 1: Spec Ambiguity — clarify spec
        │         └─ NO → Acceptable variation
        └─ NO → Does spec address this?
                ├─ YES → Cat 2: Builder Misread — re-prompt
                └─ NO → Cat 4: Design Gap — add to spec
(Always check: Test contradicts spec → Cat 3: Test Problem)
```

### Anti-Defensive Reading Checklist
- [ ] Did I read what I WROTE, not what I MEANT?
- [ ] Did I scan for red flag words?
- [ ] Did I ask "Could a 5-year-old do this from my words?"
- [ ] Am I blaming AI for something I left ambiguous?
- [ ] Did I read the Assumptions section first?

---

## FDE Methodology (ATX Framework)

### The ATX Process (4 Steps)

**Step 1: Discovery** — Find pain points from real workers, not SOPs. Output: volume-estimated task list.

**Step 2: Cognitive Load Mapping** — Jobs to be Done, Cognitive Zones (understand → gather → diagnose → decide → act), Breakpoints (where control shifts).

**Step 3: Delegation Qualification** — Score on 7 dimensions, assign archetype:

| Archetype | When to Use |
|-----------|-------------|
| Fully Agentic | High volume, structured, reversible, well-governed |
| Agent-Led + Human Oversight | High volume but needs human backstop |
| Human-Led + Agent Support | Complex analysis, agent synthesizes, human decides |
| Human-Led + Automation Support | Agent does rote tasks, human keeps control |
| Human Only | Ethics, tacit knowledge, irreversible |

**Anti-pattern**: NOT everything should be Fully Agentic. Good ATX shows mixed archetypes.

**Step 4: Prioritize** — Volume × Value grid, payback ≤ 18 months, Year 1 ROI > 0%.

### ATX Scoring Dimensions

| Dimension | Good for Agents | Bad for Agents |
|-----------|-----------------|----------------|
| Input Structure | Structured data | Messy, ambiguous |
| Decision Determinism | Follows patterns | Needs judgment |
| Tool Coverage | APIs available | Systems inaccessible |
| Context Complexity | Explicit rules | Tribal knowledge |
| Exception Rate | Rare edge cases | Frequent surprises |
| Latency | Can wait seconds | Needs instant response |
| Risk/Compliance | Low consequence, reversible | Irreversible, regulated |

### Key ATX Principles
1. **Start from LIVED work, not SOPs** — real work ≠ documented processes
2. **Owned agents, not rented** — own the orchestration logic, boundaries, prompts
3. **Platform thinking (compounding)** — reusable integrations; each new agent cheaper
4. **Cognitive work, not processes** — target interpretation, judgment, exception handling
5. **Economics must close BEFORE production** — token cost is both cost measure and governance instrument

### Buildability Standards (for D#4)
Specs must include:
- Entity definitions (tables, columns, types, constraints)
- State machines (status transitions, validation rules)
- API contracts (request/response formats with examples)
- Error handling for ALL failure modes (not just happy path)
- Escalation patterns with explicit triggers
- Worked examples for calculations/transformations
- Edge cases listed explicitly
- Production readiness: logging, metrics, alerts, concurrency, security

---

## Capability Spec Template (D#4)

```markdown
# Capability Spec: [Name]

## Constraints (Read First!)
DO: [specific actions]
DO NOT: [forbidden actions]

## Requirement: [Name]

### Description
[Concrete actions only — no abstract words]

### Examples (Worked)
- Input: [case 1] → Output: [expected 1]
- Input: [edge case] → Output: [expected 2]
- Input: [invalid] → Output: [error message]

### Edge Cases
- Happy path: [...]
- Empty/null input: [...]
- Concurrent requests: [...]
- Invalid values: [...]

### Error Handling
| Failure Mode | Response | Example |
|--------------|----------|---------|
| API timeout (>5s) | Escalate | "Unable to verify..." |
| Network error | Retry 3x, escalate | [...] |

### Process Steps
1. [Step with code/query example]
2. [Step with validation]
3. [Step with error handling]

### Observability
- Log: [what gets logged]
- Metrics: [what gets tracked]
- Alerts: [when to alert]

### Acceptance Criteria
- [ ] Accuracy: [measurable target]
- [ ] Performance: [response time]
- [ ] Error handling: [all modes covered]
```

---

## Anti-Patterns to Avoid

1. **AI-as-a-feature on traditional matching** — deterministic system with LLM sprinkled on, not AI-native
2. **Build-loop diagnostic stops at first impression** — name surface signal without reading spec + code together
3. **Client feedback appeased, not addressed** — "Yes CEO, 6 weeks!" = capitulation
4. **Self-spec reflection defends instead of diagnoses** — "mostly got it right" when it clearly didn't
5. **No ADR trade-off analysis** — "we chose X because it's right" without alternatives/consequences = theater
6. **Generic consulting templates** — ground everything in specific artefacts and constraints
7. **Spec with only happy path** — error path should be ~50% of spec coverage

---

## File Navigation

### Gate 3 scenario and requirements:
- `FDE/Week 3/Gate3-Participant-Pack.md` — full scenario, deliverables, scoring guidance

### Build-loop diagnostic reference:
- `FDE/Reference/spec-ambiguity-vs-builder-mistakes.md` — diagnostic taxonomy
- `Deliverables/Build-loop-exercise-outcome-Andrzej_Bihun.md` — your W3D3 results (reference for D#5)
- `FDE/Week 3/W3D3-BuildLoop-Exercise.md` — Cascade Public Libraries fixture

### Spec writing reference:
- `FDE/Reference/production-spec-checklist.md` — cross-check D#4 buildability
- `FDE/Reference/integration-spec-template.md` — template

### Discovery preparation:
- `FDE/Reference/discovery-questioning-patterns.md`

### ATX methodology:
- `FDE/Reference/atx/atx-concepts.md`

---

## Critical Success Factors

✅ **Genuinely AI-native solution** — agents as the mechanism, not a feature label
✅ **Accurate build-loop diagnosis** — classify signals correctly, right tone per category
✅ **Problem framing addresses real problem** — not just stated request
✅ **Honest self-spec build-loop reflection** — diagnosis quality > code correctness
✅ **Professional client feedback response** — hold scope, don't cave, don't stonewall
✅ **Specifications enable near-autonomous build** — no guessing at intent

## Verbal Defense Preparation

Coach probes:
- "The CEO's two failed AI projects — how is yours different?"
- "What kills this in production?"
- One specific architectural decision + one acknowledged weakness

Good defense: "I noticed that gap during the build-loop reflection and here's what I'd change"
Bad defense: "The spec is precisely correct"

---

## Contact & Support

For FDE program questions:
- Check Teams General channel for exact physical dates for virtual days
- Confirm verbal defense slot with coach on Friday
- Ask squad lead about submission format/location
