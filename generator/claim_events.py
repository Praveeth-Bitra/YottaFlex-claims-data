from generator.config import REFERENCE_DATE
from generator.ids import next_id


def generate_claim_events(
    claims,
    incidents,
    assignments,
    assessments,
    settlements
):
    """Create a chronological history of claim activities."""

    events = []

    incident_lookup = {
        incident["claim_id"]: incident
        for incident in incidents
    }

    assignment_lookup = {
        assignment["claim_id"]: assignment
        for assignment in assignments
    }

    assessment_lookup = {
        assessment["claim_id"]: assessment
        for assessment in assessments
    }

    settlement_lookup = {
        settlement["claim_id"]: settlement
        for settlement in settlements
    }

    for claim in claims:
        claim_id = claim["claim_id"]

        incident = incident_lookup[claim_id]
        assessment = assessment_lookup[claim_id]

        incident_date = incident["incident_date"]

        claim_events = [
            ("Claim Submitted", claim["submitted_date"]),
            ("Policy Validated", incident_date)
        ]

        if assessment["decision"] == "Pending Information":
            claim_events.append(
                ("Documents Requested", incident_date)
            )

        if claim_id in assignment_lookup:
            claim_events.append(
                ("Adjuster Assigned", incident_date)
            )

        claim_events.append(
            ("Assessment Completed", assessment["assessment_date"])
        )

        if assessment["decision"] == "Approved":
            claim_events.append(
                ("Claim Approved", assessment["assessment_date"])
            )

        elif assessment["decision"] == "Partially Approved":
            claim_events.append(
                ("Claim Partially Approved", assessment["assessment_date"])
            )

        elif assessment["decision"] == "Rejected":
            claim_events.append(
                ("Claim Rejected", assessment["assessment_date"])
            )

        if claim_id in settlement_lookup:
            settlement = settlement_lookup[claim_id]

            claim_events.append(
                ("Settlement Recommended", settlement["settlement_date"])
            )

        # Sort events by date before assigning sequence numbers.
        claim_events.sort(key=lambda event: event[1])

        for sequence, (event_type, event_date) in enumerate(
            claim_events, start=1
        ):
            events.append({
                "claim_event_id": next_id("claim_event"),
                "claim_id": claim_id,
                "event_sequence": sequence,
                "event_type": event_type,
                "event_date": event_date
            })

    return events