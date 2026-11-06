# ⚙️ Core Application Source Modules (`src/`)

This directory contains the production backend modules that power the **UPI Financial Wellness & Predictive Spending Assistant** web application.

---

## 📦 Module Overview

- [`auth_manager.py`](file:///c:/Users/jashn/upi/src/auth_manager.py): Secure user authentication engine implementing salted SHA-256 password hashing, user registration, and persistent JSON profile storage in `data/users.json`.
- [`login_ui.py`](file:///c:/Users/jashn/upi/src/login_ui.py): Glassmorphism Streamlit UI components for user login, account registration, demo user profiles, and active session badges.
- [`chatbot_engine.py`](file:///c:/Users/jashn/upi/src/chatbot_engine.py): Natural language conversational assistant grounded in the user's active transaction ledger, supporting affordability checks, merchant queries, and financial briefings.
- [`ml_models.py`](file:///c:/Users/jashn/upi/src/ml_models.py): Machine learning core implementing `LinearRegression`, `RandomForestRegressor`, `IsolationForest` anomaly detector, What-If simulation algorithms, and smart alert rules.
- [`data_engine.py`](file:///c:/Users/jashn/upi/src/data_engine.py): End-to-end data pipeline managing synthetic UPI transaction generation, data cleaning, calendar feature engineering, and Safe-to-Spend calculations.
- [`config.py`](file:///c:/Users/jashn/upi/src/config.py): Environment configuration resolving relative and system paths across platforms, and ensuring UTF-8 console output.
