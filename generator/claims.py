from datetime import timedelta

from generator.config import CLAIM_COUNT, REFERENCE_DATE
from generator.ids import generate_claim_id


CLAIM_AMOUNT_RANGES = {
    "MOTOR": (150, 8000),
    "HEALTH": (80, 15000),
    "HOME": (200, 12000),
    "TRAVEL": (30, 2500),
    "THEFT": (100, 6000)
}


def generate_claims(policies, rng, count=CLAIM_COUNT):

    claims = []

    policies_by_type = {}

    for policy in policies:
        product_type = policy["product_type"]

        if product_type not in policies_by_type:
            policies_by_type[product_type] = []

        policies_by_type[product_type].append(policy)

    available_types = [
        product_type
        for product_type in CLAIM_AMOUNT_RANGES
        if policies_by_type.get(product_type)
    ]

    if not available_types:
        return claims

    for _ in range(count):
        claim_type = rng.choice(available_types)

        policy = rng.choice(policies_by_type[claim_type])

        minimum, maximum = CLAIM_AMOUNT_RANGES[claim_type]
        claimed_amount = round(rng.uniform(minimum, maximum), 2)

        claim = {
            "claim_id": generate_claim_id(),
            "policy_id": policy["policy_id"],
            "customer_id": policy["customer_id"],
            "claim_type": claim_type,
            "claimed_amount": claimed_amount,
            "submitted_date": REFERENCE_DATE.isoformat(),
            "status": "Submitted"
        }

        claims.append(claim)

    return claims