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
print("PHASE 4 - STEP 13: SAFE-TO-SPEND CALCULATION")
print("=" * 70)


# ---------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------

print("\n1. Loading feature engineered dataset...")

file_path = (
    __import__("config").get_data_path("processed/feature_engineered_transactions.csv")
)

if not os.path.exists(file_path):
    print("ERROR: Dataset not found!")
    print("Please run feature engineering first.")
    exit()

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# ---------------------------------------------------------
# 2. CONVERT DATE
# ---------------------------------------------------------

print("\n2. Preparing date information...")

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values(
    ["date", "time"]
)

print("Date preparation completed.")


# ---------------------------------------------------------
# 3. FIND LATEST TRANSACTION
# ---------------------------------------------------------

print("\n3. Finding latest account information...")

latest_transaction = df.iloc[-1]

latest_date = latest_transaction["date"]

current_balance = (
    latest_transaction[
        "balance_after_transaction"
    ]
)

print(
    "Latest transaction date:",
    latest_date.date()
)

print(
    "Current balance:",
    round(current_balance, 2)
)


# ---------------------------------------------------------
# 4. CALCULATE MONTHLY INCOME
# ---------------------------------------------------------

print("\n4. Calculating average monthly income...")

income_df = df[
    df["transaction_type"] == "Credit"
].copy()

income_df["month_period"] = (
    income_df["date"].dt.to_period("M")
)

monthly_income = (
    income_df
    .groupby("month_period")["amount"]
    .sum()
)

average_monthly_income = (
    monthly_income.mean()
)

print("Monthly income:")
print(monthly_income)

print(
    "\nAverage monthly income:",
    round(average_monthly_income, 2)
)


# ---------------------------------------------------------
# 5. CALCULATE MONTHLY EXPENSE
# ---------------------------------------------------------

print("\n5. Calculating average monthly expenses...")

expense_df = df[
    df["transaction_type"] == "Debit"
].copy()

expense_df["month_period"] = (
    expense_df["date"].dt.to_period("M")
)

monthly_expense = (
    expense_df
    .groupby("month_period")["amount"]
    .sum()
)

average_monthly_expense = (
    monthly_expense.mean()
)

print("Monthly expenses:")
print(monthly_expense)

print(
    "\nAverage monthly expense:",
    round(average_monthly_expense, 2)
)


# ---------------------------------------------------------
# 6. CURRENT MONTH EXPENSE
# ---------------------------------------------------------

print("\n6. Calculating current month spending...")

latest_month = latest_date.to_period("M")

current_month_expense = (
    expense_df[
        expense_df["month_period"] == latest_month
    ]["amount"]
    .sum()
)

print(
    "Current month:",
    latest_month
)

print(
    "Current month expense:",
    round(current_month_expense, 2)
)


# ---------------------------------------------------------
# 7. PREDICTED MONTHLY SPENDING
# ---------------------------------------------------------

print("\n7. Checking spending prediction...")

prediction_file = (
    __import__("config").get_data_path("processed/spending_prediction.csv", for_writing=True)
)

if os.path.exists(prediction_file):

    prediction_df = pd.read_csv(
        prediction_file
    )

    print(
        "Spending prediction file found."
    )

    if "predicted_spending" in prediction_df.columns:

        predicted_monthly_spending = (
            prediction_df[
                "predicted_spending"
            ].iloc[-1]
        )

    else:

        predicted_monthly_spending = (
            average_monthly_expense
        )

else:

    print("Prediction file not found.")
    print(
        "Using average monthly expense instead."
    )

    predicted_monthly_spending = (
        average_monthly_expense
    )

print(
    "Expected monthly spending:",
    round(predicted_monthly_spending, 2)
)


# ---------------------------------------------------------
# 8. CALCULATE UPCOMING EXPENSE RESERVE
# ---------------------------------------------------------

print(
    "\n8. Calculating upcoming expense reserve..."
)

remaining_expected_expense = (
    predicted_monthly_spending
    - current_month_expense
)

if remaining_expected_expense < 0:

    remaining_expected_expense = 0

print(
    "Expected remaining expense:",
    round(remaining_expected_expense, 2)
)


# ---------------------------------------------------------
# 9. CALCULATE SAFETY BUFFER
# ---------------------------------------------------------

print("\n9. Calculating safety buffer...")

safety_buffer = (
    average_monthly_income * 0.20
)

print(
    "Safety buffer = 20% of average monthly income"
)

print(
    "Safety buffer:",
    round(safety_buffer, 2)
)


# ---------------------------------------------------------
# 10. CALCULATE SAFE-TO-SPEND
# ---------------------------------------------------------

print("\n10. Calculating safe-to-spend amount...")

safe_to_spend = (
    current_balance
    - remaining_expected_expense
    - safety_buffer
)

if safe_to_spend < 0:

    safe_to_spend = 0


# ---------------------------------------------------------
# 11. CALCULATE DAILY SAFE SPENDING
# ---------------------------------------------------------

print("\n11. Calculating daily safe spending...")

days_in_month = (
    latest_date.days_in_month
)

current_day = (
    latest_date.day
)

remaining_days = (
    days_in_month
    - current_day
    + 1
)

if remaining_days > 0:

    daily_safe_spending = (
        safe_to_spend
        / remaining_days
    )

else:

    daily_safe_spending = (
        safe_to_spend
    )


# ---------------------------------------------------------
# 12. DISPLAY FINAL RESULT
# ---------------------------------------------------------

print(
    "\n" + "=" * 70
)

print("SAFE-TO-SPEND RESULT")

print(
    "=" * 70
)

print("\nLatest Date:")

print(
    latest_date.date()
)

print("\nCurrent Balance:")

print(
    round(current_balance, 2)
)

print("\nAverage Monthly Income:")

print(
    round(average_monthly_income, 2)
)

print("\nAverage Monthly Expense:")

print(
    round(average_monthly_expense, 2)
)

print("\nPredicted Monthly Spending:")

print(
    round(predicted_monthly_spending, 2)
)

print("\nRemaining Expected Expense:")

print(
    round(remaining_expected_expense, 2)
)

print("\nSafety Buffer:")

print(
    round(safety_buffer, 2)
)

print(
    "\n----------------------------------------"
)

print("SAFE TO SPEND:")

print(
    round(safe_to_spend, 2)
)

print("DAILY SAFE SPENDING:")

print(
    round(daily_safe_spending, 2)
)

print(
    "----------------------------------------"
)


# ---------------------------------------------------------
# 13. SIMPLE FINANCIAL MESSAGE
# ---------------------------------------------------------

print(
    "\n12. Generating financial wellness message..."
)

if safe_to_spend == 0:

    message = (
        "Your available safe-to-spend amount is 0. "
        "Try to avoid unnecessary spending until "
        "your balance improves."
    )

elif safe_to_spend < (
    average_monthly_income * 0.10
):

    message = (
        "Your safe-to-spend amount is relatively low. "
        "Consider limiting discretionary spending."
    )

else:

    message = (
        "You have some available spending capacity "
        "after accounting for expected expenses "
        "and the safety buffer."
    )


print("\nFinancial Wellness Message:")

print(message)


# ---------------------------------------------------------
# 14. SAVE RESULT
# ---------------------------------------------------------

print("\n13. Saving result...")

result = pd.DataFrame({

    "latest_date": [
        latest_date.date()
    ],

    "current_balance": [
        current_balance
    ],

    "average_monthly_income": [
        average_monthly_income
    ],

    "average_monthly_expense": [
        average_monthly_expense
    ],

    "predicted_monthly_spending": [
        predicted_monthly_spending
    ],

    "remaining_expected_expense": [
        remaining_expected_expense
    ],

    "safety_buffer": [
        safety_buffer
    ],

    "safe_to_spend": [
        safe_to_spend
    ],

    "daily_safe_spending": [
        daily_safe_spending
    ],

    "financial_message": [
        message
    ]
})


output_file = (
    __import__("config").get_data_path("processed/safe_to_spend_result.csv")
)

result.to_csv(
    output_file,
    index=False
)

print(
    "Result saved successfully!"
)

print(
    "File:",
    output_file
)


print(
    "\n" + "=" * 70
)

print(
    "STEP 13 COMPLETED SUCCESSFULLY!"
)

print(
    "=" * 70
)