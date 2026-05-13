# Deliverable 9 — Self-Spec Build-Loop Reflection

**Spec used:** `04a-capability-spec-intake-parsing.md` (Agent 1 — Intake Parsing Agent)
**Scope:** End-to-end demo build of the three-agent MedFlex flow in Streamlit, with Agent 1 (`core/intake_parser.py`) as the primary focus. Integration-testing across all three agents surfaced additional gaps in `04b-capability-spec-shift-matching.md`.
**Build duration:** Full session (not a fresh 30-minute run — this is an honest reflection on the actual build)

---

## (a) What Claude Code built and whether it matches intent

Claude Code built a working `intake_parser.py` implementing all six requirements: date/time extraction, credential parsing, hospital identity resolution, confidence scoring, preview queue logic, and escalation. The three sample emails produce the intended routing outcomes after corrections. On first build, the code was structurally correct but four signals required intervention before results matched spec intent.

The match to intent is partial. The structure is right; several numerical results were wrong due to gaps in the spec's arithmetic specification.

---

## (b) What it asked — and what it should have asked but didn't

Claude Code did not ask clarifying questions before building. It made four silent decisions that turned out to be wrong or underspecified. The questions that should have been explicitly raised before implementation:

1. **Confidence deduction scope:** Are assumed-credential deductions applied within the credentials component (reducing it from 0.25), or as post-sum deductions from the total?
2. **Time format enumeration:** Are abbreviated suffixes `7p` and `7a` (without `m`) valid inputs, or only `am`/`pm`/24h?
3. **Stopwords for ALL-CAPS scanning:** What tokens should be excluded from the credential scan (common words that happen to be uppercase)?
4. **Assumed credentials in hard filter:** The main criterion says CONFIRMED only; the edge case table says apply to ASSUMED too. Which governs?

None of these were asked. The builder resolved them by making a choice, and corrections happened downstream when test results diverged from expected behaviour.

---

## (c) Diagnosis of each gap

**Gap 1 — Double deduction on assumed credentials**
*Category: Spec Ambiguity*
The credentials component internally deducted 0.05 per assumed credential, then `parse()` applied the same deduction again. Root cause: the spec's deduction table (`−0.05 per assumed`) and the worked example (`credentials: 0.15 (one assumed)`, implying −0.10 for one) contradict each other. The builder could not have resolved this without guessing. I should have made the formula unambiguous: either show exact arithmetic in the example or state where in the calculation the deduction applies.

**Gap 2 — `hosp_conf` excluded from confidence sum**
*Category: Builder Misread*
The spec states "weighted sum of four component scores" and names hospital identity as one. The implementation summed only three. The spec is clear; the builder dropped a component. Re-prompting with the scoring formula table resolved it.

**Gap 3 — Abbreviated time suffix `7p`/`7a` not matching**
*Category: Spec Gap (Design Gap)*
The spec's worked examples show `19:00–07:00` and "7pm to 7am" but never specify `7p` or `7a` as valid inputs. The regex pattern only matched `am`/`pm`. A real hospital email used this format. The spec needed an explicit list of accepted time suffixes, or a regex pattern, in Requirement 1.

**Gap 4 — False unresolved credentials from stopwords**
*Category: Design Gap*
The spec says "ALL-CAPS abbreviation not in taxonomy → store in `unresolved_credentials[]`." This is correct as stated, but the spec gave no exceptions. "ASAP", "URGENT", "STAT" all triggered false escalations. A stopwords list (or an explicit note that non-credential ALL-CAPS tokens should be filtered by context) was missing from Requirement 2.

**Gap 5 — Assumed credentials in hard filter (D#4b contradiction)**
*Category: Spec Ambiguity — internal contradiction*
D#4b's hard filter criterion says `required_credentials (CONFIRMED)` only. Its edge case table says "Apply hard filter on the ASSUMED credential." These conflict. The builder followed the edge case table, causing all nurses to fail for the medium email (Pediatrics, inferred from "peds unit", blocked every ICU nurse). The correct behaviour is CONFIRMED-only in hard filter; assumed credentials belong in soft scoring. The edge case row was wrong and I should have caught it in the spec review. This gap was only visible through integration testing across both agents.

**Gap 6 — `assumed_penalty = 0.10` added without spec authorisation**
*Category: Unjustified Implementation Addition*
An `assumed_penalty` of 0.10 was added to `shift_matcher.run_matching()` to produce ASYNC_REVIEW routing for the medium email. This is not in D#4b. It was added to make the demo scenarios differentiable. It produces correct demo behaviour but deviates from spec. This addition should either be backed out, or added to D#4b as an explicit requirement with a worked example showing the adjustment.

---

## (d) What I would change in the spec with 30 more minutes

**Requirement 4 (Confidence Scoring) — fix the arithmetic inconsistency:**
Change worked Example 2 to show `credentials: 0.20 (one assumed, −0.05)` or change the deduction table to `−0.10 per assumed`. Pick one; delete the other. Add a note: "Deductions are applied within each component score, not from the total."

**Requirement 1 (Date/Time) — specify valid time suffixes explicitly:**
Add to the worked examples or edge case table: "Accepted time formats include: `7am`, `7:00am`, `0700`, `7pm`, `7p`, `7a` (abbreviated single-character suffix treated as am/pm)."

**Requirement 2 (Credentials) — add stopword exclusion rule:**
Add an edge case row: "ALL-CAPS tokens that are common language words (`ASAP`, `URGENT`, `STAT`, `UNIT`, `WARD`, `PLEASE`) are excluded from credential scanning. If a new all-caps token appears and is ambiguous, store in `unresolved_credentials[]`."

**D#4b Hard Filter edge case — delete the contradictory row:**
Remove "Apply hard filter on the ASSUMED credential" from the edge case table. Replace with: "ASSUMED credentials are not hard filter criteria — they reduce soft scoring confidence only. Coordinator can see assumed credentials in the proposal rationale."

---

## Reflection

The most instructive gap was the internal contradiction in D#4b (assumed credentials). I wrote the edge case table row independently of the main criterion, and didn't catch that they conflict. This is precisely the anti-pattern the spec checklist warns about: edge cases added without checking consistency against the main requirement. The contradiction was invisible until integration testing across two agents produced a NO_MATCH that should have been ASYNC_REVIEW.

The second lesson: the spec's worked examples are the most testable part of the spec — but only if the arithmetic is actually correct. Example 2 of Requirement 4 has a computation error that the builder faithfully reproduced. Running even one manual calculation against the example before submission would have caught it.

The build produced working code. But "working" in a demo with stub data is not the same as "correct against spec." Four of six gaps were in the spec, not the code — which means the spec would have produced the same mismatches against a production AI builder as it did here.
