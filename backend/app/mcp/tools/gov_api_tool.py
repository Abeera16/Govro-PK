"""
Wrapper for structured lookups against known Pakistani government service categories.
In production these would call real departmental APIs where available (e.g. FBR IRIS,
NADRA verification endpoints). Where no public API exists, this returns curated
service metadata (fees, required documents, processing time) sourced from the
scraped/RAG corpus, so the agent has a deterministic fallback.
"""

SERVICE_CATALOG: dict[str, dict] = {
    "passport": {
        "department": "Directorate General of Immigration & Passports (DGIP)",
        "portal": "https://dgip.gov.pk",
        "documents": ["CNIC", "Old passport (if renewal)", "Passport fee receipt"],
        "processing_time": "Normal: 10-15 working days, Urgent: 3-5 working days",
    },
    "nadra_cnic": {
        "department": "NADRA",
        "portal": "https://nadra.gov.pk",
        "documents": ["Form B / Birth certificate", "Proof of residence", "Parent CNICs"],
        "processing_time": "Normal: 15-20 working days, Executive: 2-3 working days",
    },
    "driving_license": {
        "department": "Provincial Excise & Taxation / Traffic Police",
        "portal": "https://excise.punjab.gov.pk",
        "documents": ["CNIC", "Medical certificate", "Learner permit (min 6 months old)"],
        "processing_time": "Learner: same day, Permanent: 1-2 weeks after road test",
    },
    "tax_filing": {
        "department": "Federal Board of Revenue (FBR)",
        "portal": "https://iris.fbr.gov.pk",
        "documents": ["NTN/CNIC", "Salary certificate / bank statements", "Wealth statement"],
        "processing_time": "Instant e-filing, refunds 30-60 days",
    },
    "scholarship": {
        "department": "HEC / Provincial Education Departments",
        "portal": "https://hec.gov.pk",
        "documents": ["Academic transcripts", "Domicile", "Income certificate"],
        "processing_time": "Varies by scheme, typically 4-8 weeks",
    },
    "utility_complaint": {
        "department": "WAPDA / LESCO / SNGPL / Provincial regulators",
        "portal": "https://pitc.com.pk/wapda-complaint",
        "documents": ["Account/reference number", "CNIC"],
        "processing_time": "7-15 working days depending on complaint type",
    },
    "legal_aid": {
        "department": "Provincial Legal Aid Authorities / District Bar Associations",
        "portal": "https://punjab.gov.pk/legal_aid",
        "documents": ["CNIC", "Case details / FIR (if applicable)"],
        "processing_time": "Initial consultation typically within 1 week",
    },
    "health": {
        "department": "Sehat Sahulat Program / Provincial Health Departments",
        "portal": "https://sehatsahulat.gov.pk",
        "documents": ["CNIC", "Family registration certificate"],
        "processing_time": "Card issuance instant if eligible in NSER database",
    },
}


async def gov_lookup(service_key: str) -> dict | None:
    return SERVICE_CATALOG.get(service_key.lower().strip())


async def list_service_keys() -> list[str]:
    return list(SERVICE_CATALOG.keys())
