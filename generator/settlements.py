from datetime import date

from generator.ids import generate_settlement_id


def generate_settlements(claims, assessments, policies=None, policy_coverages=None):
    """
    Derive settlement recommendations from the final assessment records.

    The selected coverage, limit and deductible are taken from the assessment.
    This prevents settlement generation from independently selecting a
    different policy coverage.
    """

    settlements = []
    assessment_lookup = {a["claim_id"]: a for a in assessments}

    for claim in claims:
        claim_id = claim["claim_id"]
        assessment = assessment_lookup.get(claim_id)

        if assessment is None:
            raise ValueError(f"Assessment missing for claim {claim_id}.")

        decision = assessment["decision"]
        if decision not in ("Approved", "Partially Approved"):
            continue

        approved_amount = assessment["approved_amount"]
        deductible = assessment["deductible_amount"]
        coverage_limit = assessment["coverage_limit"]
        coverage_id = assessment["coverage_id"]

        if approved_amount is None or coverage_id is None:
            raise ValueError(
                f"Approved claim {claim_id} is missing approved amount "
                "or selected coverage."
            )

        approved_amount = round(float(approved_amount), 2)
        deductible = round(float(deductible), 2)
        coverage_limit = round(float(coverage_limit), 2)

        if approved_amount < 0 or deductible < 0 or coverage_limit <= 0:
            raise ValueError(f"Invalid settlement inputs for claim {claim_id}.")
        payout_amount = round(max(0.0, approved_amount - deductible), 2)
        payout_amount = round(min(payout_amount, coverage_limit), 2)

        if payout_amount < 1000:
            payment_method = "Check"
        elif payout_amount < 10000:
            payment_method = "ACH"
        else:
            payment_method = "Wire Transfer"

        settlements.append({
            "settlement_id": generate_settlement_id(claim_id),
            "claim_id": claim_id,
            "coverage_id": coverage_id,
            "approved_amount": approved_amount,
            "deductible_amount": deductible,
            "payout_amount": payout_amount,
            "payment_method": payment_method,
            "payment_status": "Pending",
            "settlement_date": date.today().isoformat()
        })

    return settlements
