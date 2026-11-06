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
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

print("=" * 70)
print("PHASE 3 - STEP 12: MODEL EVALUATION")
print("=" * 70)


# ---------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------

print("\n1. Loading dataset...")

df = pd.read_csv(
    __import__("config").get_data_path("processed/feature_engineered_transactions.csv")
)

print("Dataset loaded!")


# ---------------------------------------------------------
# 2. CONVERT DATE
# ---------------------------------------------------------

df["date"] = pd.to_datetime(
    df["date"]
)


# ---------------------------------------------------------
# 3. EXPENSE DATA
# ---------------------------------------------------------

print("\n2. Preparing expense data...")

expense_df = df[
    df["transaction_type"] == "Debit"
].copy()


# ---------------------------------------------------------
# 4. MONTHLY SPENDING
# ---------------------------------------------------------

expense_df["month"] = (
    expense_df["date"]
    .dt.to_period("M")
)

monthly_data = (
    expense_df
    .groupby("month")["amount"]
    .sum()
    .reset_index()
)

monthly_data.columns = [
    "month",
    "monthly_spending"
]

print("\nMonthly spending:")
print(monthly_data)


# ---------------------------------------------------------
# 5. TIME INDEX
# ---------------------------------------------------------

monthly_data["time_index"] = (
    np.arange(
        len(monthly_data)
    )
)


# ---------------------------------------------------------
# 6. FEATURES AND TARGET
# ---------------------------------------------------------

print("\n3. Preparing X and y...")

X = monthly_data[
    ["time_index"]
]

y = monthly_data[
    "monthly_spending"
]


# ---------------------------------------------------------
# 7. TRAIN TEST SPLIT
# ---------------------------------------------------------

print("\n4. Splitting dataset...")

X_train, X_test, y_train, y_test = (
    train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )
)

print(
    "Training records:",
    len(X_train)
)

print(
    "Testing records:",
    len(X_test)
)


# ---------------------------------------------------------
# 8. MODEL
# ---------------------------------------------------------

print("\n5. Creating model...")

model = LinearRegression()

model.fit(
    X_train,
    y_train
)

print(
    "Model trained successfully!"
)


# ---------------------------------------------------------
# 9. PREDICTION
# ---------------------------------------------------------

print("\n6. Making test predictions...")

y_pred = model.predict(
    X_test
)

print("\nPredictions:")
print(y_pred)


# ---------------------------------------------------------
# 10. MAE
# ---------------------------------------------------------

mae = mean_absolute_error(
    y_test,
    y_pred
)

print(
    "\n7. Mean Absolute Error (MAE):"
)

print(
    round(mae, 2)
)


# ---------------------------------------------------------
# 11. MSE
# ---------------------------------------------------------

mse = mean_squared_error(
    y_test,
    y_pred
)

print(
    "\n8. Mean Squared Error (MSE):"
)

print(
    round(mse, 2)
)


# ---------------------------------------------------------
# 12. RMSE
# ---------------------------------------------------------

rmse = np.sqrt(
    mse
)

print(
    "\n9. Root Mean Squared Error (RMSE):"
)

print(
    round(rmse, 2)
)


# ---------------------------------------------------------
# 13. R2
# ---------------------------------------------------------

r2 = r2_score(
    y_test,
    y_pred
)

print(
    "\n10. R2 SCORE:"
)

print(
    round(r2, 4)
)


# ---------------------------------------------------------
# 14. INTERPRETATION
# ---------------------------------------------------------

print("\n11. MODEL INTERPRETATION")

print(
    "MAE tells us the average prediction error."
)

print(
    "RMSE gives more importance to larger errors."
)

print(
    "R2 indicates how much variation is explained "
    "by the model."
)

print(
    "\nHigher R2 is generally better, "
    "while lower MAE/RMSE means smaller errors."
)


# ---------------------------------------------------------
# 15. SAVE METRICS
# ---------------------------------------------------------

metrics = pd.DataFrame({

    "metric": [
        "MAE",
        "MSE",
        "RMSE",
        "R2"
    ],

    "value": [
        mae,
        mse,
        rmse,
        r2
    ]
})

output_file = (
    __import__("config").get_data_path("processed/model_evaluation.csv", for_writing=True)
)

metrics.to_csv(
    output_file,
    index=False
)

print(
    "\nEvaluation metrics saved!"
)

print(
    "Location: ",
    __import__("config").get_data_path("processed/model_evaluation.csv", for_writing=True)
)

print(
    "\nMODEL EVALUATION COMPLETED!"
)

print("=" * 70)