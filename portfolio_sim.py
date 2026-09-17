import streamlit as st
import pandas as pd

st.set_page_config(page_title="Portfolio Simulator", layout="wide")
st.title("⚖️ Portfolio Simulator")

# --- 1. เตรียมข้อมูลผลตอบแทนรายปี (Yearly Return %) ---
# หุ้น: ผลตอบแทนสูง แต่ผันผวนหนัก (มีปีที่บวกเยอะและปีที่ลบเยอะ)
# พันธบัตร: ผลตอบแทนต่ำ แต่นิ่งและมั่นคง
data = {
    "Year": [2020, 2021, 2022, 2023, 2024],
    "Stock_Return": [15.0, 20.0, -18.0, 12.0, 25.0],
    "Bond_Return": [2.0, 1.5, -5.0, 3.0, 4.0]
}
df = pd.DataFrame(data).set_index("Year")

# --- 2. รับค่า Asset Allocation จากผู้ใช้ ---
st.subheader("⚙️ ปรับสัดส่วนพอร์ต (Asset Allocation)")

# ใช้ slider เพื่อให้นักเรียนลากปรับน้ำหนักหุ้น (0 ถึง 100%)
stock_pct = st.slider("น้ำหนักหุ้น (Stocks %)", 0, 100, 60)

# คำนวณน้ำหนักพันธบัตรและแปลงเปอร์เซ็นต์ให้เป็นทศนิยมเพื่อใช้คำนวณ
bond_pct = 100 - stock_pct
w_stock = stock_pct / 100
w_bond = bond_pct / 100

st.write(f"สัดส่วนปัจจุบัน: หุ้น **{stock_pct}%** | พันธบัตร **{bond_pct}%**")

# --- 3. คำนวณผลตอบแทนของพอร์ตในแต่ละปี ---
# สูตร: (น้ำหนักหุ้น * กำไรหุ้นปีนั้น) + (น้ำหนักพันธบัตร * กำไรพันธบัตรปีนั้น)
# ข้อดีของ Pandas คือคำนวณรวดเดียวครบทุกแถว
df["Portfolio_Return"] = (df["Stock_Return"] * w_stock) + (df["Bond_Return"] * w_bond)

# คำนวณสถิติเพื่อนำไปโชว์
avg_port_ret = df["Portfolio_Return"].mean()
vol_port = df["Portfolio_Return"].std() # std() หาความผันผวน
worst_year = df["Portfolio_Return"].min() # min() หาปีที่ติดลบหนักสุด (Drawdown)

# --- 4. สร้าง UI แสดงผลสถิติ ---
st.divider()
st.subheader("📊 สถิติของพอร์ตฟอลิโอ (เฉลี่ย 5 ปี)")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("📈 Average Yearly Return", f"{avg_port_ret:.2f}%")
with c2:
    st.metric("🌪️ Volatility (ความผันผวน)", f"{vol_port:.2f}%")
with c3:
    st.metric("📉 Worst Year (ปีที่แย่ที่สุด)", f"{worst_year:.2f}%")

# --- 5. วาดกราฟเปรียบเทียบ ---
st.subheader("📈 ผลตอบแทนรายปี: พอร์ตผสม VS หุ้น 100%")

# เลือกให้กราฟแสดงเฉพาะข้อมูลของ หุ้นล้วน เทียบกับ พอร์ตผสมที่เราจัดเอง
st.bar_chart(df[["Stock_Return", "Portfolio_Return"]])

# โชว์ตารางข้อมูลดิบสำหรับ Data Dictionary
with st.expander("🔍 ดูข้อมูลตาราง (Raw Data)"):
    st.dataframe(df, use_container_width=True)