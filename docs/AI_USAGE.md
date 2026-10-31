# AI Usage
The challenge allows LLM tools, so this file explains where I used AI and how I controlled it. My prompts are in `docs/prompt_hist.md`.

# 1. Tools I used
- Gemini for planning, drafting documents and talking through decisions.
- Claude for writing code.

# 2. How I worked with AI
I did not ask AI to "build the project". I made the plan first and gave AI one small task at a time.
1. I decided what the system should do: the 5 claim types, the tables, the claim workflow, the anomalies to inject and the output formats.
2. I wrote the business rules in `docs/business_rules.md` first, and edited them until they matched what I wanted. The code had to follow these rules.
3. I split the work into numbered tasks (business rules, data dictionary, ids and config, master tables, policies, claims and items, assessments and settlements, anomalies, validation, export, documentation) and gave AI one task per prompt.
4. After each task I read the changes myself. I did not commit anything I had not reviewed.
5. I ran the code. I only kept a change if it ran and the validation checks passed. If something failed or looked wrong, I fixed it or asked for a correction, and ran it again.

# 3. What I decided and wrote myself
- The problem setup, assumptions and business rules.
- The decision to use only the Python standard library with plain lists of dictionaries.
- The validation checks and the reproducibility test, which decide whether the output is accepted.
- Fixes to the data dictionary, where field names were corrupted, done by hand.

# 4. Where AI saved me time
- The code that generates random data (customers, policies, claim items, documents and so on). This is repetitive, and I gave it clear rules to follow.
- First drafts of the data dictionary and some documentation.
- The README and this file, written to meet the deadline. I checked both against the actual code and output.

# 5. What I checked
- I read the generated code and made sure I could explain it.
- I ran `python -m generator.main` and checked that all 15 validation checks pass.
- I ran `python -m generator.reproducibility` and checked that two runs give the same checksum.
- I compared the data dictionary with the business rules and the real CSV headers.
- I checked that the output files have no broken `claim_id` references.