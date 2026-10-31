from datetime import date, timedelta

from generator.config import CUSTOMER_COUNT, REFERENCE_DATE
from generator.ids import next_id


FIRST_NAMES = [
    "James", "John", "Robert", "Michael", "William",
    "David", "Richard", "Joseph", "Thomas", "Daniel",
    "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth",
    "Barbara", "Susan", "Jessica", "Sarah", "Karen"
]

LAST_NAMES = [
    "Smith", "Johnson", "Brown", "Taylor", "Anderson",
    "Thomas", "Jackson", "White", "Harris", "Martin",
    "Thompson", "Garcia", "Martinez", "Robinson", "Clark"
]


def generate_customers(rng, count=CUSTOMER_COUNT):
    """Generate synthetic customer records."""

    customers = []

    for _ in range(count):
        age = rng.randint(18, 80)
        birth_year = REFERENCE_DATE.year - age

        birth_date = date(
            birth_year,
            rng.randint(1, 12),
            rng.randint(1, 28)
        )

        customer = {
            "customer_id": next_id("customer"),
            "first_name": rng.choice(FIRST_NAMES),
            "last_name": rng.choice(LAST_NAMES),
            "date_of_birth": birth_date.isoformat(),
            "email": None,
            "phone": None,
            "country": "USA"
        }

        customer["email"] = (
            f"{customer['first_name'].lower()}."
            f"{customer['last_name'].lower()}."
            f"{customer['customer_id'][-6:]}@example.com"
        )

        customer["phone"] = (
            f"+1-555-{rng.randint(100, 999)}-"
            f"{rng.randint(1000, 9999)}"
        )

        customers.append(customer)

    return customers