from dataclasses import dataclass, field
from datetime import date, time, datetime
from typing import Optional


@dataclass
class ShiftRequest:
    id: str
    hospital_id: Optional[str]
    hospital_name: Optional[str]
    shift_date: Optional[date]
    shift_start_time: Optional[time]
    shift_end_time: Optional[time]
    overnight: bool
    required_credentials: list
    assumed_credentials: list
    unresolved_credentials: list
    specialty: Optional[str]
    unit: Optional[str]
    urgency: str  # STANDARD | URGENT | EMERGENCY
    raw_input: str
    parse_confidence: float
    status: str  # PENDING_REVIEW | RELEASED | ESCALATED
    escalation_codes: list
    source_channel: str
    created_at: datetime


@dataclass
class NurseProfile:
    nurse_id: str
    name: str
    credentials: list
    compliance_valid_until: date
    available_dates: list
    available_start: time
    available_end: time
    communication_preference: str  # SMS | EMAIL
    reliability_score: float
    distance_miles: float
    hospital_preference: dict  # hospital_id -> preference_score (0.0-1.0)


@dataclass
class ScoreBreakdown:
    proximity_score: float
    proximity_weight: float
    preference_score: float
    preference_weight: float
    reliability_score: float
    reliability_weight: float
    specialty_score: float
    specialty_weight: float
    total: float
    notes: list = field(default_factory=list)


@dataclass
class CandidateResult:
    nurse: NurseProfile
    passed_hard_filter: bool
    hard_filter_failure: Optional[str]
    score_breakdown: Optional[ScoreBreakdown]


@dataclass
class MatchProposal:
    id: str
    shift_request_id: str
    nurse: Optional[NurseProfile]
    confidence_score: float
    routing: str  # AUTO_SUBMIT | ASYNC_REVIEW | HUMAN_ESCALATE | NO_MATCH
    score_breakdown: Optional[ScoreBreakdown]
    status: str  # PROPOSED | ACCEPTED | RECALLED | NO_MATCH
    proposed_at: Optional[datetime]
    all_candidates: list  # list[CandidateResult]


@dataclass
class ConfirmationEvent:
    event_type: str
    occurred_at: datetime
    actor: str
    notes: Optional[str]


@dataclass
class NurseAssignment:
    id: str
    match_proposal: MatchProposal
    shift_request: ShiftRequest
    confirmation_status: str  # PENDING_CONFIRMATION | CONFIRMED | UNCONFIRMED_ESCALATED | CANCELLED | NO_SHOW | COMPLETED
    notification_sent_at: Optional[datetime]
    confirmed_at: Optional[datetime]
    escalation_reason: Optional[str]
    events: list = field(default_factory=list)  # list[ConfirmationEvent]
