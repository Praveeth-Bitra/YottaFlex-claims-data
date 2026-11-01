
from datetime import date
from collections import Counter


def check_primary_keys(records, key):
    values = [record[key] for record in records]
    return len(values) == len(set(values))


def check_foreign_keys(child_records, child_key, parent_records, parent_key):
    parent_values = {record[parent_key] for record in parent_records}

    return all(
        record[child_key] in parent_values
        for record in child_records
    )


def check_claim_item_totals(claims, claim_items):
    totals = {}

    for item in claim_items:
        claim_id = item["claim_id"]
        totals[claim_id] = totals.get(claim_id, 0) + item["item_amount"]

    return all(
        round(totals.get(claim["claim_id"], 0), 2)
        == round(claim["claimed_amount"], 2)
        for claim in claims
    )


def check_policy_dates(policies):
    for policy in policies:
        start = date.fromisoformat(policy["effective_date"])
        end = date.fromisoformat(policy["expiration_date"])

        if end <= start:
            return False

        if policy["cancellation_date"]:
            cancellation = date.fromisoformat(
                policy["cancellation_date"]
            )

            if cancellation < start:
                return False

    return True


def check_incident_before_policy_start(data):
    policies = {p["policy_id"]: p for p in data["policies"]}
    claims = {c["claim_id"]: c for c in data["claims"]}

    for incident in data["incidents"]:
        claim = claims.get(incident["claim_id"])

        if not claim:
            continue

        policy = policies.get(claim["policy_id"])

        if policy and date.fromisoformat(
            incident["incident_date"]
        ) < date.fromisoformat(policy["effective_date"]):
            return True

    return False


def check_policy_cancelled_before_incident(data):
    policies = {p["policy_id"]: p for p in data["policies"]}
    claims = {c["claim_id"]: c for c in data["claims"]}

    for incident in data["incidents"]:
        claim = claims.get(incident["claim_id"])

        if not claim:
            continue

        policy = policies.get(claim["policy_id"])

        if policy and policy["cancellation_date"]:
            if date.fromisoformat(
                policy["cancellation_date"]
            ) < date.fromisoformat(incident["incident_date"]):
                return True

    return False


def check_duplicate_incidents(incidents):
    counts = Counter(
        incident["claim_id"] for incident in incidents
    )

    return any(count > 1 for count in counts.values())


def check_missing_documents(claims, documents):
    documented_claims = {
        document["claim_id"] for document in documents
    }

    return any(
        claim["claim_id"] not in documented_claims
        for claim in claims
    )



def check_settlement_exceeds_limit(settlements, policy_coverages, claims):

    claim_policy_lookup = {
        claim["claim_id"]: claim["policy_id"]
        for claim in claims
    }

    limits = {}

    for coverage in policy_coverages:
        policy_id = coverage["policy_id"]
        limits.setdefault(policy_id, []).append(
            coverage["coverage_limit"]
        )

    for settlement in settlements:
        policy_id = claim_policy_lookup.get(settlement["claim_id"])

        if policy_id is None:
            continue

        matching_limits = limits.get(policy_id, [])

        if matching_limits:
            maximum_limit = max(matching_limits)

            if settlement["payout_amount"] > maximum_limit:
                return True

    return False


def check_duplicate_payments(settlements):
    paid_claims = [
        settlement["claim_id"]
        for settlement in settlements
        if settlement["payment_status"] == "Paid"
    ]

    counts = Counter(paid_claims)

    return any(count > 1 for count in counts.values())


def run_validation(data):
    results = {}

    results["customer_primary_keys"] = check_primary_keys(
        data["customers"], "customer_id"
    )

    results["policy_primary_keys"] = check_primary_keys(
        data["policies"], "policy_id"
    )

    results["claim_primary_keys"] = check_primary_keys(
        data["claims"], "claim_id"
    )

    results["incident_primary_keys"] = check_primary_keys(
        data["incidents"], "incident_id"
    )

    results["customer_foreign_keys"] = check_foreign_keys(
        data["policies"], "customer_id",
        data["customers"], "customer_id"
    )

    results["policy_foreign_keys"] = check_foreign_keys(
        data["claims"], "policy_id",
        data["policies"], "policy_id"
    )

    results["claim_item_foreign_keys"] = check_foreign_keys(
        data["claim_items"], "claim_id",
        data["claims"], "claim_id"
    )

    results["claim_item_totals"] = check_claim_item_totals(
        data["claims"], data["claim_items"]
    )

    results["policy_dates"] = check_policy_dates(data["policies"])
    
    results["anomaly_incident_before_policy_start"] = (
        check_incident_before_policy_start(data)
    )

    results["anomaly_policy_cancelled_before_incident"] = (
        check_policy_cancelled_before_incident(data)
    )

    results["anomaly_duplicate_incident"] = (
        check_duplicate_incidents(data["incidents"])
    )

    results["anomaly_missing_documents"] = (
        check_missing_documents(data["claims"], data["documents"])
    )

    results["anomaly_settlement_exceeds_limit"] = (
    check_settlement_exceeds_limit(
        data["settlements"],
        data["policy_coverages"],
        data["claims"]
    )
)

    results["anomaly_duplicate_payments"] = (
        check_duplicate_payments(data["settlements"])
    )

    return results
