from datetime import date

from generator.ids import generate_settlement_id


def generate_settlements(claims, assessments, policies, policy_coverages):
    """Generate settlement records for approved claims."""

    settlements = []

    policy_lookup = {
        policy["policy_id"]: policy
        for policy in policies
    }

    for claim in claims:
        assessment = next(
            item for item in assessments
            if item["claim_id"] == claim["claim_id"]
        )

        # Only approved and partially approved claims can be settled.
        if assessment["decision"] not in [
            "Approved",
            "Partially Approved"
        ]:
            continue

        policy = policy_lookup[claim["policy_id"]]

        applicable_coverages = [
            item for item in policy_coverages
            if item["policy_id"] == policy["policy_id"]
        ]

        if not applicable_coverages:
            continue

        # Use the same first linked coverage selected by the basic
        # assessment implementation.
        coverage = applicable_coverages[0]

        approved_amount = assessment["approved_amount"]
        deductible = coverage["deductible_amount"]

        payout_amount = round(
            max(0, approved_amount - deductible), 2
        )

        # Never allow settlement to exceed the coverage limit.
        payout_amount = min(
            payout_amount,
            coverage["coverage_limit"]
        )

        if payout_amount < 1000:
            payment_method = "Check"
        elif payout_amount < 10000:
            payment_method = "ACH"
        else:
            payment_method = "Wire Transfer"

        settlement = {
            "settlement_id": generate_settlement_id(claim["claim_id"]),
            "claim_id": claim["claim_id"],
            "approved_amount": approved_amount,
            "deductible_amount": deductible,
            "payout_amount": payout_amount,
            "payment_method": payment_method,
            "payment_status": "Pending",
            "settlement_date": date.today().isoformat()
        }

        settlements.append(settlement)

    return settlements