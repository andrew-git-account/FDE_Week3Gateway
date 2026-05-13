import re
import uuid
from datetime import date, time, datetime, timedelta
from typing import Optional

from dateutil import parser as dateutil_parser
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU

from core.models import ShiftRequest
from stubs.hospital_registry import lookup_by_domain, lookup_by_name

# ── Credential taxonomy ───────────────────────────────────────────────────────

CREDENTIAL_TAXONOMY = [
    "RN", "LPN", "CNA", "NP", "PA", "MD",
    "ACLS", "BLS", "PALS", "NRP", "TNCC", "CCRN", "CEN", "PCCN",
    "ICU", "PICU", "NICU", "ER", "OR", "PACU", "MedSurg", "Telemetry",
    "Psych", "Oncology", "Pediatrics",
]

SPECIALTY_TAXONOMY = ["ICU", "PICU", "NICU", "ER", "OR", "PACU", "MedSurg",
                      "Telemetry", "Psych", "Oncology", "Pediatrics"]

ABBREVIATION_MAP = {
    "critical care": ["RN", "ICU", "ACLS"],
    "labor and delivery": ["RN", "L&D"],
    "l&d": ["RN", "L&D"],
    "neonatal": ["RN", "NICU"],
    "neo ": ["RN", "NICU"],
    "peds": ["Pediatrics"],
    "tele": ["Telemetry"],
    "advanced cardiac life support": ["ACLS"],
    "basic life support": ["BLS"],
    "emergency room": ["ER"],
    "operating room": ["OR"],
    "med surg": ["MedSurg"],
    "med/surg": ["MedSurg"],
    "intensive care": ["ICU"],
    "cardiac icu": ["ICU", "ACLS"],
    "cardiac care": ["ICU", "ACLS"],
    "pediatric icu": ["PICU"],
}

URGENCY_KEYWORDS = {
    "EMERGENCY": ["emergency", "stat", "immediately", "right now"],
    "URGENT": ["urgent", "asap", "as soon as possible", "rush"],
}

# ── Date/time patterns ────────────────────────────────────────────────────────

MONTH_NAMES = (
    r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|"
    r"jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
)
DATE_PATTERN = re.compile(
    rf"({MONTH_NAMES}\s+\d{{1,2}}(?:st|nd|rd|th)?(?:\s*,?\s*\d{{4}})?)|"
    r"(\d{1,2}/\d{1,2}(?:/\d{2,4})?)",
    re.IGNORECASE,
)
RELATIVE_DATE_MAP = {
    "today": 0, "tonight": 0,
    "tomorrow": 1, "tomorrow night": 1,
    "day after tomorrow": 2,
}
WEEKDAY_MAP = {
    "monday": MO(1), "tuesday": TU(1), "wednesday": WE(1),
    "thursday": TH(1), "friday": FR(1), "saturday": SA(1), "sunday": SU(1),
}

TIME_PATTERN = re.compile(
    r"(\d{1,2}):?(\d{2})?\s*(am|pm|a\.m\.|p\.m\.)|(\d{1,2})(am|pm|a\.m\.|p\.m\.)|(\d{2}):(\d{2})",
    re.IGNORECASE,
)
TIME_RANGE_PATTERN = re.compile(
    r"(\d{1,2}(?::\d{2})?\s*(?:am|pm|a\.m\.|p\.m\.|a|p))\s*[-–to]+\s*(\d{1,2}(?::\d{2})?\s*(?:am|pm|a\.m\.|p\.m\.|a|p))",
    re.IGNORECASE,
)


def _parse_time_str(s: str) -> Optional[time]:
    s = s.strip().lower().replace("a.m.", "am").replace("p.m.", "pm")
    try:
        dt = dateutil_parser.parse(s)
        return dt.time()
    except Exception:
        return None


def _extract_date(text: str) -> tuple:
    """Return (shift_date, confidence_contribution, notes)."""
    text_lower = text.lower()

    # Relative dates
    for phrase, delta in RELATIVE_DATE_MAP.items():
        if phrase in text_lower:
            d = date.today() + timedelta(days=delta)
            return d, 0.25, []

    # "next <weekday>" or just "<weekday>"
    for weekday, relval in WEEKDAY_MAP.items():
        if f"next {weekday}" in text_lower or weekday in text_lower:
            try:
                d = (datetime.now() + relativedelta(weekday=relval)).date()
                if d == date.today():
                    d = (datetime.now() + relativedelta(weeks=1, weekday=relval)).date()
                return d, 0.25, []
            except Exception:
                pass

    # Absolute date patterns
    match = DATE_PATTERN.search(text)
    if match:
        raw = match.group(0)
        try:
            d = dateutil_parser.parse(raw, default=datetime(date.today().year, 1, 1)).date()
            if d < date.today():
                d = d.replace(year=d.year + 1)
            return d, 0.25, []
        except Exception:
            pass

    return None, 0.0, ["shift_date could not be extracted"]


def _extract_times(text: str) -> tuple:
    """Return (start_time, end_time, overnight, confidence, notes)."""
    match = TIME_RANGE_PATTERN.search(text)
    if match:
        start = _parse_time_str(match.group(1))
        end = _parse_time_str(match.group(2))
        if start and end:
            overnight = end < start
            return start, end, overnight, 0.25, []

    # Fallback: find individual times
    times = []
    for m in TIME_PATTERN.finditer(text):
        t = _parse_time_str(m.group(0))
        if t and t not in times:
            times.append(t)
    if len(times) >= 2:
        overnight = times[1] < times[0]
        return times[0], times[1], overnight, 0.25, []
    return None, None, False, 0.0, ["shift times could not be extracted"]


def _extract_credentials(text: str) -> tuple:
    """Return (confirmed, assumed, unresolved, confidence, notes)."""
    text_lower = text.lower()
    confirmed = []
    assumed = []
    unresolved = []
    notes = []

    # Abbreviation expansions first (order matters — longer phrases first)
    for phrase, creds in sorted(ABBREVIATION_MAP.items(), key=lambda x: -len(x[0])):
        if phrase in text_lower:
            for c in creds:
                if c not in assumed and c not in confirmed:
                    assumed.append(c)
            notes.append(f"'{phrase}' → {creds} (assumed)")

    # Direct taxonomy matches
    for cred in CREDENTIAL_TAXONOMY:
        pattern = re.compile(rf"\b{re.escape(cred)}\b", re.IGNORECASE)
        if pattern.search(text):
            if cred not in confirmed and cred not in assumed:
                confirmed.append(cred)
            elif cred in assumed:
                # Explicitly mentioned — promote to confirmed
                assumed.remove(cred)
                confirmed.append(cred)

    # Look for unknown ALL-CAPS tokens that might be credentials
    _stopwords = {"ASAP", "AM", "PM", "RE", "CC", "FW", "FYI", "NOTE", "ATTN",
                  "ETA", "NEED", "UNIT", "WARD", "URGENT", "STAT", "PLEASE", "THANKS"}
    unknown = re.findall(r"\b([A-Z]{2,6})\b", text)
    for token in unknown:
        if token not in confirmed and token not in assumed and token not in CREDENTIAL_TAXONOMY and token not in _stopwords:
            unresolved.append(token)

    if not confirmed and not assumed:
        confidence = 0.0
        notes.append("no credentials found")
    elif unresolved:
        confidence = max(0.0, 0.25 - len(unresolved) * 0.10)
    elif assumed and not confirmed:
        confidence = 0.15
    else:
        confidence = 0.25 - len(assumed) * 0.05

    return confirmed, assumed, unresolved, max(0.0, confidence), notes


def _extract_specialty(text: str, confirmed: list, assumed: list) -> tuple:
    """Return (specialty, confidence)."""
    for spec in SPECIALTY_TAXONOMY:
        if re.search(rf"\b{re.escape(spec)}\b", text, re.IGNORECASE):
            return spec, 0.25
    # Infer from credentials
    all_creds = confirmed + assumed
    if "ICU" in all_creds:
        return "ICU", 0.15
    if "PICU" in all_creds:
        return "PICU", 0.15
    if "NICU" in all_creds:
        return "NICU", 0.15
    if "ER" in all_creds:
        return "ER", 0.15
    return None, 0.10


def _extract_unit(text: str) -> Optional[str]:
    match = re.search(r"\b(unit|ward|floor|department|dept)\b[:\s]+([A-Za-z0-9 \-]+)", text, re.IGNORECASE)
    if match:
        return match.group(2).strip()
    # "cardiac ICU unit" pattern
    match2 = re.search(r"(cardiac(?: icu)?|peds(?: icu)?|trauma|surgical|telemetry)[^\n,\.]{0,20}unit", text, re.IGNORECASE)
    if match2:
        return match2.group(0).strip()
    return None


def _extract_urgency(text: str, shift_date: Optional[date]) -> str:
    text_lower = text.lower()
    for level in ["EMERGENCY", "URGENT"]:
        for kw in URGENCY_KEYWORDS[level]:
            if kw in text_lower:
                return level
    if shift_date:
        delta = (shift_date - date.today()).days
        if delta == 0:
            return "EMERGENCY"
        if delta <= 1:
            return "URGENT"
    return "STANDARD"


def _extract_hospital(text: str) -> tuple:
    """Return (hospital_id, hospital_name, confidence, notes)."""
    hid, hname = lookup_by_domain(text)
    if hid:
        return hid, hname, 0.25, []
    hid, hname = lookup_by_name(text)
    if hid:
        return hid, hname, 0.20, ["hospital identified by name match (no domain)"]
    return None, None, 0.0, ["hospital could not be identified"]


def _build_escalation_codes(
    shift_date, start_time, hospital_id, confirmed, assumed, unresolved, confidence
) -> list:
    codes = []
    if shift_date is None:
        codes.append("MISSING_DATE")
    elif shift_date < date.today():
        codes.append("PAST_DATE")
    if start_time is None:
        codes.append("MISSING_TIME")
    if hospital_id is None:
        codes.append("HOSPITAL_AMBIGUOUS")
    if not confirmed and not assumed:
        codes.append("MISSING_CREDENTIALS")
    for u in unresolved:
        codes.append(f"UNRESOLVED_CREDENTIAL:{u}")
    if confidence < 0.80 and not codes:
        codes.append("LOW_CONFIDENCE")
    return codes


# ── Public API ────────────────────────────────────────────────────────────────

def parse(raw_text: str, source_channel: str = "EMAIL") -> ShiftRequest:
    now = datetime.utcnow()

    shift_date, date_conf, date_notes = _extract_date(raw_text)
    start_time, end_time, overnight, time_conf, time_notes = _extract_times(raw_text)
    confirmed, assumed, unresolved, cred_conf, cred_notes = _extract_credentials(raw_text)
    specialty, spec_conf = _extract_specialty(raw_text, confirmed, assumed)
    unit = _extract_unit(raw_text)
    hospital_id, hospital_name, hosp_conf, hosp_notes = _extract_hospital(raw_text)
    urgency = _extract_urgency(raw_text, shift_date)

    # cred_conf already includes deductions for assumed/unresolved — no double-deduction
    confidence = max(0.0, min(1.0, date_conf + time_conf + cred_conf + spec_conf + hosp_conf))

    # Past date cap
    if shift_date and shift_date < date.today():
        confidence = min(confidence, 0.60)

    escalation_codes = _build_escalation_codes(
        shift_date, start_time, hospital_id, confirmed, assumed, unresolved, confidence
    )
    status = "ESCALATED" if escalation_codes else "PENDING_REVIEW"

    return ShiftRequest(
        id=str(uuid.uuid4())[:8],
        hospital_id=hospital_id,
        hospital_name=hospital_name,
        shift_date=shift_date,
        shift_start_time=start_time,
        shift_end_time=end_time,
        overnight=overnight,
        required_credentials=confirmed,
        assumed_credentials=assumed,
        unresolved_credentials=unresolved,
        specialty=specialty,
        unit=unit,
        urgency=urgency,
        raw_input=raw_text,
        parse_confidence=round(confidence, 2),
        status=status,
        escalation_codes=escalation_codes,
        source_channel=source_channel,
        created_at=now,
    )
