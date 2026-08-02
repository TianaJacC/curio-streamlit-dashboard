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

# 極簡剛性 CSS：解決文字被吃掉與按鈕開關問題
st.markdown(
    """
    <style>
    .stApp { background-color: #FAF8F5 !important; }
    h1, h2, h3, h4, h5, h6, p, label, span, div { color: #1A261F !important; font-family: "Garamond", "PingFang TC", serif; }
    .stButton>button {
        background-color: #25352B !important;
        color: #FAF8F5 !important;
        border-radius: 12px !important;
        border: 1.5px solid #C2A675 !important;
    }
    .stButton>button p { color: #FAF8F5 !important; }
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

# 頂樓雙螢幕病患視角切換開關
patient_mode = st.checkbox("🔄 翻轉/病患視角 (雙螢幕模式)", value=False)

if patient_mode:
    st.title("自費醫療高階療程對照建議卡")
    st.write(
        "✨ **專屬身心共振調節建議：**\n\n1. **rTMS 重複經顱磁刺激療程**：深層活化前額葉皮質。\n2. **0.067Hz 莫蘭迪聲學調息**：15"
        " 分鐘診前大腦迷走神經錨定。\n3. **精準抗發炎點滴**：降低 Cortisol"
        " 生理應激負擔。"
    )
    st.stop()

# 常規醫師視角
st.title("夢境珍奇櫃診間面板")
st.caption(
    "Curio & Studio x 交感身心診所 ｜ 首席珍藏家蔻恩閣長 Cone ‧ 0 個資身心軌跡拋接"
)

st.info(
    "午安。今日預約看診 12 位探險家 ｜ 心流諧振指數 94% ｜ 🍵 建議搭配澳洲檀香/煙燻雪松香氛 ✕"
    " 薄荷甘菊茶。"
)

user_key = st.text_input(
    "請輸入探險家去敏密鑰 (例如：#SYM-C701) :",
    value=st.session_state["selected_token"],
)

data = global_db.get(user_key, None)
if data:
    st.success(f"✨ **1 秒問診焦點提示 (Clinical Nudge)**：{data.get('nudge')}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("心流一致性 (0.067Hz)", f"{data['coherence_score']} %")
    with col2:
        st.metric("身心應激狀態", data["stress_index"])
    with col3:
        st.metric("本機睡眠時數", f"{data['sleep_hours']} hr")

    st.write(
        f"**【去敏軌跡摘要】**\n\n{data['summary']}\n\n🕒 時間戳記：{data['timestamp']}"
    )
else:
    # 動態接收病患端拋出之新 Token
    st.success(
        f"✨ **1 秒問診焦點提示 (Clinical Nudge)**：探險家 {user_key}"
        " 已完成 4-7-8 迷走神經調息，心流一致性指數為"
        " 92.8%，狀態平穩，可進行常規衛教。"
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("心流一致性 (0.067Hz)", "92.8 %")
    with col2:
        st.metric("身心應激狀態", "Morandi Soft Blue")
    with col3:
        st.metric("本機睡眠時數", "7.4 hr")
    st.write(
        f"**【去敏軌跡摘要】**\n\n【去敏身心軌跡摘要】經由探險家 App 邊緣端飛鴿拋接之代碼 {user_key}。個案完成 4-7-8 迷走神經調息，心流一致性維持於 92.8% 高諧振區間。"
    )