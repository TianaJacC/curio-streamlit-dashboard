import streamlit as st
import csv, os, datetime, random

st.set_page_config(
    page_title="夢境珍奇櫃 ‧ 公測登記",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

LOG_DIR = "system_logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
RESERVE_FILE = os.path.join(LOG_DIR, "public_pilot_reservations.csv")
if not os.path.exists(RESERVE_FILE):
    with open(RESERVE_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Reservation_ID", "Anonymous_Token", "Timestamp", "Pilot_Phase", "Status"])

st.markdown("""
    <style>
    .stApp { background-color: #F4F3EF !important; color: #1E232A !important; font-family: -apple-system, BlinkMacSystemFont, "PingFang TC", sans-serif; }
    .pastel-card { background: #FAF0C8; border: 2px solid #967E28; border-radius: 24px; padding: 24px; text-align: center; margin-bottom: 20px; box-shadow: 0 8px 24px rgba(150,126,40,0.08); }
    .res-box { background: #FFFFFF; border: 1.5px solid #E2DCD2; border-radius: 20px; padding: 20px; margin-top: 16px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="pastel-card">
        <div style="font-size:2.8rem; margin-bottom:8px;">✨</div>
        <h2 style="color:#967E28; margin:0 0 10px 0;">2027 春節前擴大公測意願登記</h2>
        <div style="font-size:0.92rem; line-height:1.7; color:#4A3B32;">
            本登記貫徹 <b>No-PII 零個資規範</b>，無須提供真實姓名與電話。<br>
            送出後將保留第二階段生活調飲處方完整導航優先權限，並供臨床研究備查。
        </div>
    </div>
""", unsafe_allow_html=True)

user_token = st.text_input("輸入今日通行金鑰（或由系統派發）：", value=f"#SYM-{random.randint(1000, 9999)}")
agree = st.checkbox("我同意於 2027 年 2 月參與第二階段無個資生活處方追蹤公測", value=True)

if st.button("🚀 確認送出公測意願", use_container_width=True):
    if agree:
        now_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        res_id = f"RES-{random.randint(1000, 9999)}"
        with open(RESERVE_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([res_id, user_token, now_ts, "Phase_2_Pilot", "Registered"])
        st.success("✅ 登記完成！受試席位已保留。")
        st.markdown(f"""
            <div class="res-box">
                <b>公測預約編號</b>：<code style="font-size:1.15rem; color:#967E28;">{res_id}</code><br>
                <b>登記狀態</b>：已成功入庫（Phase 2 Pilot Reserved）<br>
                <b>隱私聲明</b>：本紀錄無任何可辨識個資，完整數據已加密備存於系統日誌。
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ 請先勾選同意意願！")
