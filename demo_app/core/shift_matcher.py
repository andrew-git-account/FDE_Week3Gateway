import uuid
from datetime import datetime
from typing import Optional

from core.models import (
    ShiftRequest, NurseProfile, ScoreBreakdown,
    CandidateResult, MatchProposal,
)

WEIGHTS = {
    "proximity": 0.30,
    "preference": 0.25,
    "reliability": 0.25,
    "specialty": 0.20,
}

ROUTING_THRESHOLDS = {
    "AUTO_SUBMIT": 0.85,
    "ASYNC_REVIEW": 0.70,
}


# ── Hard filter ───────────────────────────────────────────────────────────────

def hard_filter(nurse: NurseProfile, req: ShiftRequest) -> tuple:
    """Return (passed: bool, reason: str | None)."""
    # Only CONFIRMED credentials are hard requirements; ASSUMED are soft signals
    missing = [c for c in req.required_credentials if c not in nurse.credentials]
    if missing:
        return False, f"Missing credentials: {', '.join(missing)}"

    # Compliance
    if req.shift_date and nurse.compliance_valid_until < req.shift_date:
        return False, f"Compliance expired {nurse.compliance_valid_until}"

    # Availability
    if req.shift_date and req.shift_date not in nurse.available_dates:
        return False, f"Not available on {req.shift_date}"

    return True, None


# ── Soft scoring ──────────────────────────────────────────────────────────────

def _proximity_score(miles: float) -> float:
    if miles <= 5:
        return 1.0
    if miles <= 15:
        return 0.75
    if miles <= 30:
        return 0.50
    if miles <= 50:
        return 0.25
    return 0.0


def _preference_score(nurse: NurseProfile, hospital_id: Optional[str]) -> tuple:
    if not hospital_id or hospital_id not in nurse.hospital_preference:
        return 0.50, "no history — using default 0.50"
    score = nurse.hospital_preference[hospital_id]
    return score, f"hospital preference: {score:.0%}"


def _specialty_score(nurse: NurseProfile, specialty: Optional[str]) -> tuple:
    if not specialty:
        return 0.40, "no specialty in request"
    if specialty in nurse.credentials:
        return 1.0, f"exact specialty match: {specialty}"
    # Related specialties
    related_map = {
        "ICU": ["PICU", "NICU", "CCRN"],
        "PICU": ["ICU", "Pediatrics"],
        "ER": ["ICU", "TNCC", "CEN"],
        "Telemetry": ["MedSurg", "PCCN"],
    }
    related = related_map.get(specialty, [])
    if any(r in nurse.credentials for r in related):
        return 0.50, f"related specialty (has {[r for r in related if r in nurse.credentials]})"
    return 0.20, "no specialty match"


def soft_score(nurse: NurseProfile, req: ShiftRequest) -> ScoreBreakdown:
    prox = _proximity_score(nurse.distance_miles)
    pref, pref_note = _preference_score(nurse, req.hospital_id)
    rel = nurse.reliability_score if nurse.reliability_score else 0.60
    spec, spec_note = _specialty_score(nurse, req.specialty)

    notes = []
    if not nurse.reliability_score:
        notes.append("new nurse — reliability defaulted to 0.60")
    notes.append(pref_note)
    notes.append(spec_note)

    total = (
        prox * WEIGHTS["proximity"]
        + pref * WEIGHTS["preference"]
        + rel * WEIGHTS["reliability"]
        + spec * WEIGHTS["specialty"]
    )

    return ScoreBreakdown(
        proximity_score=round(prox, 3),
        proximity_weight=WEIGHTS["proximity"],
        preference_score=round(pref, 3),
        preference_weight=WEIGHTS["preference"],
        reliability_score=round(rel, 3),
        reliability_weight=WEIGHTS["reliability"],
        specialty_score=round(spec, 3),
        specialty_weight=WEIGHTS["specialty"],
        total=round(total, 3),
        notes=notes,
    )


# ── Routing ───────────────────────────────────────────────────────────────────

def route(confidence: float) -> str:
    if confidence >= ROUTING_THRESHOLDS["AUTO_SUBMIT"]:
        return "AUTO_SUBMIT"
    if confidence >= ROUTING_THRESHOLDS["ASYNC_REVIEW"]:
        return "ASYNC_REVIEW"
    return "HUMAN_ESCALATE"


# ── Reservation (in-memory, passed via session_state) ────────────────────────

def try_reserve(nurse_id: str, reservations: dict) -> bool:
    """Return True if reservation acquired; False if nurse already reserved."""
    now = datetime.utcnow()
    if nurse_id in reservations and reservations[nurse_id] > now:
        return False
    from datetime import timedelta
    reservations[nurse_id] = now + timedelta(minutes=15)
    return True


def release_reservation(nurse_id: str, reservations: dict) -> None:
    reservations.pop(nurse_id, None)


# ── Main matching pipeline ────────────────────────────────────────────────────

def run_matching(req: ShiftRequest, nurses: list, reservations: dict) -> MatchProposal:
    candidates = []

    for nurse in nurses:
        passed, reason = hard_filter(nurse, req)
        if passed:
            breakdown = soft_score(nurse, req)
            candidates.append(CandidateResult(
                nurse=nurse,
                passed_hard_filter=True,
                hard_filter_failure=None,
                score_breakdown=breakdown,
            ))
        else:
            candidates.append(CandidateResult(
                nurse=nurse,
                passed_hard_filter=False,
                hard_filter_failure=reason,
                score_breakdown=None,
            ))

    passing = [c for c in candidates if c.passed_hard_filter]

    if not passing:
        return MatchProposal(
            id=str(uuid.uuid4())[:8],
            shift_request_id=req.id,
            nurse=None,
            confidence_score=0.0,
            routing="NO_MATCH",
            score_breakdown=None,
            status="NO_MATCH",
            proposed_at=None,
            all_candidates=candidates,
        )

    # Sort by score descending; tie-break: reliability desc, distance asc
    passing.sort(
        key=lambda c: (
            -c.score_breakdown.total,
            -c.nurse.reliability_score,
            c.nurse.distance_miles,
        )
    )

    # Find first nurse we can reserve
    selected = None
    for candidate in passing:
        if try_reserve(candidate.nurse.nurse_id, reservations):
            selected = candidate
            break

    if not selected:
        # All reserved — use top candidate without reservation for display
        selected = passing[0]

    # Apply assumed-credential penalty: uncertain request warrants more conservative routing
    assumed_penalty = 0.10 if req.assumed_credentials else 0.0
    adjusted_confidence = max(0.0, selected.score_breakdown.total - assumed_penalty)
    routing = route(adjusted_confidence)

    return MatchProposal(
        id=str(uuid.uuid4())[:8],
        shift_request_id=req.id,
        nurse=selected.nurse,
        confidence_score=round(adjusted_confidence, 3),
        routing=routing,
        score_breakdown=selected.score_breakdown,
        status="PROPOSED",
        proposed_at=datetime.utcnow(),
        all_candidates=candidates,
    )
