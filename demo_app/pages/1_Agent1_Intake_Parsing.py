import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from core.intake_parser import parse

st.set_page_config(page_title="Agent 1 — Intake Parsing", page_icon="📧", layout="wide")

SAMPLE_EMAILS = {
    "Easy — well-formed request": (
        "Hi team,\n\n"
        "We need an ICU RN with ACLS and BLS for Thursday June 12th, 7am to 7pm in our cardiac ICU unit. "
        "This is urgent — please confirm ASAP.\n\n"
        "Thanks,\nSt. Mary's Scheduling\nscheduling@stmarys-boston.org"
    ),
    "Medium — abbreviations & relative date": (
        "Need critical care nurse with ACLS tomorrow night 7p-7a, peds unit. "
        "Springfield General. URGENT."
    ),
    "Hard — vague (will escalate)": (
        "We need a nurse ASAP for our ward. Please send someone."
    ),
}

st.title("Agent 1 — Intake Parsing")
st.caption("Transforms free-text hospital emails into structured ShiftRequest records")

left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown("#### Input")
    sample_choice = st.selectbox("Load sample email", list(SAMPLE_EMAILS.keys()))
    raw_text = st.text_area(
        "Hospital email (editable)",
        value=SAMPLE_EMAILS[sample_choice],
        height=220,
    )
    source = st.selectbox("Source channel", ["EMAIL", "PORTAL", "PHONE"])
    parse_clicked = st.button("⚙ Parse Email", type="primary", use_container_width=True)

with right:
    st.markdown("#### Parsed Output")

    if parse_clicked and raw_text.strip():
        req = parse(raw_text, source_channel=source)
        st.session_state["_last_parsed"] = req

    req = st.session_state.get("_last_parsed")

    if req is None:
        st.info("Click **Parse Email** to see results.")
    else:
        # Confidence score
        conf = req.parse_confidence
        color = "green" if conf >= 0.80 else ("orange" if conf >= 0.65 else "red")
        st.markdown(
            f"**Confidence Score:** "
            f"<span style='color:{color}; font-size:1.4rem; font-weight:bold'>{conf:.0%}</span>",
            unsafe_allow_html=True,
        )

        # Status badge
        if req.status == "RELEASED":
            st.success("Status: RELEASED")
        elif req.status == "PENDING_REVIEW":
            st.warning("Status: PENDING_REVIEW — 5-minute coordinator preview")
        else:
            st.error("Status: ESCALATED — coordinator action required")

        st.divider()

        # Extracted fields
        st.markdown("**Extracted Fields**")

        def field_row(label, value, status="OK"):
            icon = "✅" if status == "OK" else ("⚠️" if status == "ASSUMED" else "❌")
            val_str = str(value) if value is not None else "—"
            return f"| {icon} | **{label}** | {val_str} | {status} |"

        rows = [
            "| | Field | Value | Status |",
            "|---|---|---|---|",
            field_row("Hospital", req.hospital_name or "Unknown",
                      "OK" if req.hospital_id else "MISSING"),
            field_row("Shift Date", req.shift_date,
                      "OK" if req.shift_date else "MISSING"),
            field_row("Start Time", req.shift_start_time,
                      "OK" if req.shift_start_time else "MISSING"),
            field_row("End Time", req.shift_end_time,
                      "OK" if req.shift_end_time else "MISSING"),
            field_row("Overnight", req.overnight, "OK"),
            field_row("Urgency", req.urgency, "OK"),
            field_row("Specialty", req.specialty or "—",
                      "OK" if req.specialty else "MISSING"),
            field_row("Unit", req.unit or "—", "OK"),
        ]
        st.markdown("\n".join(rows))

        # Credentials
        st.markdown("**Credentials**")
        if req.required_credentials:
            st.success(f"✅ Confirmed: {', '.join(req.required_credentials)}")
        if req.assumed_credentials:
            st.warning(f"⚠️ Assumed (verify): {', '.join(req.assumed_credentials)}")
        if req.unresolved_credentials:
            st.error(f"❌ Unresolved: {', '.join(req.unresolved_credentials)}")
        if not req.required_credentials and not req.assumed_credentials:
            st.error("❌ No credentials extracted")

        # Escalation codes
        if req.escalation_codes:
            st.divider()
            st.markdown("**Escalation Codes**")
            for code in req.escalation_codes:
                st.error(f"🚨 {code}")

        st.divider()

        # Release / override section
        if req.status == "ESCALATED":
            st.markdown("**Coordinator Override**")
            st.caption("Escalated records require coordinator review before release.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Override & Release to Agent 2", use_container_width=True):
                    req.status = "RELEASED"
                    st.session_state["shift_request"] = req
                    st.session_state["_last_parsed"] = req
                    st.success("Released. Navigate to Agent 2.")
            with col2:
                if st.button("🔄 Re-parse", use_container_width=True):
                    st.session_state.pop("_last_parsed", None)
                    st.rerun()
        else:
            if st.button("→ Release to Agent 2", type="primary", use_container_width=True):
                req.status = "RELEASED"
                st.session_state["shift_request"] = req
                st.session_state["_last_parsed"] = req
                st.success("ShiftRequest saved. Go to **Agent 2 — Shift Matching**.")
                st.switch_page("pages/2_Agent2_Shift_Matching.py")
