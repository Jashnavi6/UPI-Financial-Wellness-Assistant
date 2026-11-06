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

from sklearn.ensemble import IsolationForest

print("=" * 70)
print("PHASE 3 - STEP 11: UNUSUAL SPENDING DETECTION")
print("=" * 70)


# ---------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------

print("\n1. Loading feature-engineered dataset...")

df = pd.read_csv(
    __import__("config").get_data_path("processed/feature_engineered_transactions.csv")
)

print("Dataset loaded successfully!")


# ---------------------------------------------------------
# 2. SELECT EXPENSE TRANSACTIONS
# ---------------------------------------------------------

print("\n2. Selecting debit transactions...")

expense_df = df[
    df["transaction_type"] == "Debit"
].copy()

print(
    "Number of expense transactions:"
)

print(
    len(expense_df)
)


# ---------------------------------------------------------
# 3. CHECK AMOUNT
# ---------------------------------------------------------

print("\n3. Spending amount statistics:")

print(
    expense_df["amount"].describe()
)


# ---------------------------------------------------------
# 4. PREPARE ML DATA
# ---------------------------------------------------------

print("\n4. Preparing data for anomaly detection...")

X = expense_df[
    ["amount"]
]

print("\nAmount data:")

print(
    X.head(10)
)


# ---------------------------------------------------------
# 5. CREATE ISOLATION FOREST
# ---------------------------------------------------------

print("\n5. Creating Isolation Forest model...")

model = IsolationForest(
    contamination=0.05,
    random_state=42
)

print(
    "Isolation Forest model created."
)


# ---------------------------------------------------------
# 6. TRAIN MODEL
# ---------------------------------------------------------

print("\n6. Training anomaly detection model...")

model.fit(X)

print(
    "Model training completed!"
)


# ---------------------------------------------------------
# 7. PREDICT ANOMALIES
# ---------------------------------------------------------

print("\n7. Detecting unusual transactions...")

expense_df["anomaly"] = model.predict(X)


# ---------------------------------------------------------
# 8. CONVERT RESULT
# ---------------------------------------------------------

expense_df["is_unusual"] = (
    expense_df["anomaly"] == -1
)


# ---------------------------------------------------------
# 9. DISPLAY RESULTS
# ---------------------------------------------------------

print("\n8. Anomaly results:")

print(
    expense_df[
        [
            "transaction_id",
            "date",
            "amount",
            "merchant",
            "category",
            "is_unusual"
        ]
    ].head(20)
)


# ---------------------------------------------------------
# 10. COUNT NORMAL / UNUSUAL
# ---------------------------------------------------------

print("\n9. Normal vs unusual transactions:")

print(
    expense_df["is_unusual"].value_counts()
)


# ---------------------------------------------------------
# 11. SHOW ONLY UNUSUAL
# ---------------------------------------------------------

unusual_transactions = expense_df[
    expense_df["is_unusual"] == True
]

print(
    "\n10. UNUSUAL TRANSACTIONS:"
)

print(
    unusual_transactions[
        [
            "transaction_id",
            "date",
            "amount",
            "merchant",
            "category"
        ]
    ]
)


# ---------------------------------------------------------
# 12. SAVE RESULTS
# ---------------------------------------------------------

output_file = (
    __import__("config").get_data_path("processed/anomaly_detection_results.csv", for_writing=True)
)

expense_df.to_csv(
    output_file,
    index=False
)

print(
    "\nAnomaly detection results saved!"
)

print(
    "Location: ",
    __import__("config").get_data_path("processed/anomaly_detection_results.csv", for_writing=True)
)


print(
    "\nUNUSUAL SPENDING DETECTION COMPLETED!"
)

print("=" * 70)
