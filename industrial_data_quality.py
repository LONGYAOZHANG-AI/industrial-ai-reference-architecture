import csv
import io
from datetime import datetime

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
        except ValueError:
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


if __name__ == "__main__":
    rows, issues = validate_data(SAMPLE_DATA)

    print(f"Records checked: {len(rows)}")
    print(f"Quality issues found: {len(issues)}")

    for row_number, issue in issues:
        print(f"Row {row_number}: {issue}")
