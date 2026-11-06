"""
Machine Learning and Financial Analytics Engine for UPI Financial Wellness Assistant.
Contains:
1. Spending Predictor (Linear Regression, Random Forest, Multi-month Forecast, Evaluation Metrics)
2. Anomaly Detection (Isolation Forest, Contamination tuning, Explanations, Live Transaction Evaluator)
3. Financial Simulators (What-If Analysis, Savings Goal Tracker, Smart Rule & ML Alerts)
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ==============================================================================
# 1. SPENDING PREDICTION & FORECASTING
# ==============================================================================

def prepare_monthly_spending_series(df):
    """
    Extracts monthly debit spending and creates time indexing.
    """
    expense_df = df[df["transaction_type"].str.lower() == "debit"].copy()
    if not pd.api.types.is_datetime64_any_dtype(expense_df["date"]):
        expense_df["date"] = pd.to_datetime(expense_df["date"])

    expense_df["month_period"] = expense_df["date"].dt.to_period("M").astype(str)

    monthly_data = (
        expense_df.groupby("month_period")["amount"]
        .sum()
        .reset_index()
        .rename(columns={"month_period": "month", "amount": "monthly_spending"})
    )
    monthly_data = monthly_data.sort_values("month").reset_index(drop=True)
    monthly_data["time_index"] = np.arange(len(monthly_data))
    return monthly_data


def train_spending_models(monthly_data, test_size=0.25, random_state=42):
    """
    Trains Linear Regression, Ridge, and Random Forest on monthly spending.
    Returns models, predictions, and evaluation metrics.
    """
    X = monthly_data[["time_index"]]
    y = monthly_data["monthly_spending"]

    n_samples = len(monthly_data)
    # Ensure test set has at least 1 record if enough data, else fit on all
    if n_samples >= 4:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, shuffle=False
        )
    else:
        X_train, X_test, y_train, y_test = X, X, y, y

    # 1. Linear Regression
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)

    # 2. Random Forest Regressor
    rf = RandomForestRegressor(n_estimators=50, random_state=random_state, max_depth=3)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)

    # Calculate metrics for Linear Regression
    mae_lr = mean_absolute_error(y_test, lr_pred)
    mse_lr = mean_squared_error(y_test, lr_pred)
    rmse_lr = np.sqrt(mse_lr)
    r2_lr = r2_score(y_test, lr_pred) if len(y_test) > 1 else 1.0

    # Calculate metrics for Random Forest
    mae_rf = mean_absolute_error(y_test, rf_pred)
    mse_rf = mean_squared_error(y_test, rf_pred)
    rmse_rf = np.sqrt(mse_rf)
    r2_rf = r2_score(y_test, rf_pred) if len(y_test) > 1 else 1.0

    metrics_df = pd.DataFrame([
        {
            "Model": "Linear Regression (Baseline)",
            "MAE (₹)": round(mae_lr, 2),
            "RMSE (₹)": round(rmse_lr, 2),
            "R² Score": round(r2_lr, 4),
            "Interpretation": "Strong trend capture, intuitive coefficients"
        },
        {
            "Model": "Random Forest Regressor",
            "MAE (₹)": round(mae_rf, 2),
            "RMSE (₹)": round(rmse_rf, 2),
            "R² Score": round(r2_rf, 4),
            "Interpretation": "Handles non-linear surges and holiday seasonality"
        }
    ])

    test_comparison = pd.DataFrame({
        "Month": monthly_data.iloc[X_test.index]["month"].values,
        "Actual (₹)": y_test.values,
        "Linear Regression (₹)": np.round(lr_pred, 2),
        "Random Forest (₹)": np.round(rf_pred, 2)
    })

    # Fit best model on all available data for future forecasting
    full_lr = LinearRegression().fit(X, y)
    full_rf = RandomForestRegressor(n_estimators=50, random_state=random_state, max_depth=3).fit(X, y)

    return {
        "lr_model": full_lr,
        "rf_model": full_rf,
        "metrics_df": metrics_df,
        "test_comparison": test_comparison,
        "slope": float(full_lr.coef_[0]),
        "intercept": float(full_lr.intercept_)
    }


def forecast_future_spending(monthly_data, trained_info, horizon_months=3, model_choice="Linear Regression"):
    """
    Generate forecast points for the next N months.
    """
    last_index = monthly_data["time_index"].max()
    last_month_str = monthly_data["month"].iloc[-1]
    last_period = pd.Period(last_month_str, freq="M")

    future_indices = np.arange(last_index + 1, last_index + 1 + horizon_months).reshape(-1, 1)
    future_periods = [(last_period + i).strftime("%Y-%m") for i in range(1, horizon_months + 1)]

    if model_choice == "Random Forest":
        preds = trained_info["rf_model"].predict(future_indices)
    else:
        preds = trained_info["lr_model"].predict(future_indices)

    # Add reasonable bounds based on historical standard deviation
    hist_std = float(monthly_data["monthly_spending"].std()) if len(monthly_data) > 1 else 2500.0
    lower_bounds = np.maximum(0, preds - (1.15 * hist_std))
    upper_bounds = preds + (1.15 * hist_std)

    forecast_df = pd.DataFrame({
        "Month": future_periods,
        "Forecasted Spending (₹)": np.round(preds, 2),
        "Lower Bound (₹)": np.round(lower_bounds, 2),
        "Upper Bound (₹)": np.round(upper_bounds, 2),
        "Type": ["Forecast"] * horizon_months
    })

    return forecast_df


def forecast_category_spending(df, top_n=5):
    """
    Provides monthly trends and growth rates for top spending categories.
    """
    expense_df = df[df["transaction_type"].str.lower() == "debit"].copy()
    expense_df["month"] = pd.to_datetime(expense_df["date"]).dt.to_period("M").astype(str)

    top_cats = expense_df.groupby("category")["amount"].sum().nlargest(top_n).index.tolist()
    cat_df = expense_df[expense_df["category"].isin(top_cats)].groupby(["month", "category"])["amount"].sum().reset_index()

    return cat_df


# ==============================================================================
# 2. UNUSUAL SPENDING & ANOMALY DETECTION
# ==============================================================================

def train_anomaly_detector(df, contamination=0.05, random_state=42):
    """
    Trains Isolation Forest to detect anomalous debit transactions.
    """
    expense_df = df[df["transaction_type"].str.lower() == "debit"].copy()
    if expense_df.empty:
        return df, None, {}

    # Feature extraction
    features = []
    # 1. Amount
    features.append(expense_df["amount"].values)

    # 2. Transaction hour if available
    if "time" in expense_df.columns:
        hours = pd.to_datetime(expense_df["time"], format="%H:%M:%S", errors="coerce").dt.hour.fillna(14).values
    else:
        hours = np.full(len(expense_df), 14)

    # 3. Weekend flag
    if "is_weekend" in expense_df.columns:
        is_weekend = expense_df["is_weekend"].astype(int).values
    else:
        is_weekend = (pd.to_datetime(expense_df["date"]).dt.dayofweek >= 5).astype(int).values

    X = np.column_stack([expense_df["amount"].values, hours, is_weekend])

    model = IsolationForest(
        contamination=contamination,
        random_state=random_state,
        n_estimators=100
    )
    model.fit(X)

    preds = model.predict(X)
    scores = model.decision_function(X)

    expense_df["anomaly_raw"] = preds
    expense_df["is_unusual"] = preds == -1
    # Lower decision function means more abnormal. Normalize to 0-100 anomaly severity index
    # Invert so higher score = higher abnormality
    min_score, max_score = scores.min(), scores.max()
    if max_score > min_score:
        severity = 100 * (1 - (scores - min_score) / (max_score - min_score))
    else:
        severity = np.zeros(len(scores))
    expense_df["anomaly_severity"] = np.round(severity, 1)

    # Add human-interpretable reasoning for each anomaly
    cat_medians = expense_df.groupby("category")["amount"].median().to_dict()
    reasons = []
    for _, row in expense_df.iterrows():
        if not row["is_unusual"]:
            reasons.append("Normal spending pattern")
        else:
            cat = row.get("category", "")
            amt = row["amount"]
            cat_med = cat_medians.get(cat, amt)
            mult = amt / cat_med if cat_med > 0 else 1.0

            if mult >= 3.0:
                reasons.append(f"Significant spike: {mult:.1f}x higher than median {cat} expense")
            elif amt > 15000:
                reasons.append(f"High-value lump transaction (₹{amt:,.0f})")
            elif row.get("is_weekend", False) and amt > 5000:
                reasons.append("High weekend discretionary surge")
            else:
                reasons.append("Statistical deviation from standard baseline")

    expense_df["anomaly_reason"] = reasons

    summary = {
        "total_expenses": len(expense_df),
        "unusual_count": int(expense_df["is_unusual"].sum()),
        "unusual_percent": round(100 * expense_df["is_unusual"].sum() / len(expense_df), 2),
        "unusual_total_amount": round(float(expense_df[expense_df["is_unusual"]]["amount"].sum()), 2),
        "avg_normal_amount": round(float(expense_df[~expense_df["is_unusual"]]["amount"].mean()), 2),
        "avg_unusual_amount": round(float(expense_df[expense_df["is_unusual"]]["amount"].mean()), 2)
    }

    return expense_df, model, summary


def evaluate_single_transaction_anomaly(amount, category, hour, is_weekend, model, historical_df):
    """
    Evaluates whether a prospective user-entered transaction is an anomaly.
    """
    X_single = np.array([[amount, hour, int(is_weekend)]])
    is_anomaly = bool(model.predict(X_single)[0] == -1)
    score = float(model.decision_function(X_single)[0])

    # Category comparison
    cat_df = historical_df[historical_df["category"] == category]
    if not cat_df.empty:
        cat_median = float(cat_df["amount"].median())
        cat_max = float(cat_df["amount"].max())
        ratio = amount / cat_median if cat_median > 0 else 1.0
    else:
        cat_median = 1000.0
        cat_max = 5000.0
        ratio = 1.0

    return {
        "is_anomaly": is_anomaly,
        "score": score,
        "cat_median": cat_median,
        "cat_max": cat_max,
        "ratio_to_median": round(ratio, 1)
    }


# ==============================================================================
# 3. FINANCIAL PLANNING & SIMULATORS
# ==============================================================================

def simulate_what_if_budget(df, cuts_dict):
    """
    Simulates budget reductions across specified categories.
    cuts_dict: e.g. {"Food": 20, "Shopping": 15, "Entertainment": 30} in percentages.
    """
    expense_df = df[df["transaction_type"].str.lower() == "debit"].copy()
    expense_df["month_period"] = pd.to_datetime(expense_df["date"]).dt.to_period("M").astype(str)
    n_months = max(1, expense_df["month_period"].nunique())

    current_cat_monthly = expense_df.groupby("category")["amount"].sum() / n_months

    simulation_results = []
    total_current_monthly = float(current_cat_monthly.sum())
    total_savings_monthly = 0.0

    for cat, monthly_amt in current_cat_monthly.items():
        cut_pct = float(cuts_dict.get(cat, 0.0))
        saved_amt = (monthly_amt * cut_pct) / 100.0
        new_amt = monthly_amt - saved_amt
        total_savings_monthly += saved_amt

        simulation_results.append({
            "Category": cat,
            "Current Monthly (₹)": round(monthly_amt, 2),
            "Cut (%)": cut_pct,
            "Monthly Savings (₹)": round(saved_amt, 2),
            "New Monthly (₹)": round(new_amt, 2)
        })

    sim_df = pd.DataFrame(simulation_results)
    sim_df = sim_df.sort_values("Monthly Savings (₹)", ascending=False).reset_index(drop=True)

    annual_savings = total_savings_monthly * 12
    three_year_compounded = annual_savings * 3 * 1.07  # ~7% index fund compounding

    return {
        "table": sim_df,
        "current_total_monthly": round(total_current_monthly, 2),
        "new_total_monthly": round(total_current_monthly - total_savings_monthly, 2),
        "monthly_savings": round(total_savings_monthly, 2),
        "annual_savings": round(annual_savings, 2),
        "three_year_compounded": round(three_year_compounded, 2)
    }


def simulate_savings_goal(goal_amount, current_savings, monthly_saving_capacity, timeline_months=None):
    """
    Calculates time or required monthly amount to reach a financial goal.
    """
    remaining_goal = max(0.0, goal_amount - current_savings)

    if timeline_months is not None and timeline_months > 0:
        required_per_month = remaining_goal / timeline_months
        feasible = required_per_month <= monthly_saving_capacity
        months_needed = timeline_months
    else:
        if monthly_saving_capacity > 0:
            months_needed = int(np.ceil(remaining_goal / monthly_saving_capacity))
            required_per_month = monthly_saving_capacity
            feasible = True
        else:
            months_needed = 999
            required_per_month = 0
            feasible = False

    # Trajectory points
    trajectory = []
    bal = current_savings
    for m in range(min(36, max(1, months_needed) + 1)):
        trajectory.append({
            "Month": f"M+{m}",
            "Projected Savings (₹)": min(goal_amount, round(bal, 2)),
            "Target Goal (₹)": goal_amount
        })
        bal += required_per_month

    traj_df = pd.DataFrame(trajectory)

    return {
        "remaining_goal": round(remaining_goal, 2),
        "months_needed": months_needed,
        "required_per_month": round(required_per_month, 2),
        "feasible": feasible,
        "trajectory_df": traj_df
    }


def generate_personalized_alerts(df, safe_df):
    """
    Scans transactions and financial status to generate intelligent, actionable alerts.
    """
    alerts = []
    expense_df = df[df["transaction_type"].str.lower() == "debit"].copy()
    income_df = df[df["transaction_type"].str.lower() == "credit"].copy()

    total_income = income_df["amount"].sum()
    total_expense = expense_df["amount"].sum()

    safe_to_spend = float(safe_df["safe_to_spend"].iloc[0]) if not safe_df.empty else 0.0
    current_balance = float(safe_df["current_balance"].iloc[0]) if not safe_df.empty else 0.0

    # 1. Cash flow deficit alert
    if total_expense > total_income:
        alerts.append({
            "level": "Critical",
            "icon": "🚨",
            "title": "Expense Exceeds Income Deficit",
            "description": f"Total outgoing expenses (₹{total_expense:,.0f}) exceed total credits (₹{total_income:,.0f}). You are drawing down reserves.",
            "recommendation": "Review high discretionary categories immediately and pause non-essential purchases."
        })

    # 2. Safe to spend warning
    if safe_to_spend <= 0:
        alerts.append({
            "level": "Warning",
            "icon": "⚠️",
            "title": "Zero Safe-to-Spend Balance",
            "description": f"Calculated Safe-to-Spend for this cycle is ₹0. Current balance is committed to pending obligations and buffer.",
            "recommendation": "Maintain a strict essential-only spending rule until the next salary or credit cycle."
        })
    elif safe_to_spend > 15000:
        alerts.append({
            "level": "Success",
            "icon": "✅",
            "title": "Healthy Surplus Available",
            "description": f"You currently have ₹{safe_to_spend:,.0f} in Safe-to-Spend headroom above your safety buffer.",
            "recommendation": "Consider routing 50% of this surplus into an automated SIP, emergency fund, or fixed deposit."
        })

    # 3. Large transaction detector
    large_tx = expense_df[expense_df["amount"] >= 20000]
    if not large_tx.empty:
        alerts.append({
            "level": "Warning",
            "icon": "💳",
            "title": f"{len(large_tx)} High-Value Transaction(s) Detected",
            "description": f"Detected {len(large_tx)} transactions of ₹20,000 or above, led by ₹{large_tx['amount'].max():,.0f} at {large_tx.iloc[0]['merchant']}.",
            "recommendation": "Verify these debit entries against your UPI records to ensure no unauthorized deductions occurred."
        })

    # 4. Weekend surge alert
    if "is_weekend" in expense_df.columns:
        weekend_sum = expense_df[expense_df["is_weekend"]]["amount"].sum()
        weekday_sum = expense_df[~expense_df["is_weekend"]]["amount"].sum()
        weekend_ratio = weekend_sum / (weekend_sum + weekday_sum) if (weekend_sum + weekday_sum) > 0 else 0
        if weekend_ratio > 0.40:
            alerts.append({
                "level": "Info",
                "icon": "🏖️",
                "title": "Weekend Spending Surge",
                "description": f"{weekend_ratio * 100:.1f}% of total expenses happen on Saturdays and Sundays (₹{weekend_sum:,.0f}).",
                "recommendation": "Set an explicit weekend UPI spending limit on your primary payment app."
            })

    # 5. Top category dominance alert
    cat_spending = expense_df.groupby("category")["amount"].sum()
    if not cat_spending.empty:
        top_cat = cat_spending.idxmax()
        top_cat_amt = cat_spending.max()
        top_cat_share = (top_cat_amt / total_expense) * 100 if total_expense > 0 else 0
        if top_cat_share > 30:
            alerts.append({
                "level": "Info",
                "icon": "📊",
                "title": f"Category Concentration: {top_cat}",
                "description": f"The '{top_cat}' category consumes {top_cat_share:.1f}% (₹{top_cat_amt:,.0f}) of all your expenses.",
                "recommendation": f"Focusing budget optimization primarily on {top_cat} will yield the highest cost savings."
            })

    # 6. Recurring commitments alert
    if "is_recurring" in expense_df.columns:
        rec_sum = expense_df[expense_df["is_recurring"]]["amount"].sum()
        alerts.append({
            "level": "Info",
            "icon": "🔄",
            "title": "Recurring Bill Burden",
            "description": f"Recurring commitments total ₹{rec_sum:,.0f} across subscription, utility, and recurring merchants.",
            "recommendation": "Audit your active auto-pay mandates and cancel unused streaming or app subscriptions."
        })

    return alerts
