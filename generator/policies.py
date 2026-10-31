from datetime import timedelta

from generator.config import POLICY_COUNT, REFERENCE_DATE, PRODUCT_TYPES
from generator.ids import generate_policy_id


PRODUCT_COUNTS = {
    "MOTOR": 700,
    "HEALTH": 500,
    "HOME": 360,
    "TRAVEL": 240,
    "THEFT": 200
}

PREMIUM_RANGES = {
    "MOTOR": (400, 1800),
    "HEALTH": (800, 3500),
    "HOME": (500, 2500),
    "TRAVEL": (40, 400),
    "THEFT": (100, 600)
}

DEDUCTIBLE_OPTIONS = [250, 500, 1000, 2500]


def generate_policies(customers, rng, count=POLICY_COUNT):

    policies = []

    product_types = []

    for product_type, product_count in PRODUCT_COUNTS.items():
        product_types.extend([product_type] * product_count)

    if count != len(product_types):
        product_types = [
            rng.choice(PRODUCT_TYPES) for _ in range(count)
        ]

    rng.shuffle(product_types)

    for index in range(count):
        product_type = product_types[index]

        customer = customers[index % len(customers)]

        effective_date = REFERENCE_DATE - timedelta(
            days=rng.randint(0, 1000)
        )

        expiration_date = effective_date + timedelta(days=365)

        status = (
            "Active"
            if REFERENCE_DATE <= expiration_date
            else "Expired"
        )

        cancellation_date = None

        if rng.random() < 0.05:
            status = "Cancelled"

            cancellation_date = (
                effective_date + timedelta(
                    days=rng.randint(30, 300)
                )
            )

            cancellation_date = min(
                cancellation_date,
                REFERENCE_DATE
            )

        premium_min, premium_max = PREMIUM_RANGES[product_type]

        policy = {
            "policy_id": generate_policy_id(product_type),
            "customer_id": customer["customer_id"],
            "product_type": product_type,
            "effective_date": effective_date.isoformat(),
            "expiration_date": expiration_date.isoformat(),
            "cancellation_date": (
                cancellation_date.isoformat()
                if cancellation_date else None
            ),
            "status": status,
            "premium_amount": round(
                rng.uniform(premium_min, premium_max), 2
            ),
            "deductible_amount": rng.choice(DEDUCTIBLE_OPTIONS)
        }

        policies.append(policy)

    return policies