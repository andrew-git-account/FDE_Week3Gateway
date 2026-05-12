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
    }

S = build_styles()

def b(text): return f"<b>{text}</b>"
def accent(text): return f'<font color="#E8501A"><b>{text}</b></font>'

slides = [
    # ── SLIDE 1 ──────────────────────────────────────────────────────────────
    {
        "slide_num": "01 / 05",
        "header_title": "The Constraint",
        "header_sub": "Why the current model can't reach the board's target",
        "content": [
            (S["h2"], "MedFlex today vs. what the board requires"),
            (S["body"], ""),
            (S["bullet"], f"• Current: {b('$14M revenue')}, {b('8 coordinators')}, 4.2h average fill time"),
            (S["bullet"], f"• Board target: {b('$200M in 24 months')} — roughly 14× growth"),
            (S["bullet"], f"• At current productivity: {b('112 coordinators needed')} to match that volume manually"),
            (S["body"], ""),
            (S["callout"], f"The bottleneck isn't effort — {accent('it\'s architecture')}."),
            (S["body"], ""),
            (S["body"], "Reaching the board target requires the coordinator role to shift "
                        "from doing every match to supervising agents that handle standard cases autonomously. "
                        "That is an infrastructure problem, not a hiring problem."),
        ],
    },
    # ── SLIDE 2 ──────────────────────────────────────────────────────────────
    {
        "slide_num": "02 / 05",
        "header_title": "What's Breaking Today",
        "header_sub": "Three operational failures that compound as volume grows",
        "content": [
            (S["h2"], "Process design gaps — not coordinator mistakes"),
            (S["body"], ""),
            (S["bullet"], f"• {b('Speed loss')} — Hospitals submit to multiple agencies simultaneously. At 4.2h fill time, "
                          "MedFlex loses contracts before a proposal is even sent."),
            (S["bullet"], f"• {b('Throughput ceiling')} — 8 coordinators × 120 decisions/day is a hard cap. "
                          "Demand spikes create queues; queues create more delay; delay compounds competitive loss."),
            (S["bullet"], f"• {b('Tribal knowledge lock')} — Senior coordinators carry undocumented matching logic. "
                          "New hires take longer and produce inconsistent results. When people leave, the knowledge leaves."),
            (S["body"], ""),
            (S["h2"], "Hidden problems surfaced in discovery"),
            (S["body"], ""),
            (S["bullet"], f"• {b('Free-text intake')} — Every hospital email is manually parsed before matching begins. Hidden latency step."),
            (S["bullet"], f"• {b('12% no-show rate')} — Nurses are notified by SMS; silence is treated as acceptance. "
                          "MedFlex finds out at shift time."),
            (S["bullet"], f"• {b('Double-booking risk')} — Same nurse submitted to multiple hospitals simultaneously. "
                          "No automated conflict resolution at scale."),
        ],
    },
    # ── SLIDE 3 ──────────────────────────────────────────────────────────────
    {
        "slide_num": "03 / 05",
        "header_title": "The Solution",
        "header_sub": "Three agents, existing systems unchanged",
        "content": [
            (S["h2"], "Agent relay: intake → matching → confirmation"),
            (S["body"], ""),
            (S["bullet"], f"• {b('Agent 1 — Reader')}"),
            (S["subbullet"], "Converts unstructured hospital emails into structured shift records. "
                             "5-minute coordinator preview before proceeding — catches silent misreads before they cascade."),
            (S["bullet"], f"• {b('Agent 2 — Matchmaker')}"),
            (S["subbullet"], "Scores each candidate against credentials, availability, proximity, and hospital history. "
                             "High-confidence (>85%) proposals go automatically. Mid-confidence proposals go with a 30-minute coordinator recall window. "
                             "Low-confidence cases are escalated to a human with ranked options."),
            (S["bullet"], f"• {b('Agent 3 — Follow-up')}"),
            (S["subbullet"], "Requests explicit nurse confirmation after hospital accepts. "
                             "Escalates silence before shift day. Triggers emergency re-match if no-show detected."),
            (S["body"], ""),
            (S["callout"], f"Coordinator role: {accent('exception management')}, not routine matching."),
            (S["body"], ""),
            (S["bullet"], f"• {b('What stays the same:')} ServiceNow queue, hospital email/portal/phone channels, nurse SMS/email comms"),
        ],
    },
    # ── SLIDE 4 ──────────────────────────────────────────────────────────────
    {
        "slide_num": "04 / 05",
        "header_title": "How Risk Is Managed",
        "header_sub": "Incremental trust-building, not a big-bang cutover",
        "content": [
            (S["h2"], "Four safeguards built into the design"),
            (S["body"], ""),
            (S["bullet"], f"• {b('Phased rollout')} — Phase 1 handles only the highest-confidence 50% of daily volume. "
                          "Coordinators review everything else. Full autonomy is earned, not assumed."),
            (S["bullet"], f"• {b('Coordinator recall window')} — Every mid-confidence automated proposal can be pulled back "
                          "within 30 minutes. Oversight without blocking speed."),
            (S["bullet"], f"• {b('Nurse reservation protocol')} — When a nurse is proposed to a hospital, a 15-minute soft lock "
                          "prevents the same nurse being offered elsewhere simultaneously. Eliminates double-booking at scale."),
            (S["bullet"], f"• {b('30-day calibration gate')} — Full automation of high-confidence cases is not activated until "
                          "30 days of shadow review confirms the mismatch rate stays below 3%."),
            (S["body"], ""),
            (S["h2"], "Why this is different from the two prior AI projects"),
            (S["body"], ""),
            (S["bullet"], "• Previous chatbot: tried to change how hospitals submit requests. This engagement keeps hospital channels unchanged."),
            (S["bullet"], "• Previous recommendation engine: coordinators didn't trust it. This engagement starts with high-confidence automation only, "
                          "keeping coordinators visible and in control for all borderline cases."),
        ],
    },
    # ── SLIDE 5 ──────────────────────────────────────────────────────────────
    {
        "slide_num": "05 / 05",
        "header_title": "The Ask",
        "header_sub": "Phase 1 approval to establish the ROI signal",
        "content": [
            (S["h2"], "Phase 1 — 8 weeks, measurable outcome"),
            (S["body"], ""),
            (S["bullet"], f"• {b('Scope:')} Intake parsing agent + high-confidence matching agent + coordinator dashboard"),
            (S["bullet"], f"• {b('Target:')} 50% of daily proposals handled autonomously; fill time under 1 hour"),
            (S["bullet"], f"• {b('Success signal:')} Coordinator time freed × cost savings; mismatch rate tracked separately "
                          "from hospital preference rejection"),
            (S["body"], ""),
            (S["h2"], "What's needed from IT"),
            (S["body"], ""),
            (S["bullet"], "• ServiceNow API access (read queue, write structured ShiftRequest back)"),
            (S["bullet"], "• Read access to nurse database (credentials, availability, history)"),
            (S["bullet"], "• Confirmation on availability data freshness — current assumption: <24h lag"),
            (S["bullet"], "• SMS/email gateway configuration for nurse confirmation notifications"),
            (S["body"], ""),
            (S["callout"], f"Decision needed: {accent('approve Phase 1 build')} to prove ROI before Phase 2 investment."),
            (S["body"], ""),
            (S["body"], f"Phase 2 (weeks 9-16) and Phase 3 (weeks 17-24) are scoped and ready — "
                        f"but contingent on Phase 1 results."),
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

    # reportlab doesn't support per-page callbacks in SimpleDocTemplate directly,
    # so we use a custom onPage dispatcher
    slide_index = [0]

    def on_page_dispatch(canvas, doc):
        idx = slide_index[0]
        if idx < len(page_callbacks):
            page_callbacks[idx](canvas, doc)
        slide_index[0] += 1

    doc.build(all_elements, onFirstPage=on_page_dispatch, onLaterPages=on_page_dispatch)
    print(f"PDF written to: {output_path}")


if __name__ == "__main__":
    build_pdf(r"C:\Users\Andrzej_Bihun\Projects\FDE_Week3Gateway\Deliverables\MedFlex-CIO-Presentation.pdf")
