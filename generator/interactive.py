
from datetime import date

from generator.main import generate_dataset
from generator.ids import (
    generate_claim_id,
    generate_assessment_id,
    generate_document_id,
    next_id,
)
from generator.incidents import INCIDENT_TYPES
from generator.documents import REQUIRED_DOCUMENTS
from generator.assessments import assess_claims
from generator.settlements import generate_settlements


def get_user_input(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty.")


def get_positive_amount():
    while True:
        try:
            amount = float(input("Enter claimed amount: "))

            if amount > 0:
                return round(amount, 2)

            print("Amount must be greater than zero.")

        except ValueError:
            print("Please enter a valid number.")


def get_incident_date():
    while True:
        value = input("Enter incident date (YYYY-MM-DD): ").strip()

        try:
            incident_date = date.fromisoformat(value)

            if incident_date > date.today():
                print("Incident date cannot be in the future.")
                continue

            return incident_date.isoformat()

        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")


def select_incident_type(claim_type):
    options = INCIDENT_TYPES[claim_type]

    print("\nSelect incident type:")

    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")

    while True:
        try:
            choice = int(input("Enter choice: "))

            if 1 <= choice <= len(options):
                return options[choice - 1]

            print("Select a valid option.")

        except ValueError:
            print("Enter a number.")


def ask_yes_no(prompt):
    while True:
        answer = input(prompt).strip().upper()

        if answer in ("Y", "N"):
            return answer == "Y"

        print("Please enter Y or N.")


def submit_claim(data):

    print("\n========== NEW CLAIM ==========")

    policy_id = get_user_input("Enter policy ID: ")

    policy = next(
        (
            item for item in data["policies"]
            if item["policy_id"] == policy_id
        ),
        None
    )

    if policy is None:
        print("\nPolicy not found.")
        return

    claim_type = policy["product_type"]

    print("Customer ID:", policy["customer_id"])
    print("Policy type:", claim_type)
    print("Policy status:", policy["status"])

    incident_date = get_incident_date()

    incident_type = select_incident_type(claim_type)

    claimed_amount = get_positive_amount()

    required_document = REQUIRED_DOCUMENTS[claim_type]

    print("\nMandatory document:", required_document)

    document_available = ask_yes_no(
        "Is this document available? (Y/N): "
    )

    document_verified = False

    if document_available:
        document_verified = ask_yes_no(
            "Has this document been verified? (Y/N).lower(): "
        )

    claim = {
        "claim_id": generate_claim_id(),
        "policy_id": policy_id,
        "customer_id": policy["customer_id"],
        "claim_type": claim_type,
        "claimed_amount": claimed_amount,
        "submitted_date": date.today().isoformat(),
        "status": "Submitted",
    }

    incident = {
        "incident_id": next_id("incident"),
        "claim_id": claim["claim_id"],
        "incident_type": incident_type,
        "incident_date": incident_date,
        "reported_date": date.today().isoformat(),
        "location": "User Submitted",
    }

    claim_documents = []

    if document_available:
        document = {
            "document_id": generate_document_id(claim["claim_id"]),
            "claim_id": claim["claim_id"],
            "document_type": required_document,
            "is_mandatory": True,
            "status": (
                "Verified"
                if document_verified
                else "Pending Verification"
            ),
        }

        claim_documents.append(document)

    assessment = assess_claims(
        [claim],
        [policy],
        [incident],
        claim_documents,
        data["policy_coverages"],
    )[0]
    settlements = generate_settlements(
        [claim],
        [assessment],
        [policy],
        data["policy_coverages"],
    )

    print("\n========== CLAIM RESULT ==========")

    print("Claim ID:", claim["claim_id"])
    print("Policy ID:", policy_id)
    print("Claim amount: ₹", claimed_amount)

    print("\nAssessment:", assessment["decision"])
    print("Reason:", assessment["reason"])

    if assessment["approved_amount"] is not None:
        print(
            "Approved amount: ₹",
            assessment["approved_amount"]
        )

    if settlements:
        settlement = settlements[0]

        print("\nSettlement ID:", settlement["settlement_id"])
        print("Deductible: ₹", settlement["deductible_amount"])
        print("Recommended payout: ₹", settlement["payout_amount"])
        print("Payment status:", settlement["payment_status"])

    else:
        print("\nNo settlement generated for this claim.")
    data["claims"].append(claim)
    data["incidents"].append(incident)
    data["documents"].extend(claim_documents)
    data["assessments"].append(assessment)
    data["settlements"].extend(settlements)


def view_claim(data):
    """Find and display an existing claim."""

    claim_id = get_user_input("\nEnter claim ID: ")

    claim = next(
        (
            item for item in data["claims"]
            if item["claim_id"] == claim_id
        ),
        None
    )

    if claim is None:
        print("Claim not found.")
        return

    print("\n========== CLAIM DETAILS ==========")

    for key, value in claim.items():
        print(f"{key}: {value}")

    assessment = next(
        (
            item for item in data["assessments"]
            if item["claim_id"] == claim_id
        ),
        None
    )

    if assessment:
        print("\nAssessment:", assessment["decision"])
        print("Reason:", assessment["reason"])


def main():
    """Start the interactive application."""

    print("Generating insurance dataset...")

    data = generate_dataset()

    print("Dataset loaded successfully.")

    while True:

        print("\n===================================")
        print("      INSURANCE CLAIMS SYSTEM")
        print("===================================")
        print("1. Submit a new insurance claim")
        print("2. View existing claim")
        print("3. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            submit_claim(data)

        elif choice == "2":
            view_claim(data)

        elif choice == "3":
            print("\nThank you for using this Project.")
            break

        else:
            print("Invalid choice. Please select 1, 2 or 3.")


if __name__ == "__main__":
    main()
