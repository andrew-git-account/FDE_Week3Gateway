import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from datetime import datetime

from core.shift_matcher import run_matching
from stubs.nurse_db import get_all_nurses

st.set_page_config(page_title="Agent 2 — Shift Matching", page_icon="🔍", layout="wide")

st.title("Agent 2 — Shift Matching")
st.caption("Hard filter → soft scoring → confidence-gated routing")

# ── ShiftRequest banner ───────────────────────────────────────────────────────
req = st.session_state.get("shift_request")

if req is None:
    st.warning("No ShiftRequest found. Please complete Agent 1 first.")
    if st.button("← Go to Agent 1"):
        st.switch_page("pages/1_Agent1_Intake_Parsing.py")
    st.stop()

with st.container(border=True):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Hospital", req.hospital_name or "Unknown")
    c2.metric("Shift Date", str(req.shift_date) if req.shift_date else "—")
    c3.metric("Time", f"{req.shift_start_time}–{req.shift_end_time}" if req.shift_start_time else "—")
    c4.metric("Urgency", req.urgency)
    st.caption(f"Credentials required: {', '.join(req.required_credentials + req.assumed_credentials) or '—'} | "
               f"Specialty: {req.specialty or '—'} | Parse confidence: {req.parse_confidence:.0%}")

st.divider()

# ── Run matching ──────────────────────────────────────────────────────────────
if "reservations" not in st.session_state:
    st.session_state["reservations"] = {}

run_clicked = st.button("⚙ Run Matching", type="primary")

if run_clicked:
    nurses = get_all_nurses()
    proposal = run_matching(req, nurses, st.session_state["reservations"])
    st.session_state["_last_proposal"] = proposal

proposal = st.session_state.get("_last_proposal")

if proposal is None:
    st.info("Click **Run Matching** to evaluate candidates.")
    st.stop()

# ── Hard filter results ───────────────────────────────────────────────────────
st.markdown("### Hard Filter Results")

filter_data = []
for c in proposal.all_candidates:
    filter_data.append({
        "Nurse": c.nurse.name,
        "Result": "✅ PASS" if c.passed_hard_filter else "❌ FAIL",
        "Reason": c.hard_filter_failure or "—",
        "Credentials": ", ".join(c.nurse.credentials),
        "Compliance Until": str(c.nurse.compliance_valid_until),
    })
st.dataframe(filter_data, use_container_width=True, hide_index=True)

# ── Soft scoring ──────────────────────────────────────────────────────────────
passing = [c for c in proposal.all_candidates if c.passed_hard_filter]

if passing:
    st.markdown("### Soft Scoring (passing candidates)")
    score_data = []
    for c in sorted(passing, key=lambda x: -x.score_breakdown.total):
        sb = c.score_breakdown
        selected_marker = " ⭐ Selected" if c.nurse.nurse_id == (proposal.nurse.nurse_id if proposal.nurse else None) else ""
        score_data.append({
            "Nurse": c.nurse.name + selected_marker,
            "Proximity (30%)": f"{sb.proximity_score:.2f}",
            "Hosp. Preference (25%)": f"{sb.preference_score:.2f}",
            "Reliability (25%)": f"{sb.reliability_score:.2f}",
            "Specialty (20%)": f"{sb.specialty_score:.2f}",
            "Total": f"{sb.total:.3f}",
            "Notes": " | ".join(sb.notes),
        })
    st.dataframe(score_data, use_container_width=True, hide_index=True)

st.divider()

# ── Routing decision ──────────────────────────────────────────────────────────
st.markdown("### Routing Decision")

routing = proposal.routing
conf = proposal.confidence_score

if routing == "AUTO_SUBMIT":
    st.success(f"🟢 **AUTO_SUBMIT** — confidence {conf:.0%}  \n"
               f"Proposal submitted to hospital automatically. "
               f"Phase 1: coordinator sees in audit log; 30-min non-blocking recall window.")

elif routing == "ASYNC_REVIEW":
    st.warning(f"🟡 **ASYNC_REVIEW** — confidence {conf:.0%}  \n"
               f"Proposal submitted to hospital. Coordinator has 30 minutes to recall.")

elif routing == "HUMAN_ESCALATE":
    st.error(f"🔴 **HUMAN_ESCALATE** — confidence {conf:.0%}  \n"
             f"Proposal NOT sent. Coordinator selects from ranked candidates below.")

elif routing == "NO_MATCH":
    st.error("⛔ **NO_MATCH** — no nurses passed the hard filter.  \n"
             "Escalated to coordinator with failure breakdown.")
    st.stop()

# ── Action panel ──────────────────────────────────────────────────────────────
st.divider()
st.markdown(f"**Selected nurse:** {proposal.nurse.name if proposal.nurse else '—'} | "
            f"Confidence: {conf:.3f} | Distance: {proposal.nurse.distance_miles if proposal.nurse else '—'} miles")

if routing in ("AUTO_SUBMIT", "ASYNC_REVIEW"):
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✅ Simulate Hospital Accept", type="primary", use_container_width=True):
            proposal.status = "ACCEPTED"
            st.session_state["_last_proposal"] = proposal
            st.session_state["match_proposal"] = proposal
            st.rerun()

    with col2:
        if st.button("❌ Simulate Hospital Reject", use_container_width=True):
            proposal.status = "REJECTED"
            st.session_state["_last_proposal"] = proposal
            st.warning("Hospital rejected. Proposal recalled. Re-run matching to try next candidate.")

    if routing == "ASYNC_REVIEW":
        with col3:
            if st.button("↩ Coordinator Recall", use_container_width=True):
                proposal.status = "RECALLED"
                st.session_state["_last_proposal"] = proposal
                st.info("Proposal recalled by coordinator. Re-run matching to adjust.")

elif routing == "HUMAN_ESCALATE":
    st.markdown("**Coordinator: select a candidate to assign**")
    nurse_options = {c.nurse.name: c.nurse for c in passing}
    selected_name = st.selectbox("Select nurse", list(nurse_options.keys()))
    if st.button("✅ Assign Selected Nurse", type="primary"):
        selected_nurse = nurse_options[selected_name]
        selected_candidate = next(c for c in passing if c.nurse.nurse_id == selected_nurse.nurse_id)
        proposal.nurse = selected_nurse
        proposal.score_breakdown = selected_candidate.score_breakdown
        proposal.confidence_score = selected_candidate.score_breakdown.total
        proposal.status = "ACCEPTED"
        proposal.proposed_at = datetime.utcnow()
        st.session_state["_last_proposal"] = proposal
        st.session_state["match_proposal"] = proposal
        st.rerun()

# ── Navigate to Agent 3 ───────────────────────────────────────────────────────
if proposal.status == "ACCEPTED":
    st.success(f"✓ Hospital accepted — **{proposal.nurse.name}** assigned.")
    if st.button("→ Send to Agent 3 — Confirmation", type="primary"):
        st.switch_page("pages/3_Agent3_Confirmation.py")
