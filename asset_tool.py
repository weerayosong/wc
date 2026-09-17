import streamlit as st
import pandas as pd

st.set_page_config(page_title="Asset Comparison", layout="wide")
st.title("📈 Asset Comparison Tool")
st.write("เปรียบเทียบการเติบโตของสินทรัพย์ ด้วยการปรับฐาน 100 (Normalization)")

# --- 1. เตรียมข้อมูลจำลอง (Mock Data) 5 ปี ---
data = {
    "Year": [2020, 2021, 2022, 2023, 2024],
    "Stock (S&P500)": [3000, 4000, 3800, 4500, 5000],
    "Bond (US Treasuries)": [100, 102, 95, 105, 110],
    "Gold": [1500, 1800, 1750, 1950, 2000]
}
# สร้าง DataFrame และตั้งค่า Year ให้เป็นแกน X (Index)
df = pd.DataFrame(data).set_index("Year")

# --- 2. คำนวณ Normalization ---
# นำข้อมูลทั้งตาราง ไปหารด้วยข้อมูลบรรทัดแรกสุด (iloc[0] คือปี 2020) แล้วคูณ 100
df_normalized = (df / df.iloc[0]) * 100

# คำนวณผลตอบแทนรวม (Total Return) จากค่าบรรทัดสุดท้าย (iloc[-1]) หักด้วยต้นทุนที่ฐาน 100
stock_return = df_normalized["Stock (S&P500)"].iloc[-1] - 100
bond_return = df_normalized["Bond (US Treasuries)"].iloc[-1] - 100
gold_return = df_normalized["Gold"].iloc[-1] - 100

# --- 3. สร้าง User Interface ---
st.subheader("📊 ผลตอบแทนสะสม (5 ปี)")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📈 หุ้น (Stocks)", f"{stock_return:.2f}%")
with col2:
    st.metric("🏛️ พันธบัตร (Bonds)", f"{bond_return:.2f}%")
with col3:
    st.metric("⛏️ ทองคำ (Gold)", f"{gold_return:.2f}%")

st.divider()
st.subheader("📈 กราฟเปรียบเทียบการเติบโต (ฐาน 100)")

# Streamlit จะวาดกราฟเส้นแยกสีให้แต่ละคอลัมน์โดยอัตโนมัติ
st.line_chart(df_normalized)

st.info("💡 **ข้อสังเกต:** สินทรัพย์ที่ให้ผลตอบแทนสูง มักจะมีความผันผวน (ขึ้นลงรุนแรง) ในระหว่างทางมากกว่าเสมอ! การลงทุนที่ดีจึงต้องรู้จักผสมผสาน (Diversification)")