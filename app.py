import datetime
import os
import random
import time
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="夢境珍奇櫃診間面板 ‧ Curio & Studio",
    page_icon="🐿️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 高對比修正 CSS：解決手機上按鈕/Toggle 看不到的問題
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Didot&family=Garamond:ital,wght@0,400;0,600;1,400&display=swap');

    .stApp { background-color: #FAF8F5; font-family: -apple-system, sans-serif; }
    header[data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    footer { visibility: hidden; }

    /* 強制側邊欄與按鈕高對比可見 */
    button[data-testid="aria-label-SidebarToggle"], 
    [data-testid="stSidebarCollapseButton"] button {
        background-color: #25352B !important;
        color: #D4AF37 !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 12px !important;
        z-index: 999999 !important;
    }

    /* 翻轉病患視角 Toggle 樣式剛性修正 */
    div[data-testid="stToggle"] {
        background: #25352B !important;
        padding: 8px 16px !important;
        border-radius: 16px !important;
        border: 1.5px solid #C2A675 !important;
    }
    div[data-testid="stToggle"] label p {
        color: #FAF8F5 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    .curio-hero-card {
        background: linear-gradient(135deg, #25352B 0%, #1A261F 100%);
        color: #FAF8F5;
        padding: 28px 36px;
        border-radius: 28px;
        border: 1px solid #C2A675;
        margin-bottom: 20px;
    }
    .curio-hero-card h1 { font-family: "Didot", serif !important; color: #FAF8F5 !important; font-size: 1.8rem !important; }

    .doctor-care-card {
        background: linear-gradient(135deg, #F4F0E8 0%, #EAE4D8 100%);
        border: 1px solid #C2A675;
        border-radius: 22px;
        padding: 18px 24px;
        margin-bottom: 16px;
    }

    .quick-nudge-box {
        background-color: #FFFFFF;
        border-left: 4px solid #C2A675;
        border-radius: 16px;
        padding: 16px 20px;
        margin-bottom: 20px;
        border: 1px solid #E4DCD0;
    }
    </style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource
def get_global_database():
    return {
        "#SYM-C701": {
            "status": "已完成診前 15s 共振調息",
            "coherence_score": 92.5,
            "stress_index": "Morandi Soft Blue",
            "stress_desc": "莫蘭迪藍放縮區 ‧ 平穩",
            "sleep_hours": 7.2,
            "timestamp": "2026-08-01 01:20:15",
            "weekly_trend": [82, 85, 87, 84, 89, 91, 92.5],
            "nudge": "探險家近 3 天夜間無應激爆發，心流穩定（92.5%）。建議問診重點：維持優質睡眠時數。",
            "summary": "【去敏身心軌跡摘要】個案於看診前於候診區完成 4-7-8 迷走神經調息。連續 7 日數據顯示夜間無應激爆發，心流一致性維持於 90% 以上高諧振區間。",
        }
    }


global_db = get_global_database()

# 接收網址帶入之 Token 參數 (實現雙端連線)
query_params = st.query_params
url_token = query_params.get("token", "#SYM-C701")

if "selected_token" not in st.session_state:
    st.session_state["selected_token"] = url_token
else:
    if "token" in query_params:
        st.session_state["selected_token"] = query_params["token"]

# 頂樓雙螢幕病患視角切換開關 (高對比修復版)
pv_col1, pv_col2 = st.columns([2.5, 1.5])
with pv_col2:
    patient_mode = st.toggle(
        "🔄 翻轉/病患視角 (雙螢幕)",
        value=False,
        key="p_mode_toggle",
    )

if patient_mode:
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #FAF8F5 0%, #F4F0E8 100%); padding: 40px; border-radius: 32px; border: 2px solid #C2A675; text-align: center; margin-top: 10px;">
            <div style="font-size: 3rem; margin-bottom: 8px;">🐿️</div>
            <h2 style="color: #25352B; font-family: 'Garamond', serif; font-size: 2.2rem; margin: 12px 0;">自費醫療高階療程對照建議卡</h2>
            <div style="font-size: 1.15rem; color: #25352B; line-height: 2.2; max-width: 680px; margin: 0 auto; text-align: left;">
                ✨ <b>專屬身心共振調節建議：</b><br>
                1. <b>rTMS 重複經顱磁刺激療程</b>：深層活化前額葉皮質，快速調節交感神經高活性。<br>
                2. <b>0.067Hz 莫蘭迪聲學調息</b>：搭配專屬音場，進行 15 分鐘診前大腦迷走神經錨定。<br>
                3. <b>精準抗發炎點滴</b>：降低 Cortisol 生理應激負擔，恢復優質睡眠品質。
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )
    st.stop()

# 常規醫師視角
st.markdown(
    """
    <div class="curio-hero-card">
        <h1>夢境珍奇櫃診間面板</h1>
        <p>Curio & Studio x 交感身心診所 ｜ 首席珍藏家蔻恩閣長 Cone ‧ 0 個資身心軌跡拋接</p>
    </div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="doctor-care-card">
        <div style="font-size:0.9rem; color:#25352B; line-height:1.65;">
            午安。今日預約看診 <b>12</b> 位探險家 ｜ 心流諧振指數 <b>94%</b><br>
            <span style="font-size:0.82rem; color:#596B60;">🍵 <b>診間莫蘭迪茶飲/沉香建議</b>：本日交感神經活性略高，建議搭配<b>澳洲檀香/煙燻雪松</b>香氛 ✕ <b>薄荷甘菊茶</b>。</span>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

user_key = st.text_input(
    "請輸入探險家去敏密鑰 (例如：#SYM-C701) :",
    value=st.session_state["selected_token"],
)

data = global_db.get(user_key, None)
if data:
    st.markdown(
        f"""
        <div class="quick-nudge-box">
            <div style="font-size:0.88rem; font-weight:600; color:#25352B; margin-bottom:4px;">
                ✨ 小松鼠蔻恩閣長 Cone 1 秒問診焦點提示 (Clinical Nudge)
            </div>
            <div style="font-size:0.86rem; color:#596B60; line-height:1.5;">
                {data.get('nudge')}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("心流一致性 (0.067Hz)", f"{data['coherence_score']} %")
    with col2:
        st.metric("身心應激狀態", data["stress_index"])
    with col3:
        st.metric("本機睡眠時數", f"{data['sleep_hours']} hr")

    st.markdown(
        f"**【去敏軌跡摘要】**\n\n{data['summary']}\n\n🕒 時間戳記：{data['timestamp']}"
    )
else:
    st.info(
        f"💡 正在等待代碼 `{user_key}` 之去敏數據。請於病患端完成調息並點擊拋接！"
    )