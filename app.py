import streamlit as st

def calculate_future_cost(pv, rate, n):
    """
    ฟังก์ชันคำนวณมูลค่าในอนาคต (Future Value)
    pv: Present Value (ราคาปัจจุบัน)
    rate: อัตราเงินเฟ้อ (เป็นทศนิยม เช่น 0.03)
    n: ระยะเวลา (ปี)
    """
    fv = pv * ((1 + rate) ** n)
    return fv

st.title("🎯 Goal Calculator")
st.write("คำนวณเป้าหมาย สู้เงินเฟ้อ!")

# สร้างหน้าต่างแบ่งครึ่งซ้าย-ขวา
col1, col2 = st.columns(2)

# ส่วนที่ 1: ข้อมูลเป้าหมาย (ฝั่งซ้าย)
with col1:
    st.subheader("เป้าหมายของคุณ")
    goal_name = st.text_input("ชื่อเป้าหมาย", "รถยนต์คันแรก")
    pv = st.number_input("ราคาปัจจุบัน (บาท)", value=1000000)
    years = st.slider("ระยะเวลา (ปี)", 1, 40, 10)

# ส่วนที่ 2: สมมติฐานเศรษฐกิจ (ฝั่งขวา)
with col2:
    st.subheader("สมมติฐานเศรษฐกิจ")
    inflation = st.number_input("เงินเฟ้อคาดการณ์ (%)", value=3.0)
    inf_rate = inflation / 100  # แปลงเปอร์เซ็นต์เป็นทศนิยมเพื่อใช้คำนวณ

# --- 3. ทำการคำนวณ ---
future_cost = calculate_future_cost(pv, inf_rate, years)
monthly_savings = future_cost / (years * 12) # หารด้วยจำนวนเดือน

# --- 4. โชว์ผลลัพธ์ด้วยตัวเลขใหญ่ๆ ---
st.divider() # ขีดเส้นคั่น
st.subheader(f"สรุปเป้าหมาย: {goal_name}")

st.metric("มูลค่าที่ต้องจ่ายในอนาคต (รวมเงินเฟ้อ)", f"฿{future_cost:,.2f}")
st.metric("ถ้าเก็บเงินเฉยๆ (ไม่ลงทุน) ต้องเก็บเดือนละ", f"฿{monthly_savings:,.2f}")