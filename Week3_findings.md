# Week 3 FDE Program - Findings & Summary

**Program:** Full-Delivery Engineer (FDE) Internal Training  
**Week:** 3 of 5  
**Role:** Business Analyst Participant  
**Date Analyzed:** 2026-05-08

---

## Overview: End-to-End AI-Native Engagement

Week 3 integrates the skills from Weeks 1 and 2 into a **complete FDE engagement simulation**. You'll execute the full cycle: messy discovery → agentic solution design → production-grade specification → build-loop correction → stakeholder management.

**Scenario:** MedFlex healthcare staffing agency (200 employees) wants to "10x the business without 10x-ing the coordinators." CEO is impatient after two failed AI projects (chatbot and recommendation engine).

---

## Core Skills to Demonstrate by Friday

By end of Week 3, you must prove you can:

1. ✅ **Navigate realistic discovery** with incomplete/contradictory information
2. ✅ **Design AI-native agentic solutions** (agents as primary mechanism, not bolt-on features)
3. ✅ **Write production-grade specifications** precise enough for AI coding agents to build from
4. ✅ **Diagnose build-loop failures** accurately:
   - Spec gap (you fix via spec revision)
   - Builder misread (builder fixes via direct correction)
   - Unjustified implementation choice (collaborative removal)
   - Test/environment issue (diagnostic fix)
   - Legitimate unknown (acknowledge + revise + confirm)
5. ✅ **Handle client pushback** and scope pressure professionally
6. ✅ **Write Architecture Decision Records (ADRs)** with explicit trade-off analysis
7. ✅ **Run closed loop on your own spec** under exam conditions with honest diagnosis

---

## Week 3 Detailed Schedule

### **Monday (Virtual Day 1)**
**Timeline:** TBD - confirmed in Teams General channel

**Activities:**
- 1-hour coach-led week orientation
- Self-directed preparation begins

**Required Actions:**
- Read `../Reference/spec-ambiguity-vs-builder-mistakes.md` end-to-end (including FDE Response Protocol)
- Audit your Week 2 specs for ambiguities
- Prepare personal note: identify one ambiguous requirement from your own work

---

### **Tuesday (Virtual Day 2)**

**Activities:**
- Continue self-directed preparation
- Production-spec-checklist audit of draft specs

**Required Actions:**
- Deep dive into production-spec-checklist.md
- Practice applying checklist to any draft specs you've started

---

### **Wednesday (Virtual Day 3) - Build-Loop Diagnosis Day**

**Critical Prep - By 09:00 CET:**
- Submit one-line classification prediction to critique pool: *"The hardest part of build-loop diagnosis for me will be ___."*

**Morning Session (90 minutes):**
- Whole-cohort coach-led build-review walkthrough
- Fixture: **Coffee Subscription Credit Handler**
- Coach demonstrates live diagnosis of each category:
  - Spec gap
  - Builder misread
  - Unjustified implementation choice
  - Test/environment issue
  - Legitimate unknown

**Afternoon Session:**
- Solo build-loop exercise on **different** fixture
- Fixture: **Cascade Public Libraries Hold Queue** (released at end of morning session)
- Document: `W3D3-BuildLoop-Exercise.md`

**Submission:**
- Submit your Cascade fixture diagnosis to squad lead by EOD Wednesday
- NOT a Gate 3 deliverable, but feeds into Deliverable #5 on Friday

**Required Preparation (must complete before 09:00):**
1. Read `spec-ambiguity-vs-builder-mistakes.md` end-to-end
2. Audit your own Week 2/Week 3 draft spec for at least one ambiguous requirement
3. Submit classification prediction to critique pool

---

### **Thursday (Virtual Day 4) - Discovery & Initial Design**

**09:00 CET:**
- **Gate 3 scenario released** - `Gate3-Participant-Pack.md`
- Read end-to-end before discovery call

**09:30-10:30 CET:**
- **Live 60-minute simulated client discovery session**
- All 10 squads run in parallel
- Coach (or designated squad lead) plays named MedFlex stakeholder
- You ask questions; they answer (some precisely, some vaguely, some contradictorily)
- Extract what you need to design the right solution
- Notice inconsistencies and gaps

**Afternoon:**
- Specification work based on discovery findings
- Draft Deliverables #1 (problem framing), #2 (intake & scope), #3 (architecture + ADRs)
- Rough drafts are fine - this is NOT final submission

**By 23:59 CET Thursday:**
- **Submit interim engagement design** to squad lead
- Deliverables: whatever you've drafted of D#1, D#2, D#3
- **NOT GRADED** - this is input for personalized CEO feedback overnight
- Rough drafts acceptable

---

### **Friday (Virtual Day 5) - Gate 3 Exam Day**

**09:00 CET:**
- Receive **personalized client feedback** - Marcus Reyes (CEO) email
- Pushback tailored to YOUR specific interim design
- Includes: timeline pressure + scope/architecture pushback + stakeholder/operational complications

**09:00-13:30 CET - UNTIMED PREPARATION (4.5 hours):**
- **NOT THE GATE YET - THIS IS PREP TIME**
- Read Marcus's pushback closely
- Decide: which points to concede with concrete alternatives vs hold scope on
- Refine your D#1-D#3 thinking against discovery + pushback evidence
- Plan your D#6 response strategy
- **DO NOT finalize deliverables in this window**

**13:30-17:00 CET - TIMED GATE 3 EXAM (3.5 hours):**
- Produce all 9 deliverables under exam conditions
- Final, polished, complete
- Single markdown folder submission

**17:00 CET SHARP:**
- **SUBMISSION CUTOFF** (NOT EOD!)
- Anything not in the package at 17:00 is not graded

**17:50-19:00 CET:**
- **10-minute verbal defense** with coach
- 5-minute stagger per participant
- Coach probes:
  - One architectural decision (defend with trade-off reasoning)
  - One acknowledged weakness (honest acknowledgment)
  - "The CEO's two failed AI projects - how is yours different?"
  - "What kills this in production?"
- Specific slot confirmed by your coach

**Following Monday (Week 4):**
- Gate 3 results released

---

## Gate 3 Deliverables (9 Total)

Must submit by 17:00 Friday in single markdown folder:

### **D#1: Problem Framing & Success Metrics**
- What is actually broken (not just stated request)
- Measurable success outcomes for:
  - MedFlex (the company)
  - Hospitals (the clients)
  - Nurses (the workers)
- Focus on business problem, not technical request

### **D#2: Engagement Intake & Scope**
- Business context
- Stakeholder map
- Constraints
- Risks
- MVP scope definition
- **What's OUT of scope and why** (explicit boundaries)

### **D#3: Agentic Solution Architecture**
- Which workflow parts become agentic
- Delegation levels for each agent
- **At least 2 ADRs** with:
  - Alternatives considered
  - Trade-off analysis
  - Consequences of each option
  - Why decision could be revisited later
- Avoid justification theater ("We chose X because it's right")

### **D#4: Two Production-Grade Capability Specifications**
- Precise enough for Claude Code to build from
- Shared entities consistent across both specs
- Near-autonomous build enablement
- Where ambiguity unavoidable, name it as assumption with confidence level
- **Heaviest deliverable - will consume largest share of 3.5 hours**

### **D#5: Build-Loop Response Memo**
- References Wednesday's Cascade Public Libraries fixture
- Different domain from MedFlex (same diagnostic move)
- What did the build get wrong?
- What did your spec leave unclear?
- What must change?
- Correct classification and tone per category

### **D#6: Client Feedback Response**
- Professional response to Marcus's pushback
- Address each pushback point concretely
- Scope discipline - hold boundary without alienating
- Avoid capitulation ("Yes, 6 weeks!") and stonewalling
- Honest replanning where needed

### **D#7: Validation Plan**
- How do you know the agentic system works?
- What to test before production?
- Testing strategy

### **D#8: Reflection Document**
- What would you do differently?
- What did you learn about your own process?
- Process improvements identified

### **D#9: Self-Spec Build-Loop Reflection (1 page)**
- Take ONE of your two D#4 capability specs
- Run it through Claude Code under exam conditions
- Write 1-page reflection:
  - What it built
  - What it asked
  - What you'd change in the spec
- **Graded on diagnosis honesty, NOT code correctness**
- Broken build with honest diagnosis > working code by accident

---

## Timeline: When You Work on What

**Wednesday Afternoon:**
- Cascade Public Libraries Hold Queue fixture diagnosed
- Submitted to squad lead (feeds D#5 on Friday)

**Thursday Morning (09:30-10:30):**
- Discovery role-play
- Input gathering for D#1, D#2, D#3
- No writing yet

**Thursday Afternoon:**
- Rough drafts of D#1, D#2, D#3
- Based on discovery + scenario pack

**Thursday 23:59:**
- Interim submission of D#1, D#2, D#3 to squad lead
- Not graded - input for Marcus pushback generator

**Friday 09:00-13:30 (Untimed Prep):**
- Read Marcus's personalized pushback
- Refine D#1/D#3 thinking against it
- Plan D#6 response strategy (concede vs hold scope)
- No deliverables finalized

**Friday 13:30-17:00 (Timed Gate - 3.5h):**
- Finalize everything:
  - Revise D#1-D#3 against Marcus + clearer thinking
  - Produce D#4 (two capability specs - heaviest work)
  - Write D#5 (build-loop response on Cascade)
  - Write D#6 (client feedback response)
  - Produce D#7 (validation plan)
  - Produce D#8 (reflection)
  - Produce D#9 (self-spec build-loop reflection)

**Friday 17:00:**
- Submission cutoff

---

## What Coaches Are Looking For

### **Critical Success Factors:**

1. **Genuinely AI-Native Solution**
   - Agents are the mechanism, not a feature label
   - Not traditional matching algorithm with LLM sprinkled on top
   - Coach will ask: "Show me the agent decision - the specific point where reasoning over context determines an outcome that a rule-based system couldn't reach"

2. **Accurate Build-Loop Diagnosis**
   - Classify signals correctly
   - Write right corrective response in right tone for each category
   - Go beyond surface signal to read spec alongside code

3. **Problem Framing Addresses Real Problem**
   - Not just the stated request
   - "10x without 10x-ing" is not a technical requirement
   - Figure out what it actually demands of architecture

4. **Honest Self-Spec Build-Loop Reflection**
   - Spec producing broken build but diagnosed precisely > working code by accident
   - Graded on diagnosis quality, not build-output correctness
   - Avoid defensive reading or bluffing

5. **Professional Client Feedback Response**
   - Hold boundary without alienating
   - Neither caving nor stonewalling
   - Scope discipline with honest replanning

6. **Specifications Enable Near-Autonomous Build**
   - AI coding agent shouldn't need to guess at intent
   - Where ambiguity unavoidable, name it as assumption with confidence level

---

## Common Week 3 Failure Modes to Avoid

### **1. AI-as-a-Feature on Traditional Matching**
- **What it looks like:** Deterministic matcher with LLM call sprinkled on top
- **Why it fails:** Not AI-native architecture
- **How coaches test:** "Show me the agent decision in your design"

### **2. Build-Loop Diagnostic Stops at First Impression**
- **What it looks like:** "The test is wrong"
- **Why it fails:** Misses that test reflects real spec gap in expiry semantics
- **How to avoid:** Read spec alongside code for second-order analysis

### **3. Client Feedback is Appeased, Not Addressed**
- **What it looks like:** "Yes CEO, we'll deliver in 6 weeks"
- **Why it fails:** Capitulation that breaks at week 4
- **How to succeed:** Scope discipline and honest replanning

### **4. Self-Spec Reflection Defends Instead of Diagnoses**
- **What it looks like:** "Claude Code mostly got it right, just needs minor polish"
- **Why it fails:** Defensive reading when Claude clearly missed the point
- **How to succeed:** Honest diagnosis ("Claude built X because my spec failed to distinguish Y from Z; I'd add worked example for case A")

### **5. No ADR Trade-Off Analysis**
- **What it looks like:** "We chose X because it is the right choice"
- **Why it fails:** Decision theater without alternatives or trade-offs
- **How to succeed:** Name alternatives considered, consequences of each, why decision could be revisited

---

## Required Reading & Resources

### **Must Read Before Wednesday 09:00:**
- `FDE/Reference/spec-ambiguity-vs-builder-mistakes.md` (including FDE Response Protocol)

### **Build-Loop & Spec Quality:**
- `FDE/Reference/production-spec-checklist.md`
- `FDE/Reference/spec-ambiguity-vs-builder-mistakes.md`
- Kent Beck: Augmented Coding - https://tidyfirst.substack.com/p/augmented-coding-beyond-the-vibes

### **Architecture Decisions:**
- ADR overview and templates - https://adr.github.io/
- ADR examples - https://github.com/joelparkerhenderson/architecture-decision-record
- AWS: ADR Best Practices - https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/

### **AI Governance:**
- NIST AI Risk Management Framework - https://www.nist.gov/itl/ai-risk-management-framework
- Microsoft: Responsible AI Principles - https://learn.microsoft.com/en-us/training/modules/embrace-responsible-ai-principles-practices/
- Google: Responsible AI Practices - https://ai.google/responsibility/responsible-ai-practices/

### **Specification Craft:**
- `FDE/Reference/integration-spec-template.md`
- `FDE/Reference/discovery-questioning-patterns.md` (review before Thursday discovery)

### **Carried Forward from Week 2:**
- ATX framework references (`FDE/Week 2/references/atx-*.md`)
- Cognitive Load Map and Delegation Matrix still use ATX vocabulary

---

## Assessment Notes

- **Friday has no peer cross-review window** (unlike previous weeks)
- Engagement simulation runs Thursday-Friday back-to-back
- Assessment flow: self-assessment → coach review → live verbal defense
- Scoring rubric held by coach and NOT shared with participants from Week 3 onward
- See §7 of `Gate3-Participant-Pack.md` for explanation

---

## Immediate Action Items

### **Before Monday Session:**
- [ ] Review this findings document
- [ ] Familiarize with Week 3 structure and timing
- [ ] Note Friday timing in calendar (09:00, 13:30, 17:00, 17:50)

### **Monday-Tuesday Prep:**
- [ ] Read `spec-ambiguity-vs-builder-mistakes.md` end-to-end
- [ ] Review `production-spec-checklist.md`
- [ ] Audit Week 2 specs for ambiguities
- [ ] Prepare one-line classification prediction for Wednesday
- [ ] Research ADR best practices
- [ ] Review `discovery-questioning-patterns.md`

### **Before Wednesday 09:00:**
- [ ] Complete all required preparation (taxonomy, audit, prediction)
- [ ] Submit classification prediction to critique pool
- [ ] Be ready for fast-paced walkthrough

### **Thursday Prep:**
- [ ] Read Gate3-Participant-Pack.md as soon as released (09:00)
- [ ] Prepare discovery questions before 09:30 call
- [ ] Have note-taking system ready for discovery session

### **Friday Prep:**
- [ ] Understand Friday timing: 09:00 (prep starts), 13:30 (gate starts), 17:00 (cutoff)
- [ ] Set up environment for Claude Code self-spec run (D#9)
- [ ] Have markdown folder structure ready for all 9 deliverables

---

## Key Dates to Confirm

Check Teams General channel at start of week for exact physical dates for:
- Monday orientation (1h)
- Wednesday morning walkthrough (90 min)
- Thursday discovery session (09:30-10:30 CET)
- Friday all-day events (09:00, 13:30, 17:00, 17:50)

---

## Questions to Ask Coach/Squad Lead

1. Exact physical dates for each virtual day (check Teams General)
2. Specific verbal defense slot on Friday (17:50-19:00 range)
3. Submission format/location for interim Thursday deliverables
4. Submission format/location for final Friday deliverables
5. Any squad-specific guidance for discovery session format

---

**Document Status:** Initial analysis complete  
**Next Review:** After Monday orientation  
**Owner:** Andrzej Bihun (BA, FDE Week 3 Participant)
