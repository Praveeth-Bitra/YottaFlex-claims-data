
from datetime import date, timedelta

from generator.ids import generate_settlement_id


def inject_anomalies(
    claims, policies, incidents, documents,
    settlements, policy_coverages
):
    """Inject six required negative scenarios and record ground truth."""

    ground_truth = []

    policy_lookup = {
        policy["policy_id"]: policy
        for policy in policies
    }

    incident_lookup = {
        incident["claim_id"]: incident
        for incident in incidents
    }

    selected_claims = claims[:6]

    if len(selected_claims) < 6:
        raise ValueError("At least six claims are required.")

    # 1. Incident before policy start date.
    claim = selected_claims[0]
    policy = policy_lookup[claim["policy_id"]]
    incident = incident_lookup[claim["claim_id"]]

    original_value = incident["incident_date"]

    new_value = (
        date.fromisoformat(policy["effective_date"])
        - timedelta(days=10)
    ).isoformat()

    incident["incident_date"] = new_value

    ground_truth.append({
        "record_id": incident["incident_id"],
        "table_name": "Incident",
        "issue_type": "Incident Before Policy Start",
        "affected_field": "incident_date",
        "original_value": original_value,
        "injected_value": new_value,
        "expected_outcome": "Rejected",
        "expected_reason": "Incident occurred before policy coverage began."
    })

    # 2. Policy cancelled before incident.
    claim = selected_claims[1]
    policy = policy_lookup[claim["policy_id"]]
    incident = incident_lookup[claim["claim_id"]]

    original_value = policy["cancellation_date"]

    cancellation_date = (
        date.fromisoformat(incident["incident_date"])
        - timedelta(days=5)
    )

    policy["cancellation_date"] = cancellation_date.isoformat()
    policy["status"] = "Cancelled"

    ground_truth.append({
        "record_id": policy["policy_id"],
        "table_name": "Policy",
        "issue_type": "Policy Cancelled Before Incident",
        "affected_field": "cancellation_date",
        "original_value": original_value,
        "injected_value": cancellation_date.isoformat(),
        "expected_outcome": "Rejected",
        "expected_reason": "Policy was cancelled before the incident."
    })

    # 3. Duplicate incident.
    claim = selected_claims[2]
    incident = incident_lookup[claim["claim_id"]]

    duplicate = incident.copy()
    duplicate["incident_id"] = f"{incident['incident_id']}-DUP"

    incidents.append(duplicate)

    ground_truth.append({
        "record_id": duplicate["incident_id"],
        "table_name": "Incident",
        "issue_type": "Duplicate Incident",
        "affected_field": "claim_id",
        "original_value": None,
        "injected_value": duplicate["claim_id"],
        "expected_outcome": "Duplicate Detected",
        "expected_reason": "Two incident records refer to the same claim."
    })

    # 4. Settlement exceeds coverage limit.
    claim = selected_claims[3]

    existing_settlement = next(
        (
            settlement for settlement in settlements
            if settlement["claim_id"] == claim["claim_id"]
        ),
        None
    )

    if existing_settlement is None:
        raise ValueError(
            "Cannot inject settlement anomaly: no settlement exists "
            "for the selected claim."
        )

    matching_coverages = [
        coverage for coverage in policy_coverages
        if coverage["policy_id"] == claim["policy_id"]
    ]

    if not matching_coverages:
        raise ValueError("No coverage found for settlement anomaly.")

    maximum_limit = max(
        coverage["coverage_limit"]
        for coverage in matching_coverages
    )

    original_value = existing_settlement["payout_amount"]
    new_value = maximum_limit + 1000

    existing_settlement["payout_amount"] = new_value

    ground_truth.append({
        "record_id": existing_settlement["settlement_id"],
        "table_name": "Settlement",
        "issue_type": "Settlement Exceeds Limit",
        "affected_field": "payout_amount",
        "original_value": original_value,
        "injected_value": new_value,
        "expected_outcome": "Invalid Settlement",
        "expected_reason": "Settlement exceeds the coverage limit."
    })

    # 5. Missing mandatory document.
    claim = selected_claims[4]

    claim_documents = [
        document for document in documents
        if document["claim_id"] == claim["claim_id"]
    ]

    original_documents = len(claim_documents)

    documents[:] = [
        document for document in documents
        if document["claim_id"] != claim["claim_id"]
    ]

    ground_truth.append({
        "record_id": claim["claim_id"],
        "table_name": "Document",
        "issue_type": "Missing Mandatory Document",
        "affected_field": "document_type",
        "original_value": original_documents,
        "injected_value": 0,
        "expected_outcome": "Pending Information",
        "expected_reason": "Mandatory claim evidence is missing."
    })

    # 6. Claim paid twice.
    previously_used_claim_ids = {
        selected_claims[index]["claim_id"]
        for index in range(5)
    }

    existing_settlement = next(
        (
            settlement for settlement in settlements
            if settlement["claim_id"] not in previously_used_claim_ids
        ),
        None
    )

    if existing_settlement is None:
        raise ValueError(
            "Cannot inject duplicate payment: no suitable settlement exists."
        )

    existing_settlement["payment_status"] = "Paid"

    duplicate_payment = existing_settlement.copy()

    duplicate_payment["settlement_id"] = generate_settlement_id(
        existing_settlement["claim_id"]
    )

    duplicate_payment["payment_status"] = "Paid"

    settlements.append(duplicate_payment)

    ground_truth.append({
        "record_id": duplicate_payment["settlement_id"],
        "table_name": "Settlement",
        "issue_type": "Claim Paid Twice",
        "affected_field": "claim_id",
        "original_value": 1,
        "injected_value": 2,
        "expected_outcome": "Duplicate Payment Detected",
        "expected_reason": "More than one payment exists for the same claim."
    })

    return ground_truth
