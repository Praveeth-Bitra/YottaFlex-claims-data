
# Store counters for each entity type.
_id_counters = {}


def reset_id_counters():
    """Reset all ID counters."""
    global _id_counters
    _id_counters = {}


def next_id(entity_name):
    """Generate a unique six-digit ID."""

    prefixes = {
        "customer": "CUST",
        "coverage": "COV",
        "policy_coverage": "PLC",
        "claim_item": "ITM",
        "incident": "INC",
        "adjuster": "ADJ",
        "reserve": "RES",
        "claim_event": "EVT",
    }

    if entity_name not in prefixes:
        raise ValueError(f"Unknown entity: {entity_name}")

    _id_counters[entity_name] = (
        _id_counters.get(entity_name, 0) + 1
    )

    return f"{prefixes[entity_name]}-{_id_counters[entity_name]:06d}"


def generate_policy_id(product_type):
    _id_counters["policy"] = _id_counters.get("policy", 0) + 1
    return f"POL-{product_type}-2026-{_id_counters['policy']:06d}"


def generate_claim_id():
    _id_counters["claim"] = _id_counters.get("claim", 0) + 1
    return f"CLM-2026-{_id_counters['claim']:06d}"


def _linked_id(entity, prefix, claim_id):
    key = f"{entity}_{claim_id}"
    _id_counters[key] = _id_counters.get(key, 0) + 1
    return f"{prefix}-{claim_id}-{_id_counters[key]:03d}"


def generate_document_id(claim_id):
    return _linked_id("document", "DOC", claim_id)


def generate_assessment_id(claim_id):
    return _linked_id("assessment", "ASN", claim_id)


def generate_settlement_id(claim_id):
    return _linked_id("settlement", "SET", claim_id)
