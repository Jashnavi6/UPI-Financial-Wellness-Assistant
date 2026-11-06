import os
import sys

# Ensure root and src directories are in sys.path
_current = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(_current) if os.path.basename(_current) == "scripts" else _current
_src = os.path.join(_root, "src")
for _p in (_root, _src):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import pandas as pd

print("=" * 60)
print("STEP 3 - TEST DATASET GENERATION")
print("=" * 60)

data = {
    "transaction_id": ["TX001", "TX002", "TX003", "TX004", "TX005"],
    "date": [
        "2026-01-01",
        "2026-01-02",
        "2026-01-03",
        "2026-01-04",
        "2026-01-05"
    ],
    "amount": [250, 1200, 500, 3000, 150],
    "category": [
        "Food",
        "Shopping",
        "Travel",
        "Bills",
        "Food"
    ]
}

df = pd.DataFrame(data)

print("\nDataset created!")

print("\nFull dataset:")
print(df)

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

import os

# Create the folder if it doesn't exist
os.makedirs(os.path.join(_root, "data", "raw"), exist_ok=True)

# Save the dataset
df.to_csv(
    os.path.join(_root, "data", "raw", "test_transactions.csv"),
    index=False
)

print("\nCSV file saved successfully!")
print("Location: C:/Users/jashn/data/raw/test_transactions.csv")

print("\nSTEP 3 COMPLETED!")