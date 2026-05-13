# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Context

This is an FDE (Full-Delivery Engineer) learning program repository for Week 3. The participant (Andrzej Bihun, Business Analyst) is working through an AI-native engagement simulation focused on building agentic solutions.

### Program Structure
- **Week 2**: Completed — Gate 2 deliverables archived and removed from this repo
- **Week 3 Current**: End-to-end AI-native engagement simulation (MedFlex healthcare staffing scenario)
- **Gate 3 Scenario**: `FDE/Week 3/Gate3-Participant-Pack.md` — released Thursday 09:00 CET

### Current Status (ALL DELIVERABLES COMPLETE — post-exam, pre-verbal-defense)
- ✅ Gate 3 scenario pack received and read
- ✅ Discovery role-play with Marcus Reyes completed (09:30-10:30 CET)
- ✅ W3D3 Build-loop exercise submitted: `FDE/Week 3/Build-loop-exercise-outcome-Andrzej_Bihun.md`
- ✅ D#1 final: `Deliverables/01-problem-framing.md` (revised — 6-week targets, leading indicators added)
- ✅ D#2 final: `Deliverables/02-intake-scope.md` (revised — Phase 1b added, 90-min window, 6-week constraint)
- ✅ D#3 final: `Deliverables/03-architecture.md` (revised — ADR-03 rewritten for 90-min window + LAPSED_UNREVIEWED; ADR-01 updated; Phase 1b added)
- ✅ D#4a capability spec: `Deliverables/04a-capability-spec-intake-parsing.md`
- ✅ D#4b capability spec: `Deliverables/04b-capability-spec-shift-matching.md` (revised — 90-min recall window, LAPSED_UNREVIEWED state, leading drift indicators in observability)
- ✅ D#4c capability spec: `Deliverables/04c-capability-spec-confirmation-noshow.md`
- ✅ D#5 build-loop response: `Deliverables/05-build-loop-response.md` (8 Cascade signals, all classified)
- ✅ D#6 client feedback: `Deliverables/06-client-feedback.md` (3 Marcus pushback points answered; 2 accepted, 1 acknowledged spec gap)
- ✅ D#7 validation plan: `Deliverables/07-validation-plan.md` (revised — Phase 1 Weeks 1-6, HIGH+MEDIUM, 90-min adoption target)
- ✅ D#8 reflection: `Deliverables/08-reflection.md` (written in B2 English; 4 lessons: business context, workflow observation, process diagram, employee pain points)
- ✅ D#9 self-spec reflection: `Deliverables/09-self-spec-reflection.md` (6 gaps diagnosed against D#4a/b)
- ✅ CIO presentation v2: `Deliverables/MedFlex-CIO-Presentation-v2.pdf` (6 slides; B2 English; new Slide 5 covers Marcus feedback + responses)
- ✅ Demo app updated: 90-min recall window, LAPSED_UNREVIEWED state, shadow_flagged field, Phase 1 drift indicator panel
- ✅ Cross-deliverable consistency verified: no stale 8-week or 30-min recall references remain
- **OUTSTANDING**: Verbal defense 17:50-19:00 CET

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
- **DRAFTED** — based on actual demo app build. 6 gaps identified:
  1. Double deduction on assumed credentials — Spec Ambiguity (worked example contradicts deduction table)
  2. `hosp_conf` excluded from confidence sum — Builder Misread
  3. Abbreviated time suffix `7p`/`7a` not matched — Spec Gap
  4. No stopwords for ALL-CAPS scan — Design Gap
  5. Assumed credentials in hard filter: main criterion vs. edge case row contradict — Spec Ambiguity (internal contradiction across D#4a/D#4b)
  6. `assumed_penalty = 0.10` added without spec authorisation — Unjustified Addition

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

## Demo App (`demo_app/`)

### Purpose
Local Streamlit web app demonstrating the three-agent MedFlex flow end-to-end. No database, no external integrations, no LLM — rule-based stubs throughout. Used for D#9 self-spec build-loop reflection.

### How to Run
```bash
cd demo_app
python -m streamlit run Home.py --server.headless true --browser.gatherUsageStats false
# Opens at http://localhost:8501
```

### Demo Scenarios (verified routing outcomes)
| Email | Agent 1 result | Agent 2 routing | Key driver |
|-------|---------------|-----------------|------------|
| Easy (St. Mary's, explicit ICU RN ACLS BLS) | PENDING_REVIEW, 100% confidence | AUTO_SUBMIT (0.955) | Sarah Johnson exact match, no assumed creds |
| Medium (Springfield General, "critical care" + "peds unit") | PENDING_REVIEW, 95% confidence | ASYNC_REVIEW (0.817) | 3 assumed creds → −0.10 penalty drops below 0.85 |
| Hard ("need a nurse ASAP for our ward") | ESCALATED, 10% confidence | Blocked (coordinator must override) | Missing date/time/hospital/credentials |

### Key Design Decisions (non-obvious)
- **Hard filter only checks `required_credentials`** (confirmed), not `assumed_credentials`. Assumed creds are soft signals — treating them as hard requirements caused NO_MATCH on the medium scenario (Pediatrics from "peds unit" blocked all ICU nurses).
- **`assumed_penalty = 0.10`** applied in `shift_matcher.run_matching()` when `req.assumed_credentials` is non-empty. Reduces routing confidence without changing the displayed score decomposition.
- **`MatchProposal.confidence_score` stores the adjusted (post-penalty) score**, not the raw soft-score total. This ensures the number shown in the UI is consistent with the routing decision.
- **`recall_window_expires_at`** — set to `proposed_at + 90 minutes` for ASYNC_REVIEW proposals only; None for all other routings. Based on Kim's input that coordinators batch-check every 1–2 hours.
- **`shadow_flagged: bool = False`** — on MatchProposal; allows coordinator to flag an AUTO_SUBMIT proposal during the 90-min shadow review window. Tracked as leading drift indicator.
- **LAPSED_UNREVIEWED status** — when an ASYNC_REVIEW proposal's recall window expires without the coordinator opening it, status becomes LAPSED_UNREVIEWED and escalates to team lead (15-min intervention window). Never auto-cleared.
- **Phase 1 Shadow Monitoring panel** in Agent 2 page shows two leading drift indicators (hospital acceptance rate by band, weekly coordinator flag rate) visible from week 2.
- **Nurse reservation** — 15-minute in-memory soft-lock per nurse in `st.session_state["reservations"]`. If all passing nurses are reserved, top candidate displayed without reservation.
- **`st.session_state` keys**: `shift_request` (Agent 1→2), `match_proposal` (Agent 2→3), `nurse_assignment` (Agent 3 internal), `reservations` (Agent 2 internal).

### Stub Data Design
Nurses engineered to produce varied outcomes for the same ICU shift (St. Mary's Boston):
- Sarah Johnson: 3mi, 0.92 reliability, HOSP-001 pref 0.90 → AUTO_SUBMIT top pick
- Michael Chen: 12mi, CCRN, HOSP-001 pref 0.70 → passes, lower score
- James Rodriguez: 35mi, 0.95 reliability → distance penalty
- David Kim: PICU not ICU → passes only if no ICU required in confirmed creds
- Emma Wilson, Lisa Park: fail hard filter for ICU shifts (no ICU credential)

---

## File Navigation

### Gate 3 scenario and requirements:
- `FDE/Week 3/Gate3-Participant-Pack.md` — full scenario, deliverables, scoring guidance

### Completed deliverables:
- `Deliverables/01-problem-framing.md` — D#1 final: 6-week targets, leading indicators, architectural requirements decoded
- `Deliverables/02-intake-scope.md` — D#2 final: Phase 1 (Wks 1-6) + Phase 1b (Wks 7-8), 90-min window, 6-week board deadline constraint
- `Deliverables/03-architecture.md` — D#3 final: 3 ADRs; ADR-03 revised for 90-min window + LAPSED_UNREVIEWED; Phase 1b added
- `Deliverables/04a-capability-spec-intake-parsing.md` — Agent 1 spec (shared entity glossary, 6 requirements)
- `Deliverables/04b-capability-spec-shift-matching.md` — Agent 2 spec (hard filter, soft scoring, routing, 90-min recall window, LAPSED_UNREVIEWED, Phase 1 shadow review + leading drift indicators)
- `Deliverables/04c-capability-spec-confirmation-noshow.md` — Agent 3 spec (state machine, reply classification, retry schedule)
- `Deliverables/05-build-loop-response.md` — D#5: 8 Cascade Public Libraries signals classified (3 builder misread, 2 unjustified choice, 1 test/env, 1 spec gap, 1 legitimate clarification)
- `Deliverables/06-client-feedback.md` — D#6: Marcus 3-point pushback response; 6-week accepted (dashboard deferred); leading indicators added; 90-min window + lapse escalation
- `Deliverables/07-validation-plan.md` — accuracy targets, failure modes, compliance risks, drift, SPoFs; Phase 1 Weeks 1-6, HIGH+MEDIUM scope
- `Deliverables/08-reflection.md` — D#8: 4 lessons in B2 English (business context, workflow observation, process diagram, employee pain points)
- `Deliverables/09-self-spec-reflection.md` — D#9: 6 gaps diagnosed against D#4a/D#4b actual build; 4 spec-owned, 1 builder misread, 1 unjustified addition
- `Deliverables/MedFlex-CIO-Presentation-v2.pdf` — 6-slide CIO deck in B2 English; Slide 5 = Marcus feedback response (generated via `generate_cio_presentation.py`)
- `FDE/Week 3/Build-loop-exercise-outcome-Andrzej_Bihun.md` — W3D3 exercise submission (reference for D#5)

### Demo app:
- `demo_app/Home.py` — entry point + flow overview
- `demo_app/core/intake_parser.py` — rule-based parser (regex date/time, credential taxonomy, confidence scoring)
- `demo_app/core/shift_matcher.py` — hard filter + soft scoring + routing + reservation
- `demo_app/core/confirmation_agent.py` — state machine + reply classification
- `demo_app/stubs/nurse_db.py` — 6 hardcoded nurses
- `demo_app/stubs/hospital_registry.py` — 3 hospitals + email domain lookup

### Build-loop diagnostic reference:
- `FDE/Reference/spec-ambiguity-vs-builder-mistakes.md` — diagnostic taxonomy
- `FDE/Week 3/Build-loop-exercise-outcome-Andrzej_Bihun.md` — your W3D3 results (reference for D#5)
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
