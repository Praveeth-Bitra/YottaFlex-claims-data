# 1. Data Dictionary

This data dictionary explains how the synthetic insurance claims dataset is organised. It covers the fields used in each table, their data types, which ones are required, and how the tables are connected. It also includes the allowed values and the checks each field needs to pass.
Reference date: 2026-10-22  
Currency: USD  
Date format: YYYY-MM-DD  
Datetime format: YYYY-MM-DDTHH:MM:SS

# 2. Customer

*Purpose:* This table contains the basic details for each customer.
*Primary Key:* customer_id

| Field | Type | Required | Unique | Validation |

|---|---|---|---|---|

| customer_id | String | Yes | Yes | Customer ID format |

| first_name | String | Yes | No | Non-empty |

| last_name | String | Yes | No | Non-empty |

| date_of_birth | Date | Yes | No | Valid date |

| gender | String | No | No | Male, Female, Other, Unknown |

| email | String | Yes | Yes | Valid synthetic email |

| phone_number | String | No | No | Digits and separators |

| address_line1 | String | Yes | No | Non-empty |

| address_line2 | String | No | No | Optional address |

| city | String | Yes | No | Non-empty |

| state | String | Yes | No | Valid state code |

| postal_code | String | Yes | No | Five digits |

| country | String | Yes | No | USA |

| created_at | Datetime | Yes | No | Valid creation date |

# 3. Policy

*Purpose:* This table holds the insurance policies linked to customers.
*Primary Key:* policy_id  
*Foreign Key:* customer_id references Customer.

| Field | Type | Required | Unique | Validation |

|---|---|---|---|---|

| policy_id | String | Yes | Yes | Policy ID format |

| customer_id | String | Yes | No | Existing customer |

| policy_type | String | Yes | No | Motor, Health, Home, Travel, Theft |

| status | String | Yes | No | Active, Expired, Cancelled |

| effective_date | Date | Yes | No | Valid policy start |

| expiration_date | Date | Yes | No | Valid policy expiry |

| premium_amount | Decimal | Yes | No | Non-negative |

| deductible_amount | Decimal | Yes | No | Non-negative |

| created_at | Datetime | Yes | No | Valid creation timestamp |

# 4. Coverage

*Purpose:* This table lists the different types of coverage and the limits that apply to them.
*Primary Key:* coverage_id

| Field | Type | Required | Unique | Validation |

|---|---|---|---|---|

| coverage_id | String | Yes | Yes | Coverage ID format |

| policy_type | String | Yes | No | Supported policy type |

| coverage_code | String | Yes | Yes | Unique coverage code |

| coverage_name | String | Yes | No | Non-empty |

| max_limit | Decimal | Yes | No | Greater than zero |

| deductible_amount | Decimal | No | No | Non-negative |

| exclusions | String | No | No | Documented exclusion details |

# 5. PolicyCoverage

*Purpose:* This table shows which coverages are included in each policy.
*Primary Key:* policy_coverage_id
*Foreign Keys:* policy_id references Policy; coverage_id references Coverage.

| Field | Type | Required | Unique | Validation |

|---|---|---|---|---|

| policy_coverage_id | String | Yes | Yes | Unique ID |

| policy_id | String | Yes | No | Existing policy |

| coverage_id | String | Yes | No | Existing coverage |

| limit_amount | Decimal | Yes | No | Must not exceed coverage limit |

| deductible_amount | Decimal | Yes | No | Non-negative |

The combination of policy_id and coverage_id must be unique.

## 6. Claim

*Purpose:* This table contains the claims submitted by customers.
*Primary Key:* claim_id
*Foreign Keys:* customer_id references Customer; policy_id references Policy.

| Field | Type | Required | Unique | Validation |

|---|---|---|---|---|

| claim_id | String | Yes | Yes | Claim ID format |

| customer_id | String | Yes | No | Existing customer |

| policy_id | String | Yes | No | Existing policy |

| claim_type | String | Yes | No | Supported claim type |

| incident_id | String | Yes | No | Valid incident |

| incident_date | Date | Yes | No | Valid incident date |

| reported_date | Date | Yes | No | Valid reporting date |

| claim_amount | Decimal | Yes | No | Greater than zero |

| approved_amount | Decimal | No | No | Between zero and claim amount |

| status | String | Yes | No | Valid lifecycle status |

| decision_reason | String | No | No | Explanation of decision |

| created_at | Datetime | Yes | No | Submission timestamp |

# 7. ClaimItem

*Purpose:* This table breaks each claim down into its individual expenses or losses.
*Primary Key:* claim_item_id
*Foreign Key:* claim_id references Claim.

| Field | Type | Required | Unique | Validation |

|---|---|---|---|---|

| claim_item_id | String | Yes | Yes | Unique ID |

| claim_id | String | Yes | No | Existing claim |

| item_category | String | Yes | No | Valid category |

| description | String | Yes | No | Non-empty |

| claimed_amount | Decimal | Yes | No | Greater than zero |

| approved_amount | Decimal | No | No | Between zero and claimed amount |

 The total amount for a claim should come from the claim items linked to it.

# 8. Document

*Purpose:* This table keeps track of the documents submitted for a claim, along with their verification status.
*Primary Key:* document_id
*Foreign Key:* claim_id references Claim.

| Field | Type | Required | Unique | Validation |

|---|---|---|---|---|

| document_id | String | Yes | Yes | Document ID format |

| claim_id | String | Yes | No | Existing claim |

| document_type | String | Yes | No | Allowed document type |

| file_name | String | Yes | No | Non-empty |

| file_size | Integer | No | No | Non-negative bytes |

| uploaded_at | Datetime | Yes | No | Valid timestamp |

| verification_status | String | Yes | No | Pending, Verified, Rejected |

| verification_reason | String | No | No | Explanation if applicable |

# 9. Incident

*Purpose:* This table records the incident that led to a claim being raised.
*Primary Key:* incident_id
*Foreign Key:* claim_id references Claim.

| Field | Type | Required | Unique | Validation |

|---|---|---|---|---|

| incident_id | String | Yes | Yes | Unique ID |

| claim_id | String | Yes | No | Existing claim |

| incident_type | String | Yes | No | Valid incident category |

| incident_date | Date | Yes | No | Valid date |

| location | String | Yes | No | Non-empty |

| description | String | Yes | No | Non-empty |

# 10. Adjuster

*Purpose:* This table contains details about the adjusters who handle insurance claims.
*Primary Key:* adjuster_id

| Field | Type | Required | Unique | Validation |

|---|---|---|---|---|

| adjuster_id | String | Yes | Yes | Unique ID |

| first_name | String | Yes | No | Non-empty |

| last_name | String | Yes | No | Non-empty |

| email | String | Yes | Yes | Unique email |

| specialization | String | Yes | No | Supported claim type or General |

| is_active | Boolean | Yes | No | True or False |

# 11. Assessment

*Purpose:* This table records the assessment of a claim, including the adjuster's recommendation.
*Primary Key:* assessment_id
*Foreign Keys:* claim_id references Claim; adjuster_id references Adjuster.

| Field | Type | Required | Unique | Validation |

|---|---|---|---|---|

| assessment_id | String | Yes | Yes | Unique ID |

| claim_id | String | Yes | No | Existing claim |

| adjuster_id | String | Yes | No | Existing adjuster |

| recommendation | String | Yes | No | Approved, Partial, Rejected, Pending Information |

| recommended_amount | Decimal | Yes | No | Non-negative |

| decision_reason | String | Yes | No | Explanation |

| assessed_at | Datetime | Yes | No | Valid timestamp |

# 12. Reserve

*Purpose:* This table keeps track of the estimated reserve amounts set aside for claims.
*Primary Key:* reserve_id
*Foreign Key:* claim_id references Claim.

| Field | Type | Required | Unique | Validation |

|---|---|---|---|---|

| reserve_id | String | Yes | Yes | Unique ID |

| claim_id | String | Yes | No | Existing claim |

| reserve_type | String | Yes | No | Indemnity or Expense |

| reserve_amount | Decimal | Yes | No | Non-negative |

| updated_at | Datetime | Yes | No | Valid timestamp |

# 13. Settlement

*Purpose:* This table records the settlement details and tracks the related payment information.
*Primary Key:* settlement_id
*Foreign Key:* claim_id references Claim.

| Field | Type | Required | Unique | Validation |

|---|---|---|---|---|

| settlement_id | String | Yes | Yes | Unique ID |

| claim_id | String | Yes | No | Existing claim |

| approved_amount | Decimal | Yes | No | Non-negative |

| deductible_amount | Decimal | Yes | No | Non-negative |

| payout_amount | Decimal | Yes | No | Non-negative and within applicable limits |

| payment_status | String | Yes | No | Recommended, Pending, Paid, Failed |

| payment_method | String | No | No | Valid payment method |

| disbursed_date | Date | No | No | Required when paid |

# 14. ClaimEvent

*Purpose:* This table keeps a record of the different activities and updates that happen while a claim is being processed.
*Primary Key:* event_id
*Foreign Key:* claim_id references Claim.

| Field | Type | Required | Unique | Validation |

|---|---|---|---|---|

| event_id | String | Yes | Yes | Unique ID |

| claim_id | String | Yes | No | Existing claim |

| event_type | String | Yes | No | Valid event |

| event_timestamp | Datetime | Yes | No | Valid chronological order |

| actor | String | Yes | No | Customer, Adjuster or System |

| description | String | Yes | No | Event explanation |

# 15. Ground Truth

Ground-truth information is kept separately. It is used to record the issues that were intentionally added to the dataset, so it is not treated as one of the normal business tables.

| Field | Type | Required | Validation |

|---|---|---|---|

| record_id | String | Yes | Affected record ID |

| table_name | String | Yes | Affected table |

| issue_type | String | Yes | Known issue category |

| field_name | String | No | Affected field |

| original_value | String | No | Original value |

| injected_value | String | No | Injected value |

| expected_outcome | String | No | Expected processing outcome |

| expected_reason | String | No | Explanation |

# 16. Relationships and Cardinality

| Parent | Child | Relationship |

|---|---|---|

| Customer | Policy | One-to-Many |

| Policy | PolicyCoverage | One-to-Many |

| Coverage | PolicyCoverage | One-to-Many |

| Policy | Claim | One-to-Many |

| Claim | ClaimItem | One-to-Many |

| Claim | Document | One-to-Many |

| Claim | Incident | One-to-One |

| Claim | Assessment | One-to-One or Optional |

| Adjuster | Assessment | One-to-Many |

| Claim | Reserve | One-to-Many |

| Claim | Settlement | One-to-One or Optional |

| Claim | ClaimEvent | One-to-Many |

Every foreign key in the clean baseline dataset must point to a parent record that actually exists.

# 17. ID Conventions

Use the ID formats given in the assignment:
- Policy: POL-<product>-2026-000001
- Claim: CLM-2026-000001
- Document: DOC-<claim-id>-001
- Assessment: ASN-<claim-id>-001
- Settlement: SET-<claim-id>-001

Each of the other entities should also have its own documented prefix and a unique, zero-padded number.

Once an ID is assigned, it should not change. The same ID must be used consistently across all files.

# 18. Validation Summary

The generated dataset needs to pass the following checks:
- Primary key uniqueness.
- Foreign key integrity.
- Required fields.
- Valid data types.
- Allowed values.
- Date consistency.
- Claim amount reconciliation.
- Coverage and settlement limits.
- Lifecycle event order.
- Duplicate detection.
- Ground-truth consistency.

The final validation report should make it clear which records are valid baseline data and which ones contain intentionally added issues.