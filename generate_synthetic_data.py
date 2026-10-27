
import csv
import random
from datetime import datetime, timedelta


def generate_data(n=1000, output="synthetic_industrial_data.csv", seed=42):
    rng = random.Random(seed)
    start = datetime(2026, 1, 1, 8, 0)
    devices = [f"M{i:03d}" for i in range(1, 6)]

    records = []

    for i in range(n):
        device = rng.choice(devices)
        timestamp = start + timedelta(minutes=i)

        temp = round(rng.gauss(80, 10), 2)
        pressure = round(rng.gauss(4.5, 0.8), 2)

        # Add a few known data quality problems
        if rng.random() < 0.03:
            temp = ""
        elif rng.random() < 0.02:
            temp = 150.0

        ts = timestamp.isoformat()
        if rng.random() < 0.01:
            ts = "invalid-date"

        records.append({
            "device_id": device,
            "timestamp": ts,
            "temperature_c": temp,
            "pressure_bar": pressure
        })

    # Duplicate a few rows to test deduplication
    records.extend(row.copy() for row in records[:min(10, n)])

    columns = [
        "device_id",
        "timestamp",
        "temperature_c",
        "pressure_bar"
    ]

    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(records)

    print(f"Wrote {len(records)} rows to {output}")


if __name__ == "__main__":
    generate_data()
