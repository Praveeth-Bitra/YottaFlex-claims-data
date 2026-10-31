import hashlib
import json

from generator.main import generate_dataset


def calculate_checksum(data):
    """Calculate a checksum for the generated dataset."""

    serialized_data = json.dumps(
        data,
        sort_keys=True,
        default=str
    )

    return hashlib.sha256(
        serialized_data.encode("utf-8")
    ).hexdigest()


def check_reproducibility():
    """Generate the dataset twice and compare the checksums."""

    print("Running reproducibility test...")

    first_dataset = generate_dataset()
    first_checksum = calculate_checksum(first_dataset)

    second_dataset = generate_dataset()
    second_checksum = calculate_checksum(second_dataset)

    print("\nFirst checksum: ", first_checksum)
    print("Second checksum:", second_checksum)

    if first_checksum == second_checksum:
        print("\nPASS: Dataset is reproducible.")
        return True

    print("\nFAIL: Dataset differs between runs.")
    return False


if __name__ == "__main__":
    check_reproducibility()