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
print("PHASE 4 - STEP 16: PERSONALIZED FINANCIAL ALERTS")
print("=" * 70)

# ----------------------------------------------------------
# 1. LOAD TRANSACTION DATA
# ----------------------------------------------------------

print("\n1. Loading transaction data...")

file_path = (
    __import__("config").get_data_path("processed/feature_engineered_transactions.csv")
)

if not os.path.exists(file_path):
    print("\nERROR: Transaction dataset not found!")
    print("Expected location:")
    print(file_path)
    print("\nPlease run feature_engineering.py first.")
    exit()

df = pd.read_csv(file_path)

print("Transaction dataset loaded successfully!")

print(
    f"Total transactions: {len(df)}"
)

# ----------------------------------------------------------
# 2. PREPARE DATA
# ----------------------------------------------------------

print("\n2. Preparing transaction data...")
print("-" * 70)

df["date"] = pd.to_datetime(
    df["date"]
)

df["amount"] = pd.to_numeric(
    df["amount"],
    errors="coerce"
)

print("Data prepared successfully!")

# ----------------------------------------------------------
# 3. CALCULATE BASIC FINANCIAL VALUES
# ----------------------------------------------------------

print("\n3. CALCULATING FINANCIAL INFORMATION")
print("-" * 70)

income = df[
    df["transaction_type"].str.lower() == "credit"
]["amount"].sum()

expenses = df[
    df["transaction_type"].str.lower() == "debit"
]["amount"].sum()

print(
    f"Total Income   : ₹{income:,.2f}"
)

print(
    f"Total Expenses : ₹{expenses:,.2f}"
)

# ----------------------------------------------------------
# 4. ALERT 1 - HIGH SPENDING
# ----------------------------------------------------------

print("\n4. CHECKING HIGH SPENDING ALERT")
print("-" * 70)

expense_transactions = df[
    df["transaction_type"].str.lower() == "debit"
]

average_expense = (
    expense_transactions["amount"].mean()
)

high_spending_threshold = (
    average_expense * 2
)

high_spending_transactions = (
    expense_transactions[
        expense_transactions["amount"]
        > high_spending_threshold
    ]
)

print(
    f"Average expense transaction: "
    f"₹{average_expense:,.2f}"
)

print(
    f"High spending threshold: "
    f"₹{high_spending_threshold:,.2f}"
)

print(
    f"High spending transactions: "
    f"{len(high_spending_transactions)}"
)

# ----------------------------------------------------------
# 5. ALERT 2 - LARGE TRANSACTION
# ----------------------------------------------------------

print("\n5. CHECKING LARGE TRANSACTION ALERT")
print("-" * 70)

large_transaction_threshold = 25000

large_transactions = (
    expense_transactions[
        expense_transactions["amount"]
        >= large_transaction_threshold
    ]
)

print(
    f"Large transaction threshold: "
    f"₹{large_transaction_threshold:,.2f}"
)

print(
    f"Large transactions detected: "
    f"{len(large_transactions)}"
)

# ----------------------------------------------------------
# 6. ALERT 3 - CATEGORY SPENDING
# ----------------------------------------------------------

print("\n6. CHECKING CATEGORY SPENDING ALERT")
print("-" * 70)

category_spending = (
    expense_transactions
    .groupby("category")["amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\nCategory spending:")

for category, amount in category_spending.items():

    print(
        f"{category:<20} ₹{amount:,.2f}"
    )

# Find highest spending category

highest_category = (
    category_spending.idxmax()
)

highest_category_amount = (
    category_spending.max()
)

print(
    f"\nHighest spending category: "
    f"{highest_category}"
)

print(
    f"Amount spent: "
    f"₹{highest_category_amount:,.2f}"
)

# ----------------------------------------------------------
# 7. ALERT 4 - RECURRING EXPENSES
# ----------------------------------------------------------

print("\n7. CHECKING RECURRING EXPENSE ALERT")
print("-" * 70)

if "is_recurring" in df.columns:

    recurring_expenses = expense_transactions[
        expense_transactions["is_recurring"] == True
    ]

else:

    recurring_expenses = pd.DataFrame()

print(
    f"Recurring expense transactions: "
    f"{len(recurring_expenses)}"
)

recurring_expense_amount = (
    recurring_expenses["amount"].sum()
)

print(
    f"Recurring expense amount: "
    f"₹{recurring_expense_amount:,.2f}"
)

# ----------------------------------------------------------
# 8. ALERT 5 - WEEKEND SPENDING
# ----------------------------------------------------------

print("\n8. CHECKING WEEKEND SPENDING ALERT")
print("-" * 70)

if "is_weekend" in expense_transactions.columns:

    weekend_expenses = expense_transactions[
        expense_transactions["is_weekend"] == True
    ]

else:

    df["is_weekend"] = (
        df["date"].dt.dayofweek >= 5
    )

    weekend_expenses = expense_transactions[
        expense_transactions["is_weekend"] == True
    ]

weekend_spending = (
    weekend_expenses["amount"].sum()
)

print(
    f"Weekend spending: "
    f"₹{weekend_spending:,.2f}"
)

# ----------------------------------------------------------
# 9. GENERATE PERSONALIZED ALERTS
# ----------------------------------------------------------

print("\n9. GENERATING PERSONALIZED ALERTS")
print("=" * 70)

alerts = []

# High spending alert

if len(high_spending_transactions) > 0:

    alerts.append(
        f"High Spending Alert: "
        f"{len(high_spending_transactions)} "
        f"transactions are significantly higher "
        f"than your average expense."
    )

# Large transaction alert

if len(large_transactions) > 0:

    alerts.append(
        f"Large Transaction Alert: "
        f"{len(large_transactions)} transactions "
        f"are ₹{large_transaction_threshold:,.0f} or above."
    )

# Category alert

if highest_category_amount > average_expense * 100:

    alerts.append(
        f"Category Alert: "
        f"{highest_category} is your highest "
        f"spending category with "
        f"₹{highest_category_amount:,.2f} spent."
    )

# Recurring expense alert

if recurring_expense_amount > 0:

    alerts.append(
        f"Recurring Expense Alert: "
        f"You have ₹{recurring_expense_amount:,.2f} "
        f"in recurring transactions."
    )

# Weekend spending alert

if weekend_spending > 0:

    alerts.append(
        f"Weekend Spending Alert: "
        f"₹{weekend_spending:,.2f} was spent "
        f"during weekends."
    )

# ----------------------------------------------------------
# 10. DISPLAY ALERTS
# ----------------------------------------------------------

print("\nPERSONALIZED ALERTS")
print("-" * 70)

if len(alerts) == 0:

    print(
        "No major financial alerts detected."
    )

else:

    for i, alert in enumerate(
        alerts,
        start=1
    ):

        print(
            f"{i}. {alert}"
        )

# ----------------------------------------------------------
# 11. GENERATE FINANCIAL ADVICE
# ----------------------------------------------------------

print("\n10. PERSONALIZED FINANCIAL ADVICE")
print("-" * 70)

advice = []

if len(high_spending_transactions) > 0:

    advice.append(
        "Review unusually large transactions "
        "before making similar purchases."
    )

if len(large_transactions) > 0:

    advice.append(
        "Monitor large transactions carefully "
        "to avoid unexpected cash-flow pressure."
    )

if highest_category_amount > 0:

    advice.append(
        f"Monitor your {highest_category} spending "
        f"because it is your highest spending category."
    )

if recurring_expense_amount > 0:

    advice.append(
        "Review recurring expenses periodically "
        "and cancel unnecessary subscriptions."
    )

if weekend_spending > 0:

    advice.append(
        "Track weekend spending separately "
        "to identify discretionary expenses."
    )

if len(advice) == 0:

    advice.append(
        "Continue monitoring your transactions "
        "and maintain a regular savings habit."
    )

for item in advice:

    print(
        "- " + item
    )

# ----------------------------------------------------------
# 12. CREATE ALERT DATASET
# ----------------------------------------------------------

print("\n11. Creating alert dataset...")
print("-" * 70)

alert_records = []

for alert in alerts:

    alert_records.append({
        "alert_type": "Personalized Financial Alert",
        "alert_message": alert
    })

if len(alert_records) == 0:

    alert_records.append({
        "alert_type": "No Major Alert",
        "alert_message":
            "No major financial alerts detected."
    })

alerts_df = pd.DataFrame(
    alert_records
)

# ----------------------------------------------------------
# 13. SAVE RESULT
# ----------------------------------------------------------

output_file = (
    __import__("config").get_data_path("processed/personalized_financial_alerts.csv", for_writing=True)
)

alerts_df.to_csv(
    output_file,
    index=False
)

print(
    "\nPersonalized alerts saved successfully!"
)

print(
    "Location:",
    output_file
)

# ----------------------------------------------------------
# 14. FINAL SUMMARY
# ----------------------------------------------------------

print("\n" + "=" * 70)
print("PERSONALIZED FINANCIAL ALERT SUMMARY")
print("=" * 70)

print(
    f"\nTotal Transactions : {len(df)}"
)

print(
    f"Total Income       : ₹{income:,.2f}"
)

print(
    f"Total Expenses     : ₹{expenses:,.2f}"
)

print(
    f"High Spending      : "
    f"{len(high_spending_transactions)} transactions"
)

print(
    f"Large Transactions : "
    f"{len(large_transactions)}"
)

print(
    f"Highest Category   : {highest_category}"
)

print(
    f"Recurring Expenses : "
    f"₹{recurring_expense_amount:,.2f}"
)

print(
    f"Weekend Spending   : "
    f"₹{weekend_spending:,.2f}"
)

print(
    f"\nTotal Alerts       : {len(alerts)}"
)

print("\n" + "=" * 70)
print(
    "PHASE 4 - STEP 16 COMPLETED SUCCESSFULLY!"
)
print("=" * 70)