# D#2 — Engagement Intake & Scope

**Client:** MedFlex Healthcare Staffing  
**Engagement:** AI-native shift matching transformation  
**Prepared by:** Andrzej Bihun | Thursday interim draft

---

## 1. Business Context

MedFlex is a 200-person healthcare staffing agency operating B2B (hospital clients) and B2C (travel nurse supply) across 5 US states. After closing Series B, the board mandates $14M → $200M revenue in 24 months without proportional headcount growth. Two prior AI projects failed (hospital-facing chatbot, internal recommendation engine), leaving the CEO skeptical and the coordinator team resistant to change.

The core operational loop: hospital submits shift request → coordinator parses it → coordinator matches nurse → hospital accepts/rejects → nurse notified → nurse shows up (or doesn't). Every step in this loop is currently manual, serial, and bounded by 8 coordinator working hours.

---

## 2. Stakeholder Map

| Person | Role | Engagement Relevance |
|--------|------|----------------------|
| Marcus Reyes | CEO (sponsor) | Decision authority; revenue-focused; skeptical of AI; two past failures shape his risk tolerance |
| Kim | Head of Operations | Owns the matching workflow; source of truth for coordinator process detail; not available in discovery |
| Aaron | IT lead | System access, ServiceNow configuration, API availability; not available in discovery |
| Linda | Compliance lead | Nurse credentialing and re-verification process; not available in discovery |
| 8 Coordinators | Shift matching team | Primary workflow owners; change-resistance risk; 10-year veterans carry undocumented matching logic |
| Hospitals | B2B clients | Multi-agency sourcing; competitive market; reject mismatched nurses, causing reputational damage |
| Travel Nurses | Supply side | Self-manage availability; passive shift acceptance (no explicit confirmation); 12% no-show rate |

**Discovery gaps:** Kim (operational detail), Aaron (system internals), Linda (compliance cadence) were unavailable. Assumptions in this document are flagged where their input is needed.

---

## 3. Constraints

| Constraint | Source | Impact |
|------------|--------|--------|
| ServiceNow is the queue manager only — no matching logic | Discovery | Agent must integrate via ServiceNow API; matching logic built outside it |
| Hospital shift requests arrive as unstructured free text | Discovery | Intake parsing is a required agent capability |
| Nurse availability is self-managed; no push/sync API confirmed | Discovery | Agent reads availability data; cannot write it; staleness is a risk |
| Credential re-verification is a separate compliance team process | Discovery | Out of scope for coordinator agent; but agent must read credential status |
| No explicit nurse confirmation protocol exists today | Discovery | Agent must introduce one; nurse UX change required |
| Marcus has low AI trust; two prior failures | Discovery | Phase 1 must show measurable ROI within 6 weeks — board update is week 6; no extensions |
| Competitive market: same nurses submitted by multiple agencies | Discovery | Agent must handle double-booking race conditions |
| State regulatory requirements govern credential check cadence | Discovery (Linda TBD) | Compliance check frequency must respect state law; confirm with Linda |

---

## 4. MVP Scope

**What this engagement designs and specifies:**

1. **Intake Parsing Agent** — parse free-text shift requests from email/portal/phone into structured shift records
2. **Shift Matching Agent** — match structured shift records to qualified nurses; score confidence; auto-propose or escalate
3. **Confirmation & No-Show Prevention Agent** — notify matched nurse, request explicit confirmation, escalate if unconfirmed
4. **Coordinator Oversight Dashboard** — surfaces MEDIUM-confidence proposals for async review; exception queue; match audit trail
5. **Nurse reservation protocol** — atomic soft-lock to prevent double-booking across concurrent hospital submissions

**Phase 1 (Weeks 1-6) — Board demo target:**
- Intake parsing + Matching agent for HIGH-confidence (>85%) AND MEDIUM-confidence (70–85%) cases
- HIGH: auto-submit to hospital; 90-min non-blocking shadow review window for coordinator
- MEDIUM: auto-submit to hospital; 90-min coordinator recall window; unreviewed lapse escalates to team lead (not auto-cleared)
- LOW: agent surfaces ranked candidates to coordinator; coordinator decides
- Dashboard UI deferred to weeks 7–8; coordinators work from raw email/SMS alerts in weeks 1–6
- Target: 50% of daily proposals handled autonomously; response time <1h; live on real volume for week-6 board demo

**Phase 1b (Weeks 7-8) — Dashboard launch:**
- Coordinator review queue UI, audit trail, and recall interface deployed
- Full coordinator workflow adoption; no functional scope change to agents

**Phase 2 (Weeks 9-16):**
- Agent 3 confirmation loop launched (nurse explicit acceptance via SMS/email)
- No-show prevention state machine live
- Target: 75% autonomous; no-show rate decline starts

**Phase 3 (Weeks 17-24):**
- Nurse reputation model (hospital feedback signals)
- Predictive no-show detection
- Target: 85% autonomous; coordinator role = exception management

---

## 5. Explicit Out-of-Scope

| Item | Why Out of Scope |
|------|-----------------|
| Hospital-facing shift submission portal | Hospitals use existing channels (email/portal/phone); changing their UX is a separate commercial project |
| Nurse-facing mobile app | Nurses communicate via SMS/email today; new app is a separate product initiative |
| Pricing engine / margin optimisation | Commercial decision; not part of coordinator workflow |
| Continuing-education renewal automation | Compliance team's domain (Linda); separate system, separate team, separate regulatory cadence |
| Nurse onboarding / re-credentialing workflow | Out of scope per Marcus; compliance team owns this process |
| Agency-to-agency coordination | MedFlex cannot control competitor submission; out of scope |
| No-show root cause investigation and dispute resolution | Relationship-sensitive; human judgment required; agent surfaces the no-show, human resolves it |
| Coordinator headcount decisions / offboarding | HR and business decision; not part of this engagement |

**Important precision:** Compliance *check-at-match-time* (reading credential expiry from nurse profile before proposing) IS in scope — it's part of the coordinator's current workflow. Credential *re-verification* (the compliance team's cadence-based re-check process) is NOT in scope.

---

## 6. Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Coordinator resistance to agent adoption | High | Blocks Phase 2 | Phase 1 keeps coordinators in loop; frame as "coordinator gets to stop doing the boring part" |
| Nurse availability data is stale / unreliable | Medium | Wrong availability = failed proposals | Confirmation loop catches mismatches before shift date |
| Competitive double-booking unresolvable at scale | Medium | Hospital loses trust | Reservation protocol (see ADR in D#3) |
| Hospital rejects agent-proposed nurses at higher rate than human-proposed | Medium | Reputational damage | HIGH band (>85%) auto-submits; MEDIUM band (70–85%) has 90-min coordinator recall window as safety net. Weekly drift signals (acceptance rate trend + coordinator flag rate) detect rejection pattern from week 2 — before reputational damage accumulates |
| Kim / Aaron / Linda unavailable for design sign-off | High (discovery gap) | Spec gaps in D#4 | Flag assumptions explicitly; plan follow-up sessions before Phase 1 build |
| State regulatory requirements conflict with agent automation of credential checking | Unknown | Legal exposure | Confirm with Linda before Phase 2 launch |
