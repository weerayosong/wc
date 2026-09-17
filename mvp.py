import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Personal Wealth Dashboard v7", page_icon="💼", layout="wide")

# ==========================================
# ฟังก์ชันสนับสนุน (Helper Functions)
# ==========================================
def calculate_future_cost(pv, rate, n):
    return pv * ((1 + rate) ** n)

def simulate_wealth(monthly_inv, annual_return_pct, months):
    r_monthly = (annual_return_pct / 100) / 12
    if r_monthly == 0:
        return monthly_inv * months
    return monthly_inv * (((1 + r_monthly)**months - 1) / r_monthly)

st.title("💼 Personal Wealth Dashboard (Version 7 - Final)")
st.markdown("ระบบบริหารความมั่งคั่งครบวงจร: **แผนการเงิน -> พอร์ตฟอลิโอ -> กลยุทธ์ -> บททดสอบความเครียด**")

# ==========================================
# Sidebar: Setup User Profile & Stress Parameters
# ==========================================
st.sidebar.header("1. My Money System")
cashflow = st.sidebar.number_input("เงินเหลือเก็บ (Cashflow/เดือน)", value=15000, step=5000)

st.sidebar.divider()
st.sidebar.header("2. My Goal")
goal_price = st.sidebar.number_input("ราคาเป้าหมายปัจจุบัน", value=1500000, step=50000)
goal_years = st.sidebar.slider("ระยะเวลาเก็บเงิน (ปี)", 1, 20, 5)
inflation_rate = 0.03

st.sidebar.divider()
st.sidebar.header("🛡️ Stress Test Config")
st.sidebar.write("จำลองวิกฤตเศรษฐกิจ")
volatility_shock = st.sidebar.slider("ความผันผวนตลาด (%)", 5, 50, 20) / 100
black_swan_drop = st.sidebar.slider("Black Swan Drop (%)", 0, 80, 30) / 100
# บังคับให้ปีที่เกิดวิกฤตอยู่ในช่วงระยะเวลาเก็บเงิน
crash_year = st.sidebar.slider("เกิดวิกฤตในปีที่", 1, goal_years, max(1, goal_years//2))

# ==========================================
# Main UI: Tabs Organization
# ==========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 1. Health", 
    "⚙️ 2. Allocation", 
    "📈 3. Projection",
    "🤖 4. Tactical",
    "⚡ 5. Stress Test (New!)"
])

# --- Tab 1: Financial Health ---
with tab1:
    future_goal_cost = calculate_future_cost(goal_price, inflation_rate, goal_years)
    monthly_saving_req = future_goal_cost / (goal_years * 12)
    st.subheader("สถานะเป้าหมาย")
    st.info(f"คุณต้องการเงิน **฿{monthly_saving_req:,.0f}/เดือน** เพื่อให้ถึงเป้าหมาย **฿{future_goal_cost:,.0f}** ในอีก {goal_years} ปี")

# --- Tab 2: Asset Allocation ---
with tab2:
    st.subheader("จัดสรรพอร์ตฟอลิโอ")
    stock_weight = st.slider("สัดส่วนหุ้น (%)", 0, 100, 60, key="port_weight_v7")
    w_s = stock_weight / 100
    w_b = (100 - stock_weight) / 100
    expected_port_return = (w_s * 8.0) + (w_b * 3.0)
    # สมมติความผันผวนพื้นฐาน: หุ้น 15%, พันธบัตร 5%
    base_port_volatility = (w_s * 0.15) + (w_b * 0.05)
    st.success(f"Expected Return: **{expected_port_return:.2f}% / ปี** | Base Volatility: **{base_port_volatility*100:.2f}%**")

# --- Tab 3: Wealth Projection ---
with tab3:
    st.subheader("จำลองการเติบโต (โลกสวยงาม)")
    fv_portfolio = simulate_wealth(cashflow, expected_port_return, goal_years * 12)
    st.metric("มูลค่าพอร์ตจำลองในอนาคต", f"฿{fv_portfolio:,.0f}", delta=f"เทียบกับเป้าหมาย ฿{future_goal_cost:,.0f}")

# --- Tab 4: Tactical Strategy ---
with tab4:
    st.subheader("🛡️ ทดสอบกลยุทธ์ป้องกันพอร์ต (Tactical)")
    st.write("การตั้งค่ากลยุทธ์ถูกผสานเข้ากับระบบ Backtest อัตโนมัติแล้ว ข้ามไปดูผลลัพธ์ในหน้า Stress Test ได้เลย!")

# --- Tab 5: Stress Test (บทที่ 7) ---
with tab5:
    st.subheader("⚡ บททดสอบความเครียด (โลกความเป็นจริง)")
    st.markdown("จำลองการนำ **Cashflow** ไปลงทุนตลอดระยะเวลาเป้าหมาย แต่เผชิญกับ **ความผันผวน** และ **เหตุการณ์ Black Swan**")
    
    total_years = goal_years
    yearly_cashflow = cashflow * 12
    
    # 1. Base Case (ผลตอบแทนตามที่คาดหวัง)
    np.random.seed(42)
    yearly_base_returns = np.random.normal(expected_port_return/100, base_port_volatility, total_years)
    
    # 2. Stress Case (โดนวิกฤตเต็มๆ ไม่มีกลยุทธ์ป้องกัน)
    np.random.seed(42)
    yearly_stress_returns = np.random.normal(expected_port_return/100, volatility_shock, total_years)
    yearly_stress_returns[crash_year - 1] = -black_swan_drop 
    
    # 3. Tactical Stress Case (มีกลยุทธ์ป้องกัน)
    # สมมติว่ากลยุทธ์ Tactical (เช่น SMA) ช่วยตัดขาดทุนได้ครึ่งหนึ่งในปีที่ตลาดลงหนักกว่า -10%
    yearly_tactical_returns = np.where(yearly_stress_returns < -0.10, yearly_stress_returns * 0.5, yearly_stress_returns)
    
    df_wealth = pd.DataFrame({"Year": list(range(1, total_years + 1))})
    
    # ฟังก์ชันจำลองการสะสมเงินแบบมีการเพิ่มเงินลงทุนใหม่เข้าไปทุกปี
    def calc_accumulated_wealth(returns):
        wealth = []
        current_val = 0
        for r in returns:
            # สิ้นปี เงินที่มีอยู่ + เงินเติมใหม่ จะเติบโตตามผลตอบแทนปีนั้น
            current_val = (current_val + yearly_cashflow) * (1 + r)
            wealth.append(current_val)
        return wealth
        
    df_wealth["Base_Wealth"] = calc_accumulated_wealth(yearly_base_returns)
    df_wealth["Stress_Wealth"] = calc_accumulated_wealth(yearly_stress_returns)
    df_wealth["Tactical_Stress_Wealth"] = calc_accumulated_wealth(yearly_tactical_returns)
    
    # วาดกราฟ 3 เส้นเปรียบเทียบ
    df_chart = df_wealth.set_index("Year")[["Base_Wealth", "Stress_Wealth", "Tactical_Stress_Wealth"]]
    st.line_chart(df_chart)
    
    st.markdown(f"**เป้าหมายของคุณคือ:** ฿{future_goal_cost:,.0f}")
    c1, c2, c3 = st.columns(3)
    
    final_base = df_wealth["Base_Wealth"].iloc[-1]
    final_stress = df_wealth["Stress_Wealth"].iloc[-1]
    final_tactical = df_wealth["Tactical_Stress_Wealth"].iloc[-1]
    
    c1.metric("โลกปกติ (Base)", f"฿{final_base:,.0f}")
    
    c2.metric("โลกวิกฤต (Stressed)", f"฿{final_stress:,.0f}", 
              delta=f"{final_stress - future_goal_cost:,.0f} เทียบเป้า", 
              delta_color="normal" if final_stress >= future_goal_cost else "inverse")
              
    c3.metric("โลกวิกฤต + กลยุทธ์ป้องกัน", f"฿{final_tactical:,.0f}",
              delta=f"{final_tactical - future_goal_cost:,.0f} เทียบเป้า", 
              delta_color="normal" if final_tactical >= future_goal_cost else "inverse")
              
    # ประเมินผลลัพธ์สุดท้าย
    if final_stress < future_goal_cost and final_tactical >= future_goal_cost:
        st.success("💡 **บทสรุป:** พอร์ตของคุณเจอวิกฤตแล้วพัง (ไปไม่ถึงเป้า) แต่การมี 'กลยุทธ์ป้องกันความเสี่ยง (Tactical)' ช่วยชีวิตคุณไว้ได้!")
    elif final_stress < future_goal_cost and final_tactical < future_goal_cost:
        st.error("⚠️ **บทสรุป:** แม้จะมีกลยุทธ์ป้องกันก็ยังไปไม่ถึงเป้า! คุณต้องปรับ Asset Allocation (ลดหุ้น) หรือเพิ่มเงินเก็บรายเดือน (Cashflow) เพื่อให้แผนการเงินแข็งแกร่งกว่านี้")
    else:
        st.success("🎉 **บทสรุป:** ยอดเยี่ยม! พอร์ตและ Cashflow ของคุณแข็งแกร่งมาก ต่อให้เจอวิกฤตหนักคุณก็ยังไปถึงเป้าหมายได้อย่างสบายๆ")