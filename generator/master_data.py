from generator.ids import next_id


def generate_coverage_catalog():
    """Create coverage definitions, including limits, deductibles and exclusions."""

    coverage_definitions = [
        ("MOTOR", "Collision", 50000, ["Intentional Damage", "Mechanical Breakdown"]),
        ("MOTOR", "Liability", 100000, ["Wear and Tear", "Intentional Damage"]),
        ("MOTOR", "Comprehensive", 40000, ["Mechanical Breakdown", "Normal Wear and Tear"]),

        ("HEALTH", "Hospitalization", 200000, ["Cosmetic Treatment", "Experimental Treatment"]),
        ("HEALTH", "Outpatient", 20000, ["Cosmetic Treatment", "Experimental Treatment"]),
        ("HEALTH", "Dental", 5000, ["Cosmetic Treatment", "Experimental Treatment"]),

        ("HOME", "Structure", 300000, ["Normal Wear and Tear", "Intentional Damage"]),
        ("HOME", "Contents", 50000, ["Normal Wear and Tear", "Intentional Damage"]),
        ("HOME", "Personal Liability", 100000, ["Intentional Damage", "Contractual Liability"]),

        ("TRAVEL", "Trip Medical", 50000, ["Pre-existing Condition", "Elective Treatment"]),
        ("TRAVEL", "Trip Cancellation", 10000, ["Voluntary Cancellation", "Known Event"]),
        ("TRAVEL", "Baggage Loss", 3000, ["Unattended Baggage", "Normal Wear and Tear"]),

        ("THEFT", "Personal Property", 20000, ["Unattended Property", "Fraudulent Claim"]),
        ("THEFT", "Vehicle Theft", 40000, ["Keys Left in Vehicle", "Fraudulent Claim"]),
        ("THEFT", "Burglary", 30000, ["Unforced Entry", "Fraudulent Claim"])
    ]

    coverages = []

    for product_type, coverage_name, coverage_limit, exclusions in coverage_definitions:
        coverages.append({
            "coverage_id": next_id("coverage"),
            "product_type": product_type,
            "coverage_name": coverage_name,
            "coverage_limit": coverage_limit,
            "exclusions": exclusions
        })

    return coverages


def generate_adjusters(rng):

    specializations = ["MOTOR", "HEALTH", "HOME", "TRAVEL", "THEFT"]
    adjusters = []

    for specialization in specializations:
        for _ in range(6):
            adjusters.append({
                "adjuster_id": next_id("adjuster"),
                "specialization": specialization,
                "status": "Active"
            })

    for _ in range(10):
        adjusters.append({
            "adjuster_id": next_id("adjuster"),
            "specialization": "GENERAL",
            "status": "Active"
        })

    for adjuster in rng.sample(adjusters, 4):
        adjuster["status"] = "Inactive"

    return adjusters
