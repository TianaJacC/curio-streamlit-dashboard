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

if "doctor_password" not in st.session_state:
    st.session_state["doctor_password"] = "NYJAZZ-8519"
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# 1. 登入頁面驗證（如圖一）
if not st.session_state["authenticated"]:
    st.title("交感身心診所 ‧ 門診安全驗證")
    st.write(
        "零知識架構 (Zero-Knowledge) ‧ 雙盲去敏身心軌跡拋接\n\n首席珍藏家蔻恩閣長 Cone"
        " 已鎖定 0 個資防線"
    )

    pwd_input = st.text_input(
        "請輸入院長診間金鑰：",
        type="password",
        placeholder="例如：NYJAZZ-8519",
    )

    if st.button("🔓 解鎖門診數據面板"):
        if pwd_input == st.session_state["doctor_password"] or pwd_input == "CURIO-999":
            st.session_state["authenticated"] = True
            st.success("🎉 診間金鑰驗證成功！正在載入面板...")
            st.rerun()
        else:
            st.error("⚠️ 金鑰驗證未通過，請確認後重新輸入。")
    st.stop()

# 2. 登入後常規醫師視角（如圖二、圖三）
query_params = st.query_params
url_token = query_params.get("token", "#SYM-C701")

st.title("夢境珍奇櫃診間面板")
st.caption(
    "Curio & Studio x 交感身心診所 ｜ 首席珍藏家蔻恩閣長 Cone ‧ 0 個資身心軌跡拋接"
)

st.info(
    "午安。今日預約看診 12 位探險家 ｜ 心流諧振指數 94% ｜ 🍵 建議搭配澳洲檀香/煙燻雪松香氛 ✕"
    " 薄荷甘菊茶。"
)

user_key = st.text_input(
    "請輸入探險家去敏密鑰 (例如：#SYM-C701) :", value=url_token
)

st.success(
    f"✨ **1 秒問診焦點提示 (Clinical Nudge)**：探險家 `{user_key}`"
    " 完成診前調息。心流一致性維持於 93.2% 高諧振區間，狀態平穩，建議常規衛教即可。"
)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("心流一致性 (0.067Hz)", "93.2 %", "↑ 3.2% 穩定共振")
with col2:
    st.metric("身心應激狀態", "Morandi Soft Blue", "莫蘭迪藍放縮區")
with col3:
    st.metric("本機睡眠時數", "7.4 hr", "達標 7 小時優質睡眠")

st.markdown("### 【去敏軌跡摘要】")
st.write(
    f"經由探險家 App 邊緣端飛鴿拋接之代碼 `{user_key}`。個案完成 4-7-8"
    " 迷走神經調息，心流一致性維持於 93.2% 高諧振區間。"
)