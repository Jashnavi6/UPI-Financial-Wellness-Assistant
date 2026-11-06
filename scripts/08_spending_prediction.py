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
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("=" * 70)
print("PHASE 3 - STEP 10: SPENDING PREDICTION")
print("=" * 70)


# ---------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------

print("\n1. Loading feature-engineered dataset...")

df = pd.read_csv(
    __import__("config").get_data_path("processed/feature_engineered_transactions.csv")
)

print("Dataset loaded successfully!")

print("\nFirst 10 rows:")
print(df.head(10))


# ---------------------------------------------------------
# 2. CONVERT DATE
# ---------------------------------------------------------

print("\n2. Converting date...")

df["date"] = pd.to_datetime(
    df["date"]
)

print("Date conversion completed.")


# ---------------------------------------------------------
# 3. SELECT EXPENSE TRANSACTIONS
# ---------------------------------------------------------

print("\n3. Selecting expense transactions...")

expense_df = df[
    df["transaction_type"] == "Debit"
].copy()

print("Expense transactions:")
print(len(expense_df))


# ---------------------------------------------------------
# 4. CREATE MONTHLY DATA
# ---------------------------------------------------------

print("\n4. Creating monthly spending dataset...")

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
# 5. CREATE TIME INDEX
# ---------------------------------------------------------

print("\n5. Creating time index...")

monthly_data["time_index"] = (
    np.arange(len(monthly_data))
)

print(
    monthly_data
)


# ---------------------------------------------------------
# 6. CHECK DATA
# ---------------------------------------------------------

print("\n6. Number of monthly records:")

print(
    len(monthly_data)
)


# ---------------------------------------------------------
# 7. PREPARE FEATURES
# ---------------------------------------------------------

print("\n7. Preparing ML features...")

X = monthly_data[
    ["time_index"]
]

y = monthly_data[
    "monthly_spending"
]

print("\nFeature X:")
print(X)

print("\nTarget y:")
print(y)


# ---------------------------------------------------------
# 8. TRAIN TEST SPLIT
# ---------------------------------------------------------

print("\n8. Splitting data into training and testing...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nTraining records:")
print(len(X_train))

print("\nTesting records:")
print(len(X_test))


# ---------------------------------------------------------
# 9. CREATE MODEL
# ---------------------------------------------------------

print("\n9. Creating Linear Regression model...")

model = LinearRegression()

print("Model created successfully.")


# ---------------------------------------------------------
# 10. TRAIN MODEL
# ---------------------------------------------------------

print("\n10. Training model...")

model.fit(
    X_train,
    y_train
)

print("Model training completed!")


# ---------------------------------------------------------
# 11. MAKE PREDICTIONS
# ---------------------------------------------------------

print("\n11. Making predictions...")

predictions = model.predict(
    X_test
)

print("\nActual vs Predicted:")

results = pd.DataFrame({

    "Actual_Spending": y_test.values,

    "Predicted_Spending": predictions

})

print(results)


# ---------------------------------------------------------
# 12. MODEL EVALUATION
# ---------------------------------------------------------

print("\n12. MODEL EVALUATION")

mae = mean_absolute_error(
    y_test,
    predictions
)

mse = mean_squared_error(
    y_test,
    predictions
)

rmse = np.sqrt(mse)

r2 = r2_score(
    y_test,
    predictions
)

print("\nMean Absolute Error:")

print(
    round(mae, 2)
)

print("\nMean Squared Error:")

print(
    round(mse, 2)
)

print("\nRoot Mean Squared Error:")

print(
    round(rmse, 2)
)

print("\nR2 Score:")

print(
    round(r2, 4)
)


# ---------------------------------------------------------
# 13. PREDICT NEXT MONTH
# ---------------------------------------------------------

print("\n13. PREDICTING NEXT MONTH SPENDING...")

last_index = monthly_data[
    "time_index"
].max()

next_month_index = (
    last_index + 1
)

next_month_prediction = model.predict(
    [[next_month_index]]
)

print(
    "\nPredicted next month spending:"
)

print(
    "₹",
    round(
        next_month_prediction[0],
        2
    )
)


# ---------------------------------------------------------
# 14. SAVE PREDICTION
# ---------------------------------------------------------

prediction_output = pd.DataFrame({

    "predicted_next_month_spending":
    [next_month_prediction[0]]

})

prediction_output.to_csv(
    __import__("config").get_data_path("processed/spending_prediction.csv", for_writing=True),
    index=False
)

print("\nPrediction saved successfully!")

print(
    "Location: ",
    __import__("config").get_data_path("processed/spending_prediction.csv", for_writing=True)
)

print("\nSPENDING PREDICTION COMPLETED!")

print("=" * 70)