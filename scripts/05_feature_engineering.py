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

print("=" * 70)
print("PHASE 2 - STEP 9: FEATURE ENGINEERING")
print("=" * 70)

# ---------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------

print("\n1. Loading cleaned dataset...")

df = pd.read_csv(
    __import__("config").get_data_path("processed/clean_transactions.csv")
)

print("Dataset loaded!")

# ---------------------------------------------------------
# 2. CONVERT DATE
# ---------------------------------------------------------

df["date"] = pd.to_datetime(
    df["date"]
)

print("\n2. Date converted.")

# ---------------------------------------------------------
# 3. CREATE YEAR
# ---------------------------------------------------------

df["year"] = df["date"].dt.year

print("\n3. Year feature created.")

print(
    df[["date", "year"]].head()
)

# ---------------------------------------------------------
# 4. CREATE MONTH
# ---------------------------------------------------------

df["month"] = df["date"].dt.month

print("\n4. Month feature created.")

print(
    df[["date", "month"]].head()
)

# ---------------------------------------------------------
# 5. CREATE DAY
# ---------------------------------------------------------

df["day"] = df["date"].dt.day

print("\n5. Day feature created.")

print(
    df[["date", "day"]].head()
)

# ---------------------------------------------------------
# 6. CREATE DAY OF WEEK
# ---------------------------------------------------------

df["day_of_week"] = (
    df["date"].dt.dayofweek
)

print("\n6. Day-of-week feature created.")

print(
    df[["date", "day_of_week"]].head()
)

# ---------------------------------------------------------
# 7. CREATE WEEKEND FEATURE
# ---------------------------------------------------------

df["is_weekend"] = (
    df["day_of_week"] >= 5
)

print("\n7. Weekend feature created.")

print(
    df[
        ["date", "day_of_week", "is_weekend"]
    ].head(10)
)

# ---------------------------------------------------------
# 8. CREATE SPENDING LEVEL
# ---------------------------------------------------------

def spending_level(amount):

    if amount < 500:
        return "Low"

    elif amount < 2000:
        return "Medium"

    else:
        return "High"


df["spending_level"] = (
    df["amount"].apply(spending_level)
)

print("\n8. Spending level created.")

print(
    df[
        ["amount", "spending_level"]
    ].head(10)
)

# ---------------------------------------------------------
# 9. CREATE MONTH PERIOD
# ---------------------------------------------------------

df["month_period"] = (
    df["date"]
    .dt.to_period("M")
    .astype(str)
)

print("\n9. Month period created.")

print(
    df[
        ["date", "month_period"]
    ].head()
)

# ---------------------------------------------------------
# 10. CALCULATE MONTHLY SPENDING
# ---------------------------------------------------------

print("\n10. Calculating monthly spending...")

expense_df = df[
    df["transaction_type"] == "Debit"
].copy()

monthly_spending = (
    expense_df
    .groupby("month_period")["amount"]
    .sum()
)

print("\nMonthly spending:")

print(monthly_spending)

# ---------------------------------------------------------
# 11. ADD MONTHLY SPENDING TO DATA
# ---------------------------------------------------------

df["monthly_spending"] = (
    df["month_period"]
    .map(monthly_spending)
)

df["monthly_spending"] = (
    df["monthly_spending"]
    .fillna(0)
)

print("\n11. Monthly spending feature added.")

print(
    df[
        [
            "date",
            "amount",
            "month_period",
            "monthly_spending"
        ]
    ].head(10)
)

# ---------------------------------------------------------
# 12. CREATE INCOME FLAG
# ---------------------------------------------------------

df["is_income"] = (
    df["transaction_type"] == "Credit"
)

print("\n12. Income flag created.")

print(
    df[
        [
            "transaction_type",
            "is_income"
        ]
    ].head(10)
)

# ---------------------------------------------------------
# 13. CREATE EXPENSE FLAG
# ---------------------------------------------------------

df["is_expense"] = (
    df["transaction_type"] == "Debit"
)

print("\n13. Expense flag created.")

print(
    df[
        [
            "transaction_type",
            "is_expense"
        ]
    ].head(10)
)

# ---------------------------------------------------------
# 14. DISPLAY FINAL DATASET
# ---------------------------------------------------------

print("\n14. FINAL FEATURE-ENGINEERED DATASET:")

print(df.head(10))

print("\nFinal columns:")

print(df.columns.tolist())

print("\nFinal shape:")

print(df.shape)

# ---------------------------------------------------------
# 15. SAVE FEATURE DATA
# ---------------------------------------------------------

output_file = (
    __import__("config").get_data_path("processed/feature_engineered_transactions.csv")
)

df.to_csv(
    output_file,
    index=False
)

print("\nFeature-engineered dataset saved!")

print(
    "Location: ",
    __import__("config").get_data_path("processed/feature_engineered_transactions.csv")
)

print("\nFEATURE ENGINEERING COMPLETED!")

print("=" * 70)