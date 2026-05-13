import streamlit as st

st.set_page_config(page_title="MedFlex Agent Demo", page_icon="🏥", layout="wide")

st.title("MedFlex — AI-Native Shift Matching Demo")
st.caption("Agentic solution demo | FDE Week 3 | Andrzej Bihun")

st.markdown("""
This demo shows three agents operating as a connected relay to match nurses to hospital shifts.
Each agent hands its output to the next. No external systems — all data is stubbed.
""")

st.divider()

# Flow diagram
col1, col2, col3, col4, col5 = st.columns([2, 0.4, 2, 0.4, 2])

with col1:
    st.markdown("### 1 — Intake Parsing")
    st.markdown("""
    **Input:** Free-text hospital email
    **Output:** Structured ShiftRequest
    **Key:** Confidence scoring + 5-min coordinator preview
    """)

with col2:
    st.markdown("<div style='text-align:center; font-size:2rem; padding-top:3rem'>→</div>", unsafe_allow_html=True)

with col3:
    st.markdown("### 2 — Shift Matching")
    st.markdown("""
    **Input:** ShiftRequest
    **Output:** MatchProposal with routing decision
    **Key:** Hard filter → soft scoring → AUTO/ASYNC/HUMAN
    """)

with col4:
    st.markdown("<div style='text-align:center; font-size:2rem; padding-top:3rem'>→</div>", unsafe_allow_html=True)

with col5:
    st.markdown("### 3 — Confirmation")
    st.markdown("""
    **Input:** Accepted MatchProposal
    **Output:** Confirmed assignment or escalation
    **Key:** Explicit confirmation loop + no-show prevention
    """)

st.divider()

# Session state status
st.markdown("### Current flow status")

col_a, col_b, col_c = st.columns(3)

with col_a:
    if "shift_request" in st.session_state and st.session_state.shift_request:
        req = st.session_state.shift_request
        st.success(f"✓ ShiftRequest ready  \n`{req.id}` | Confidence: {req.parse_confidence:.0%}")
    else:
        st.info("⬜ No ShiftRequest yet — start with Agent 1")

with col_b:
    if "match_proposal" in st.session_state and st.session_state.match_proposal:
        prop = st.session_state.match_proposal
        st.success(f"✓ MatchProposal ready  \n`{prop.id}` | {prop.routing} | {prop.status}")
    else:
        st.info("⬜ No MatchProposal yet — complete Agent 2")

with col_c:
    if "nurse_assignment" in st.session_state and st.session_state.nurse_assignment:
        asgn = st.session_state.nurse_assignment
        st.success(f"✓ Assignment `{asgn.id}`  \nStatus: {asgn.confirmation_status}")
    else:
        st.info("⬜ No assignment yet — complete Agent 3")

st.divider()

st.markdown("### Demo scenarios")
st.markdown("""
| Scenario | Email to use | Expected outcome |
|----------|-------------|-----------------|
| Happy path | Easy email | AUTO_SUBMIT → nurse confirms YES |
| Async review | Medium email | ASYNC_REVIEW → coordinator recall window |
| Escalation | Hard email | ESCALATED in Agent 1 — coordinator override required |
| Ambiguous reply | Easy email → match | Nurse replies "I'll probably be there" → escalated |
| No-show | Easy email → match → confirm | Simulate no-show → emergency re-match |
""")

if st.button("Start with Agent 1 →", type="primary"):
    st.switch_page("pages/1_Agent1_Intake_Parsing.py")
