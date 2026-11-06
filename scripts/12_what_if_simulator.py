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
print("PHASE 4 - STEP 15: WHAT-IF SPENDING SIMULATOR")
print("=" * 70)

# ----------------------------------------------------------
# 1. LOAD SAFE-TO-SPEND DATA
# ----------------------------------------------------------

print("\n1. Loading safe-to-spend data...")

file_path = (
    __import__("config").get_data_path("processed/safe_to_spend_result.csv")
)

if not os.path.exists(file_path):
    print("\nERROR: safe_to_spend_result.csv not found!")
    print("Expected location:")
    print(file_path)
    print("\nPlease run safe_to_spend.py first.")
    exit()

df = pd.read_csv(file_path)

print("Safe-to-Spend data loaded successfully!")

# ----------------------------------------------------------
# 2. DISPLAY CURRENT FINANCIAL STATUS
# ----------------------------------------------------------

print("\n2. CURRENT FINANCIAL STATUS")
print("-" * 70)

current_balance = float(
    df["current_balance"].iloc[0]
)

safe_to_spend = float(
    df["safe_to_spend"].iloc[0]
)

average_monthly_income = float(
    df["average_monthly_income"].iloc[0]
)

average_monthly_expense = float(
    df["average_monthly_expense"].iloc[0]
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
    f"Current Safe-to-Spend  : ₹{safe_to_spend:,.2f}"
)

# ----------------------------------------------------------
# 3. ENTER CURRENT MONTHLY SPENDING
# ----------------------------------------------------------

print("\n3. CURRENT MONTHLY SPENDING")
print("-" * 70)

while True:
    try:
        current_spending = float(
            input(
                "Enter your current monthly spending (₹): "
            )
        )

        if current_spending < 0:
            print("Please enter a value greater than or equal to ₹0.")
        else:
            break

    except ValueError:
        print("Please enter a valid number.")

# ----------------------------------------------------------
# 4. ENTER WHAT-IF SPENDING
# ----------------------------------------------------------

print("\n4. WHAT-IF SPENDING SCENARIO")
print("-" * 70)

while True:
    try:
        what_if_spending = float(
            input(
                "Enter your new monthly spending scenario (₹): "
            )
        )

        if what_if_spending < 0:
            print("Please enter a value greater than or equal to ₹0.")
        else:
            break

    except ValueError:
        print("Please enter a valid number.")

# ----------------------------------------------------------
# 5. CALCULATE DIFFERENCE
# ----------------------------------------------------------

print("\n5. CALCULATING IMPACT")
print("-" * 70)

spending_difference = (
    what_if_spending - current_spending
)

if current_spending > 0:
    percentage_change = (
        spending_difference / current_spending
    ) * 100
else:
    percentage_change = 0

# ----------------------------------------------------------
# 6. CALCULATE REMAINING MONEY
# ----------------------------------------------------------

current_remaining = (
    average_monthly_income - current_spending
)

what_if_remaining = (
    average_monthly_income - what_if_spending
)

remaining_difference = (
    what_if_remaining - current_remaining
)

# ----------------------------------------------------------
# 7. DISPLAY RESULT
# ----------------------------------------------------------

print("\n6. WHAT-IF SIMULATION RESULT")
print("=" * 70)

print(
    f"Current Monthly Spending : ₹{current_spending:,.2f}"
)

print(
    f"What-If Monthly Spending : ₹{what_if_spending:,.2f}"
)

print(
    f"Spending Difference      : ₹{spending_difference:,.2f}"
)

print(
    f"Percentage Change        : {percentage_change:.2f}%"
)

print(
    f"Current Remaining Money  : ₹{current_remaining:,.2f}"
)

print(
    f"What-If Remaining Money  : ₹{what_if_remaining:,.2f}"
)

print(
    f"Change in Remaining Money: ₹{remaining_difference:,.2f}"
)

# ----------------------------------------------------------
# 8. INTERPRETATION
# ----------------------------------------------------------

print("\n7. WHAT-IF INTERPRETATION")
print("-" * 70)

if what_if_spending > current_spending:

    print(
        "Your monthly spending increases in this scenario."
    )

    print(
        f"Additional spending: ₹"
        f"{spending_difference:,.2f}"
    )

    print(
        "This will reduce the amount of money remaining "
        "after monthly expenses."
    )

elif what_if_spending < current_spending:

    print(
        "Your monthly spending decreases in this scenario."
    )

    print(
        f"Monthly spending reduction: ₹"
        f"{abs(spending_difference):,.2f}"
    )

    print(
        "This will increase the amount of money remaining "
        "after monthly expenses."
    )

else:

    print(
        "Your spending remains unchanged."
    )

# ----------------------------------------------------------
# 9. FINANCIAL MESSAGE
# ----------------------------------------------------------

print("\n8. FINANCIAL MESSAGE")
print("-" * 70)

if what_if_spending > average_monthly_income:

    message = (
        "Warning: The what-if spending scenario is higher "
        "than your average monthly income."
    )

elif what_if_remaining < 0:

    message = (
        "Warning: This scenario may result in a monthly "
        "shortfall."
    )

elif what_if_spending > average_monthly_expense:

    message = (
        "This scenario increases spending above your "
        "historical average monthly expense."
    )

else:

    message = (
        "This spending scenario is within your "
        "average monthly income."
    )

print(message)

# ----------------------------------------------------------
# 10. SAVE RESULT
# ----------------------------------------------------------

print("\n9. SAVING SIMULATION RESULT")
print("-" * 70)

result = pd.DataFrame({
    "current_balance": [
        current_balance
    ],
    "safe_to_spend": [
        safe_to_spend
    ],
    "average_monthly_income": [
        average_monthly_income
    ],
    "average_monthly_expense": [
        average_monthly_expense
    ],
    "current_monthly_spending": [
        current_spending
    ],
    "what_if_monthly_spending": [
        what_if_spending
    ],
    "spending_difference": [
        spending_difference
    ],
    "percentage_change": [
        percentage_change
    ],
    "current_remaining_money": [
        current_remaining
    ],
    "what_if_remaining_money": [
        what_if_remaining
    ],
    "remaining_money_difference": [
        remaining_difference
    ],
    "financial_message": [
        message
    ]
})

output_file = (
    __import__("config").get_data_path("processed/what_if_simulation.csv", for_writing=True)
)

result.to_csv(
    output_file,
    index=False
)

print(
    "What-if simulation saved successfully!"
)

print(
    "Location:",
    output_file
)

print("\n" + "=" * 70)
print(
    "PHASE 4 - STEP 15 COMPLETED SUCCESSFULLY!"
)
print("=" * 70)