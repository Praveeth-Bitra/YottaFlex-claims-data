# Business Rules

*** 1. Project Overview ***
The project generates synthetic insurance data and simulates an end-to-end claims processing workflow.
1. Customer and policy creation.
2. Claim intake.
3. Policy and coverage validation.
4. Document verification.
5. Adjuster assignment.
6. Claim eligibility assessment.
7. Reserve calculation.
8. Settlement recommendation.
9. Exception identification and audit history.

*** 2. Configuration ***
- Python version: 3.11.
- Random seed: 20261022.
- Use one shared random.Random(seed) instance.
- Use Python standard library only.
- Use lists of dictionaries for records.
- Currency: USD.
- Round monetary calculations to two decimal places.
- Reference date: 2026-10-22.
- Baseline policies: 2,000.
- Baseline claims: 1,000.
- Claim types: Motor, Health, Home, Travel and Theft.

*** 3. ID Conventions ***

Use counters and immutable IDs.

| Entity | ID Format |
|---|---|
| Customer | CUST-000001 |
| Policy | POL-MOTOR-2026-000001 |
| Coverage | COV-000001 |
| PolicyCoverage | PLC-000001 |
| Claim | CLM-2026-000001 |
| ClaimItem | ITM-000001 |
| Document | DOC-CLM-2026-000001-001 |
| Incident | INC-000001 |
| Adjuster | ADJ-000001 |
| Assessment | ASN-CLM-2026-000001-001 |
| Reserve | RES-000001 |
| Settlement | SET-CLM-2026-000001-001 |
| ClaimEvent | EVT-000001 |
Policy product names in IDs are MOTOR, HEALTH, HOME, TRAVEL and THEFT.

*** 4. Customer Generation ***
- Generate 1,200 synthetic customers.
- Each customer receives a unique ID.
- Use fixed lists of first names, last names, cities and states.
- Generate synthetic email addresses using the customer ID.
- Country is always USA.
- Date of birth must represent an age between 18 and 80 on the reference date.

*** 5. Coverage Catalog ***
Create three coverages for each policy type.
| Policy Type | Coverage | Maximum Limit |
|---|---|---:|
| Motor | Collision | 50,000 |
| Motor | Liability | 100,000 |
| Motor | Comprehensive | 40,000 |
| Health | Hospitalization | 200,000 |
| Health | Outpatient | 20,000 |
| Health | Dental | 5,000 |
| Home | Structure | 300,000 |
| Home | Contents | 50,000 |
| Home | Personal Liability | 100,000 |
| Travel | Trip Medical | 50,000 |
| Travel | Trip Cancellation | 10,000 |
| Travel | Baggage Loss | 3,000 |
| Theft | Personal Property | 20,000 |
| Theft | Vehicle Theft | 40,000 |
| Theft | Burglary | 30,000 |

*** 6. Policy Generation ***
Generate 2,000 policies.
Policy type distribution:

| Policy Type | Policies |
|---|---:|
| Motor | 700 |
| Health | 500 |
| Home | 360 |
| Travel | 240 |
| Theft | 200 |
| Total | 2,000 |

Rules:

- Every customer receives at least one policy.
- Remaining policies are distributed among customers.
- Policy effective dates are between 2024-01-01 and 2026-10-22.
- Expiration date is effective date plus 365 days.
- A policy is Active when the reference date falls within its effective period.
- A policy is Expired when its expiration date is before the reference date.
- Cancelled policies have an explicit cancellation date.
- A cancelled policy cannot provide coverage after its cancellation date.

Premium ranges:

| Policy Type | Premium Range |
|---|---:|
| Motor | 400–1,800 |
| Health | 800–3,500 |
| Home | 500–2,500 |
| Travel | 40–400 |
| Theft | 100–600 |

*** 7. Policy Exclusions ***
Use simple, documented exclusions.
| Policy Type | Example Exclusion |
|---|---|
| Motor | Routine maintenance and intentional damage |
| Health | Cosmetic procedures and non-medically necessary treatment |
| Home | Normal wear and tear |
| Travel | Voluntary trip cancellation without a covered reason |
| Theft | Unattended property without reasonable security |

*** 8. Claim Generation ***
Generate 1,000 claims across the five claim types.
Every claim must reference an existing customer and policy.
A policy may have no more than two claims in the clean baseline.
Claim amounts are generated using these ranges:
| Claim Type | Claimed Amount |
|---|---:|
| Motor | 150–8,000 |
| Health | 80–15,000 |
| Home | 200–12,000 |
| Travel | 30–2,500 |
| Theft | 100–6,000 |

*** 9. Incident Validation ***
- Incident date must normally be on or after policy effective date.
- Incident date must be on or before policy expiration date.
- Incident date must be on or before cancellation date for a cancelled policy.
- Reported date must be on or after incident date.

*** 10. Required Documents ***
Use these required document types:
| Claim Type | Required Document |
|---|---|
| Motor | Repair Estimate |
| Health | Medical Bill |
| Home | Photo |
| Travel | Receipt |
| Theft | Police Report |

*** 11. Adjuster Assignment ***
Generate 40 adjusters.
- 6 Motor.
- 6 Health.
- 6 Home.
- 6 Travel.
- 6 Theft.
- 10 General.

*** 12. Claim Assessment Logic ***
Evaluate claims in this order:
1. Check whether the policy exists.
2. Check whether the policy was valid on the incident date.
3. Check whether the policy was cancelled before the incident.
4. Check whether the incident is covered by the policy.
5. Check whether the incident type is excluded.
6. Check whether mandatory documents are available and verified.
7. Compare the claimed amount with the applicable coverage limit.
8. Calculate the recommended approval amount.

Decision outcomes:

| Condition | Outcome |
|---|---|
| Invalid policy or incident outside policy period | Rejected |
| Policy cancelled before incident | Rejected |
| Excluded incident | Rejected |
| Required document missing or unverified | Pending Information |
| Claim amount exceeds applicable coverage limit | Partially Approved |
| All checks pass | Approved |

*** Approval Calculations ***
Approved:
approved_amount = claimed_amount

Partially Approved:
approved_amount = applicable coverage limit

Rejected:
approved_amount = 0

Pending Information:
approved_amount remains blank until assessment is completed.

*** 13. Reserve Calculation ***

Generate two reserve records per claim:

1. Indemnity Reserve.
2. Expense Reserve.

Rules:

- Indemnity reserve initially equals the claimed amount.
- Expense reserve equals 5% of the indemnity reserve.
- Both amounts are rounded to two decimal places.
- After assessment, reserves are updated using the recommended approval amount.
- Rejected claims have zero remaining indemnity reserve.
- Reserve updates must be traceable.

*** 14. Settlement Calculation ***
Rules:

- Payout cannot exceed the applicable coverage limit.
- Rejected claims receive no settlement recommendation.
- Pending Information claims receive no settlement recommendation.
- Settlement payment status is recorded separately from recommendation.
- A claim can have at most one successful payment in the clean baseline.

Payment methods:

| Payout Amount | Method |
|---|---|
| Below 1,000 | Check |
| 1,000–9,999.99 | ACH |
| 10,000 and above | Wire Transfer |

*** 15. Claim Lifecycle and Events ***
Event types:

- Claim Submitted.
- Policy Validated.
- Documents Requested.
- Adjuster Assigned.
- Assessment Completed.
- Claim Approved.
- Claim Partially Approved.
- Claim Rejected.
- Settlement Recommended.
- Settlement Paid.
- Claim Closed.

*** 16. Required Negative Scenarios ***

Generate valid baseline records first.
Then inject six labelled negative scenarios:
| Scenario | Expected Detection |
|---|---|
| Claim date before policy start | Invalid incident date |
| Policy cancelled before incident | Cancelled policy exception |
| Duplicate incident | Duplicate incident exception |
| Settlement exceeds policy limit | Settlement limit violation |
| Missing mandatory document | Missing document exception |
| Claim paid twice | Duplicate payment exception |

*** 17. Ground Truth ***
Generate separate ground_truth.csv and ground_truth.json.
Each record should include:

- Record ID.
- Table name.
- Issue type.
- Affected field.
- Original value, where applicable.
- Injected value, where applicable.
- Expected outcome.
- Expected reason.

*** 18. Validation ***
Implement checks for:

1. Primary key uniqueness.
2. Foreign key integrity.
3. Required fields.
4. Allowed values.
5. Date consistency.
6. Policy and coverage compatibility.
7. Claim and policy relationships.
8. Claim amount reconciliation.
9. Approval amount limits.
10. Reserve calculations.
11. Settlement calculations.
12. Event ordering.
13. Duplicate incidents.
14. Duplicate payments.
15. Ground-truth consistency.

*** 19. Reproducibility ***
- Use seed 20261022.
- Use one shared random generator.
- Generate records in a consistent order.
- Export rows in deterministic ID order.
- Generate SHA-256 checksums.
- Running twice with the same configuration must produce identical output files.

*** 20. Export Requirements ***
Generate:

- CSV files for each entity.
- JSON files for each entity.
- SQL CREATE TABLE and INSERT statements.
- Separate ground_truth CSV and JSON.
- Validation summary.
- Reproducibility checksum report.

*** 21. Implementation Principles ***
- Use simple Python functions.
- Use lists and dictionaries.
- Avoid classes and unnecessary frameworks.
- Use Python standard library only.
- Keep functions small and understandable.
- Add a one-line comment above each function.
- Do not randomly assign calculated outcomes.
- Document assumptions and decision reasons.
- Keep the solution easy to explain.