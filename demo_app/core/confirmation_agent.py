import uuid
from datetime import datetime

from core.models import NurseAssignment, MatchProposal, ShiftRequest, ConfirmationEvent

YES_PATTERNS = {"yes", "y", "confirmed", "confirm", "ok", "sure", "on my way",
                "i'll be there", "ill be there", "definitely", "absolutely"}
NO_PATTERNS = {"no", "n", "can't", "cannot", "cant", "declining", "decline",
               "not available", "won't make it", "wont make it", "cancel"}
AMBIGUOUS_PATTERNS = {"probably", "should be", "i'll try", "ill try", "maybe",
                      "hopefully", "might", "not sure", "possibly"}


def _event(event_type: str, actor: str, notes: str = None) -> ConfirmationEvent:
    return ConfirmationEvent(
        event_type=event_type,
        occurred_at=datetime.utcnow(),
        actor=actor,
        notes=notes,
    )


def create_assignment(proposal: MatchProposal, req: ShiftRequest) -> NurseAssignment:
    return NurseAssignment(
        id=str(uuid.uuid4())[:8],
        match_proposal=proposal,
        shift_request=req,
        confirmation_status="PENDING_CONFIRMATION",
        notification_sent_at=None,
        confirmed_at=None,
        escalation_reason=None,
        events=[_event("ASSIGNMENT_CREATED", "system")],
    )


def send_notification(assignment: NurseAssignment) -> NurseAssignment:
    assignment.notification_sent_at = datetime.utcnow()
    channel = assignment.match_proposal.nurse.communication_preference
    assignment.events.append(_event(
        "NOTIFICATION_SENT",
        "agent-3",
        f"Confirmation request sent via {channel}",
    ))
    return assignment


def classify_reply(text: str) -> str:
    """Return CONFIRMED | CANCELLED | AMBIGUOUS."""
    lower = text.lower().strip()
    if any(p in lower for p in YES_PATTERNS):
        return "CONFIRMED"
    if any(p in lower for p in NO_PATTERNS):
        return "CANCELLED"
    return "AMBIGUOUS"


def process_reply(assignment: NurseAssignment, reply_text: str) -> NurseAssignment:
    classification = classify_reply(reply_text)
    assignment.events.append(_event(
        "REPLY_RECEIVED", "nurse",
        f'"{reply_text}" → classified as {classification}',
    ))

    if classification == "CONFIRMED":
        assignment.confirmation_status = "CONFIRMED"
        assignment.confirmed_at = datetime.utcnow()
        assignment.events.append(_event("CONFIRMED", "agent-3"))

    elif classification == "CANCELLED":
        assignment.confirmation_status = "CANCELLED"
        assignment.escalation_reason = "NURSE_CANCELLED"
        assignment.events.append(_event("CANCELLED", "agent-3", "Nurse declined — re-match required"))

    else:  # AMBIGUOUS
        assignment.confirmation_status = "UNCONFIRMED_ESCALATED"
        assignment.escalation_reason = "AMBIGUOUS_REPLY"
        assignment.events.append(_event(
            "ESCALATED", "agent-3",
            f'Ambiguous reply: "{reply_text}" — coordinator must interpret',
        ))

    return assignment


def simulate_no_reply_timeout(assignment: NurseAssignment) -> NurseAssignment:
    """Simulate T+24h no-reply escalation."""
    assignment.confirmation_status = "UNCONFIRMED_ESCALATED"
    assignment.escalation_reason = "NO_CONFIRMATION_24H"
    assignment.events.append(_event(
        "ESCALATED", "agent-3",
        "No reply received within 24h — coordinator action required",
    ))
    return assignment


def simulate_no_show(assignment: NurseAssignment) -> NurseAssignment:
    assignment.confirmation_status = "NO_SHOW"
    assignment.escalation_reason = "NO_SHOW_DETECTED"
    assignment.events.append(_event(
        "NO_SHOW_REPORTED", "coordinator",
        "Hospital reported nurse did not arrive — emergency re-match triggered",
    ))
    return assignment


def coordinator_confirm(assignment: NurseAssignment) -> NurseAssignment:
    """Coordinator manually confirms an escalated assignment."""
    assignment.confirmation_status = "CONFIRMED"
    assignment.confirmed_at = datetime.utcnow()
    assignment.events.append(_event("CONFIRMED", "coordinator", "Manually confirmed by coordinator"))
    return assignment


def coordinator_cancel(assignment: NurseAssignment) -> NurseAssignment:
    """Coordinator cancels an escalated assignment."""
    assignment.confirmation_status = "CANCELLED"
    assignment.escalation_reason = "COORDINATOR_CANCELLED"
    assignment.events.append(_event("CANCELLED", "coordinator", "Cancelled by coordinator — re-match required"))
    return assignment
