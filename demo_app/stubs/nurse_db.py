from datetime import date, time, timedelta
from core.models import NurseProfile

# Available dates: next 30 days
_today = date.today()
_available = [_today + timedelta(days=i) for i in range(30)]

NURSES = [
    NurseProfile(
        nurse_id="NURSE-001",
        name="Sarah Johnson",
        credentials=["RN", "ACLS", "ICU", "BLS"],
        compliance_valid_until=date(2027, 6, 30),
        available_dates=_available,
        available_start=time(6, 0),
        available_end=time(20, 0),
        communication_preference="SMS",
        reliability_score=0.92,
        distance_miles=3.0,
        hospital_preference={
            "HOSP-001": 0.90,  # 9/10 accepted
            "HOSP-002": 0.75,
        },
    ),
    NurseProfile(
        nurse_id="NURSE-002",
        name="Michael Chen",
        credentials=["RN", "ACLS", "ICU", "CCRN"],
        compliance_valid_until=date(2027, 3, 15),
        available_dates=_available,
        available_start=time(6, 0),
        available_end=time(20, 0),
        communication_preference="EMAIL",
        reliability_score=0.85,
        distance_miles=12.0,
        hospital_preference={
            "HOSP-001": 0.70,  # 7/10 accepted
            "HOSP-003": 0.80,
        },
    ),
    NurseProfile(
        nurse_id="NURSE-003",
        name="James Rodriguez",
        credentials=["RN", "ACLS", "ICU"],
        compliance_valid_until=date(2026, 11, 1),
        available_dates=_available,
        available_start=time(6, 0),
        available_end=time(20, 0),
        communication_preference="SMS",
        reliability_score=0.95,
        distance_miles=35.0,
        hospital_preference={
            "HOSP-001": 0.85,  # 17/20 accepted
            "HOSP-002": 0.90,
        },
    ),
    NurseProfile(
        nurse_id="NURSE-004",
        name="David Kim",
        credentials=["RN", "ACLS", "PICU", "BLS"],
        compliance_valid_until=date(2027, 8, 20),
        available_dates=_available,
        available_start=time(6, 0),
        available_end=time(20, 0),
        communication_preference="SMS",
        reliability_score=0.72,
        distance_miles=8.0,
        hospital_preference={},  # no history — new to HOSP-001
    ),
    NurseProfile(
        nurse_id="NURSE-005",
        name="Emma Wilson",
        credentials=["RN", "BLS"],  # no ICU, no ACLS — fails hard filter for ICU shifts
        compliance_valid_until=date(2027, 1, 10),
        available_dates=_available,
        available_start=time(6, 0),
        available_end=time(20, 0),
        communication_preference="EMAIL",
        reliability_score=0.78,
        distance_miles=5.0,
        hospital_preference={"HOSP-001": 0.60},
    ),
    NurseProfile(
        nurse_id="NURSE-006",
        name="Lisa Park",
        credentials=["LPN", "BLS"],  # LPN, no ACLS — fails hard filter for RN shifts
        compliance_valid_until=date(2026, 9, 30),
        available_dates=_available,
        available_start=time(6, 0),
        available_end=time(20, 0),
        communication_preference="SMS",
        reliability_score=0.88,
        distance_miles=2.0,
        hospital_preference={"HOSP-001": 0.60},
    ),
]


def get_all_nurses() -> list:
    return NURSES
