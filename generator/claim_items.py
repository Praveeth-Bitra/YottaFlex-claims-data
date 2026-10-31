from generator.ids import next_id


ITEM_DESCRIPTIONS = {
    "MOTOR": [
        "Vehicle Repair",
        "Replacement Parts",
        "Labor Charges",
        "Towing Charges"
    ],
    "HEALTH": [
        "Hospital Charges",
        "Medical Consultation",
        "Medicine Expenses",
        "Diagnostic Tests"
    ],
    "HOME": [
        "Building Repairs",
        "Furniture Replacement",
        "Electrical Repairs",
        "Cleaning Expenses"
    ],
    "TRAVEL": [
        "Flight Expenses",
        "Hotel Expenses",
        "Medical Expenses",
        "Baggage Replacement"
    ],
    "THEFT": [
        "Stolen Electronics",
        "Stolen Jewellery",
        "Personal Belongings",
        "Property Replacement"
    ]
}


def generate_claim_items(claims, rng):
    """Generate 1-4 items for each claim."""

    claim_items = []

    for claim in claims:
        item_count = rng.randint(1, 4)

        descriptions = ITEM_DESCRIPTIONS[claim["claim_type"]]

        # Split the claim amount into item amounts.
        remaining_amount = claim["claimed_amount"]

        for index in range(item_count):
            if index == item_count - 1:
                item_amount = remaining_amount
            else:
                # Keep enough amount for the remaining items.
                maximum = remaining_amount / (item_count - index)

                item_amount = round(
                    rng.uniform(0, maximum), 2
                )

                remaining_amount -= item_amount

            item = {
                "claim_item_id": next_id("claim_item"),
                "claim_id": claim["claim_id"],
                "description": rng.choice(descriptions),
                "item_amount": round(item_amount, 2)
            }

            claim_items.append(item)

    return claim_items


def calculate_claim_totals(claims, claim_items):
    """Calculate claim amounts from their item records."""

    totals = {}

    for item in claim_items:
        claim_id = item["claim_id"]

        if claim_id not in totals:
            totals[claim_id] = 0

        totals[claim_id] += item["item_amount"]

    for claim in claims:
        claim["claimed_amount"] = round(
            totals.get(claim["claim_id"], 0), 2
        )

    return claims