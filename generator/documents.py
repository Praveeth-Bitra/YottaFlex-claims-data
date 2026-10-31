from generator.ids import generate_document_id


# Every claim type has one mandatory document.
REQUIRED_DOCUMENTS = {
    "MOTOR": "Repair Estimate",
    "HEALTH": "Medical Bill",
    "HOME": "Property Damage Photo",
    "TRAVEL": "Travel Receipt",
    "THEFT": "Police Report"
}


def generate_documents(claims, rng):
    """Generate document metadata for every claim."""

    documents = []

    for claim in claims:
        claim_type = claim["claim_type"]
        required_document = REQUIRED_DOCUMENTS[claim_type]

        # Some claims will have incomplete evidence.
        include_required = rng.random() >= 0.10

        if include_required:
            document_names = [required_document]
        else:
            document_names = []

        # Add zero or more optional documents.
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