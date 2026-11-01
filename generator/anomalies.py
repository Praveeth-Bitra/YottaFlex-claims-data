from datetime import date, timedelta

from generator.ids import generate_settlement_id


def inject_source_anomalies(claims, policies, incidents, documents):
    if len(claims) < 5:
        raise ValueError("At least five claims are required for source anomalies.")

    ground_truth = []
    policy_lookup = {policy["policy_id"]: policy for policy in policies}

    selected_claims = claims[:5]
    incident_by_claim = {incident["claim_id"]: incident for incident in incidents}

    claim = selected_claims[0]
    policy = policy_lookup[claim["policy_id"]]
    incident = incident_by_claim[claim["claim_id"]]

    original_value = incident["incident_date"]
    injected_value = (
        date.fromisoformat(policy["effective_date"]) - timedelta(days=10)
    ).isoformat()
    incident["incident_date"] = injected_value

    ground_truth.append({
        "record_id": incident["incident_id"],
        "table_name": "Incident",
        "issue_type": "Incident Before Policy Start",
        "affected_field": "incident_date",
        "original_value": original_value,
        "injected_value": injected_value,
        "expected_outcome": "Rejected",
        "expected_reason": "Incident occurred before policy coverage began."
    })

    claim = selected_claims[1]
    policy = policy_lookup[claim["policy_id"]]
    incident = incident_by_claim[claim["claim_id"]]

    original_value = policy["cancellation_date"]
    cancellation_date = (
        date.fromisoformat(incident["incident_date"]) - timedelta(days=5)
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

    claim = selected_claims[2]
    incident = incident_by_claim[claim["claim_id"]]
    duplicate_incident = incident.copy()
    duplicate_incident["incident_id"] = f"{incident['incident_id']}-DUP"
    incidents.append(duplicate_incident)

    ground_truth.append({
        "record_id": duplicate_incident["incident_id"],
        "table_name": "Incident",
        "issue_type": "Duplicate Incident",
        "affected_field": "claim_id",
        "original_value": None,
        "injected_value": duplicate_incident["claim_id"],
        "expected_outcome": "Duplicate Detected",
        "expected_reason": "Two incident records refer to the same claim."
    })

    claim = selected_claims[3]
    claim_documents = [
        document for document in documents
        if document["claim_id"] == claim["claim_id"]
    ]
    original_document_count = len(claim_documents)

    documents[:] = [
        document for document in documents
        if document["claim_id"] != claim["claim_id"]
    ]

    ground_truth.append({
        "record_id": claim["claim_id"],
        "table_name": "Document",
        "issue_type": "Missing Mandatory Document",
        "affected_field": "document_type",
        "original_value": original_document_count,
        "injected_value": 0,
        "expected_outcome": "Pending Information",
        "expected_reason": "Mandatory claim evidence is missing."
    })

    return ground_truth


def inject_settlement_anomalies(claims, settlements, policy_coverages):
    if len(settlements) < 2:
        raise ValueError(
            "At least two settlements are required for settlement anomalies."
        )

    ground_truth = []
    claim_lookup = {claim["claim_id"]: claim for claim in claims}

    settlement_for_limit = settlements[0]
    claim_for_limit = claim_lookup[settlement_for_limit["claim_id"]]
    policy_id = claim_for_limit["policy_id"]

    policy_limits = [
        coverage["coverage_limit"]
        for coverage in policy_coverages
        if coverage["policy_id"] == policy_id
    ]
    if not policy_limits:
        raise ValueError(
            f"No policy coverage found for {policy_id}; cannot inject limit anomaly."
        )

    maximum_limit = max(policy_limits)
    original_payout = settlement_for_limit["payout_amount"]
    injected_payout = maximum_limit + 1000
    settlement_for_limit["payout_amount"] = injected_payout

    ground_truth.append({
        "record_id": settlement_for_limit["settlement_id"],
        "table_name": "Settlement",
        "issue_type": "Settlement Exceeds Limit",
        "affected_field": "payout_amount",
        "original_value": original_payout,
        "injected_value": injected_payout,
        "expected_outcome": "Invalid Settlement",
        "expected_reason": "Settlement exceeds the coverage limit."
    })

    limit_claim_id = settlement_for_limit["claim_id"]
    settlement_for_duplicate = next(
        (
            settlement for settlement in settlements
            if settlement["claim_id"] != limit_claim_id
        ),
        None
    )
    if settlement_for_duplicate is None:
        raise ValueError(
            "A second claim settlement is required for the duplicate-payment anomaly."
        )

    settlement_for_duplicate["payment_status"] = "Paid"
    duplicate_payment = settlement_for_duplicate.copy()
    duplicate_payment["settlement_id"] = generate_settlement_id(
        settlement_for_duplicate["claim_id"]
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