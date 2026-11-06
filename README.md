# 💰 AI-Powered UPI Financial Wellness & Predictive Spending Assistant

An end-to-end intelligent financial management platform built with **Python**, **Streamlit**, **Scikit-Learn**, **Plotly**, and **Pandas**. 

The application helps UPI users understand their cashflow, forecast upcoming monthly outflows using Machine Learning regression models, detect anomalous and irregular spending with Isolation Forests, dynamically calculate daily Safe-to-Spend allowances, simulate budget reductions with What-If analytics, and work toward savings goals.

---

## 🚀 Key Features

### 0. 🔐 User Authentication & Personal Profile Dashboard
- **Dedicated Authentication Gateway:** Secure access gate with modern dark fintech glassmorphism design.
- **3-Tab Authentication Portal:**
  - **🔐 Sign In:** Authenticate via username or email with SHA-256 + salt password verification.
  - **✨ Create Account:** Register a new user with personal financial targets (monthly income baseline & target savings goal).
  - **🚀 1-Click Demo Access:** Instant 1-click evaluation profiles for `Jashnavi` (Premium Member • Admin) and `Demo Analyst` (Standard User).
- **Persistent User Registry:** Offline account store in `data/users.json`.
- **User Profile Cards:** Displays active user badge in top bar and interactive sidebar profile with income target, goal trajectory, and 1-click Sign Out.

### 1. 📊 Financial Dashboard & Exploratory Data Analysis (EDA)
- **Top Metrics:** Real-time Current Balance, Total Income, Total Outflow, Net Savings, Savings Rate (%), and Safe-to-Spend headroom.
- **Visual Analytics:**
  - Horizontal bar breakdown of spending across merchant categories (Food, Shopping, Travel, Bills, Entertainment, Groceries, Healthcare, Education).
  - Monthly cashflow trendline comparing Credits (Income) vs. Debits (Expenses).
  - Donut distribution of payment modes (UPI, QR Code, Net Banking, Credit Card, Bank Transfer).
  - Recurring auto-pay mandates vs. one-time discretionary expenses.
  - Top 10 Merchants by expenditure volume.
  - Filterable, searchable transaction history table.

### 2. 💬 AI Financial Chatbot & Conversational Assistant
- **Context-Aware Intelligence:** Real-time conversational assistant connected directly to your active transaction ledger.
- **Natural Language Affordability Check:** Ask *"Can I afford to buy an iPad for ₹35,000?"* — the bot calculates immediate impact on your Safe-to-Spend limit, committed bills, and remaining balance.
- **Spending Queries by Category & Merchant:** Inquire about specific categories (*"How much did I spend on Food?"*) or specific merchants (*"Tell me about my Swiggy expenses"*).
- **Anomaly & Forecast Reports:** Summarizes detected unusual spending and next month's ML predictive trajectory upon request.
- **Quick Action Prompts:** One-click pre-built prompt pills for instant financial briefings.

### 3. 🤖 Machine Learning Spending Prediction & Forecasting
- **Multi-Model Regression:** Trains and compares **Linear Regression** and non-linear **Random Forest Regressors** on monthly expenditure trends.
- **Multi-Month Horizon:** Interactive slider to forecast 1 to 12 months ahead with upper and lower standard deviation confidence intervals.
- **Statistical Evaluation Metrics:** Benchmarks Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared Error (RMSE), and R² Score.
- **Category-Level Trajectory:** Tracks and plots time-series growth rates for top spending categories.

### 3. 🔍 Machine Learning Unusual Spending & Anomaly Detection
- **Isolation Forest Model:** Unsupervised tree algorithm that identifies spending outliers, accidental high-value debits, and potential fraudulent transactions.
- **Configurable Sensitivity:** Dynamic contamination slider (1% to 15%) adjusting anomaly thresholds in real-time.
- **Interpretability & Severity:** Ranks each anomaly with a 0–100 severity index and provides human-readable explanations (e.g. *"Spike: 4.2x higher than category median"*).
- **⚡ Live Single-Transaction Anomaly Tester:** Enter a hypothetical transaction (Amount, Category, Hour of Day, Weekend) to let the ML model evaluate it on the fly.

### 4. 🛡️ Dynamic Safe-to-Spend Financial Planner
- **Formula-Driven Cushioning:**
  $$\text{Safe-to-Spend} = \max\left(0, \text{Current Balance} - \text{Expected Remaining Expenses} - \text{Safety Buffer} - \text{Committed Bills}\right)$$
- **Interactive Controls:** Adjust current balance, safety buffer percentage (5% to 40%), and upcoming fixed bills/rent.
- **Actionable Outputs:** Generates **Daily Safe Allowance** (₹/day), **Weekly Safe Allowance** (₹/week), and an interactive waterfall chart detailing capital distribution.

### 5. 💡 What-If Category Spending Simulator
- **Scenario Modeling:** Adjust percentage cutback sliders (0% to 50%) across key discretionary categories.
- **Compounding Analysis:** Live calculations of monthly savings, annual savings, and 3-year compounded investment growth.
- **Side-by-Side Comparison:** Grouped visual bar charts comparing current vs. proposed budgets.

### 6. 🎯 Savings Goal & Emergency Fund Simulator
- **Milestone Tracking:** Input a goal amount (e.g., Emergency Fund, Vacation, Downpayment) and target date or monthly capacity.
- **Feasibility Evaluation:** Automatically checks if required monthly contributions align with historical net income surplus.
- **Trajectory Visualizer:** Interactive milestone line chart projecting monthly savings progress toward the target.
- **Emergency Reserve Benchmarks:** Formulates 3-month and 6-month safety net targets based on actual monthly expenses.

### 7. 🚨 Personalized Financial Alerts & Smart Insights
- Rule-based and ML alerts detecting:
  - ⚠️ Expense exceeding income deficit warnings.
  - 💳 High-value transaction flags (transactions ≥ ₹20,000).
  - 🏖️ Weekend spending surges (>40% of spend concentrated on Saturdays/Sundays).
  - 📊 High category concentration (single category consuming >30% of outflow).
  - 🔄 Recurring subscription and auto-pay burden.

### 8. 📁 Data Studio & Statement Uploader
- **Custom CSV Statement Uploader:** Upload any bank or UPI statement CSV (Google Pay, PhonePe, Paytm, HDFC, SBI, ICICI). The app automatically cleans and engineers features to display your personal data.
- **Synthetic Data Generator:** Generate fresh realistic synthetic datasets with 1,000 to 10,000 transactions at the click of a button.
- **Ledger Export:** Download cleaned and feature-engineered datasets with one click.

---

## 📥 Installation & Setup

1. **Clone the repository:**
```bash
git clone https://github.com/Jashnavi6/upi-financial-wellness-assistant.git
cd upi-financial-wellness-assistant
```

2. **Create and activate a virtual environment (recommended):**
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

3. **Install required packages:**
```bash
pip install -r requirements.txt
```

---

## 🛠️ How to Run the Application

### Option A: Standard Python (Works with VS Code ▶️ Play Button)
You can now run directly using standard `python`:
```bash
python run.py
```
*or*
```bash
python app.py
```
In **VS Code**, you can simply open `app.py` or `run.py` and click the top-right **▶️ Run Python File (Play)** button, or press **F5**!

### Option B: Streamlit Command
Run in your terminal:streamlit run app.py


The app will open automatically in your browser at http://localhost:8501.

---

## 📂 Project Structure

`	ext
upi/
├── .gitignore                         # Excludes cache (__pycache__), IDE files, credentials
├── requirements.txt                   # Production Python package requirements
├── LICENSE                            # Open-source MIT License
├── README.md                          # Project documentation & execution guide
├── app.py                             # Main Streamlit web application & AI/ML dashboard
├── run.py                             # Standard Python Launcher (VS Code ▶️ Play button)
│
├── src/                               # ⚙️ Core Application Source Modules
│   ├── __init__.py
│   ├── auth_manager.py                # Secure SHA-256 + salt authentication manager
│   ├── login_ui.py                    # Modern glassmorphism UI for login/register/profile
│   ├── chatbot_engine.py              # Context-aware AI financial conversational assistant
│   ├── ml_models.py                   # ML algorithms (Random Forest, Linear Regression, Isolation Forest)
│   ├── data_engine.py                 # Synthetic data generator & feature engineering pipeline
│   ├── config.py                      # Cross-platform data path helper & UTF-8 console setup
│   └── README.md                      # Source modules documentation
│
├── scripts/                           # 📜 Step-by-Step CLI Pipeline Modules (Phases 1-6)
│   ├── 01_library_check.py            # Phase 1: Environment & library import verification
│   ├── 02_schema_inspection.py        # Phase 1: Raw schema & toy dataset test
│   ├── 03_generate_transactions.py    # Phase 1: Synthetic 5,000 transaction dataset generator
│   ├── 04_data_cleaning.py            # Phase 2: Data cleaning and missing value handling
│   ├── 05_feature_engineering.py      # Phase 2: Calendar extraction & spending levels
│   ├── 06_eda_analysis.py             # Phase 3: Exploratory data analysis
│   ├── 07_visualizations.py           # Phase 3: Matplotlib & Seaborn plot generator
│   ├── 08_spending_prediction.py      # Phase 4: Regression spending forecasting
│   ├── 09_anomaly_detection.py        # Phase 4: Isolation Forest outlier detection
│   ├── 10_model_evaluation.py         # Phase 4: Model evaluation metrics (MAE, RMSE, R²)
│   ├── 11_safe_to_spend.py            # Phase 5: Dynamic Safe-to-Spend calculator
│   ├── 12_what_if_simulator.py        # Phase 5: Category cutback simulation
│   ├── 13_savings_simulator.py        # Phase 5: Goal trajectory & emergency reserve planner
│   ├── 14_personalized_alerts.py      # Phase 6: Risk detection & smart financial alerts
│   └── README.md                      # Pipeline catalog and execution guide
│
├── data/                              # 📊 Datasets & Local Database
│   ├── users.json                     # Local user authentication profiles
│   ├── raw/
│   │   └── synthetic_upi_transactions.csv
│   └── processed/
│       ├── clean_transactions.csv
│       ├── feature_engineered_transactions.csv
│       ├── safe_to_spend_result.csv
│       ├── spending_prediction.csv
│       ├── anomaly_detection_results.csv
│       ├── model_evaluation.csv
│       └── personalized_financial_alerts.csv
│
├── visualizations/                    # 📈 Pre-generated EDA Figures (PNG)
│   ├── 01_spending_by_category.png
│   ├── 02_debit_vs_credit.png
│   ├── 03_payment_mode.png
│   ├── 04_recurring_transactions.png
│   ├── 05_transactions_over_time.png
│   ├── 06_amount_distribution.png
│   ├── 07_top_merchants.png
│   ├── 08_income_vs_expenses.png
│   └── 09_transactions_by_category.png
│
├── assets/                            # 🎨 Brand Assets & Chatbot Badges
│   ├── chatbot_icon.png
│   ├── chatbot_logo.png
│   └── ...
│
└── .streamlit/
    └── config.toml                    # Server & headless display settings
`

---

## 📦 Required Dependencies
- Python 3.10+
- streamlit
- pandas
- 
umpy
- scikit-learn
- plotly
- matplotlib
=======
# UPI-Financial-Wellness-Assistant
AI-powered UPI spending analysis and financial wellness prediction system
>>>>>>> d929b308f52bcb1a426b18fcabed9f538bad0c0e
