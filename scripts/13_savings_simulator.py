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
import math

print("=" * 70)
print("PHASE 4 - STEP 14: SAVINGS GOAL SIMULATOR")
print("=" * 70)


# ---------------------------------------------------------
# 1. LOAD SAFE-TO-SPEND RESULT
# ---------------------------------------------------------

print("\n1. Loading Safe-to-Spend result...")

file_path = (
    __import__("config").get_data_path("processed/safe_to_spend_result.csv")
)

if not os.path.exists(file_path):
    print("\nERROR: Safe-to-Spend file not found!")
    print(
        "Please run the Safe-to-Spend calculation first."
    )
    exit()

df = pd.read_csv(file_path)

print("Safe-to-Spend result loaded successfully!")


# ---------------------------------------------------------
# 2. READ FINANCIAL INFORMATION
# ---------------------------------------------------------

print("\n2. CURRENT FINANCIAL STATUS")
print("-" * 70)

latest_date = pd.to_datetime(
    df["latest_date"].iloc[0]
)

current_balance = float(
    df["current_balance"].iloc[0]
)

average_monthly_income = float(
    df["average_monthly_income"].iloc[0]
)

average_monthly_expense = float(
    df["average_monthly_expense"].iloc[0]
)

safe_to_spend = float(
    df["safe_to_spend"].iloc[0]
)

daily_safe_spending = float(
    df["daily_safe_spending"].iloc[0]
)

print(
    f"Latest Date            : {latest_date.date()}"
)

print(
    f"Current Balance        : ₹{current_balance:,.2f}"
)

print(
    f"Average Monthly Income : ₹{average_monthly_income:,.2f}"
)

print(
    f"Average Monthly Expense: ₹{average_monthly_expense:,.2f}"
)

print(
    f"Safe-to-Spend          : ₹{safe_to_spend:,.2f}"
)

print(
    f"Daily Safe Spending    : ₹{daily_safe_spending:,.2f}"
)


# ---------------------------------------------------------
# 3. SAFE-TO-SPEND WARNING
# ---------------------------------------------------------

print("\n3. FINANCIAL STATUS CHECK")
print("-" * 70)

if safe_to_spend == 0:

    print(
        "WARNING: Your calculated Safe-to-Spend amount is ₹0."
    )

    print(
        "The savings simulator can still calculate a"
    )

    print(
        "savings target, but the monthly saving amount"
    )

    print(
        "should be chosen carefully."
    )

else:

    print(
        "You have some calculated spending capacity."
    )


# ---------------------------------------------------------
# 4. GET SAVINGS GOAL
# ---------------------------------------------------------

print("\n4. SAVINGS GOAL")
print("-" * 70)

while True:

    try:

        savings_goal = float(
            input("Enter your savings goal (₹): ")
        )

        if savings_goal <= 0:

            print(
                "Please enter a savings goal greater than ₹0."
            )

        else:

            break

    except ValueError:

        print(
            "Please enter a valid number."
        )


print(
    f"Savings Goal: ₹{savings_goal:,.2f}"
)


# ---------------------------------------------------------
# 5. GET MONTHLY SAVING
# ---------------------------------------------------------

print("\n5. MONTHLY SAVING")
print("-" * 70)

while True:

    try:

        monthly_saving = float(
            input(
                "Enter amount you can save per month (₹): "
            )
        )

        if monthly_saving <= 0:

            print(
                "Please enter an amount greater than ₹0."
            )

        else:

            break

    except ValueError:

        print(
            "Please enter a valid number."
        )


print(
    f"Monthly Saving: ₹{monthly_saving:,.2f}"
)


# ---------------------------------------------------------
# 6. CALCULATE MONTHS REQUIRED
# ---------------------------------------------------------

print("\n6. SAVINGS CALCULATION")
print("-" * 70)

months_required = math.ceil(
    savings_goal / monthly_saving
)

projected_savings = (
    monthly_saving * months_required
)

print(
    f"Savings Goal        : ₹{savings_goal:,.2f}"
)

print(
    f"Monthly Saving      : ₹{monthly_saving:,.2f}"
)

print(
    f"Months Required     : {months_required}"
)

print(
    f"Projected Savings   : ₹{projected_savings:,.2f}"
)


# ---------------------------------------------------------
# 7. CALCULATE SAVINGS PROGRESS
# ---------------------------------------------------------

print("\n7. SAVINGS PROGRESS")
print("-" * 70)

if savings_goal > 0:

    monthly_progress = (
        monthly_saving / savings_goal
    ) * 100

else:

    monthly_progress = 0

print(
    f"Monthly contribution toward goal: "
    f"{monthly_progress:.2f}%"
)


# ---------------------------------------------------------
# 8. ESTIMATED COMPLETION DATE
# ---------------------------------------------------------

print("\n8. ESTIMATED GOAL COMPLETION")
print("-" * 70)

completion_date = (
    latest_date
    + pd.DateOffset(months=months_required)
)

print(
    "Estimated Completion Date:",
    completion_date.date()
)


# ---------------------------------------------------------
# 9. CHECK SAVINGS GOAL
# ---------------------------------------------------------

print("\n9. SAVINGS GOAL STATUS")
print("-" * 70)

if projected_savings >= savings_goal:

    print(
        f"Goal Status: ACHIEVABLE"
    )

    print(
        f"You can reach ₹{savings_goal:,.2f} "
        f"in approximately {months_required} months."
    )

else:

    print(
        "Goal Status: NEEDS MORE SAVING"
    )


# ---------------------------------------------------------
# 10. FINANCIAL MESSAGE
# ---------------------------------------------------------

print("\n10. FINANCIAL WELLNESS MESSAGE")
print("-" * 70)

if safe_to_spend == 0:

    message = (
        "Your current calculated Safe-to-Spend amount is ₹0. "
        "Focus on essential expenses and maintain a financial buffer "
        "before increasing discretionary spending."
    )

elif monthly_saving > safe_to_spend:

    message = (
        "Your planned monthly saving is greater than your "
        "current Safe-to-Spend amount. Consider reviewing "
        "your monthly saving target."
    )

else:

    message = (
        "Your savings target has been calculated successfully. "
        "Maintain the planned monthly contribution to reach "
        "your goal."
    )

print(message)


# ---------------------------------------------------------
# 11. FINAL RESULT
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("SAVINGS GOAL SIMULATION RESULT")
print("=" * 70)

print(
    f"\nLatest Date              : {latest_date.date()}"
)

print(
    f"Current Balance          : ₹{current_balance:,.2f}"
)

print(
    f"Safe-to-Spend            : ₹{safe_to_spend:,.2f}"
)

print(
    f"Savings Goal             : ₹{savings_goal:,.2f}"
)

print(
    f"Monthly Saving           : ₹{monthly_saving:,.2f}"
)

print(
    f"Months Required          : {months_required}"
)

print(
    f"Projected Savings        : ₹{projected_savings:,.2f}"
)

print(
    f"Estimated Completion Date: {completion_date.date()}"
)

print(
    "\nFinancial Message:"
)

print(message)

print("\n" + "=" * 70)


# ---------------------------------------------------------
# 12. SAVE RESULT
# ---------------------------------------------------------

print("\n11. Saving simulation result...")

result = pd.DataFrame({

    "latest_date": [
        latest_date.date()
    ],

    "current_balance": [
        current_balance
    ],

    "safe_to_spend": [
        safe_to_spend
    ],

    "savings_goal": [
        savings_goal
    ],

    "monthly_saving": [
        monthly_saving
    ],

    "months_required": [
        months_required
    ],

    "projected_savings": [
        projected_savings
    ],

    "estimated_completion_date": [
        completion_date.date()
    ],

    "monthly_progress_percent": [
        monthly_progress
    ],

    "financial_message": [
        message
    ]
})


output_file = (
    __import__("config").get_data_path("processed/savings_goal_simulation.csv", for_writing=True)
)

result.to_csv(
    output_file,
    index=False
)

print(
    "\nSavings simulation saved successfully!"
)

print(
    "Location:",
    output_file
)


# ---------------------------------------------------------
# 13. COMPLETION
# ---------------------------------------------------------

print("\n" + "=" * 70)

print(
    "PHASE 4 - STEP 14 COMPLETED SUCCESSFULLY!"
)

print("=" * 70)
