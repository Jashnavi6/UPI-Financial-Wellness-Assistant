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
print("PHASE 2 - STEP 7: EXPLORATORY DATA ANALYSIS")
print("=" * 70)


# =========================================================
# 1. LOAD CLEANED DATASET
# =========================================================

print("\n1. Loading cleaned dataset...")

input_file = (
    __import__("config").get_data_path("processed/clean_transactions.csv")
)

df = pd.read_csv(input_file)

print("Dataset loaded successfully!")


# =========================================================
# 2. BASIC INFORMATION
# =========================================================

print("\n2. Dataset shape:")

print(df.shape)


print("\n3. Column names:")

print(df.columns.tolist())


print("\n4. Data types:")

print(df.dtypes)


# =========================================================
# 3. BASIC STATISTICS
# =========================================================

print("\n5. Basic statistics:")

print(df.describe())


# =========================================================
# 4. TOTAL TRANSACTIONS
# =========================================================

print("\n6. Total number of transactions:")

print(len(df))


# =========================================================
# 5. TRANSACTION TYPE ANALYSIS
# =========================================================

print("\n7. Transaction type count:")

transaction_type_count = (
    df["transaction_type"]
    .value_counts()
)

print(transaction_type_count)


# =========================================================
# 6. INCOME AND EXPENSE
# =========================================================

print("\n8. Income and expense analysis:")

total_income = df.loc[
    df["transaction_type"] == "Credit",
    "amount"
].sum()

total_expense = df.loc[
    df["transaction_type"] == "Debit",
    "amount"
].sum()

print("Total Income:", total_income)

print("Total Expenses:", total_expense)


# =========================================================
# 7. AVERAGE TRANSACTION
# =========================================================

print("\n9. Average transaction amount:")

average_transaction = df["amount"].mean()

print(
    "Average Transaction:",
    round(average_transaction, 2)
)


# =========================================================
# 8. MAXIMUM AND MINIMUM
# =========================================================

print("\n10. Maximum transaction:")

print(
    df["amount"].max()
)


print("\n11. Minimum transaction:")

print(
    df["amount"].min()
)


# =========================================================
# 9. SPENDING BY CATEGORY
# =========================================================

print("\n12. Spending by category:")

expense_df = df[
    df["transaction_type"] == "Debit"
]

category_spending = (
    expense_df
    .groupby("category")["amount"]
    .sum()
    .sort_values(
        ascending=False
    )
)

print(category_spending)


# =========================================================
# 10. TRANSACTIONS BY CATEGORY
# =========================================================

print("\n13. Number of transactions by category:")

category_count = (
    df["category"]
    .value_counts()
)

print(category_count)


# =========================================================
# 11. PAYMENT MODE ANALYSIS
# =========================================================

print("\n14. Payment mode analysis:")

payment_mode_count = (
    df["payment_mode"]
    .value_counts()
)

print(payment_mode_count)


# =========================================================
# 12. RECURRING TRANSACTIONS
# =========================================================

print("\n15. Recurring transaction analysis:")

recurring_count = (
    df["is_recurring"]
    .value_counts()
)

print(recurring_count)


# =========================================================
# 13. MERCHANT ANALYSIS
# =========================================================

print("\n16. Top merchants by transaction count:")

merchant_count = (
    df["merchant"]
    .value_counts()
    .head(10)
)

print(merchant_count)


# =========================================================
# 14. BALANCE ANALYSIS
# =========================================================

print("\n17. Balance analysis:")

print(
    df["balance_after_transaction"].describe()
)


# =========================================================
# 15. DATE ANALYSIS
# =========================================================

print("\n18. Date analysis:")

df["date"] = pd.to_datetime(
    df["date"]
)

print(
    "Starting date:",
    df["date"].min().date()
)

print(
    "Ending date:",
    df["date"].max().date()
)


# =========================================================
# 16. MONTHLY SPENDING
# =========================================================

print("\n19. Monthly spending:")

expense_df = df[
    df["transaction_type"] == "Debit"
].copy()

expense_df["month"] = (
    expense_df["date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_spending = (
    expense_df
    .groupby("month")["amount"]
    .sum()
)

print(monthly_spending)


# =========================================================
# 17. MONTHLY INCOME
# =========================================================

print("\n20. Monthly income:")

income_df = df[
    df["transaction_type"] == "Credit"
].copy()

income_df["month"] = (
    income_df["date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_income = (
    income_df
    .groupby("month")["amount"]
    .sum()
)

print(monthly_income)


# =========================================================
# 18. FINAL SUMMARY
# =========================================================

print("\n" + "=" * 70)

print("EXPLORATORY DATA ANALYSIS COMPLETED!")

print("=" * 70)

print("\nTotal Transactions:")
print(len(df))

print("\nTotal Income:")
print(total_income)

print("\nTotal Expenses:")
print(total_expense)

print("\nAverage Transaction:")
print(round(average_transaction, 2))

print("\nHighest Spending Category:")

if len(category_spending) > 0:
    print(
        category_spending.index[0],
        "->",
        category_spending.iloc[0]
    )

print("\nEDA COMPLETED SUCCESSFULLY!")