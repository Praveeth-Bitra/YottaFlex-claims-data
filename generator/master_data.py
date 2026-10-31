from generator.ids import next_id


def generate_coverage_catalog():
    """Create the master catalog of available insurance coverages."""

    coverage_definitions = [
        # Motor insurance
        ("MOTOR", "Collision", 50000),
        ("MOTOR", "Liability", 100000),
        ("MOTOR", "Comprehensive", 40000),

        # Health insurance
        ("HEALTH", "Hospitalization", 200000),
        ("HEALTH", "Outpatient", 20000),
        ("HEALTH", "Dental", 5000),

        # Home insurance
        ("HOME", "Structure", 300000),
        ("HOME", "Contents", 50000),
        ("HOME", "Personal Liability", 100000),

        # Travel insurance
        ("TRAVEL", "Trip Medical", 50000),
        ("TRAVEL", "Trip Cancellation", 10000),
        ("TRAVEL", "Baggage Loss", 3000),

        # Theft insurance
        ("THEFT", "Personal Property", 20000),
        ("THEFT", "Vehicle Theft", 40000),
        ("THEFT", "Burglary", 30000)
    ]

    coverages = []

    for product_type, coverage_name, coverage_limit in coverage_definitions:
        coverage = {
            "coverage_id": next_id("coverage"),
            "product_type": product_type,
            "coverage_name": coverage_name,
            "coverage_limit": coverage_limit
        }

        coverages.append(coverage)

    return coverages


def generate_adjusters(rng):
    """Generate 40 adjusters, with 4 inactive adjusters."""

    specializations = [
        "MOTOR",
        "HEALTH",
        "HOME",
        "TRAVEL",
        "THEFT"
    ]

    adjusters = []

    # Generate 6 specialized adjusters for each product type.
    for specialization in specializations:
        for _ in range(6):
            adjuster = {
                "adjuster_id": next_id("adjuster"),
                "specialization": specialization,
                "status": "Active"
            }

            adjusters.append(adjuster)

    # Generate 10 general adjusters.
    for _ in range(10):
        adjuster = {
            "adjuster_id": next_id("adjuster"),
            "specialization": "GENERAL",
            "status": "Active"
        }

        adjusters.append(adjuster)

    # Select exactly 4 adjusters to make inactive.
    inactive_adjusters = rng.sample(adjusters, 4)

    for adjuster in inactive_adjusters:
        adjuster["status"] = "Inactive"

    return adjusters