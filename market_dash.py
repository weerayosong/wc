import streamlit as st
import pandas as pd

st.set_page_config(page_title="Market Analysis", layout="wide")
st.title("📊 Market Analysis Dashboard")

# --- 1. จำลองข้อมูลราคาสินทรัพย์ (รายเดือน 12 เดือน) ---
# จำลองวิกฤตเศรษฐกิจในเดือนที่ 6 (ราคาตกจาก 120 เหลือ 80)
data = {
    "Month": list(range(1, 13)),
    "Asset_Price": [100, 105, 110, 115, 120, 80, 70, 75, 85, 95, 110, 125]
}
df = pd.DataFrame(data).set_index("Month")

# --- 2. คำนวณความเสี่ยงและผลตอบแทน ---
# หาผลตอบแทนรวม 1 ปี
total_return = (df["Asset_Price"].iloc[-1] - df["Asset_Price"].iloc[0]) / df["Asset_Price"].iloc[0]

# หาเปอร์เซ็นต์เปลี่ยนแปลงแบบรายเดือน (ใช้คำนวณความผันผวน)
df["Monthly_Return"] = df["Asset_Price"].pct_change()

# หาความผันผวน (ส่วนเบี่ยงเบนมาตรฐานของ Return)
volatility = df["Monthly_Return"].std()

# --- อัลกอริทึม Max Drawdown ---
# 1. หาราคาสูงสุดที่เคยทำได้ ตั้งแต่วันแรกจนถึงปัจจุบัน
df["Peak"] = df["Asset_Price"].cummax()

# 2. หาเปอร์เซ็นต์ที่ตกลงมาจาก Peak ในแต่ละเดือน
df["Drawdown"] = (df["Asset_Price"] - df["Peak"]) / df["Peak"]

# 3. ดึงค่าที่ติดลบหนักที่สุดออกมา
max_drawdown = df["Drawdown"].min()


# --- 3. สร้าง UI แสดงผล ---
st.subheader("Key Risk Metrics")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("📈 1-Year Return", f"{total_return * 100:.2f}%")
with c2:
    st.metric("🌪️ Volatility (ความผันผวน)", f"{volatility * 100:.2f}%")
with c3:
    st.metric("📉 Max Drawdown (จุดขาดทุนสูงสุด)", f"{max_drawdown * 100:.2f}%")

st.divider()

st.subheader("📈 Price Action & Drawdown")
# วาดกราฟพื้นที่แสดงการเคลื่อนไหวของราคา
st.area_chart(df["Asset_Price"])

# โชว์ตารางข้อมูลดิบ
with st.expander("🔍 ดูตารางข้อมูลดิบ (Raw Data) และ Data Dictionary"):
    st.markdown("""
    **Data Dictionary:**
    * `Asset_Price`: ราคาปิดของสินทรัพย์ในเดือนนั้น
    * `Monthly_Return`: % กำไร/ขาดทุน เทียบกับเดือนก่อนหน้า
    * `Peak`: ราคาสูงสุดที่เคยทำได้จนถึงเดือนนั้น
    * `Drawdown`: % ที่ราคาตกลงมาจาก Peak (ถ้าค่าติดลบแสดงว่ากำลังขาดทุนจากจุดสูงสุด)
    """)
    st.dataframe(df, use_container_width=True)