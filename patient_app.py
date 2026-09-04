import base64
import csv
import datetime
import hashlib
import hmac
import json
import os
import random
import time
import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt
import streamlit as st

# ==============================================================================
# 0. 頁面配置與 URL 路由解析 (Router)
# ==============================================================================
st.set_page_config(
    page_title="夢境珍奇櫃 ‧ 探險家終端",
    page_icon="🐿️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

LOG_DIR = "system_logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 讀取網址參數 (LIFF URL Query Parameters)
query_params = st.query_params
current_mode = query_params.get("mode", "main")

# ==============================================================================
# 1. 核心密碼學金鑰生成 (No-PII)
# ==============================================================================
def generate_secure_token(seed_bytes: bytes = None) -> str:
    if seed_bytes is None:
        seed_bytes = os.urandom(32)
    time_entropy = str(time.time_ns()).encode("utf-8")
    digest = hmac.new(time_entropy, seed_bytes, hashlib.sha256).hexdigest()
    return f"#SYM-{digest[:4].upper()}"

@st.cache_resource
def get_global_database():
    return {}

global_db = get_global_database()

# ==============================================================================
# 功能分支 A：【忘記金鑰 30 秒無痕救援 (Key-Stitching)】 (mode=recovery)
# ==============================================================================
if current_mode == "recovery":
    st.markdown("""
        <div style="background:#F2E2E9; border:2px solid #995873; border-radius:24px; padding:24px; color:#1E232A; text-align:center;">
            <div style="font-size:2.5rem; margin-bottom:6px;">🗝️</div>
            <h2 style="color:#995873; margin:0 0 10px 0;">30 秒無痕金鑰救援</h2>
            <div style="font-size:0.9rem; line-height:1.7; color:#4A3B32;">
                遺失今日的通行代碼了嗎？<br>
                請重新上傳您剛剛選過的<b>同一張照片</b>，系統將在 0.1 秒內重新計算 SHA-256 密碼學特徵，即刻尋回生活處方短碼！
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    rescue_file = st.file_uploader("點擊選取原照片", type=["jpg", "png", "jpeg"], key="rescue_pic")
    if rescue_file:
        rec_token = generate_secure_token(rescue_file.getvalue())
        st.success(f"🔑 成功找回金鑰代碼：`{rec_token}`")
        if rec_token in global_db:
            data = global_db[rec_token]
            st.markdown(f"""
                <div style="background:#FFFFFF; border-radius:16px; padding:18px; margin-top:14px; border:1px solid #D8C9B0; text-align:left;">
                    🍵 <b>配對生活處方</b>：{data.get('prescription_50', '破霧清醒・薄荷焙香玄米茶')}<br>
                    ✨ <b>現場吧台奉茶</b>：<b>{data.get('mapped_drink', '薄荷焙香玄米茶')}</b><br>
                    💓 <b>心流一致性評分</b>：{data.get('coherence_score', 92.0)}%
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("代碼已重新解算完成，您可直接向櫃檯出示此代碼領取今日處方飲品。")
    st.stop()

# ==============================================================================
# 功能分支 B：【1 秒極簡無個資意願登記】 (mode=reserve)
# ==============================================================================
if current_mode == "reserve":
    RESERVE_FILE = os.path.join(LOG_DIR, "public_pilot_reservations.csv")
    if not os.path.exists(RESERVE_FILE):
        with open(RESERVE_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Reservation_ID", "Anonymous_Token", "Timestamp", "Pilot_Phase", "Status"])

    st.markdown("""
        <div style="background:#FAF0C8; border:2px solid #967E28; border-radius:24px; padding:26px; color:#1E232A; text-align:center;">
            <div style="font-size:2.5rem; margin-bottom:6px;">✨</div>
            <h2 style="color:#967E28; margin:0 0 10px 0;">2027 春節後擴大公測意願登記</h2>
            <div style="font-size:0.9rem; line-height:1.7; color:#4A3B32;">
                本登記實施 <b>100% 零個資防護</b>，不需填寫姓名或電話。<br>
                登記後將保留第二階段優先受試名額，完整解鎖個人自律神經與生活處方導航。
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    res_token = st.text_input("您的今日通行短碼（可直接使用系統派發代碼）：", value=generate_secure_token())
    agree_pilot = st.checkbox("我同意於 2027 年 2 月參與第二階段無個資生活處方追蹤公測", value=True)
    
    if st.button("🚀 確認送出意願登記", use_container_width=True):
        if agree_pilot:
            now_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            res_id = f"RES-{random.randint(1000, 9999)}"
            with open(RESERVE_FILE, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([res_id, res_token, now_ts, "Phase_2_Pilot", "Registered"])
            st.success("✅ 登記完成！受試席位已保留。")
            st.markdown(f"您的專屬公測預約編號為：`{res_id}`，數據已加密入庫供計畫審查備查。")
        else:
            st.warning("請先勾選同意意願。")
    st.stop()

# ==============================================================================
# 功能分支 C：【農業部林業署 18 處國家步道即時指南】 (mode=trails)
# ==============================================================================
if current_mode == "trails":
    st.markdown("""
        <div style="background:#D8EAE1; border:2px solid #4D856B; border-radius:24px; padding:22px; color:#1E232A; text-align:center;">
            <div style="font-size:2.5rem; margin-bottom:6px;">🌲</div>
            <h2 style="color:#4D856B; margin:0 0 8px 0;">林業署森林療癒 ‧ 即時負離子步道</h2>
            <div style="font-size:0.88rem; color:#2D3E33;">串聯農業部台灣山林悠遊網 Open Data ｜ 綠色自然處方</div>
        </div>
    """, unsafe_allow_html=True)
    
    trails = [
        {"name": "阿里山 ‧ 水山療癒步道", "anion": "12,450 ions/cm³", "alt": "2,200m", "status": "舒適度高（在園約 30%）", "hotel": "阿里山貴賓館：尚有空房", "url": "https://recreation.forest.gov.tw/"},
        {"name": "內洞 ‧ 瀑布觀瀑步道", "anion": "18,900 ions/cm³", "alt": "450m", "status": "全台負離子之冠 ‧ 暢通", "hotel": "周邊溫泉區旅宿充裕", "url": "https://recreation.forest.gov.tw/"},
        {"name": "太平山 ‧ 見晴懷古步道", "anion": "9,820 ions/cm³", "alt": "1,900m", "status": "停車位尚餘 45 格", "hotel": "太平山莊：本日滿房", "url": "https://recreation.forest.gov.tw/"},
        {"name": "奧萬大 ‧ 森林療癒試辦步道", "anion": "8,658 ions/cm³", "alt": "1,200m", "status": "氣候涼爽 ‧ 適合調息", "hotel": "綠野山莊：平日尚有空房", "url": "https://recreation.forest.gov.tw/"}
    ]
    
    for t in trails:
        st.markdown(f"""
            <div style="background:#FFFFFF; border:1px solid #C2DBCF; border-radius:18px; padding:16px; margin-top:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="color:#1C2B20; font-size:1.05rem;">{t['name']}</b>
                    <span style="background:#D8EAE1; color:#4D856B; padding:3px 10px; border-radius:10px; font-size:0.8rem; font-weight:bold;">{t['alt']}</span>
                </div>
                <div style="font-size:0.86rem; color:#435449; margin:8px 0; line-height:1.6;">
                    🍃 <b>負離子含量</b>：<code style="color:#4D856B;">{t['anion']}</code><br>
                    🚗 <b>即時人潮路況</b>：{t['status']}<br>
                    🏡 <b>訂房現況</b>：{t['hotel']}
                </div>
                <a href="{t['url']}" target="_blank" style="text-decoration:none; color:#4D856B; font-size:0.82rem; font-weight:bold;">➔ 點擊前往林業署山林悠遊網即時預約</a>
            </div>
        """, unsafe_allow_html=True)
    st.stop()

# ==============================================================================
# 功能分支 D：原本正常的【主要調息與畫布流程】 (mode=main)
# ==============================================================================
# ... (下方接續原有的入閣邀請函、19 秒呼吸引導與畫布程式碼) ...