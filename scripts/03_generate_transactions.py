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
import random
import os
from datetime import datetime, timedelta

print("=" * 70)
print("STEP 4 - REALISTIC SYNTHETIC UPI DATASET GENERATION")
print("=" * 70)

# ---------------------------------------------------------
# 1. SETTINGS
# ---------------------------------------------------------

NUMBER_OF_TRANSACTIONS = 5000

print("\nNumber of transactions to generate:")
print(NUMBER_OF_TRANSACTIONS)

# ---------------------------------------------------------
# 2. START DATE
# ---------------------------------------------------------

start_date = datetime(2026, 1, 1)

print("\nStarting date:")
print(start_date.date())

# ---------------------------------------------------------
# 3. LISTS
# ---------------------------------------------------------

merchants = {

    "Food": [
        "Swiggy",
        "Zomato",
        "Restaurant",
        "Cafe"
    ],

    "Shopping": [
        "Amazon",
        "Flipkart",
        "Myntra",
        "Local Store"
    ],

    "Travel": [
        "Uber",
        "Ola",
        "Metro",
        "IRCTC"
    ],

    "Bills": [
        "Electricity",
        "Airtel",
        "Jio",
        "Water Bill"
    ],

    "Entertainment": [
        "Netflix",
        "Spotify",
        "Movie",
        "Gaming"
    ],

    "Healthcare": [
        "Pharmacy",
        "Hospital",
        "Clinic"
    ],

    "Education": [
        "Course",
        "Books",
        "College"
    ]
}

categories = list(merchants.keys())

print("\nCategories:")
print(categories)

# ---------------------------------------------------------
# 4. CREATE TRANSACTIONS
# ---------------------------------------------------------

transactions = []

balance = 25000

print("\nGenerating transactions...")

for i in range(NUMBER_OF_TRANSACTIONS):

    transaction_id = f"TX{i + 1:05d}"

    date = start_date + timedelta(
        days=random.randint(0, 180)
    )

    hour = random.randint(7, 22)

    minute = random.randint(0, 59)

    second = random.randint(0, 59)

    transaction_time = (
        f"{hour:02d}:{minute:02d}:{second:02d}"
    )

    # -----------------------------------------------------
    # 90% EXPENSE
    # 10% INCOME
    # -----------------------------------------------------

    if random.random() < 0.90:

        transaction_type = "Debit"

        category = random.choice(categories)

        merchant = random.choice(
            merchants[category]
        )

        amount = random.randint(
            50,
            5000
        )

        balance -= amount

        # Maintain minimum balance
        if balance < 1000:
            balance += 10000

        payment_mode = "UPI"

        is_recurring = random.choice(
            [
                True,
                False,
                False,
                False
            ]
        )

    else:

        transaction_type = "Credit"

        category = "Income"

        merchant = random.choice(
            [
                "Salary",
                "Freelance",
                "Cashback",
                "Refund"
            ]
        )

        amount = random.randint(
            1000,
            50000
        )

        balance += amount

        payment_mode = random.choice(
            [
                "UPI",
                "Bank Transfer"
            ]
        )

        is_recurring = merchant == "Salary"

    # -----------------------------------------------------
    # ADD TRANSACTION
    # -----------------------------------------------------

    transactions.append({

        "transaction_id": transaction_id,

        "date": date.strftime(
            "%Y-%m-%d"
        ),

        "time": transaction_time,

        "amount": amount,

        "transaction_type": transaction_type,

        "merchant": merchant,

        "category": category,

        "payment_mode": payment_mode,

        "balance_after_transaction": balance,

        "is_recurring": is_recurring
    })


# ---------------------------------------------------------
# 5. CREATE DATAFRAME
# ---------------------------------------------------------

df = pd.DataFrame(transactions)

print("\nDataset generated successfully!")


# ---------------------------------------------------------
# 6. PRINT DATA
# ---------------------------------------------------------

print("\nFirst 10 transactions:")

print(
    df.head(10)
)

print("\nDataset shape:")

print(
    df.shape
)

print("\nColumn names:")

print(
    df.columns.tolist()
)

print("\nTransaction type count:")

print(
    df["transaction_type"].value_counts()
)

print("\nCategory count:")

print(
    df["category"].value_counts()
)


# ---------------------------------------------------------
# 7. SAVE DATASET
# ---------------------------------------------------------

print("\nSaving dataset...")

# Create folder automatically
output_folder = __import__("config").get_data_path("raw", for_writing=True)

os.makedirs(
    output_folder,
    exist_ok=True
)

# Complete output path
output_file = (
    __import__("config").get_data_path("raw/synthetic_upi_transactions.csv")
)

# Save CSV
df.to_csv(
    output_file,
    index=False
)


# ---------------------------------------------------------
# 8. CONFIRMATION
# ---------------------------------------------------------

print("\n" + "=" * 70)

print("DATASET SAVED SUCCESSFULLY!")

print("=" * 70)

print("\nLocation:")

print(output_file)

print("\nDataset shape:")

print(df.shape)

print("\nSTEP 4 COMPLETED!")