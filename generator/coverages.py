from generator.ids import next_id


def generate_policy_coverages(policies, coverage_catalog, rng):


    policy_coverages = []

    for policy in policies:
        product_type = policy["product_type"]

        compatible_coverages = [
            coverage for coverage in coverage_catalog
            if coverage["product_type"] == product_type
        ]

        selected_coverages = rng.sample(
            compatible_coverages,
            rng.randint(1, min(3, len(compatible_coverages)))
        )

        for coverage in selected_coverages:
            policy_coverage = {
                "policy_coverage_id": next_id("policy_coverage"),
                "policy_id": policy["policy_id"],
                "coverage_id": coverage["coverage_id"],
                "coverage_limit": coverage["coverage_limit"],
                "deductible_amount": policy["deductible_amount"]
            }

            policy_coverages.append(policy_coverage)

    return policy_coverages