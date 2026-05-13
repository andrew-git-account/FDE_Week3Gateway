HOSPITALS = {
    "HOSP-001": {"name": "St. Mary's Boston",      "domain": "stmarys-boston.org"},
    "HOSP-002": {"name": "Springfield General",    "domain": "springfieldgeneral.org"},
    "HOSP-003": {"name": "Riverside Medical",      "domain": "riversidemedical.com"},
}

DOMAIN_TO_ID = {v["domain"]: k for k, v in HOSPITALS.items()}

NAME_KEYWORDS = {
    "HOSP-001": ["st mary", "st. mary", "stmary", "mary's boston"],
    "HOSP-002": ["springfield general", "springfield"],
    "HOSP-003": ["riverside medical", "riverside"],
}


def lookup_by_domain(email: str) -> tuple:
    """Return (hospital_id, hospital_name) or (None, None)."""
    email_lower = email.lower()
    for domain, hid in DOMAIN_TO_ID.items():
        if domain in email_lower:
            return hid, HOSPITALS[hid]["name"]
    return None, None


def lookup_by_name(text: str) -> tuple:
    """Return (hospital_id, hospital_name) or (None, None)."""
    text_lower = text.lower()
    for hid, keywords in NAME_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return hid, HOSPITALS[hid]["name"]
    return None, None
