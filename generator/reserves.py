from generator.ids import next_id


EXPENSE_RESERVE_RATE = 0.05


def generate_reserves(claims, assessments):
    """
    Derive indemnity and expense reserves from final claims and assessments.

    Rules:
    - Rejected: no indemnity or expense reserve.
    - Pending Information: retain the full claimed amount as an initial reserve.
    - Approved / Partially Approved: indemnity reserve equals approved amount;
      expense reserve is calculated from the approved amount.
    """

    assessment_lookup = {a["claim_id"]: a for a in assessments}
    claim_ids = {claim["claim_id"] for claim in claims}

    missing_assessments = claim_ids - set(assessment_lookup)
    if missing_assessments:
        raise ValueError(
            "Cannot calculate reserves; assessments missing for claims: "
            + ", ".join(sorted(missing_assessments)[:10])
        )

    reserves = []

    for claim in claims:
        assessment = assessment_lookup[claim["claim_id"]]
        claimed_amount = round(float(claim["claimed_amount"]), 2)
        decision = assessment["decision"]
        approved_amount = assessment["approved_amount"]

        initial_indemnity = claimed_amount
        initial_expense = round(claimed_amount * EXPENSE_RESERVE_RATE, 2)

        if decision == "Rejected":
            final_indemnity = 0.0
            final_expense = 0.0

        elif decision == "Pending Information":
            final_indemnity = initial_indemnity
            final_expense = initial_expense

        elif decision in ("Approved", "Partially Approved"):
            if approved_amount is None:
                raise ValueError(
                    f"{claim['claim_id']} has decision {decision} "
                    "but no approved_amount."
                )
            approved_amount = round(float(approved_amount), 2)
            if approved_amount < 0 or approved_amount > claimed_amount:
                raise ValueError(
                    f"Invalid approved_amount for {claim['claim_id']}: "
                    f"{approved_amount} (claimed {claimed_amount})."
                )
            final_indemnity = approved_amount
            final_expense = round(
                approved_amount * EXPENSE_RESERVE_RATE, 2
            )

        else:
            raise ValueError(
                f"Unknown assessment decision for {claim['claim_id']}: {decision}"
            )

        reserves.append({
            "reserve_id": next_id("reserve"),
            "claim_id": claim["claim_id"],
            "reserve_type": "Indemnity",
            "initial_amount": initial_indemnity,
            "reserved_amount": round(final_indemnity, 2)
        })

        reserves.append({
            "reserve_id": next_id("reserve"),
            "claim_id": claim["claim_id"],
            "reserve_type": "Expense",
            "initial_amount": initial_expense,
            "reserved_amount": round(final_expense, 2)
        })

    return reserves
