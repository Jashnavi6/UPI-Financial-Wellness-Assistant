"""
Data Engine for UPI Financial Wellness Assistant.
Handles generation, cleaning, feature engineering, and storage of transaction data.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

_here = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_here) if os.path.basename(_here) in ("src", "scripts") else _here
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

# Also check fallback system paths if user had them previously configured
FALLBACK_RAW_FILE = "C:/Users/jashn/data/raw/synthetic_upi_transactions.csv"
FALLBACK_PROCESSED_FILE = "C:/Users/jashn/data/processed/feature_engineered_transactions.csv"
FALLBACK_SAFE_FILE = "C:/Users/jashn/data/processed/safe_to_spend_result.csv"


def ensure_directories():
    """Ensure data directories exist."""
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)


def generate_synthetic_transactions(n_transactions=5000, start_date=None, random_seed=42):
    """
    Generate realistic synthetic UPI transactions.
    """
    random.seed(random_seed)
    np.random.seed(random_seed)

    if start_date is None:
        start_date = datetime(2026, 1, 1)

    merchants = {
        "Food": ["Swiggy", "Zomato", "Restaurant", "Cafe", "Blinkit", "Zepto"],
        "Shopping": ["Amazon", "Flipkart", "Myntra", "Local Store", "Zara", "Nykaa"],
        "Travel": ["Uber", "Ola", "Metro", "IRCTC", "MakeMyTrip", "Rapido"],
        "Bills": ["Electricity", "Airtel", "Jio", "Water Bill", "Piped Gas", "Broadband"],
        "Entertainment": ["Netflix", "Spotify", "BookMyShow", "Hotstar", "Steam"],
        "Healthcare": ["Pharmacy", "Hospital", "Apollo 247", "1mg", "Dental Clinic"],
        "Education": ["Course", "Books", "Udemy", "College Fees", "Coursera"],
        "Groceries": ["DMart", "BigBasket", "Reliance Fresh", "Nature's Basket"]
    }
    categories = list(merchants.keys())

    transactions = []
    balance = 45000.0

    # Spread over ~240 days (8 months)
    days_range = 240

    for i in range(n_transactions):
        tx_id = f"TX{i + 1:05d}"
        days_offset = random.randint(0, days_range)
        tx_date = start_date + timedelta(days=days_offset)

        hour = random.randint(7, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        time_str = f"{hour:02d}:{minute:02d}:{second:02d}"

        # 88% Debit (Expenses), 12% Credit (Income/Refunds)
        is_expense = random.random() < 0.88

        if is_expense:
            tx_type = "Debit"
            category = random.choice(categories)
            merchant = random.choice(merchants[category])

            # Realistic amount distribution depending on category
            if category == "Bills":
                amount = round(random.uniform(400, 3500), 2)
                is_recurring = random.choice([True, True, False])
            elif category == "Food":
                amount = round(random.choice([random.uniform(80, 450), random.uniform(450, 1500)]), 2)
                is_recurring = False
            elif category == "Shopping":
                amount = round(random.uniform(300, 8000), 2)
                is_recurring = False
            elif category == "Travel":
                amount = round(random.uniform(60, 1800), 2)
                is_recurring = False
            elif category == "Entertainment":
                amount = round(random.uniform(199, 1200), 2)
                is_recurring = random.choice([True, False, False])
            elif category == "Healthcare":
                amount = round(random.uniform(150, 4500), 2)
                is_recurring = False
            elif category == "Education":
                amount = round(random.uniform(500, 6000), 2)
                is_recurring = False
            else:
                amount = round(random.uniform(100, 3000), 2)
                is_recurring = False

            # Occasional large anomaly transaction (contamination)
            if random.random() < 0.025:
                amount = round(random.uniform(12000, 35000), 2)

            balance -= amount
            if balance < 2500:
                balance += 25000.0  # replenish baseline

            payment_mode = random.choice(["UPI", "UPI", "UPI", "QR Code", "Credit Card", "Net Banking"])

        else:
            tx_type = "Credit"
            category = "Income"
            merchant = random.choice(["Salary", "Freelance Project", "Cashback", "UPI Refund", "Dividend", "Consulting"])

            if merchant == "Salary":
                amount = round(random.uniform(55000, 85000), 2)
                is_recurring = True
            elif merchant == "Freelance Project":
                amount = round(random.uniform(8000, 25000), 2)
                is_recurring = False
            else:
                amount = round(random.uniform(50, 3500), 2)
                is_recurring = False

            balance += amount
            payment_mode = "Bank Transfer" if merchant == "Salary" else "UPI"

        transactions.append({
            "transaction_id": tx_id,
            "date": tx_date.strftime("%Y-%m-%d"),
            "time": time_str,
            "amount": amount,
            "transaction_type": tx_type,
            "category": category,
            "merchant": merchant,
            "payment_mode": payment_mode,
            "balance_after_transaction": round(balance, 2),
            "is_recurring": is_recurring
        })

    df = pd.DataFrame(transactions)
    # Sort chronologically
    df = df.sort_values(by=["date", "time"]).reset_index(drop=True)
    return df


def clean_transactions(df):
    """
    Clean transaction dataframe.
    """
    df = df.copy()
    # Drop duplicates
    df = df.drop_duplicates()

    # Convert date and time
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Drop invalid rows
    df = df.dropna(subset=["date", "amount", "transaction_type", "category"])

    # Standardize string values
    df["transaction_type"] = df["transaction_type"].astype(str).str.strip().str.capitalize()
    df["category"] = df["category"].astype(str).str.strip()
    if "merchant" in df.columns:
        df["merchant"] = df["merchant"].astype(str).str.strip()
    if "payment_mode" in df.columns:
        df["payment_mode"] = df["payment_mode"].astype(str).str.strip()

    # Sort
    sort_cols = ["date"]
    if "time" in df.columns:
        sort_cols.append("time")
    df = df.sort_values(by=sort_cols).reset_index(drop=True)

    return df


def spending_level(amount):
    """Categorize spending magnitude."""
    if amount < 500:
        return "Low"
    elif amount < 2000:
        return "Medium"
    else:
        return "High"


def feature_engineer_transactions(df):
    """
    Apply feature engineering to transaction data.
    """
    df = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df["date"]):
        df["date"] = pd.to_datetime(df["date"])

    # Calendar features
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["day_of_week"] = df["date"].dt.dayofweek
    df["day_name"] = df["date"].dt.day_name()
    df["is_weekend"] = df["day_of_week"] >= 5

    # Spending level
    df["spending_level"] = df["amount"].apply(spending_level)

    # Monthly period
    df["month_period"] = df["date"].dt.to_period("M").astype(str)

    # Monthly aggregate spending (Debits)
    expense_df = df[df["transaction_type"].str.lower() == "debit"]
    monthly_spending = expense_df.groupby("month_period")["amount"].sum()
    df["monthly_spending"] = df["month_period"].map(monthly_spending).fillna(0)

    # Flags
    df["is_income"] = df["transaction_type"].str.lower() == "credit"
    df["is_expense"] = df["transaction_type"].str.lower() == "debit"

    return df


def calculate_safe_to_spend_data(df, buffer_percent=0.10, upcoming_bills=0.0):
    """
    Calculate dynamic Safe-to-Spend metrics from transactions.
    """
    df = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df["date"]):
        df["date"] = pd.to_datetime(df["date"])

    sort_cols = ["date"]
    if "time" in df.columns:
        sort_cols.append("time")
    df = df.sort_values(sort_cols)

    latest_row = df.iloc[-1]
    latest_date = latest_row["date"]

    current_balance = float(latest_row.get("balance_after_transaction", 25000.0))

    # Calculate average monthly income & expense
    income_df = df[df["transaction_type"].str.lower() == "credit"].copy()
    income_df["month_period"] = income_df["date"].dt.to_period("M").astype(str)
    monthly_income = income_df.groupby("month_period")["amount"].sum()
    avg_monthly_income = float(monthly_income.mean()) if not monthly_income.empty else 50000.0

    expense_df = df[df["transaction_type"].str.lower() == "debit"].copy()
    expense_df["month_period"] = expense_df["date"].dt.to_period("M").astype(str)
    monthly_expense = expense_df.groupby("month_period")["amount"].sum()
    avg_monthly_expense = float(monthly_expense.mean()) if not monthly_expense.empty else 30000.0

    predicted_monthly_spending = avg_monthly_expense

    # Days calculations
    day_of_month = latest_date.day
    # Estimated days in this month
    next_month = (latest_date.replace(day=28) + timedelta(days=4))
    last_day_of_month = (next_month - timedelta(days=next_month.day)).day
    days_remaining = max(1, last_day_of_month - day_of_month)

    remaining_expected_expense = (predicted_monthly_spending / last_day_of_month) * days_remaining

    safety_buffer = current_balance * buffer_percent

    safe_to_spend = max(0.0, current_balance - remaining_expected_expense - safety_buffer - upcoming_bills)
    daily_safe_spending = round(safe_to_spend / days_remaining, 2) if days_remaining > 0 else 0.0

    if safe_to_spend > 5000:
        message = "Healthy financial cushion. You are on track with your spending limits."
        status = "Healthy"
    elif safe_to_spend > 0:
        message = "Moderate buffer. Monitor non-essential discretionary expenses."
        status = "Moderate"
    else:
        message = "Warning: Spending buffer is zero or near overdraft. Strictly curb discretionary expenses!"
        status = "Critical"

    result_df = pd.DataFrame([{
        "latest_date": latest_date.strftime("%Y-%m-%d"),
        "current_balance": round(current_balance, 2),
        "average_monthly_income": round(avg_monthly_income, 2),
        "average_monthly_expense": round(avg_monthly_expense, 2),
        "predicted_monthly_spending": round(predicted_monthly_spending, 2),
        "remaining_expected_expense": round(remaining_expected_expense, 2),
        "safety_buffer": round(safety_buffer, 2),
        "safe_to_spend": round(safe_to_spend, 2),
        "daily_safe_spending": round(daily_safe_spending, 2),
        "days_remaining": days_remaining,
        "financial_message": message,
        "status": status
    }])

    return result_df


def get_or_create_datasets(force_regenerate=False):
    """
    Get the feature engineered dataset. If not found locally or in fallback path,
    generate, clean, feature engineer, and save.
    """
    ensure_directories()
    local_featured = os.path.join(PROCESSED_DIR, "feature_engineered_transactions.csv")
    local_safe = os.path.join(PROCESSED_DIR, "safe_to_spend_result.csv")
    local_raw = os.path.join(RAW_DIR, "synthetic_upi_transactions.csv")

    if not force_regenerate and os.path.exists(local_featured) and os.path.exists(local_safe):
        df = pd.read_csv(local_featured)
        df["date"] = pd.to_datetime(df["date"])
        safe_df = pd.read_csv(local_safe)
        return df, safe_df

    # Check fallback
    if not force_regenerate and os.path.exists(FALLBACK_PROCESSED_FILE) and os.path.exists(FALLBACK_SAFE_FILE):
        try:
            df = pd.read_csv(FALLBACK_PROCESSED_FILE)
            df["date"] = pd.to_datetime(df["date"])
            safe_df = pd.read_csv(FALLBACK_SAFE_FILE)
            # Copy to local for convenience
            df.to_csv(local_featured, index=False)
            safe_df.to_csv(local_safe, index=False)
            return df, safe_df
        except Exception:
            pass

    # Generate fresh
    print("Generating synthetic UPI transactions dataset...")
    raw_df = generate_synthetic_transactions(n_transactions=5000)
    raw_df.to_csv(local_raw, index=False)

    clean_df = clean_transactions(raw_df)
    clean_df.to_csv(os.path.join(PROCESSED_DIR, "clean_transactions.csv"), index=False)

    featured_df = feature_engineer_transactions(clean_df)
    featured_df.to_csv(local_featured, index=False)

    safe_df = calculate_safe_to_spend_data(featured_df)
    safe_df.to_csv(local_safe, index=False)

    return featured_df, safe_df


if __name__ == "__main__":
    df, safe_df = get_or_create_datasets(force_regenerate=True)
    print("Dataset ready! Rows:", len(df))
    print("Safe to Spend:", safe_df["safe_to_spend"].iloc[0])
