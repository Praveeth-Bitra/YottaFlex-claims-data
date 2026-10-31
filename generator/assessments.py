from datetime import date

from generator.ids import generate_assessment_id
from generator.documents import REQUIRED_DOCUMENTS


def assess_claims(
    claims,
    policies,
    incidents,
    documents,
    policy_coverages
):
    """Assess claims using policy, coverage and document information."""

    assessments = []

    policy_lookup = {
        policy["policy_id"]: policy
        for policy in policies
    }

    incident_lookup = {
        incident["claim_id"]: incident
        for incident in incidents
    }

    for claim in claims:
        policy = policy_lookup[claim["policy_id"]]
        incident = incident_lookup[claim["claim_id"]]

        incident_date = date.fromisoformat(
            incident["incident_date"]
        )

        effective_date = date.fromisoformat(
            policy["effective_date"]
        )

        expiration_date = date.fromisoformat(
            policy["expiration_date"]
        )

        cancellation_date = None

        if policy["cancellation_date"]:
            cancellation_date = date.fromisoformat(
                policy["cancellation_date"]
            )

        # Find the policy's coverages.
        available_coverages = [
            item for item in policy_coverages
            if item["policy_id"] == policy["policy_id"]
        ]

        applicable_coverage = (
            available_coverages[0]
            if available_coverages else None
        )

        # Find documents for this claim.
        claim_documents = [
            document for document in documents
            if document["claim_id"] == claim["claim_id"]
        ]

        required_document = REQUIRED_DOCUMENTS[claim["claim_type"]]

        required_document_received = any(
            document["document_type"] == required_document
            and document["status"] == "Verified"
            for document in claim_documents
        )

        decision = "Approved"
        reason = "All basic validation checks passed."
        approved_amount = claim["claimed_amount"]

        # 1. Check policy validity.
        if incident_date < effective_date or incident_date > expiration_date:
            decision = "Rejected"
            reason = "Incident occurred outside the policy period."
            approved_amount = 0

        # 2. Check cancellation.
        elif cancellation_date and incident_date >= cancellation_date:
            decision = "Rejected"
            reason = "Policy was cancelled before or on the incident date."
            approved_amount = 0

        # 3. Check mandatory documents.
        elif not required_document_received:
            decision = "Pending Information"
            reason = "Mandatory document is missing or not verified."
            approved_amount = None

        # 4. Check coverage.
        elif not applicable_coverage:
            decision = "Rejected"
            reason = "No coverage is linked to the policy."
            approved_amount = 0

        # 5. Check coverage limit.
        elif claim["claimed_amount"] > applicable_coverage["coverage_limit"]:
            decision = "Partially Approved"
            reason = "Claim amount exceeds the coverage limit."
            approved_amount = applicable_coverage["coverage_limit"]

        assessment = {
            "assessment_id": generate_assessment_id(claim["claim_id"]),
            "claim_id": claim["claim_id"],
            "decision": decision,
            "reason": reason,
            "claimed_amount": claim["claimed_amount"],
            "approved_amount": approved_amount,
            "assessment_date": date.today().isoformat()
        }

        assessments.append(assessment)

    return assessments