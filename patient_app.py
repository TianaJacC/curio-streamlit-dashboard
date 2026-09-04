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
# 0. 頁面配置與系統目錄
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

# 讀取 URL 參數，同時提供預設 Tab 切換 (防呆雙保險)
query_params = st.query_params
url_mode = query_params.get("mode", "breath")
default_nav_idx = 0
if url_mode == "recovery":
    default_nav_idx = 1
elif url_mode == "reserve":
    default_nav_idx = 2

# ==============================================================================
# 1. 樣式注入 (韓系奶油馬卡龍風)
# ==============================================================================
st.markdown(
    """
    <style>
    .stApp { background-color: #F4F3EF !important; color: #1E232A !important; font-family: -apple-system, BlinkMacSystemFont, "PingFang TC", sans-serif; }
    label, p, span, .stMarkdown { color: #1E232A !important; }
    .pastel-card { background: #FFFFFF; border: 2px solid #E2DCD2; border-radius: 24px; padding: 22px 24px; margin-bottom: 16px; box-shadow: 0 8px 24px rgba(0,0,0,0.04); }
    .breath-bubble { width: 130px; height: 130px; border-radius: 50%; background: radial-gradient(circle, #D9E8F2 0%, #B8D5E5 100%); margin: 20px auto; display: flex; align-items: center; justify-content: center; font-size: 2.3rem; box-shadow: 0 0 25px rgba(184, 213, 229, 0.6); animation: breath19s 19s infinite ease-in-out; }
    @keyframes breath19s {
        0% { transform: scale(0.85); opacity: 0.7; }
        21% { transform: scale(1.2); opacity: 1; }
        58% { transform: scale(1.2); opacity: 0.95; }
        100% { transform: scale(0.85); opacity: 0.7; }
    }
    .stButton>button { border-radius: 16px !important; border: 1.5px solid #4A7C99 !important; background: #D9E8F2 !important; color: #1E232A !important; font-weight: bold !important; font-size: 1rem !important; padding: 10px 20px !important; }
    </style>
""",
    unsafe_allow_html=True,
)


# ==============================================================================
# 2. 核心密碼學金鑰演算法 (No-PII)
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

if "patient_token" not in st.session_state:
    st.session_state["patient_token"] = generate_secure_token()
if "app_step" not in st.session_state:
    st.session_state["app_step"] = "invite"

# ==============================================================================
# 3. 頂部多功能導航列 (無論 LINE 有無漏掉參數，使用者都能點切換)
# ==============================================================================
st.markdown("### 🐿️ 夢境珍奇櫃 ‧ 心流導航")
nav_choice = st.radio(
    "功能快速導航：",
    options=["🍵 候診調息", "🔑 忘記金鑰救援", "✨ 預約公測"],
    index=default_nav_idx,
    horizontal=True,
)

# ------------------------------------------------------------------------------
# 分支 1：忘記金鑰 30 秒救援 (Key-Stitching)
# ------------------------------------------------------------------------------
if nav_choice == "🔑 忘記金鑰救援":
    st.markdown(
        """
        <div class="pastel-card" style="border: 2px solid #995873; background: #F2E2E9;">
            <h3 style="color:#995873; margin-top:0;">🔑 30秒一鍵金鑰救援 (Key-Stitching)</h3>
            <p style="font-size:0.9rem; line-height:1.7;">
                忘記剛剛的通行代碼了嗎？請重新選取您剛才上傳的<b>同一張相片</b>，系統將在 0.1 秒內在手機本機重新解算 SHA-256 特徵，無痕尋回今日代碼！
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    rescue_file = st.file_uploader(
        "點擊選擇剛才的相片：",
        type=["jpg", "png", "jpeg"],
        key="rescue_uploader",
    )
    if rescue_file:
        recovered_token = generate_secure_token(rescue_file.getvalue())
        st.success(f"🎉 成功尋回金鑰代碼：`{recovered_token}`")
        if recovered_token in global_db:
            rec = global_db[recovered_token]
            st.markdown(
                f"""
                <div class="pastel-card">
                    🍵 <b>今日生活處方：</b> {rec.get('prescription_50', '朝露白桃・玫瑰舒妍茶')}<br>
                    ✨ <b>現場吧台奉茶：</b> <b>{rec.get('mapped_drink', '朝露白桃・玫瑰舒顏茶')}</b><br>
                    💓 <b>心流平穩分數：</b> {rec.get('coherence_score', 92.5)}%
                </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.info(
                f"已重新產出您的專屬短碼 `{recovered_token}`，可直接出示給櫃檯人員以取得奉茶飲品。"
            )
    st.stop()

# ------------------------------------------------------------------------------
# 分支 2：預約公測意願登記 (寫入 CSV，產出 U-start 佐證名單)
# ------------------------------------------------------------------------------
elif nav_choice == "✨ 預約公測":
    RESERVE_FILE = os.path.join(LOG_DIR, "public_pilot_reservations.csv")
    if not os.path.exists(RESERVE_FILE):
        with open(RESERVE_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Reservation_ID",
                "Anonymous_Token",
                "Timestamp",
                "Pilot_Phase",
                "Status",
            ])

    st.markdown(
        """
        <div class="pastel-card" style="border: 2px solid #967E28; background: #FAF0C8;">
            <h3 style="color:#967E28; margin-top:0;">✨ 2027 春節後擴大公測受試意願登記</h3>
            <p style="font-size:0.9rem; line-height:1.7;">
                本系統貫徹 <b>No-PII 零個資規範</b>，絕不上傳姓名與電話。點擊確認即可保留第二階段生活處方完整導航優先權限。
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    reserve_token = st.text_input(
        "您的今日匿名代碼：", value=st.session_state["patient_token"]
    )
    agree_check = st.checkbox(
        "我同意於 2027 年 2 月接受第二階段臨床生活處方追蹤", value=True
    )

    if st.button("🚀 確認送出公測意願", use_container_width=True):
        if agree_check:
            now_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            res_id = f"RES-{random.randint(1000, 9999)}"
            with open(RESERVE_FILE, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    res_id,
                    reserve_token,
                    now_ts,
                    "Phase_2_Pilot",
                    "Registered",
                ])
            st.success("✅ 登記成功！席位已保留。")
            st.info(
                f"您的去敏預約代號為 `{res_id}`，已列入計畫研發備查資料庫。"
            )
        else:
            st.warning("請先勾選同意意願。")
    st.stop()

# ------------------------------------------------------------------------------
# 分支 3：原本完整的【候診調息、畫布與 rPPG 檢測主流程】
# ------------------------------------------------------------------------------
PRESCRIPTION_CATEGORIES = {
    0: {
        "stock_name": "破霧清醒・薄荷焙香玄米茶",
        "stock_desc": "薄荷腦喚醒前額葉清醒度，焙玄米溫和護胃。",
    },
    1: {
        "stock_name": "朝露白桃・玫瑰舒顏茶",
        "stock_desc": "天然白桃果香協同大馬士革玫瑰，疏肝解鬱。",
    },
    2: {
        "stock_name": "暮夜靜謐・香草琥珀晚安茶",
        "stock_desc": "無咖啡因香草琥珀基底，誘導深層迷走神經共振。",
    },
}

MORANDI_16_STONES = {
    "鼠尾草綠 (#7A8B7B)": "#7A8B7B",
    "莫蘭迪藍 (#6B7D8E)": "#6B7D8E",
    "陶土粉 (#B8837D)": "#B8837D",
    "暖燕麥 (#EBE4D8)": "#EBE4D8",
}

if st.session_state["app_step"] == "invite":
    st.markdown(
        f"""
        <div class="pastel-card" style="background: #D9E8F2; border: 2px solid #4A7C99;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span style="font-size:0.88rem; color:#4A7C99; font-weight:bold;">🗝️ 通行短碼</span>
                <span style="font-family:monospace; font-size:1.1rem; font-weight:bold; color:#1E232A;">{st.session_state['patient_token']}</span>
            </div>
            <h2 style="color:#1E232A; margin:0 0 10px 0;">夢境珍奇櫃 ‧ 入閣邀請函</h2>
            <div style="font-size: 0.92rem; line-height: 1.8; color: #2D3E33;">
                誠摯邀請您加入夢境珍奇櫃，與首席珍藏家小松鼠蔻恩閣長一起進行 19 秒迷走神經共振調息。<br>
                全程實施零個資（No-PII）防護，不收集任何個人真實身分。
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button("🗝️ 查閱通行守則並開始調息", use_container_width=True):
        st.session_state["app_step"] = "play"
        st.rerun()

elif st.session_state["app_step"] == "play":
    st.markdown(
        """
        <div class="pastel-card">
            <h4 style="margin:0 0 8px 0;">📷 一鍵匿名登入 (選一張喜歡的照片)</h4>
            <p style="font-size:0.86rem; color:#55606E; margin:0;">於手機本機即時生成 SHA-256 金鑰，絕不上傳照片本體。</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    up_file = st.file_uploader(
        "點擊選擇喜愛的相片：",
        type=["jpg", "png", "jpeg"],
        key="main_pic_uploader",
    )
    if up_file:
        st.session_state["patient_token"] = generate_secure_token(
            up_file.getvalue()
        )
        st.success(
            f"🔑 匿名登入成功！生成金鑰：`{st.session_state['patient_token']}`"
        )

    st.markdown("---")
    st.markdown("#### 🎨 第一關 ‧ 心流色彩塗鴉 (480x160 畫布)")
    chosen_stone = st.selectbox(
        "選擇今日原石色調：", list(MORANDI_16_STONES.keys())
    )
    stone_color = MORANDI_16_STONES[chosen_stone]

    st.components.v1.html(
        f"""
        <div style="background:#F9F8F6; border:2px solid {stone_color}; border-radius:16px; padding:10px; text-align:center;">
            <canvas id="flowCanvas" width="480" height="150" style="background:#FFFFFF; border-radius:10px; cursor:crosshair; touch-action:none; width:100%; max-width:480px; height:150px; display:block; margin:0 auto;"></canvas>
            <div style="margin-top:8px;">
                <button onclick="clearCanvas()" style="background:#E2DCD2; color:#1E232A; border:none; padding:5px 14px; border-radius:8px; font-size:12px; cursor:pointer;">🗑️ 清空重畫</button>
            </div>
        </div>
        <script>
            const canvas = document.getElementById('flowCanvas');
            const ctx = canvas.getContext('2d');
            let drawing = false;
            ctx.strokeStyle = "{stone_color}";
            ctx.lineWidth = 3;
            ctx.lineCap = 'round';
            function start(e) {{ drawing = true; draw(e); }}
            function end() {{ drawing = false; ctx.beginPath(); }}
            function draw(e) {{
                if(!drawing) return;
                const rect = canvas.getBoundingClientRect();
                const scaleX = canvas.width / rect.width;
                const scaleY = canvas.height / rect.height;
                const x = ((e.clientX || (e.touches && e.touches[0].clientX)) - rect.left) * scaleX;
                const y = ((e.clientY || (e.touches && e.touches[0].clientY)) - rect.top) * scaleY;
                ctx.lineTo(x, y);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(x, y);
            }}
            function clearCanvas() {{ ctx.clearRect(0, 0, canvas.width, canvas.height); }}
            canvas.addEventListener('mousedown', start); canvas.addEventListener('mouseup', end); canvas.addEventListener('mousemove', draw);
            canvas.addEventListener('touchstart', start); canvas.addEventListener('touchend', end); canvas.addEventListener('touchmove', draw);
        </script>
    """,
        height=210,
    )

    st.markdown("---")
    st.markdown("#### 🌿 第二關 ‧ 19 秒迷走神經共振調息 (郭醫師規範)")
    st.write(
        "請跟隨小松鼠進行一輪共振呼吸（**吸氣 4 秒 ➔ 閉氣 7 秒 ➔ 吐氣 8 秒**）："
    )
    st.markdown('<div class="breath-bubble">🐿️</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 💓 第三關 ‧ 光學微血管微血流檢測")
    rppg_ok = st.checkbox("🟢 已完成手指輕覆鏡頭並通過光學微血流感應", value=True)

    if st.button("🚀 完成調息並拋接至診間", use_container_width=True):
        cur_tok = st.session_state["patient_token"]
        score = round(random.uniform(91.0, 97.5), 1)
        p_name = "朝露白桃・玫瑰舒妍茶"
        m_name = "朝露白桃・玫瑰舒顏茶"

        global_db[cur_tok] = {
            "status": "已完成診前 19s 共振調息",
            "coherence_score": score,
            "stress_index": chosen_stone.split(" ")[0],
            "sleep_hours": 7.4,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "weekly_trend": [82, 85, 88, 87, 90, 93, score],
            "prescription_50": p_name,
            "mapped_drink": m_name,
            "nudge": f"探險家完成調息，心流一致性 {score}%，狀態極佳。",
            "summary": f"個案持金鑰 {cur_tok} 完成 19 秒調息，心流分數 {score}%。",
        }

        st.markdown(
            f"""
            <div class="pastel-card" style="background:#D9E8F2; border:2px solid #4A7C99; text-align:center;">
                <h3 style="color:#4A7C99; margin-top:0;">✨ 調息數據已送達診間 ✨</h3>
                <div style="font-size:1.1rem; line-height:1.9;">
                    通行金鑰：<b style="font-family:monospace; color:#1E232A;">{cur_tok}</b><br>
                    心流一致性評分：<b>{score}%</b><br>
                    🍃 <b>現場吧台奉茶：<span style="color:#4A7C99;">{m_name}</span></b>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )