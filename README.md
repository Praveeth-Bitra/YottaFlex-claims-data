# Insurance Claims Data Generator

This project generates synthetic insurance claims data with Python. It builds customers, policies, claims and the rest of the claim workflow, injects a few known errors on purpose, and checks the result with validation tests. I made it for the YottaFlex AI recruitment project.

# 1. What it does

- Creates 1,200 customers, 2,000 policies and 1,000 claims.
- Covers 5 claim types: Motor, Health, Home, Travel and Theft.
- Builds the full claim workflow for each claim: claim items, incident, documents, adjuster assignment, assessment, reserves, settlement and    claim events.
- Injects 6 known data errors (anomalies) after the clean data is created, and records each one in a ground truth file.
- Validates the data with 15 checks.
- Exports everything to CSV, JSON and SQL.
- Includes a reproducibility test.

# 2. Requirements

- Python 3.11 or newer
- No extra packages. It only uses the Python standard library, so there is nothing to install with pip.

# 3. How to run

Run these from the project root folder.

Generate the data and run the validation checks:

```
python -m generator.main

```
You should see 15 lines ending in PASS, then `CSV, JSON and SQL exports completed.`

Run the reproducibility test:

```
python -m generator.reproducibility

```
This generates the dataset twice and compares a SHA-256 checksum of both runs. It should print `PASS: Dataset is reproducible.`

Optional: try the interactive claim submission and viewing tool:
```
python -m generator.interactive

```

# 4. Output

The files are written to the `output/` folder:

```
output/csv/    one CSV file per table
output/json/   one JSON file per table
output/sql/    one SQL file per table (INSERT statements)

```

There are 15 tables:

customers, policies, coverage, policy_coverages, claims, claim_items, incidents, documents, adjusters, assignments, assessments, reserves, settlements, claim_events, and ground_truth.

The output is overwritten every time you run the generator.

# 5. Project structure

```
generator/
  config.py          seed, counts, reference date
  ids.py             ID creation
  customers.py       customers
  master_data.py     coverage catalog and adjusters
  policies.py        policies
  coverages.py       policy coverages
  claims.py          claims
  claim_items.py     claim items and claim totals
  incidents.py       incidents
  documents.py       documents
  adjusters.py       adjuster assignment
  assessments.py     claim assessment
  reserves.py        reserves
  settlements.py     settlements
  claim_events.py    claim event history
  anomalies.py       injects the known errors
  ground_truth.py    ground truth file
  validation.py      validation checks
  export.py          CSV, JSON and SQL export
  reproducibility.py reproducibility test
  interactive.py     interactive claim tool
  main.py            runs the full workflow
docs/
  business_rules.md  the rules the data follows
  data_dictionary.md fields of every table
  ai_usage.md        how I used AI
  prompt_hist.md  prompts I used
```

# 6. How it works

1. A fixed random seed (20261022) is used, so the same data is created every time. The reference date is 2026-10-22.
2. Data is created in order: customers, policies, claims, claim items, incidents, documents, adjusters, assessments, reserves, settlements and claim events.
3. Business outcomes come from the rules in `docs/business_rules.md`. For example, the assessment decision depends on the policy, the incident and the documents, and is not picked at random.
4. After the clean data is ready, `anomalies.py` changes a few records to create known errors. Each change is written to `ground_truth` with the original value, the injected value and the expected outcome.
5. `validation.py` runs the checks, and `export.py` writes the files.

# 7. Injected anomalies

| Anomaly | Expected outcome |
|---|---|
| Incident before policy start | Rejected |
| Policy cancelled before incident | Rejected |
| Duplicate incident | Duplicate Detected |
| Settlement exceeds coverage limit | Invalid Settlement |
| Missing mandatory document | Pending Information |
| Claim paid twice | Duplicate Payment Detected |

# 8. How I tested it

- `python -m generator.main` runs 15 checks: primary keys, foreign keys, claim item totals, policy dates, and one check for each of the 6 anomalies. All of them pass.
- `python -m generator.reproducibility` confirms two runs give the same checksum.
- I ran the generator again and compared the new CSV, JSON and SQL files with the ones in the repo. They are identical.
- I checked that no table has a `claim_id` that does not exist in `claims`.

# 9. Assumptions

- Currency is USD with 2 decimal places.
- All five claim types use the same workflow.
- Everything is synthetic. No real customer data is used.
- More detail is in `docs/business_rules.md`.

# 10. Limitations

- The ground truth has only 6 anomalies, one of each type. It is enough to show the idea but too small to evaluate a detection model.
- SQL files contain INSERT statements only. There are no CREATE TABLE statements, so the tables must be created first.
- Most settlements are still in Pending payment status, and only a few are Paid.
- The generator uses plain random choices, so the data does not follow real-world statistics.

# 11. How I used AI
See `docs/ai_usage.md` for where AI helped, what I reviewed and what I changed. The prompts are in `docs/prompt_history.md`.