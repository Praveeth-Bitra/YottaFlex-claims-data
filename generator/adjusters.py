def assign_adjusters(claims, adjusters, rng):

    assignments = []

    for claim in claims:
        claim_type = claim["claim_type"]
        suitable_adjusters = [
            adjuster for adjuster in adjusters
            if adjuster["status"] == "Active"
            and adjuster["specialization"] == claim_type
        ]

        if not suitable_adjusters:
            suitable_adjusters = [
                adjuster for adjuster in adjusters
                if adjuster["status"] == "Active"
                and adjuster["specialization"] == "GENERAL"
            ]

        if not suitable_adjusters:
            raise ValueError(
                f"No active adjuster available for {claim['claim_id']}"
            )

        selected_adjuster = rng.choice(suitable_adjusters)

        assignments.append({
            "claim_id": claim["claim_id"],
            "adjuster_id": selected_adjuster["adjuster_id"]
        })

    return assignments