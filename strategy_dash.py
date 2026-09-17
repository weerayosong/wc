import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Strategy Backtest", layout="wide")
st.title("🤖 Strategy Backtest Engine")

# --- 1. จำลองข้อมูลตลาด 20 ช่วงเวลา (Market Data) ---
# จำลองวัฏจักร: ตลาดขึ้น -> ฟองสบู่แตกตกหนัก -> ตลาดเริ่มฟื้นตัว
mock_prices = [
    100, 105, 110, 115, 120, 118, 122, 125, 130, 128, # ขาขึ้น (Uptrend)
    110, 95, 85, 80, 82, 85, 90, 95, 100, 105   # ถล่มและฟื้น (Crash & Recovery)
]
# สร้าง DataFrame
df = pd.DataFrame({"Time": list(range(1, 21)), "Price": mock_prices}).set_index("Time")

# --- 2. ตั้งค่ากลยุทธ์ (Moving Average) ---
st.subheader("⚙️ ปรับแต่งกฎการลงทุน (Trading Rule)")
st.write("ถ้า 'ราคาปัจจุบัน' สูงกว่า 'เส้นค่าเฉลี่ย' = เราจะถือหุ้น (1), ถ้าต่ำกว่า = ขายหลบภัยเป็นเงินสด (0)")

# สร้าง Slider ให้ผู้ใช้ลองปรับระยะเวลาเส้นค่าเฉลี่ย
sma_window = st.slider("เลือกช่วงเวลาคำนวณ SMA (SMA Window)", min_value=2, max_value=10, value=3)

# คำนวณเส้นค่าเฉลี่ย (Simple Moving Average)
df["SMA"] = df["Price"].rolling(window=sma_window).mean()

# สร้างสัญญาณ (Signal) ด้วย np.where
# ถ้า Price > SMA ให้ค่าเป็น 1, ถ้าไม่ใช่ให้เป็น 0
df["Signal"] = np.where(df["Price"] > df["SMA"], 1, 0)

# Shift สัญญาณ 1 วัน (สำคัญมาก!) 
# เพราะในโลกจริง เราดูราคาปิดของวันนี้ เพื่อตัดสินใจซื้อขายใน "วันพรุ่งนี้"
df["Position"] = df["Signal"].shift(1).fillna(0)

# --- 3. คำนวณผลตอบแทนเปรียบเทียบ (Backtesting Math) ---

# แบบที่ 1: ผลตอบแทนแบบปกติ (Buy & Hold) - ซื้อทิ้งไว้ไม่ทำอะไรเลย
df["Market_Return"] = df["Price"].pct_change().fillna(0)
# cumprod() คือการคำนวณทบต้นไปเรื่อยๆ (* 100 เพื่อตั้งฐานเงินเริ่มต้นที่ 100 บาท)
df["Buy_Hold_Growth"] = (1 + df["Market_Return"]).cumprod() * 100

# แบบที่ 2: ผลตอบแทนตามกลยุทธ์ (Strategy)
# เอาผลตอบแทนตลาด * Position (ถ้าเราไม่ได้ถือหุ้น=0 ผลตอบแทนวันนั้นจะเป็น 0 คือไม่เจ็บตัว)
df["Strategy_Return"] = df["Market_Return"] * df["Position"]
df["Strategy_Growth"] = (1 + df["Strategy_Return"]).cumprod() * 100

# --- 4. แสดงผล Dashboard ---
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📉 สัญญาณซื้อขาย (Price vs SMA)")
    # กราฟนี้ให้ดูจุดตัด ถ้าราคา(สีฟ้า) มุดลงใต้ SMA(สีแดง) ระบบจะสั่งขาย
    st.line_chart(df[["Price", "SMA"]])

with col2:
    st.subheader("🏆 ใครชนะ? (Growth Comparison)")
    # กราฟนี้เปรียบเทียบว่าเงิน 100 บาทแรก ใครโตเร็วกว่ากัน
    st.line_chart(df[["Buy_Hold_Growth", "Strategy_Growth"]])

# สรุปผลตอนจบ
final_buy_hold = df["Buy_Hold_Growth"].iloc[-1]
final_strategy = df["Strategy_Growth"].iloc[-1]
diff = final_strategy - final_buy_hold

st.markdown("### 📊 สรุปผลการทดสอบ (Performance Summary)")
c1, c2 = st.columns(2)
c1.metric("ความมั่งคั่งถ้าซื้อทิ้งไว้ (Buy & Hold)", f"{final_buy_hold:.2f}")
c2.metric("ความมั่งคั่งถ้าใช้กลยุทธ์ (Strategy)", f"{final_strategy:.2f}", 
          delta=f"{diff:.2f} เทียบกับตลาด", 
          delta_color="normal" if diff > 0 else "inverse")

if diff > 0:
    st.success("✅ กลยุทธ์ของคุณเอาชนะตลาดได้! เพราะมันช่วยขายหลบวิกฤตได้ทันเวลา")
else:
    st.error("❌ กลยุทธ์แพ้ตลาด! อาจเกิดจากสัญญาณหลอก (Whipsaw) ทำให้ซื้อๆขายๆ บ่อยเกินไป")

with st.expander("🔍 ดูข้อมูลการเทรดแบบละเอียด"):
    st.dataframe(df.round(2), use_container_width=True)