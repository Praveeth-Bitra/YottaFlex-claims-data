from generator.ids import next_id


def generate_reserves(claims, assessments):
    """Generate indemnity and expense reserves for every claim."""

    reserves = []

    assessment_lookup = {
        assessment["claim_id"]: assessment
        for assessment in assessments
    }

    for claim in claims:
        assessment = assessment_lookup[claim["claim_id"]]

        claimed_amount = claim["claimed_amount"]

        # Initial reserve estimates.
        initial_indemnity = claimed_amount
        initial_expense = round(claimed_amount * 0.05, 2)

        # Update reserves based on the assessment decision.
        if assessment["decision"] == "Rejected":
            final_indemnity = 0
            final_expense = 0

        elif assessment["decision"] == "Pending Information":
            final_indemnity = initial_indemnity
            final_expense = initial_expense

        else:
            final_indemnity = assessment["approved_amount"]
            final_expense = round(final_indemnity * 0.05, 2)

        reserves.append({
            "reserve_id": next_id("reserve"),
            "claim_id": claim["claim_id"],
            "reserve_type": "Indemnity",
            "initial_amount": initial_indemnity,
            "reserved_amount": final_indemnity
        })

        reserves.append({
            "reserve_id": next_id("reserve"),
            "claim_id": claim["claim_id"],
            "reserve_type": "Expense",
            "initial_amount": initial_expense,
            "reserved_amount": final_expense
        })

    return reserves