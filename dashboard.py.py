import streamlit as st
import pandas as pd

st.set_page_config(page_title="Money System", layout="wide")
st.title("📊 Personal Money System")

cashflow_df = pd.DataFrame({
    "Category": ["Salary", "Bonus", "Rent", "Food", "Travel"],
    "Type": ["Income", "Income", "Expense", "Expense", "Expense"],
    "Amount": [50000, 10000, 15000, 9000, 4000]
})

networth_df = pd.DataFrame({
    "Item": ["Savings", "Stocks", "Car Loan", "Credit Card"],
    "Type": ["Asset", "Asset", "Liability", "Liability"],
    "Amount": [150000, 50000, 400000, 15000]
})

# กรองเฉพาะ Income แล้วรวมผลลัพธ์
total_income = cashflow_df[cashflow_df["Type"] == "Income"]["Amount"].sum()
# กรองเฉพาะ Expense แล้วรวมผลลัพธ์
total_expense = cashflow_df[cashflow_df["Type"] == "Expense"]["Amount"].sum()

# หาเงินเหลือ และ อัตราการออม
cashflow = total_income - total_expense
savings_rate = (cashflow / total_income) * 100

total_assets = networth_df[networth_df["Type"] == "Asset"]["Amount"].sum()
total_liabs = networth_df[networth_df["Type"] == "Liability"]["Amount"].sum()

net_worth = total_assets - total_liabs

st.header("Executive Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("เงินเหลือเก็บ (Cashflow)", f"฿{cashflow:,.2f}")
    st.write(f"อัตราการออม: **{savings_rate:.1f}%**")

with col2:
    st.metric("ความมั่งคั่งสุทธิ (Net Worth)", f"฿{net_worth:,.2f}")

with col3:
    # สร้างเงื่อนไขแจ้งเตือนหากหนี้สินมากกว่าทรัพย์สิน
    if net_worth < 0:
        st.error("⚠️ คุณมีหนี้สินมากกว่าทรัพย์สิน ระวังอันตราย!")
    else:
        st.success("✅ สถานะการเงินของคุณเป็นบวก")

st.divider() 
st.header("Data Breakdown")

tab1, tab2 = st.tabs(["📈 Cashflow Data", "🏦 Net Worth Data"])

with tab1:
    st.dataframe(cashflow_df, use_container_width=True)

with tab2:
    st.dataframe(networth_df, use_container_width=True)