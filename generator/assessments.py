
from datetime import date

from generator.ids import generate_assessment_id
from generator.documents import REQUIRED_DOCUMENTS
INCIDENT_COVERAGE_MAP = {
    "Vehicle Collision": "Collision",
    "Vehicle Damage": "Comprehensive",
    "Vehicle Accident": "Collision",

    "Hospitalization": "Hospitalization",
    "Medical Treatment": "Outpatient",
    "Emergency Treatment": "Hospitalization",

    "Fire Damage": "Structure",
    "Water Damage": "Structure",
    "Property Damage": "Contents",

    "Trip Cancellation": "Trip Cancellation",
    "Medical Emergency": "Trip Medical",
    "Lost Baggage": "Baggage Loss",

    "Burglary": "Burglary",
    "Personal Property Theft": "Personal Property",
    "Vehicle Theft": "Vehicle Theft",
}


def assess_claims(claims, policies, incidents, documents, policy_coverages,
                  coverage_catalog=None):
    """Assess claims against policy dates, applicable coverage, exclusions and evidence."""

    assessments = []

    policy_lookup = {p["policy_id"]: p for p in policies}
    incident_lookup = {i["claim_id"]: i for i in incidents}
    coverage_lookup = {
        c["coverage_id"]: c for c in (coverage_catalog or [])
    }

    policy_coverage_lookup = {}
    for pc in policy_coverages:
        policy_coverage_lookup.setdefault(pc["policy_id"], []).append(pc)

    documents_lookup = {}
    for document in documents:
        documents_lookup.setdefault(document["claim_id"], []).append(document)

    for claim in claims:
        policy = policy_lookup[claim["policy_id"]]
        incident = incident_lookup[claim["claim_id"]]

        incident_date = date.fromisoformat(incident["incident_date"])
        effective_date = date.fromisoformat(policy["effective_date"])
        expiration_date = date.fromisoformat(policy["expiration_date"])
        cancellation_date = (
            date.fromisoformat(policy["cancellation_date"])
            if policy.get("cancellation_date") else None
        )

        incident_type = incident["incident_type"]
        required_coverage_name = INCIDENT_COVERAGE_MAP.get(incident_type)

        policy_coverages_for_claim = policy_coverage_lookup.get(
            policy["policy_id"], []
        )

        applicable_policy_coverage = None
        applicable_catalog_coverage = None

        for policy_coverage in policy_coverages_for_claim:
            catalog_coverage = coverage_lookup.get(policy_coverage["coverage_id"])
            if (
                catalog_coverage
                and catalog_coverage["product_type"] == claim["claim_type"]
                and catalog_coverage["coverage_name"] == required_coverage_name
            ):
                applicable_policy_coverage = policy_coverage
                applicable_catalog_coverage = catalog_coverage
                break

        claim_documents = documents_lookup.get(claim["claim_id"], [])
        required_document = REQUIRED_DOCUMENTS[claim["claim_type"]]
        required_document_received = any(
            d["document_type"] == required_document and d["status"] == "Verified"
            for d in claim_documents
        )

        decision = "Approved"
        reason = "Applicable coverage, policy period and required evidence validated."
        approved_amount = claim["claimed_amount"]
        selected_coverage_id = None
        coverage_limit = 0
        deductible_amount = 0

        if incident_date < effective_date or incident_date > expiration_date:
            decision = "Rejected"
            reason = "Incident occurred outside the policy period."
            approved_amount = 0

        elif cancellation_date and incident_date >= cancellation_date:
            decision = "Rejected"
            reason = "Policy was cancelled before or on the incident date."
            approved_amount = 0

        elif not required_document_received:
            decision = "Pending Information"
            reason = "Mandatory document is missing or not verified."
            approved_amount = None

        elif not required_coverage_name:
            decision = "Rejected"
            reason = "No coverage mapping exists for this incident type."
            approved_amount = 0

        elif not applicable_policy_coverage:
            decision = "Rejected"
            reason = f"Policy does not include the required coverage: {required_coverage_name}."
            approved_amount = 0

        else:
            selected_coverage_id = applicable_policy_coverage["coverage_id"]
            coverage_limit = applicable_policy_coverage["coverage_limit"]
            deductible_amount = applicable_policy_coverage["deductible_amount"]

            exclusions = applicable_catalog_coverage.get("exclusions", [])
            matched_exclusion = next(
                (exclusion for exclusion in exclusions
                 if exclusion.casefold() in incident_type.casefold()),
                None
            )

            if matched_exclusion:
                decision = "Rejected"
                reason = f"Incident falls under coverage exclusion: {matched_exclusion}."
                approved_amount = 0
            elif claim["claimed_amount"] > coverage_limit:
                decision = "Partially Approved"
                reason = "Claim amount exceeds the applicable coverage limit."
                approved_amount = coverage_limit

        assessments.append({
            "assessment_id": generate_assessment_id(claim["claim_id"]),
            "claim_id": claim["claim_id"],
            "coverage_id": selected_coverage_id,
            "coverage_limit": coverage_limit,
            "deductible_amount": deductible_amount,
            "decision": decision,
            "reason": reason,
            "claimed_amount": claim["claimed_amount"],
            "approved_amount": approved_amount,
            "assessment_date": date.today().isoformat()
        })

    return assessments
