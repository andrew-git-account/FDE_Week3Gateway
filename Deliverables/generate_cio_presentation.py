from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

W, H = A4

# Colors
DARK_BLUE = colors.HexColor("#1B2A4A")
MID_BLUE  = colors.HexColor("#2E5D9E")
ACCENT    = colors.HexColor("#E8501A")
LIGHT_BG  = colors.HexColor("#F4F7FB")
GRAY      = colors.HexColor("#6B7280")
WHITE     = colors.white

def build_styles():
    return {
        "slide_num": ParagraphStyle("slide_num", fontSize=9, textColor=GRAY, alignment=TA_LEFT),
        "title":     ParagraphStyle("title",     fontSize=26, textColor=WHITE,    leading=32, alignment=TA_LEFT, fontName="Helvetica-Bold"),
        "subtitle":  ParagraphStyle("subtitle",  fontSize=13, textColor=WHITE,    leading=18, alignment=TA_LEFT),
        "h2":        ParagraphStyle("h2",         fontSize=18, textColor=DARK_BLUE, leading=24, fontName="Helvetica-Bold"),
        "body":      ParagraphStyle("body",       fontSize=11, textColor=DARK_BLUE, leading=17, spaceAfter=4),
        "bullet":    ParagraphStyle("bullet",     fontSize=11, textColor=DARK_BLUE, leading=17, spaceAfter=6, leftIndent=16, bulletIndent=0),
        "subbullet": ParagraphStyle("subbullet",  fontSize=10, textColor=GRAY,      leading=15, spaceAfter=4, leftIndent=32, bulletIndent=0),
        "callout":   ParagraphStyle("callout",    fontSize=12, textColor=DARK_BLUE, leading=18, fontName="Helvetica-Bold", borderPad=8),
        "footer":    ParagraphStyle("footer",     fontSize=8,  textColor=GRAY, alignment=TA_CENTER),
        "feedback_q": ParagraphStyle("feedback_q", fontSize=11, textColor=DARK_BLUE, leading=16, fontName="Helvetica-Bold", spaceAfter=2, leftIndent=16),
        "feedback_a": ParagraphStyle("feedback_a", fontSize=10, textColor=GRAY,      leading=15, spaceAfter=10, leftIndent=32),
    }

S = build_styles()

def b(text): return f"<b>{text}</b>"
def accent(text): return f'<font color="#E8501A"><b>{text}</b></font>'
def green(text): return f'<font color="#1a7a3c"><b>{text}</b></font>'

slides = [
    # ── SLIDE 1 ──────────────────────────────────────────────────────────────
    {
        "slide_num": "01 / 06",
        "header_title": "The Constraint",
        "header_sub": "Why the current way of working cannot reach the board's target",
        "content": [
            (S["h2"], "MedFlex today vs. what the board requires"),
            (S["body"], ""),
            (S["bullet"], f"• Now: {b('$14M revenue')}, {b('8 coordinators')}, 4.2 hours average time to fill a shift"),
            (S["bullet"], f"• Board target: {b('$200M in 24 months')} — about 14 times more business"),
            (S["bullet"], f"• At today's productivity: {b('112 coordinators would be needed')} to handle that volume manually"),
            (S["body"], ""),
            (S["callout"], f"The problem is not effort — {accent('it is how the work is structured')}."),
            (S["body"], ""),
            (S["body"], "To reach the board's target, coordinators must stop doing every match themselves "
                        "and start supervising agents that handle standard cases automatically. "
                        "This is a design problem, not a staffing problem."),
        ],
    },
    # ── SLIDE 2 ──────────────────────────────────────────────────────────────
    {
        "slide_num": "02 / 06",
        "header_title": "What Is Breaking Today",
        "header_sub": "Three problems that get worse as volume grows",
        "content": [
            (S["h2"], "Process problems — not coordinator mistakes"),
            (S["body"], ""),
            (S["bullet"], f"• {b('Too slow')} — Hospitals send requests to several agencies at the same time. "
                          "At 4.2 hours to respond, MedFlex loses contracts before a proposal is even sent."),
            (S["bullet"], f"• {b('Hard ceiling on capacity')} — 8 coordinators doing 120 decisions per day is the maximum. "
                          "When more requests come in, a queue builds up. The queue makes the delay worse."),
            (S["bullet"], f"• {b('Knowledge locked in people')} — Senior coordinators know which nurse fits which hospital. "
                          "This knowledge is not written down. New people take longer and get inconsistent results. "
                          "When someone leaves, the knowledge is gone."),
            (S["body"], ""),
            (S["h2"], "Problems found during discovery"),
            (S["body"], ""),
            (S["bullet"], f"• {b('Manual email parsing')} — Every hospital email is read and interpreted by hand before matching starts. "
                          "This is a hidden delay step."),
            (S["bullet"], f"• {b('12% no-show rate')} — Nurses receive an SMS and silence is treated as acceptance. "
                          "MedFlex finds out about a no-show when the hospital calls."),
            (S["bullet"], f"• {b('Double-booking risk')} — The same nurse can be offered to two hospitals at once. "
                          "There is no automatic way to resolve conflicts when this happens at scale."),
        ],
    },
    # ── SLIDE 3 ──────────────────────────────────────────────────────────────
    {
        "slide_num": "03 / 06",
        "header_title": "The Solution",
        "header_sub": "Three agents — existing hospital and nurse channels stay the same",
        "content": [
            (S["h2"], "Agent relay: read → match → confirm"),
            (S["body"], ""),
            (S["bullet"], f"• {b('Agent 1 — Reader')}"),
            (S["subbullet"], "Converts unstructured hospital emails into structured shift records. "
                             "Coordinator gets a 5-minute preview before the record moves forward — "
                             "catches any misreads before they affect matching."),
            (S["bullet"], f"• {b('Agent 2 — Matchmaker')}"),
            (S["subbullet"], "Scores each candidate on credentials, availability, distance, and hospital history. "
                             "High-confidence matches (above 85%) are sent to the hospital automatically. "
                             "Mid-confidence matches are sent with a 90-minute coordinator recall window. "
                             "Low-confidence cases go to the coordinator with a ranked list of options."),
            (S["bullet"], f"• {b('Agent 3 — Follow-up')}"),
            (S["subbullet"], "Asks the nurse to confirm explicitly after the hospital accepts. "
                             "Escalates if there is no reply. Starts an emergency re-match if a no-show is reported."),
            (S["body"], ""),
            (S["callout"], f"Coordinator role: {accent('managing exceptions')}, not doing routine matching."),
            (S["body"], ""),
            (S["bullet"], f"• {b('What stays the same:')} ServiceNow queue, hospital email and portal channels, nurse SMS and email"),
        ],
    },
    # ── SLIDE 4 ──────────────────────────────────────────────────────────────
    {
        "slide_num": "04 / 06",
        "header_title": "How Risk Is Managed",
        "header_sub": "Trust is built step by step — not by switching everything at once",
        "content": [
            (S["h2"], "Four safeguards in the design"),
            (S["body"], ""),
            (S["bullet"], f"• {b('Step-by-step rollout')} — Phase 1 covers only the highest-confidence 50% of daily volume. "
                          "Coordinators review all other cases. Full automation is earned through results, not assumed."),
            (S["bullet"], f"• {b('90-minute coordinator recall window')} — Every mid-confidence proposal can be cancelled "
                          "within 90 minutes. If the coordinator does not review it in time, the team lead is notified. "
                          "A proposal is never automatically approved without a human seeing it."),
            (S["bullet"], f"• {b('Nurse reservation')} — When a nurse is proposed to a hospital, a 15-minute soft lock "
                          "prevents the same nurse from being offered to another hospital at the same time. "
                          "This eliminates double-booking."),
            (S["bullet"], f"• {b('30-day calibration check')} — Full automation of high-confidence cases is not permanent "
                          "until 30 days of monitoring confirms the error rate stays below 3%."),
            (S["body"], ""),
            (S["h2"], "Why this is different from the two earlier AI projects"),
            (S["body"], ""),
            (S["bullet"], "• Earlier chatbot: tried to change how hospitals send requests. This project keeps their process the same."),
            (S["bullet"], "• Earlier recommendation engine: coordinators did not trust it. This project starts with "
                          "high-confidence cases only and keeps coordinators in control for all borderline decisions."),
        ],
    },
    # ── SLIDE 5 (NEW) ─────────────────────────────────────────────────────────
    {
        "slide_num": "05 / 06",
        "header_title": "CEO Feedback — Three Questions Answered",
        "header_sub": "Changes made to the plan after review with Marcus Reyes",
        "content": [
            (S["h2"], "Marcus raised three concerns. All three have been addressed."),
            (S["body"], ""),
            (S["feedback_q"], f"Q1: The board update is in 6 weeks, not 8. What gets cut?"),
            (S["feedback_a"], f"{green('Done.')} Phase 1 now delivers the matching agent running on real volume by week 6. "
                              "The coordinator dashboard UI is moved to weeks 7–8. "
                              "The agent functionality is unchanged — only the review interface is delayed. "
                              "Coordinators work from email and SMS alerts during weeks 1–6."),
            (S["feedback_q"], f"Q2: The 30-day mismatch rate is too slow. I need a signal I can see in week 2."),
            (S["feedback_a"], f"{green('Done.')} Two leading signals are now tracked every week from week 2: "
                              "(1) hospital acceptance rate per confidence band — a drop shows the agent is drifting before any mismatch is reported; "
                              "(2) coordinator flag rate per week — a rise shows the agent and coordinator judgment are moving apart. "
                              "The 30-day gate remains but is no longer the only signal."),
            (S["feedback_q"], f"Q3: Coordinators check the queue every 1–2 hours during busy periods. "
                              "What happens to a proposal when the 30-minute window expires unreviewed?"),
            (S["feedback_a"], f"{green('Done.')} The recall window has been extended to 90 minutes — long enough to cover one full batch-check cycle. "
                              "If the window expires without the coordinator opening the proposal, "
                              "it escalates to the team lead. It is never automatically approved without a human review."),
        ],
    },
    # ── SLIDE 6 (was 5) ───────────────────────────────────────────────────────
    {
        "slide_num": "06 / 06",
        "header_title": "The Ask",
        "header_sub": "Phase 1 approval to prove the ROI signal",
        "content": [
            (S["h2"], "Phase 1 — 6 weeks, measurable result"),
            (S["body"], ""),
            (S["bullet"], f"• {b('What is built:')} Intake parsing agent + matching agent for high and mid-confidence cases"),
            (S["bullet"], f"• {b('What is deferred:')} Coordinator dashboard UI (weeks 7–8); Agent 3 confirmation loop (Phase 2)"),
            (S["bullet"], f"• {b('Target:')} 50% of daily proposals handled automatically; fill time under 1 hour"),
            (S["bullet"], f"• {b('Board demo:')} Matching agent live on real volume at week 6"),
            (S["bullet"], f"• {b('Success signal:')} Weekly acceptance rate trend + coordinator flag rate from week 2; "
                          "mismatch rate tracked separately from hospital preference rejection"),
            (S["body"], ""),
            (S["h2"], "What is needed from IT"),
            (S["body"], ""),
            (S["bullet"], "• ServiceNow API access — read queue, write structured shift record back"),
            (S["bullet"], "• Read access to nurse database — credentials, availability, history"),
            (S["bullet"], "• Confirmation on how current the availability data is — assumed under 24-hour delay"),
            (S["bullet"], "• SMS and email gateway setup for nurse confirmation notifications"),
            (S["body"], ""),
            (S["callout"], f"Decision needed: {accent('approve Phase 1 build')} to prove ROI before Phase 2 investment."),
            (S["body"], ""),
            (S["body"], "Phase 2 (weeks 9–16) and Phase 3 (weeks 17–24) are scoped and ready — "
                        "pending Phase 1 results."),
        ],
    },
]


def draw_header_bg(canvas, doc, title, subtitle):
    canvas.saveState()
    # Dark blue header band
    canvas.setFillColor(DARK_BLUE)
    canvas.rect(0, H - 5.2*cm, W, 5.2*cm, fill=1, stroke=0)
    # Accent bar
    canvas.setFillColor(ACCENT)
    canvas.rect(0, H - 5.2*cm, 0.4*cm, 5.2*cm, fill=1, stroke=0)
    # Title
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 24)
    canvas.drawString(1.2*cm, H - 2.6*cm, title)
    # Subtitle
    canvas.setFont("Helvetica", 12)
    canvas.setFillColor(colors.HexColor("#A8BFDF"))
    canvas.drawString(1.2*cm, H - 3.5*cm, subtitle)
    # Footer line
    canvas.setStrokeColor(colors.HexColor("#DDE3ED"))
    canvas.setLineWidth(0.5)
    canvas.line(1*cm, 1.4*cm, W - 1*cm, 1.4*cm)
    # Footer text
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRAY)
    canvas.drawString(1*cm, 0.9*cm, "MedFlex Healthcare Staffing — AI-Native Shift Matching")
    canvas.drawRightString(W - 1*cm, 0.9*cm, "CONFIDENTIAL")
    canvas.restoreState()


def make_slide_page(slide_data):
    title    = slide_data["header_title"]
    subtitle = slide_data["header_sub"]
    num      = slide_data["slide_num"]

    def on_page(canvas, doc):
        draw_header_bg(canvas, doc, title, subtitle)
        # Slide number top-right
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.HexColor("#A8BFDF"))
        canvas.drawRightString(W - 1.2*cm, H - 1.1*cm, num)
        canvas.restoreState()

    elements = [Spacer(1, 5.6*cm)]  # push below header band
    for style, text in slide_data["content"]:
        elements.append(Paragraph(text, style))
    elements.append(PageBreak())
    return elements, on_page


def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=1.2*cm,
        rightMargin=1.2*cm,
        topMargin=0.5*cm,
        bottomMargin=2*cm,
    )

    all_elements = []
    page_callbacks = []

    for slide in slides:
        elems, cb = make_slide_page(slide)
        all_elements.extend(elems)
        page_callbacks.append(cb)

    slide_index = [0]

    def on_page_dispatch(canvas, doc):
        idx = slide_index[0]
        if idx < len(page_callbacks):
            page_callbacks[idx](canvas, doc)
        slide_index[0] += 1

    doc.build(all_elements, onFirstPage=on_page_dispatch, onLaterPages=on_page_dispatch)
    print(f"PDF written to: {output_path}")


if __name__ == "__main__":
    build_pdf(r"C:\Users\Andrzej_Bihun\Projects\FDE_Week3Gateway\Deliverables\MedFlex-CIO-Presentation-v2.pdf")
