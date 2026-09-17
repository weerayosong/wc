import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Stress Test Dashboard", layout="wide")
st.title("⚡ Stress Test Dashboard")

# --- 1. ตั้งค่าพารามิเตอร์ของเหตุการณ์ (Sidebar) ---
st.sidebar.header("ตั้งค่าสถานการณ์จำลอง")

# ให้ผู้ใช้เลือกระดับความรุนแรงของวิกฤต (ความผันผวนโดยรวมของตลาด)
volatility_shock = st.sidebar.slider("ระดับความผันผวนของตลาด (%)", min_value=5, max_value=50, value=15) / 100

# จำลองเหตุการณ์ Black Swan (อยู่ดีๆ ตลาดหุ้นตกฮวบในเดือนเดียว)
black_swan_drop = st.sidebar.slider("Black Swan Drop (%)", min_value=0, max_value=80, value=20) / 100

# เลือกว่าจะให้เกิดเหตุการณ์ Black Swan ในเดือนที่เท่าไหร่
crash_month = st.sidebar.slider("เดือนที่เกิดวิกฤต", min_value=1, max_value=12, value=6)

# ระยะเวลาจำลอง 12 เดือน (1 ปี)
months = 12

# --- 2. สร้าง Base Case (ตลาดปกติ โลกสวย) ---
# กำหนด Seed ให้การสุ่มเหมือนเดิมทุกครั้ง (เหมาะสำหรับการสอน)
np.random.seed(42) 

# np.random.normal(ค่าเฉลี่ย, ความผันผวน, จำนวนข้อมูล)
# จำลองตลาดปกติ ให้ผลตอบแทนเฉลี่ย 1% ต่อเดือน ผันผวนต่ำแค่ 2%
base_returns = np.random.normal(0.01, 0.02, months)

df = pd.DataFrame({"Month": list(range(1, months + 1))})
df["Base_Return"] = base_returns

# คำนวณมูลค่าพอร์ต: เงินต้น 100 บาท ทบต้นไปเรื่อยๆ (cumprod)
df["Base_Portfolio"] = 100 * (1 + df["Base_Return"]).cumprod()

# --- 3. สร้าง Stress Case (ตลาดโหดร้าย เจอวิกฤต) ---
np.random.seed(42) # เริ่มต้นเหมือนกันเพื่อเทียบความต่าง

# จำลองตลาดผันผวนสูง (ตามที่ผู้ใช้ปรับใน Slider)
stress_returns = np.random.normal(0.00, volatility_shock, months)

# ยัดเหตุการณ์ Black Swan ลงไป (หักลบ 1 เพราะ index เริ่มที่ 0)
stress_returns[crash_month - 1] = -black_swan_drop 

df["Stress_Return"] = stress_returns
df["Stressed_Portfolio"] = 100 * (1 + df["Stress_Return"]).cumprod()

# --- 4. หา Max Drawdown (จุดขาดทุนลึกสุดของพอร์ต) ---
df["Peak"] = df["Stressed_Portfolio"].cummax()
df["Drawdown"] = (df["Stressed_Portfolio"] - df["Peak"]) / df["Peak"]
max_dd = df["Drawdown"].min()

# --- 5. แสดงผลบน UI ---
st.subheader("📉 เปรียบเทียบ: ตลาดปกติ VS ตลาดวิกฤต")

# วาดกราฟเปรียบเทียบพอร์ตทั้ง 2 รูปแบบ
df_chart = df.set_index("Month")[["Base_Portfolio", "Stressed_Portfolio"]]
st.line_chart(df_chart)

st.divider()

# สรุป Metrics สำคัญ 3 ตัว
c1, c2, c3 = st.columns(3)
final_base = df["Base_Portfolio"].iloc[-1]
final_stress = df["Stressed_Portfolio"].iloc[-1]

c1.metric("มูลค่าสุดท้าย (Base)", f"฿{final_base:.2f}")

# ตั้งค่า delta สีเขียวถ้าเงินต้นมากกว่า 100, สีแดงถ้าน้อยกว่า 100
c2.metric("มูลค่าสุดท้าย (Stress)", f"฿{final_stress:.2f}", 
          delta=f"{(final_stress - 100):.2f}% เทียบเงินต้น",
          delta_color="normal" if final_stress >= 100 else "inverse")

c3.metric("Max Drawdown (วิกฤต)", f"{max_dd*100:.2f}%")

# สรุปผลลัพธ์
if final_stress < 80:
    st.error("💥 พอร์ตนี้เปราะบางเกินไป! มูลค่าลดลงอย่างมีนัยสำคัญเมื่อเจอวิกฤต คุณควรกลับไปปรับกลยุทธ์ (เช่น เพิ่มสัดส่วนพันธบัตร)")
else:
    st.success("🛡️ พอร์ตมีความทนทาน (Resilient) แม้เจอตลาดโหดก็ยังรอด!")

# เผื่อนักเรียนอยากดูตารางข้อมูลดิบ
with st.expander("🔍 ดูตารางคำนวณรายเดือน"):
    st.dataframe(df.round(4), use_container_width=True)