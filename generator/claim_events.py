
from generator.config import REFERENCE_DATE
from generator.ids import next_id


def generate_claim_events(
    claims,
    incidents,
    assignments,
    assessments,
    settlements,
    anomaly_records
):
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

    settlement_lookup = {}
    settlement_id_lookup = {}

    for settlement in settlements:
        settlement_lookup.setdefault(
            settlement["claim_id"], settlement
        )
        settlement_id_lookup[settlement["settlement_id"]] = settlement
    anomaly_events = {}

    for anomaly in anomaly_records:
        issue_type = anomaly["issue_type"]
        table_name = anomaly["table_name"]
        record_id = anomaly["record_id"]

        claim_id = None
        event_type = None
        event_date = REFERENCE_DATE

        if issue_type == "Duplicate Incident":
            claim_id = anomaly["injected_value"]
            event_type = "Duplicate Incident Detected"

            incident = incident_lookup.get(claim_id)
            if incident:
                event_date = incident["incident_date"]

        elif issue_type == "Settlement Exceeds Limit":
            settlement = settlement_id_lookup.get(record_id)

            if settlement:
                claim_id = settlement["claim_id"]
                event_type = "Settlement Exceeds Limit Detected"
                event_date = settlement["settlement_date"]

        elif issue_type == "Claim Paid Twice":
            settlement = settlement_id_lookup.get(record_id)

            if settlement:
                claim_id = settlement["claim_id"]
                event_type = "Duplicate Payment Detected"
                event_date = settlement["settlement_date"]

        if claim_id and event_type:
            anomaly_events.setdefault(claim_id, []).append(
                (event_type, event_date)
            )
    for claim in claims:
        claim_id = claim["claim_id"]

        incident = incident_lookup.get(claim_id)
        assessment = assessment_lookup.get(claim_id)

        if incident is None or assessment is None:
            raise ValueError(
                f"Missing incident or assessment for {claim_id}"
            )

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
        claim_events.extend(
            anomaly_events.get(claim_id, [])
        )
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
