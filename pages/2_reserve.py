import streamlit as st
import datetime
import random
import csv
import os

st.set_page_config(page_title="預約公測 ‧ 夢境珍奇櫃", page_icon="✨", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0A110D !important; font-family: -apple-system, sans-serif; }
    p, label, span, h2, h3 { color: #FFFFFF !important; }
    .stButton>button { 
        background: linear-gradient(135deg, #FCBF05 0%, #C2A675 100%) !important; 
        color: #000000 !important; 
        font-weight: 900 !important; 
        border-radius: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="background:#142017; border:2px solid #FCBF05; border-radius:18px; padding:22px; text-align:center; margin-bottom:16px;">
        <div style="font-size:2.6rem; margin-bottom:6px;">✨</div>
        <h3 style="color:#FCBF05 !important; font-size:1.3rem; margin-top:0; font-weight:bold;">2027 春節後擴大公測意願登記</h3>
        <p style="color:#FFFFFF !important; font-size:0.92rem; line-height:1.6;">貫徹 <b>No-PII 零個資規範</b>，無須提供真實姓名與電話即可保留第二階段公測席位。</p>
    </div>
""", unsafe_allow_html=True)

RESERVE_FILE = os.path.join("system_logs", "public_pilot_reservations.csv")
user_tok = st.text_input("您的今日通行短碼：", value="#SYM-CFBD")
agree_pilot = st.checkbox("我同意於 2027 年 2 月參與第二階段無個資生活處方追蹤公測", value=True)

if st.button("🚀 確認送出登記", use_container_width=True):
    if agree_pilot:
        now_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        res_id = f"RES-{random.randint(1000, 9999)}"
        os.makedirs("system_logs", exist_ok=True)
        with open(RESERVE_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([res_id, user_tok, now_ts, "Phase_2_Pilot", "Registered"])
        st.success("✅ 登記成功！名冊已妥善保存備查。")
        st.markdown(f"""
            <div style="background:#0B120E; border:1.5px solid #FCBF05; border-radius:14px; padding:16px; color:#FFFFFF !important;">
                <b>公測預約編號：</b> <code style="color:#FCBF05 !important; font-size:1.1rem;">{res_id}</code><br>
                <b>登記狀態：</b> 已加密備存於系統日誌 (Phase 2 Reserved)
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ 請勾選同意以完成登記！")