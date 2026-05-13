import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from core.confirmation_agent import (
    create_assignment, send_notification, process_reply,
    simulate_no_reply_timeout, simulate_no_show,
    coordinator_confirm, coordinator_cancel,
)

st.set_page_config(page_title="Agent 3 — Confirmation", page_icon="✅", layout="wide")

st.title("Agent 3 — Confirmation & No-Show Prevention")
st.caption("Explicit confirmation loop | State machine | Escalation handling")

# ── Require proposal ──────────────────────────────────────────────────────────
proposal = st.session_state.get("match_proposal")

if proposal is None or proposal.status != "ACCEPTED":
    st.warning("No accepted MatchProposal found. Please complete Agent 2 first.")
    if st.button("← Go to Agent 2"):
        st.switch_page("pages/2_Agent2_Shift_Matching.py")
    st.stop()

req = st.session_state.get("shift_request")

# ── Create or load assignment ─────────────────────────────────────────────────
if "nurse_assignment" not in st.session_state or st.session_state["nurse_assignment"].match_proposal.id != proposal.id:
    st.session_state["nurse_assignment"] = create_assignment(proposal, req)

assignment = st.session_state["nurse_assignment"]

# ── Assignment banner ─────────────────────────────────────────────────────────
with st.container(border=True):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Nurse", proposal.nurse.name)
    c2.metric("Hospital", req.hospital_name if req else "—")
    c3.metric("Shift Date", str(req.shift_date) if req else "—")
    c4.metric("Time", f"{req.shift_start_time}–{req.shift_end_time}" if req and req.shift_start_time else "—")
    st.caption(f"Notification channel: {proposal.nurse.communication_preference} | "
               f"Assignment ID: {assignment.id}")

st.divider()

# ── State machine visual ──────────────────────────────────────────────────────
STATUS_COLORS = {
    "PENDING_CONFIRMATION": ("🟡", "orange"),
    "CONFIRMED": ("🟢", "green"),
    "UNCONFIRMED_ESCALATED": ("🔴", "red"),
    "CANCELLED": ("⚫", "gray"),
    "NO_SHOW": ("🚨", "red"),
    "COMPLETED": ("✅", "green"),
}

status = assignment.confirmation_status
icon, color = STATUS_COLORS.get(status, ("⬜", "gray"))

st.markdown(f"### Current State: {icon} **{status}**")

states = ["PENDING_CONFIRMATION", "CONFIRMED", "UNCONFIRMED_ESCALATED", "CANCELLED", "NO_SHOW", "COMPLETED"]
cols = st.columns(len(states))
for col, s in zip(cols, states):
    ic, cl = STATUS_COLORS.get(s, ("⬜", "gray"))
    if s == status:
        col.markdown(f"<div style='border:2px solid {cl}; border-radius:8px; padding:6px; text-align:center; background-color:{'#f0fff0' if cl=='green' else '#fff0f0' if cl=='red' else '#fffff0'}'>{ic}<br><b>{s.replace('_', ' ')}</b></div>", unsafe_allow_html=True)
    else:
        col.markdown(f"<div style='border:1px solid #ccc; border-radius:8px; padding:6px; text-align:center; color:#aaa'>{ic}<br>{s.replace('_', ' ')}</div>", unsafe_allow_html=True)

st.divider()

# ── Action panels ─────────────────────────────────────────────────────────────
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown("#### Actions")

    if status == "PENDING_CONFIRMATION":
        if assignment.notification_sent_at is None:
            if st.button("📤 Send Confirmation Notification", type="primary", use_container_width=True):
                assignment = send_notification(assignment)
                st.session_state["nurse_assignment"] = assignment
                st.rerun()
        else:
            st.success(f"Notification sent at {assignment.notification_sent_at.strftime('%H:%M:%S UTC')}")
            st.markdown("**Simulate nurse reply:**")
            reply_options = {
                "YES — confirmed": "yes",
                "NO — declining": "no",
                "Ambiguous — I'll probably be there": "I'll probably be there",
                "No reply (simulate T+24h timeout)": "__timeout__",
            }
            choice = st.radio("Nurse response", list(reply_options.keys()))
            if st.button("Submit Reply", type="primary", use_container_width=True):
                val = reply_options[choice]
                if val == "__timeout__":
                    assignment = simulate_no_reply_timeout(assignment)
                else:
                    assignment = process_reply(assignment, val)
                st.session_state["nurse_assignment"] = assignment
                st.rerun()

    elif status == "CONFIRMED":
        st.success("Nurse confirmed. Shift is covered.")
        if st.button("🚨 Simulate No-Show (hospital reports)", use_container_width=True):
            assignment = simulate_no_show(assignment)
            st.session_state["nurse_assignment"] = assignment
            st.rerun()
        if st.button("✅ Mark Shift Completed", use_container_width=True):
            assignment.confirmation_status = "COMPLETED"
            st.session_state["nurse_assignment"] = assignment
            st.rerun()

    elif status == "UNCONFIRMED_ESCALATED":
        st.error(f"**Escalation reason:** {assignment.escalation_reason}")
        st.markdown("**Coordinator action required:**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Manually Confirm", type="primary", use_container_width=True):
                assignment = coordinator_confirm(assignment)
                st.session_state["nurse_assignment"] = assignment
                st.rerun()
        with col2:
            if st.button("❌ Cancel & Re-match", use_container_width=True):
                assignment = coordinator_cancel(assignment)
                st.session_state["nurse_assignment"] = assignment
                st.rerun()

    elif status == "CANCELLED":
        st.warning("Assignment cancelled. Re-match required.")
        if st.button("↩ Return to Agent 2 for re-match"):
            st.session_state.pop("match_proposal", None)
            st.session_state.pop("_last_proposal", None)
            st.session_state.pop("nurse_assignment", None)
            st.switch_page("pages/2_Agent2_Shift_Matching.py")

    elif status == "NO_SHOW":
        st.error("No-show detected. Emergency re-match triggered.")
        st.info("Agent 2 re-triggered with EMERGENCY urgency. Coordinator notified in parallel.")
        if st.button("↩ Return to Agent 2 — Emergency Re-match", type="primary"):
            req.urgency = "EMERGENCY"
            st.session_state["shift_request"] = req
            st.session_state.pop("match_proposal", None)
            st.session_state.pop("_last_proposal", None)
            st.session_state.pop("nurse_assignment", None)
            st.switch_page("pages/2_Agent2_Shift_Matching.py")

    elif status == "COMPLETED":
        st.success("Shift completed successfully. ✓")

with right:
    st.markdown("#### Event Log")
    if assignment.events:
        for event in reversed(assignment.events):
            time_str = event.occurred_at.strftime("%H:%M:%S")
            note_str = f" — {event.notes}" if event.notes else ""
            if event.event_type in ("CONFIRMED", "ASSIGNMENT_CREATED", "NOTIFICATION_SENT"):
                st.success(f"`{time_str}` **{event.event_type}** [{event.actor}]{note_str}")
            elif event.event_type in ("ESCALATED", "NO_SHOW_REPORTED", "CANCELLED"):
                st.error(f"`{time_str}` **{event.event_type}** [{event.actor}]{note_str}")
            else:
                st.info(f"`{time_str}` **{event.event_type}** [{event.actor}]{note_str}")
    else:
        st.caption("No events yet.")
