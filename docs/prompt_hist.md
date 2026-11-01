# Tools used:
Google Gemini:
Requirement analysis, initial architecture discussions, data modelling, alternative approaches,
Initial planning, project structure and design ideas.

OpenAI Codex:
Terminal based code generation, debugging, code modifications, and repetitive development tasks.

# Prompts list:
*** Prompt 1 ***
Hey, I am currently working on this project help me understand the requirements, important components and break the work into tasks the dealine is 30 hours?

*** Prompt 2 ***
suggest a project structure nd Identify the entity and relationships, dependencies, and the order in which they need to generate. Keep it simple.

*** Prompt 3 ***
Help me prepare business rules document for this project and specify what needs to be implemented clearly behaviour, relationships, rules, scenarios and output aland also mention what should be avoided and unnecessary architectural changes."

*** Prompt 4 ***
Review the project structure and business_rules file before making changes use that as reference and Implement the project by modules and follow the requirements dont introduce unnecessary features or change the design without asking me

*** Prompt 5 ***
Implement the data generation modules according to entities and relationships also Use ID generation and fixed random seed and ensure that records that derived values are calculated from their source records.

*** Prompt 6 ***
Implement the claims and settlement workflow using the data structures and also validate policy dates, status, coverage limits and documents generate me a claim decisions and recommendations based on the rules.

*** Prompt 7 ***
It is not following the requirements and the logic check the code and compare it with business rules, correct the code without changing working code and make sure everything follow the business rules.

*** Prompt 8 ***
check implementation for the codes ive written and tell me if there are any errors and also check theprimary key, foreign key and date consistency and the anomaly scenarios run and verify

*** Prompt 9 ***
do the export functions for all generated data in CSV ,JSON and SQL formats also maintain the output folder structure and ensure that all datasets are exported

*** Prompt 10 ***
Generate me a interactive file that displays the whole functionality of this project in the terminal only it should ask for plocy id, claimed amount, reason and the required metric for generating a detailed summary for that

*** Prompt 11 ***
the project is completed and once run all files and check if everything runs perfectly fine or any issues arises instead of fixing yourself tell me what went wrong and what is your suggested fix for that issue, if everything is fine just print "Done" message and stop

*** Prompt 12 ***
generate me a readme, ai_usage files about what I have done and add commands about how to run the project and rememeber to run it generator as module bcz there are imports and we used that as modules instead of scripts.