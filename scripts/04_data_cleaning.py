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
import os

print("=" * 70)
print("PHASE 2 - STEP 6: DATA CLEANING")
print("=" * 70)

# ---------------------------------------------------------
# 1. LOAD DATASET
# ---------------------------------------------------------

print("\n1. Loading dataset...")

input_file = (
    __import__("config").get_data_path("raw/synthetic_upi_transactions.csv")
)

df = pd.read_csv(input_file)

print("Dataset loaded successfully!")

# ---------------------------------------------------------
# 2. DISPLAY BASIC INFORMATION
# ---------------------------------------------------------

print("\n2. Dataset shape:")

print(df.shape)

print("\n3. Column names:")

print(df.columns.tolist())

# ---------------------------------------------------------
# 3. CHECK MISSING VALUES
# ---------------------------------------------------------

print("\n4. Checking missing values...")

print(df.isnull().sum())

# ---------------------------------------------------------
# 4. CHECK DUPLICATES
# ---------------------------------------------------------

print("\n5. Checking duplicate rows...")

print(
    "Duplicate rows:",
    df.duplicated().sum()
)

# Remove duplicates
df = df.drop_duplicates()

print(
    "Shape after removing duplicates:",
    df.shape
)

# ---------------------------------------------------------
# 5. DATE CONVERSION
# ---------------------------------------------------------

print("\n6. Converting date column...")

df["date"] = pd.to_datetime(
    df["date"]
)

print(
    "Date conversion completed!"
)

# ---------------------------------------------------------
# 6. TIME CONVERSION
# ---------------------------------------------------------

print("\n7. Checking time column...")

print(
    df["time"].head()
)

# ---------------------------------------------------------
# 7. AMOUNT CONVERSION
# ---------------------------------------------------------

print("\n8. Converting amount to numeric...")

df["amount"] = pd.to_numeric(
    df["amount"],
    errors="coerce"
)

print(
    "Amount conversion completed!"
)

# ---------------------------------------------------------
# 8. CHECK MISSING VALUES AGAIN
# ---------------------------------------------------------

print("\n9. Missing values after cleaning:")

print(
    df.isnull().sum()
)

# ---------------------------------------------------------
# 9. REMOVE ROWS WITH CRITICAL MISSING VALUES
# ---------------------------------------------------------

print("\n10. Removing rows with missing values...")

df = df.dropna(
    subset=[
        "date",
        "amount",
        "transaction_type",
        "category"
    ]
)

print(
    "Dataset shape:",
    df.shape
)

# ---------------------------------------------------------
# 10. SORT DATA
# ---------------------------------------------------------

print("\n11. Sorting transactions by date and time...")

df = df.sort_values(
    by=[
        "date",
        "time"
    ]
).reset_index(drop=True)

print(
    "Sorting completed!"
)

# ---------------------------------------------------------
# 11. FINAL DATA CHECK
# ---------------------------------------------------------

print("\n12. Final dataset information:")

print(
    df.info()
)

print("\n13. First 10 cleaned transactions:")

print(
    df.head(10)
)

# ---------------------------------------------------------
# 12. SAVE CLEANED DATASET
# ---------------------------------------------------------

print("\n14. Saving cleaned dataset...")

output_folder = (
    __import__("config").get_data_path("processed", for_writing=True)
)

os.makedirs(
    output_folder,
    exist_ok=True
)

output_file = (
    __import__("config").get_data_path("processed/clean_transactions.csv")
)

df.to_csv(
    output_file,
    index=False
)

# ---------------------------------------------------------
# 13. COMPLETION MESSAGE
# ---------------------------------------------------------

print("\n" + "=" * 70)

print("DATA CLEANING COMPLETED SUCCESSFULLY!")

print("=" * 70)

print("\nCleaned dataset saved at:")

print(output_file)

print("\nFinal dataset shape:")

print(df.shape)