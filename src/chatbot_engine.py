"""
AI Financial Chatbot & Conversational Reasoning Engine for UPI Financial Wellness Assistant.
Provides context-aware natural language understanding, dynamic financial calculation,
and tailored recommendations based on the user's active transaction ledger.
"""

import re
import numpy as np
import pandas as pd
from datetime import datetime
import data_engine
import ml_models


class FinancialChatbot:
    """
    Intelligent conversational assistant grounded in the user's actual UPI ledger.
    """

    def __init__(self, df, safe_df=None):
        self.df = df.copy()
        if not pd.api.types.is_datetime64_any_dtype(self.df["date"]):
            self.df["date"] = pd.to_datetime(self.df["date"], errors="coerce")

        self.expense_df = self.df[self.df["transaction_type"].str.lower() == "debit"].copy()
        self.income_df = self.df[self.df["transaction_type"].str.lower() == "credit"].copy()

        if safe_df is not None and not safe_df.empty:
            self.safe_df = safe_df
        else:
            self.safe_df = data_engine.calculate_safe_to_spend_data(self.df)

        # Precalculate key statistics safely
        self.total_income = float(self.income_df["amount"].sum())
        self.total_expense = float(self.expense_df["amount"].sum())
        self.current_balance = float(self.safe_df["current_balance"].iloc[0]) if "current_balance" in self.safe_df.columns else 25000.0
        self.safe_to_spend = float(self.safe_df["safe_to_spend"].iloc[0]) if "safe_to_spend" in self.safe_df.columns else 0.0
        self.daily_safe = float(self.safe_df["daily_safe_spending"].iloc[0]) if "daily_safe_spending" in self.safe_df.columns else 0.0
        self.days_remaining = int(self.safe_df["days_remaining"].iloc[0]) if "days_remaining" in self.safe_df.columns else 15
        if "status" in self.safe_df.columns:
            self.status = str(self.safe_df["status"].iloc[0])
        else:
            self.status = "Healthy" if self.safe_to_spend > 5000 else ("Moderate" if self.safe_to_spend > 0 else "Caution")

    def respond(self, user_prompt):
        """
        Processes natural language query and generates data-grounded response.
        """
        text = user_prompt.strip().lower()

        # 1. Greeting & Help
        if any(w in text for w in ["hello", "hi", "hey", "who are you", "what can you do", "help"]):
            return self._handle_greeting()

        # 2. Safe-to-Spend & Daily Budget Queries ("How much can I spend today? / What is my safe daily limit?")
        if any(w in text for w in ["safe to spend", "daily budget", "daily limit", "spend today", "how much can i spend", "how much can i safely spend"]):
            return self._handle_safe_to_spend()

        # 3. Affordability Check ("Can I afford ₹X / buy a phone for 15000")
        if any(w in text for w in ["can i afford", "afford", "can i buy", "should i buy", "can i spend"]):
            return self._handle_affordability(text)

        # 4. Unusual Spending & Anomaly / Fraud Queries
        if any(w in text for w in ["unusual", "anomaly", "fraud", "suspicious", "outlier", "irregular"]):
            return self._handle_anomalies()

        # 5. Spending Prediction & Forecast Queries
        if any(w in text for w in ["forecast", "predict", "next month", "future spending", "future expense"]):
            return self._handle_forecast()

        # 6. Specific Merchant Queries (e.g. Swiggy, Zomato, Amazon, Uber, Netflix)
        merchant_match = self._find_merchant_in_query(text)
        if merchant_match:
            return self._handle_merchant_query(merchant_match)

        # 7. Category Queries (e.g. Food, Shopping, Travel, Bills, Groceries, Entertainment)
        category_match = self._find_category_in_query(text)
        if category_match:
            return self._handle_category_query(category_match)

        # 8. Savings Advice & How to Cut Costs
        if any(w in text for w in ["save", "saving", "cut cost", "reduce", "budget tip", "advice", "save money"]):
            return self._handle_savings_advice()

        # 9. Largest / Biggest Expense
        if any(w in text for w in ["biggest", "largest", "highest expense", "maximum spend"]):
            return self._handle_largest_expenses()

        # 10. Balance & Cashflow Overview
        if any(w in text for w in ["balance", "cashflow", "summary", "income", "overview", "net savings"]):
            return self._handle_cashflow_overview()

        # 11. Recurring Mandates & Bills
        if any(w in text for w in ["recurring", "mandate", "subscription", "bills", "autopay"]):
            return self._handle_recurring()

        # Fallback Comprehensive Financial Briefing
        return self._handle_default_fallback(user_prompt)

    # --------------------------------------------------------------------------
    # HANDLERS
    # --------------------------------------------------------------------------

    def _handle_greeting(self):
        return f"""
👋 **Hello! I am your AI Financial Wellness Assistant.**

I have real-time access to your UPI ledger ({len(self.df):,} transactions). Here is what you can ask me:

- 🛡️ *"How much can I safely spend today?"*
- 📱 *"Can I afford to buy an item for ₹15,000?"*
- 🍕 *"How much did I spend on Food or Swiggy?"*
- 🚨 *"Are there any unusual or anomalous transactions?"*
- 🔮 *"What is my predicted spending for next month?"*
- 💡 *"How can I save ₹10,000 this month?"*
- 📊 *"Give me an overview of my cashflow and balance."*

Feel free to type your question below!
"""

    def _handle_affordability(self, text):
        # Extract numerical amount from text
        numbers = re.findall(r"₹?\s*(\d+[\d,]*)", text)
        cleaned_numbers = []
        for n in numbers:
            try:
                cleaned_numbers.append(float(n.replace(",", "")))
            except ValueError:
                pass

        if not cleaned_numbers:
            return """
🤔 **Please specify the purchase amount!**  
For example:  
- *"Can I afford to spend ₹8,500 on a smartwatch?"*  
- *"Can I buy a laptop for 45000?"*
"""
        target_amount = cleaned_numbers[0]
        safe_val = self.safe_to_spend
        rem_balance_after = self.current_balance - target_amount

        if target_amount <= safe_val:
            headroom = safe_val - target_amount
            return f"""
### ✅ Yes, You Can Afford This!

- **Requested Expense:** ₹{target_amount:,.2f}
- **Current Safe-to-Spend Capacity:** ₹{safe_val:,.2f}
- **Remaining Safe Headroom After Purchase:** **₹{headroom:,.2f}**
- **Bank Balance After Purchase:** ₹{rem_balance_after:,.2f}

💡 **Advisor Verdict:** This purchase is completely within your discretionary spending cushion. It does not threaten your upcoming bills or mandatory emergency buffer.
"""
        elif target_amount <= self.current_balance:
            shortfall = target_amount - safe_val
            return f"""
### ⚠️ Caution: Exceeds Safe Spending Limit

- **Requested Expense:** ₹{target_amount:,.2f}
- **Safe-to-Spend Limit:** ₹{safe_val:,.2f}
- **Shortfall Beyond Safe Cushion:** **₹{shortfall:,.2f}**
- **Remaining Account Balance After Purchase:** ₹{rem_balance_after:,.2f}

💡 **Advisor Verdict:** You have enough raw cash in your account, **but this purchase will eat into your emergency buffer or committed upcoming expenses**.  
If this purchase is non-essential, consider postponing it or cutting ₹{shortfall:,.0f} from discretionary dining or shopping this month.
"""
        else:
            deficit = target_amount - self.current_balance
            return f"""
### 🚨 Cannot Afford Right Now (Insufficient Balance)

- **Requested Expense:** ₹{target_amount:,.2f}
- **Current Balance:** ₹{self.current_balance:,.2f}
- **Deficit:** **₹{deficit:,.2f}**

💡 **Advisor Verdict:** This transaction would overdraw your account by ₹{deficit:,.2f}. Avoid taking high-interest personal credit or overdraft for discretionary purchases.
"""

    def _handle_safe_to_spend(self):
        msg = str(self.safe_df["financial_message"].iloc[0])
        return f"""
### 🛡️ Your Safe-to-Spend Analysis

- **Total Safe-to-Spend:** **₹{self.safe_to_spend:,.2f}**
- **Daily Safe Allowance:** **₹{self.daily_safe:,.2f} / day**
- **Weekly Safe Allowance:** **₹{self.daily_safe * 7:,.2f} / week**
- **Days Remaining in Billing Cycle:** {self.days_remaining} days
- **Financial Status:** **{self.status}**

📋 **Guidance:**
> {msg}

*Tip: Discretionary expenses (eating out, impulse shopping) should stay under **₹{self.daily_safe:,.0f} per day** to guarantee your bills and savings remain safe.*
"""

    def _handle_anomalies(self):
        exp, model, summary = ml_models.train_anomaly_detector(self.df, contamination=0.05)
        if model is None or summary.get("unusual_count", 0) == 0:
            return "✅ **No anomalous transactions detected!** All recent expenses match your typical spending baseline."

        unusual_tx = exp[exp["is_unusual"]].sort_values("amount", ascending=False).head(5)
        table_rows = []
        for _, r in unusual_tx.iterrows():
            table_rows.append(f"| {r['date'].strftime('%Y-%m-%d')} | {r['merchant']} | {r['category']} | ₹{r['amount']:,.2f} | {r['anomaly_reason']} |")

        table_md = "\n".join(table_rows)

        return f"""
### 🚨 Machine Learning Anomaly Detection Report

Our **Isolation Forest** model identified **{summary['unusual_count']} unusual transactions** ({summary['unusual_percent']}% of total debit activity).

- **Total Irregular Spend:** **₹{summary['unusual_total_amount']:,.2f}**
- **Average Outlier Amount:** **₹{summary['avg_unusual_amount']:,.2f}** (vs. Normal Average: ₹{summary['avg_normal_amount']:,.2f})

#### Top Flagged Outliers:
| Date | Merchant | Category | Amount (₹) | Detection Reasoning |
| :--- | :--- | :--- | :--- | :--- |
{table_md}

💡 **Action Item:** Verify these top debits in your banking app to confirm you authorized each payment.
"""

    def _handle_forecast(self):
        series = ml_models.prepare_monthly_spending_series(self.df)
        if len(series) < 3:
            return "⚠️ Insufficient monthly history to formulate a robust time-series forecast. At least 3 calendar months of records are required."

        trained = ml_models.train_spending_models(series)
        fc = ml_models.forecast_future_spending(series, trained, horizon_months=3, model_choice="Linear Regression")

        rows = []
        for _, r in fc.iterrows():
            rows.append(f"- **{r['Month']}:** ₹{r['Forecasted Spending (₹)']:,.2f} *(Confidence: ₹{r['Lower Bound (₹)']:,.0f} - ₹{r['Upper Bound (₹)']:,.0f})*")

        fc_list = "\n".join(rows)
        slope = trained["slope"]
        trend = "Increasing 📈" if slope > 0 else "Decreasing 📉"

        return f"""
### 🔮 Predictive Spending Forecast (Next 3 Months)

Based on machine learning regression trained on your historical spending trajectory:

{fc_list}

- **Monthly Trend Slope:** **{trend} by ₹{abs(slope):,.2f} per month**
- **Model R² Accuracy Score:** `{trained['metrics_df'].iloc[0]['R² Score']}`

💡 **Recommendation:** {"Since your spending trend is upward, review high-frequency impulse categories like Food & Shopping to curb inflation." if slope > 0 else "Your spending trend is downward or stable. Maintain this discipline!"}
"""

    def _find_merchant_in_query(self, text):
        if "merchant" not in self.df.columns:
            return None
        merchants = self.df["merchant"].dropna().unique().tolist()
        for m in merchants:
            if m.lower() in text:
                return m
        return None

    def _handle_merchant_query(self, merchant_name):
        sub = self.df[self.df["merchant"].str.lower() == merchant_name.lower()]
        if sub.empty:
            return f"No transaction history found for **{merchant_name}**."

        total_spent = sub["amount"].sum()
        count = len(sub)
        avg_spent = sub["amount"].mean()
        latest = sub.sort_values("date").iloc[-1]

        return f"""
### 🏪 Spending Breakdown: **{merchant_name}**

- **Total Spend:** **₹{total_spent:,.2f}**
- **Transaction Count:** {count} times
- **Average Spend per Transaction:** ₹{avg_spent:,.2f}
- **Latest Transaction:** ₹{latest['amount']:,.2f} on {latest['date'].strftime('%Y-%m-%d')} ({latest['category']})

💡 *Tip: This merchant accounts for **{(total_spent / max(1, self.total_expense)) * 100:.1f}%** of your total overall expenses.*
"""

    def _find_category_in_query(self, text):
        categories = self.df["category"].dropna().unique().tolist()
        for c in categories:
            if c.lower() in text:
                return c
        synonyms = {
            "food": ["food", "dining", "restaurant", "zomato", "swiggy", "eating", "eat"],
            "shopping": ["shopping", "clothes", "amazon", "myntra", "flipkart"],
            "travel": ["travel", "commute", "uber", "ola", "metro", "transport"],
            "bills": ["bills", "electricity", "utility", "recharge", "airtel", "jio"],
            "entertainment": ["entertainment", "movie", "netflix", "games"],
            "groceries": ["groceries", "grocery", "supermarket", "dmart", "blinkit"],
            "healthcare": ["healthcare", "medical", "pharmacy", "doctor", "hospital"],
            "education": ["education", "courses", "books", "college"]
        }
        for cat, kw_list in synonyms.items():
            if any(k in text for k in kw_list):
                for actual_cat in categories:
                    if cat.lower() in actual_cat.lower():
                        return actual_cat
        return None

    def _handle_category_query(self, category_name):
        cat_df = self.expense_df[self.expense_df["category"].str.lower() == category_name.lower()]
        if cat_df.empty:
            return f"No expense records found for category **{category_name}**."

        total_cat = cat_df["amount"].sum()
        pct = (total_cat / max(1, self.total_expense)) * 100
        count = len(cat_df)
        avg_val = cat_df["amount"].mean()

        top_merchants = cat_df.groupby("merchant")["amount"].sum().nlargest(3).reset_index()
        m_list = "\n".join([f"- **{r['merchant']}:** ₹{r['amount']:,.2f}" for _, r in top_merchants.iterrows()])

        return f"""
### 🛒 Category Analysis: **{category_name}**

- **Total Spent:** **₹{total_cat:,.2f}** ({pct:.1f}% of all expenses)
- **Number of Transactions:** {count} transactions
- **Average Transaction:** ₹{avg_val:,.2f}

#### Top Merchants in this Category:
{m_list}

💡 **Budget Insight:** Reducing this category by **20%** would save you **₹{total_cat * 0.20:,.2f}** over this period!
"""

    def _handle_savings_advice(self):
        cat_spending = self.expense_df.groupby("category")["amount"].sum().sort_values(ascending=False)
        top_cat = cat_spending.index[0]
        top_amt = cat_spending.iloc[0]

        monthly_surplus = max(0.0, (self.total_income - self.total_expense) / max(1, self.df["date"].dt.to_period("M").nunique()))

        return f"""
### 💡 Personalized Budget & Savings Optimization

Here is how you can boost your savings based on your spending history:

1. **Target Your #1 Category ({top_cat}):**
   - You spent **₹{top_amt:,.2f}** on **{top_cat}** (largest single outflow).
   - A **15% cutback** in this category will immediately unlock **₹{top_amt * 0.15:,.2f}** in fresh savings.

2. **Leverage Your Current Cashflow Surplus:**
   - Your average monthly net surplus is **₹{monthly_surplus:,.2f}**.
   - If automated into a mutual fund or index fund yielding ~7%, this compounds to **₹{monthly_surplus * 12 * 3 * 1.07:,.2f}** in 3 years.

3. **Enforce the Daily Safe-to-Spend Ceiling:**
   - Keep daily casual debit card / UPI transfers below **₹{self.daily_safe:,.2f}/day**.

4. **Audit Weekend Spikes:**
   - Check the **💡 What-If Simulator** tab in the dashboard to model exact percentage cutbacks!
"""

    def _handle_largest_expenses(self):
        top_3 = self.expense_df.sort_values("amount", ascending=False).head(3)
        rows = []
        for i, (_, r) in enumerate(top_3.iterrows(), start=1):
            rows.append(f"{i}. **₹{r['amount']:,.2f}** at *{r['merchant']}* ({r['category']}) on {r['date'].strftime('%Y-%m-%d')}")
        return "### 💰 Your Top 3 Largest Expenses:\n\n" + "\n".join(rows)

    def _handle_cashflow_overview(self):
        net = self.total_income - self.total_expense
        rate = (net / self.total_income * 100) if self.total_income > 0 else 0.0

        return f"""
### 📊 Executive Financial Overview

- **Current Bank Balance:** **₹{self.current_balance:,.2f}**
- **Total Income Received:** ₹{self.total_income:,.2f}
- **Total Outgoing Expenses:** ₹{self.total_expense:,.2f}
- **Net Surplus / Savings:** **₹{net:,.2f}** (Savings Rate: **{rate:.1f}%**)
- **Safe-to-Spend Remaining:** **₹{self.safe_to_spend:,.2f}**
- **Financial Status:** **{self.status}**
"""

    def _handle_recurring(self):
        if "is_recurring" in self.expense_df.columns:
            rec_sub = self.expense_df[self.expense_df["is_recurring"] == True]
            rec_tot = rec_sub["amount"].sum()
            rec_cnt = len(rec_sub)
            top_rec = rec_sub.groupby("merchant")["amount"].sum().nlargest(5).reset_index()
            m_list = "\n".join([f"- **{r['merchant']}:** ₹{r['amount']:,.2f}" for _, r in top_rec.iterrows()])
            return f"""
### 🔄 Recurring Commitments & Subscriptions

- **Total Spent on Recurring Mandates:** **₹{rec_tot:,.2f}**
- **Recurring Transactions Count:** {rec_cnt} debits

#### Top Recurring Mandates:
{m_list}

💡 *Review and cancel unused streaming or app subscriptions to free up monthly cashflow.*
"""
        return "No recurring mandate flag found in active records."

    def _handle_default_fallback(self, query):
        return f"""
I analyzed your question: *"**{query}**"* against your UPI ledger.

Here is a quick snapshot of your active finances:
- **Current Balance:** ₹{self.current_balance:,.2f}
- **Safe-to-Spend Right Now:** **₹{self.safe_to_spend:,.2f}** (₹{self.daily_safe:,.2f}/day)
- **Total Spending Recorded:** ₹{self.total_expense:,.2f} across {len(self.expense_df):,} transactions

💡 **You can also try asking:**
- *"Can I afford ₹10,000?"*
- *"How much did I spend on food?"*
- *"Show me my anomalies"*
- *"What is my next month forecast?"*
"""
