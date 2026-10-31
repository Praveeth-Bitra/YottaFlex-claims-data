import csv
import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSV_DIR = os.path.join(BASE_DIR, "output", "csv")
JSON_DIR = os.path.join(BASE_DIR, "output", "json")
SQL_DIR = os.path.join(BASE_DIR, "output", "sql")


def create_output_directories():
    """Create output folders if they do not exist."""

    os.makedirs(CSV_DIR, exist_ok=True)
    os.makedirs(JSON_DIR, exist_ok=True)
    os.makedirs(SQL_DIR, exist_ok=True)


def export_to_csv(table_name, records):
    """Export a list of dictionaries to a CSV file."""

    if not records:
        return

    file_path = os.path.join(CSV_DIR, f"{table_name}.csv")

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=records[0].keys()
        )

        writer.writeheader()
        writer.writerows(records)


def export_to_json(table_name, records):
    """Export records to a JSON file."""

    file_path = os.path.join(JSON_DIR, f"{table_name}.json")

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4)


def export_to_sql(table_name, records):
    """Export records as simple SQL INSERT statements."""

    if not records:
        return

    file_path = os.path.join(SQL_DIR, f"{table_name}.sql")

    columns = list(records[0].keys())

    with open(file_path, "w", encoding="utf-8") as file:
        for record in records:
            column_names = ", ".join(columns)

            values = []

            for value in record.values():
                if value is None:
                    values.append("NULL")

                elif isinstance(value, bool):
                    values.append("TRUE" if value else "FALSE")

                elif isinstance(value, (int, float)):
                    values.append(str(value))

                else:
                    escaped_value = str(value).replace("'", "''")
                    values.append(f"'{escaped_value}'")

            value_string = ", ".join(values)

            statement = (
                f"INSERT INTO {table_name} "
                f"({column_names}) VALUES ({value_string});\n"
            )

            file.write(statement)


def export_all(data):
    """Export all generated tables into CSV, JSON and SQL."""

    create_output_directories()

    for table_name, records in data.items():
        export_to_csv(table_name, records)
        export_to_json(table_name, records)
        export_to_sql(table_name, records)

    print("CSV, JSON and SQL exports completed.")