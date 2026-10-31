from datetime import date, timedelta

from generator.config import REFERENCE_DATE
from generator.ids import next_id


INCIDENT_TYPES = {
    "MOTOR": [
        "Vehicle Collision",
        "Vehicle Damage",
        "Vehicle Accident"
    ],
    "HEALTH": [
        "Hospitalization",
        "Medical Treatment",
        "Emergency Treatment"
    ],
    "HOME": [
        "Fire Damage",
        "Water Damage",
        "Property Damage"
    ],
    "TRAVEL": [
        "Trip Cancellation",
        "Medical Emergency",
        "Lost Baggage"
    ],
    "THEFT": [
        "Burglary",
        "Personal Property Theft",
        "Vehicle Theft"
    ]
}


def generate_incidents(claims, policies, rng):

    incidents = []

    policy_lookup = {
        policy["policy_id"]: policy
        for policy in policies
    }

    for claim in claims:
        policy = policy_lookup[claim["policy_id"]]

        policy_start = date.fromisoformat(
            policy["effective_date"]
        )

        policy_end = date.fromisoformat(
            policy["expiration_date"]
        )

        if policy["cancellation_date"]:
            cancellation_date = date.fromisoformat(
                policy["cancellation_date"]
            )
            policy_end = min(policy_end, cancellation_date)

        latest_date = min(policy_end, REFERENCE_DATE)

        if latest_date < policy_start:
            incident_date = policy_start
        else:
            days_available = (latest_date - policy_start).days

            incident_date = policy_start + timedelta(
                days=rng.randint(0, days_available)
            )

        incident = {
            "incident_id": next_id("incident"),
            "claim_id": claim["claim_id"],
            "incident_type": rng.choice(
                INCIDENT_TYPES[claim["claim_type"]]
            ),
            "incident_date": incident_date.isoformat(),
            "reported_date": (
                incident_date + timedelta(
                    days=rng.randint(1, 30)
                )
            ).isoformat(),
            "location": rng.choice([
                "New York",
                "California",
                "Texas",
                "Florida",
                "Illinois"
            ])
        }

        incidents.append(incident)

    return incidents