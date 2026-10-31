
from generator.config import create_random_generator
from generator.ids import reset_id_counters
from generator.customers import generate_customers
from generator.master_data import generate_coverage_catalog, generate_adjusters
from generator.policies import generate_policies
from generator.coverages import generate_policy_coverages
from generator.claims import generate_claims
from generator.claim_items import generate_claim_items, calculate_claim_totals
from generator.incidents import generate_incidents
from generator.documents import generate_documents
from generator.adjusters import assign_adjusters
from generator.assessments import assess_claims
from generator.reserves import generate_reserves
from generator.settlements import generate_settlements
from generator.claim_events import generate_claim_events
from generator.anomalies import inject_anomalies
from generator.ground_truth import generate_ground_truth
from generator.validation import run_validation
from generator.export import export_all


def generate_dataset():
    """Run the full data generation workflow."""

    rng = create_random_generator()
    reset_id_counters()

    # 1. Customers and master data
    customers = generate_customers(rng)
    coverage_catalog = generate_coverage_catalog()
    adjusters = generate_adjusters(rng)

    # 2. Policies and policy coverages
    policies = generate_policies(customers, rng)
    policy_coverages = generate_policy_coverages(
        policies, coverage_catalog, rng
    )

    # 3. Claims and claim items
    claims = generate_claims(policies, rng)
    claim_items = generate_claim_items(claims, rng)
    claims = calculate_claim_totals(claims, claim_items)

    # 4. Incidents
    incidents = generate_incidents(claims, policies, rng)

    # 5. Documents
    documents = generate_documents(claims, rng)

    # 6. Assign adjusters
    assignments = assign_adjusters(claims, adjusters, rng)

    # 7. Assessments, reserves and settlements
    assessments = assess_claims(
        claims, policies, incidents, documents, policy_coverages
    )

    reserves = generate_reserves(claims, assessments)

    settlements = generate_settlements(
        claims, assessments, policies, policy_coverages
    )

    # 8. Claim events
    events = generate_claim_events(
        claims, incidents, assignments, assessments, settlements
    )

    # 9. Inject anomalies AFTER baseline generation
    anomaly_records = inject_anomalies(
        claims, policies, incidents, documents, settlements, policy_coverages
    )

    # 10. Ground truth
    ground_truth = generate_ground_truth(anomaly_records)

    # 11. Collect final dataset
    data = {
        "customers": customers,
        "policies": policies,
        "coverage": coverage_catalog,
        "policy_coverages": policy_coverages,
        "claims": claims,
        "claim_items": claim_items,
        "incidents": incidents,
        "documents": documents,
        "adjusters": adjusters,
        "assignments": assignments,
        "assessments": assessments,
        "reserves": reserves,
        "settlements": settlements,
        "claim_events": events,
        "ground_truth": ground_truth
    }

    return data


if __name__ == "__main__":
    dataset = generate_dataset()

    results = run_validation(dataset)

    for check, passed in results.items():
        if passed:
            print(check, "PASS")
        else:
            print(check, "FAIL")

    export_all(dataset)
