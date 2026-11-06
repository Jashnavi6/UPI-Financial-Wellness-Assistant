# 📜 Step-by-Step CLI Pipeline Scripts

This folder contains the complete pedagogical and operational CLI pipeline for the **UPI Financial Wellness & Predictive Spending Assistant**, arranged chronologically from environment setup to production machine learning models and alert generators.

---

## 🗂️ Script Catalog

| # | Script Name | Phase | Description |
|---|-------------|-------|-------------|
| **01** | [`01_library_check.py`](file:///c:/Users/jashn/upi/scripts/01_library_check.py) | Phase 1 | Verifies installation of core Python libraries (`pandas`, `numpy`, `sklearn`, `streamlit`, `plotly`, `matplotlib`). |
| **02** | [`02_schema_inspection.py`](file:///c:/Users/jashn/upi/scripts/02_schema_inspection.py) | Phase 1 | Generates a toy transaction schema for initial verification. |
| **03** | [`03_generate_transactions.py`](file:///c:/Users/jashn/upi/scripts/03_generate_transactions.py) | Phase 1 | Synthesizes a realistic dataset of 5,000 UPI transactions across 8 merchant categories with seasonal trends. |
| **04** | [`04_data_cleaning.py`](file:///c:/Users/jashn/upi/scripts/04_data_cleaning.py) | Phase 2 | Handles missing values, duplicates, datetime conversions, and sorts transactions chronologically. |
| **05** | [`05_feature_engineering.py`](file:///c:/Users/jashn/upi/scripts/05_feature_engineering.py) | Phase 2 | Extracts calendar dimensions, weekend flags, spending level classifications, and rolling monthly sums. |
| **06** | [`06_eda_analysis.py`](file:///c:/Users/jashn/upi/scripts/06_eda_analysis.py) | Phase 3 | Exploratory Data Analysis calculating category breakdowns, payment modes, and recurring expense stats. |
| **07** | [`07_visualizations.py`](file:///c:/Users/jashn/upi/scripts/07_visualizations.py) | Phase 3 | Renders and saves 9 high-resolution Matplotlib/Seaborn visualization plots into `visualizations/`. |
| **08** | [`08_spending_prediction.py`](file:///c:/Users/jashn/upi/scripts/08_spending_prediction.py) | Phase 4 | Trains Linear Regression models on monthly debit trends to forecast future expenditure. |
| **09** | [`09_anomaly_detection.py`](file:///c:/Users/jashn/upi/scripts/09_anomaly_detection.py) | Phase 4 | Implements Scikit-Learn's `IsolationForest` to isolate outlier transactions and spending spikes. |
| **10** | [`10_model_evaluation.py`](file:///c:/Users/jashn/upi/scripts/10_model_evaluation.py) | Phase 4 | Benchmarks predictive regression algorithms using MAE, MSE, RMSE, and R² scores. |
| **11** | [`11_safe_to_spend.py`](file:///c:/Users/jashn/upi/scripts/11_safe_to_spend.py) | Phase 5 | Computes dynamic daily and weekly safe spending allowances with safety buffers. |
| **12** | [`12_what_if_simulator.py`](file:///c:/Users/jashn/upi/scripts/12_what_if_simulator.py) | Phase 5 | Simulates the compounding effect of cutbacks across discretionary categories over 1, 3, and 5 years. |
| **13** | [`13_savings_simulator.py`](file:///c:/Users/jashn/upi/scripts/13_savings_simulator.py) | Phase 5 | Evaluates feasibility and milestone trajectories toward emergency funds and savings goals. |
| **14** | [`14_personalized_alerts.py`](file:///c:/Users/jashn/upi/scripts/14_personalized_alerts.py) | Phase 6 | Evaluates cashflow risk thresholds to trigger real-time deficit, high-value, and concentration alerts. |

---

## 💻 How to Run Any Script

From the root project directory:
```bash
python scripts/04_data_cleaning.py
python scripts/08_spending_prediction.py
python scripts/11_safe_to_spend.py
```
Or navigate into the `scripts/` directory:
```bash
cd scripts
python 04_data_cleaning.py
```
All scripts automatically detect the repository root and resolve `src/` modules and `data/` files without any manual path adjustments.
