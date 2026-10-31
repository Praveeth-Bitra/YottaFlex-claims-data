from generator.ids import generate_document_id


REQUIRED_DOCUMENTS = {
    "MOTOR": "Repair Estimate",
    "HEALTH": "Medical Bill",
    "HOME": "Property Damage Photo",
    "TRAVEL": "Travel Receipt",
    "THEFT": "Police Report"
}


def generate_documents(claims, rng):

    documents = []

    for claim in claims:
        claim_type = claim["claim_type"]
        required_document = REQUIRED_DOCUMENTS[claim_type]

        include_required = rng.random() >= 0.10

        if include_required:
            document_names = [required_document]
        else:
            document_names = []

        optional_documents = [
            "Identity Proof",
            "Incident Report",
            "Supporting Photograph",
            "Additional Invoice"
        ]

        for document in optional_documents:
            if rng.random() < 0.30:
                document_names.append(document)

        for document_name in document_names:
            document = {
                "document_id": generate_document_id(claim["claim_id"]),
                "claim_id": claim["claim_id"],
                "document_type": document_name,
                "is_mandatory": document_name == required_document,
                "status": rng.choice(["Received", "Verified", "Pending Verification"])
            }

            documents.append(document)

    return documents