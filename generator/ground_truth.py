def generate_ground_truth(anomaly_records):

    ground_truth = []

    for record in anomaly_records:
        ground_truth.append({
            "record_id": record["record_id"],
            "table_name": record["table_name"],
            "issue_type": record["issue_type"],
            "affected_field": record["affected_field"],
            "original_value": record["original_value"],
            "injected_value": record["injected_value"],
            "expected_outcome": record["expected_outcome"],
            "expected_reason": record["expected_reason"]
        })

    return ground_truth