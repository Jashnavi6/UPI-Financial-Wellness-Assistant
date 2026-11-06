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
import matplotlib.pyplot as plt
import os

print("=" * 70)
print("PHASE 2 - STEP 8: DATA VISUALIZATION")
print("=" * 70)


# --------------------------------------------------
# 1. LOAD DATA
# --------------------------------------------------

print("\n1. Loading cleaned dataset...")

# Exact location of cleaned dataset
input_file = __import__("config").get_data_path("processed/clean_transactions.csv")

df = pd.read_csv(input_file)

df["date"] = pd.to_datetime(df["date"])

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# --------------------------------------------------
# 2. CREATE VISUALIZATION FOLDER
# --------------------------------------------------

# Exact location where graphs will be saved
output_folder = os.path.join(_root, "visualizations")

# Create folder automatically if it does not exist
os.makedirs(output_folder, exist_ok=True)

print("\n2. Visualization folder created!")
print("Graphs will be saved in:")
print(output_folder)


# --------------------------------------------------
# GRAPH 1: SPENDING BY CATEGORY
# --------------------------------------------------

print("\nGenerating Graph 1: Spending by Category...")

spending = df[df["transaction_type"] == "Debit"]

category_spending = spending.groupby("category")["amount"].sum()

plt.figure(figsize=(10, 6))

category_spending.sort_values(ascending=False).plot(kind="bar")

plt.title("UPI Spending by Category")
plt.xlabel("Category")
plt.ylabel("Amount (₹)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(output_folder + "/01_spending_by_category.png")
plt.close()

print("Graph 1 saved!")


# --------------------------------------------------
# GRAPH 2: DEBIT VS CREDIT
# --------------------------------------------------

print("Generating Graph 2: Debit vs Credit...")

transaction_type = df["transaction_type"].value_counts()

plt.figure(figsize=(7, 7))

transaction_type.plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Debit vs Credit Transactions")
plt.ylabel("")

plt.savefig(output_folder + "/02_debit_vs_credit.png")
plt.close()

print("Graph 2 saved!")


# --------------------------------------------------
# GRAPH 3: PAYMENT MODE
# --------------------------------------------------

print("Generating Graph 3: Payment Mode Distribution...")

payment_mode = df["payment_mode"].value_counts()

plt.figure(figsize=(10, 6))

payment_mode.plot(kind="bar")

plt.title("Payment Mode Distribution")
plt.xlabel("Payment Mode")
plt.ylabel("Number of Transactions")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(output_folder + "/03_payment_mode.png")
plt.close()

print("Graph 3 saved!")


# --------------------------------------------------
# GRAPH 4: RECURRING TRANSACTIONS
# --------------------------------------------------

print("Generating Graph 4: Recurring Transactions...")

recurring = df["is_recurring"].value_counts()

plt.figure(figsize=(7, 7))

recurring.plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Recurring vs Non-Recurring Transactions")
plt.ylabel("")

plt.savefig(output_folder + "/04_recurring_transactions.png")
plt.close()

print("Graph 4 saved!")


# --------------------------------------------------
# GRAPH 5: TRANSACTIONS OVER TIME
# --------------------------------------------------

print("Generating Graph 5: Transactions Over Time...")

daily_transactions = df.groupby("date").size()

plt.figure(figsize=(12, 6))

daily_transactions.plot(kind="line")

plt.title("Transactions Over Time")
plt.xlabel("Date")
plt.ylabel("Number of Transactions")
plt.grid(True)
plt.tight_layout()

plt.savefig(output_folder + "/05_transactions_over_time.png")
plt.close()

print("Graph 5 saved!")


# --------------------------------------------------
# GRAPH 6: TRANSACTION AMOUNT DISTRIBUTION
# --------------------------------------------------

print("Generating Graph 6: Transaction Amount Distribution...")

plt.figure(figsize=(10, 6))

plt.hist(
    df["amount"],
    bins=30
)

plt.title("Transaction Amount Distribution")
plt.xlabel("Transaction Amount (₹)")
plt.ylabel("Frequency")
plt.tight_layout()

plt.savefig(output_folder + "/06_amount_distribution.png")
plt.close()

print("Graph 6 saved!")


# --------------------------------------------------
# GRAPH 7: TOP 10 MERCHANTS
# --------------------------------------------------

print("Generating Graph 7: Top 10 Merchants...")

merchant_spending = (
    spending
    .groupby("merchant")["amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))

merchant_spending.sort_values().plot(kind="barh")

plt.title("Top 10 Merchants by Spending")
plt.xlabel("Amount Spent (₹)")
plt.ylabel("Merchant")
plt.tight_layout()

plt.savefig(output_folder + "/07_top_merchants.png")
plt.close()

print("Graph 7 saved!")


# --------------------------------------------------
# GRAPH 8: INCOME VS EXPENSES
# --------------------------------------------------

print("Generating Graph 8: Income vs Expenses...")

income = df[df["transaction_type"] == "Credit"]["amount"].sum()

expenses = df[df["transaction_type"] == "Debit"]["amount"].sum()

income_expenses = pd.Series({
    "Income": income,
    "Expenses": expenses
})

plt.figure(figsize=(8, 6))

income_expenses.plot(kind="bar")

plt.title("Income vs Expenses")
plt.xlabel("Transaction Type")
plt.ylabel("Amount (₹)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(output_folder + "/08_income_vs_expenses.png")
plt.close()

print("Graph 8 saved!")


# --------------------------------------------------
# GRAPH 9: TRANSACTIONS BY CATEGORY
# --------------------------------------------------

print("Generating Graph 9: Transactions by Category...")

category_count = df["category"].value_counts()

plt.figure(figsize=(10, 6))

category_count.sort_values(ascending=False).plot(kind="bar")

plt.title("Number of Transactions by Category")
plt.xlabel("Category")
plt.ylabel("Number of Transactions")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(output_folder + "/09_transactions_by_category.png")
plt.close()

print("Graph 9 saved!")


# --------------------------------------------------
# CHECK GENERATED FILES
# --------------------------------------------------

print("\n" + "=" * 70)
print("CHECKING GENERATED GRAPH FILES")
print("=" * 70)

files = os.listdir(output_folder)

for file in files:
    print(file)


# --------------------------------------------------
# FINAL RESULT
# --------------------------------------------------

print("\n" + "=" * 70)
print("ALL VISUALIZATIONS COMPLETED!")
print("=" * 70)

print("\n9 graphs have been generated.")

print("\nGraphs saved inside:")
print(os.path.join(_root, "visualizations"))

print("\nYou can open the folder using:")
print("explorer C:/Users/jashn/visualizations")

print("\nSTEP 8 COMPLETED!")