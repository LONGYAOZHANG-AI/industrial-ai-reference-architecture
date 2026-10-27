
import csv
import io
from datetime import datetime
from pathlib import Path


SAMPLE_DATA = """device_id,timestamp,temperature_c,pressure_bar
M001,2026-01-01T08:00:00,75.5,4.2
M001,2026-01-01T09:00:00,78.0,4.3
M002,2026-01-01T08:00:00,,4.1
M003,2026-01-01T08:00:00,150.0,4.5
M001,2026-01-01T08:00:00,75.5,4.2
M004,invalid-date,80.0,4.0
"""


def validate_data(csv_text):
    rows = list(csv.DictReader(io.StringIO(csv_text)))
    issues = []
    seen = set()

    for row_number, row in enumerate(rows, start=2):
        device_id = row["device_id"]
        timestamp = row["timestamp"]
        key = (device_id, timestamp)

        if not device_id or not timestamp:
            issues.append((row_number, "Missing device ID or timestamp"))

        if key in seen:
            issues.append((row_number, "Duplicate device/timestamp"))
        seen.add(key)

        try:
            datetime.fromisoformat(timestamp)
        except (ValueError, TypeError):
            issues.append((row_number, "Invalid timestamp"))

        try:
            temperature = float(row["temperature_c"])
            if not 0 <= temperature <= 120:
                issues.append((row_number, "Temperature outside example limits"))
        except (ValueError, TypeError):
            issues.append((row_number, "Missing or invalid temperature"))

        try:
            pressure = float(row["pressure_bar"])
            if not 0 <= pressure <= 10:
                issues.append((row_number, "Pressure outside example limits"))
        except (ValueError, TypeError):
            issues.append((row_number, "Missing or invalid pressure"))

    return rows, issues


def validate_file(file_path):
    with open(file_path, encoding="utf-8", newline="") as f:
        return validate_data(f.read())


def print_report(rows, issues):
    affected_rows = {row_number for row_number, _ in issues}
    valid_rows = len(rows) - len(affected_rows)
    quality_score = 100 * valid_rows / len(rows) if rows else 0

    print(f"Records checked: {len(rows)}")
    print(f"Valid records: {valid_rows}")
    print(f"Quality issues found: {len(issues)}")
    print(f"Quality score: {quality_score:.2f}%")

    for row_number, issue in issues:
        print(f"Row {row_number}: {issue}")


if __name__ == "__main__":
    data_file = Path("synthetic_industrial_data.csv")

    if data_file.exists():
        rows, issues = validate_file(data_file)
    else:
        print("CSV file not found. Using sample data.")
        rows, issues = validate_data(SAMPLE_DATA)

    print_report(rows, issues)
