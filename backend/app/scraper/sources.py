"""
Curated list of official Pakistani government source pages to scrape and index.
Add/remove URLs here to control what GovroPK's RAG corpus covers.
"""

GOV_SOURCES: list[dict] = [
    {"url": "https://dgip.gov.pk/", "category": "passport", "title": "Directorate General of Immigration & Passports"},
    {"url": "https://www.nadra.gov.pk/", "category": "nadra_cnic", "title": "NADRA - National Database & Registration Authority"},
    {"url": "https://excise.punjab.gov.pk/", "category": "driving_license", "title": "Punjab Excise, Taxation & Narcotics Control Department"},
    {"url": "https://www.fbr.gov.pk/", "category": "tax_filing", "title": "Federal Board of Revenue"},
    {"url": "https://www.hec.gov.pk/", "category": "scholarship", "title": "Higher Education Commission Pakistan"},
    {"url": "https://sehatsahulat.gov.pk/", "category": "health", "title": "Sehat Sahulat Program"},
    {"url": "https://www.pakistan.gov.pk/", "category": "general", "title": "Government of Pakistan Official Portal"},
]
