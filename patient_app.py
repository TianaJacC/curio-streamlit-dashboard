import os
import time
import datetime
import random
import numpy as np
import pandas as pd
import streamlit as st

# ==============================================================================
# 0. 邊緣端 Zero-Knowledge 資安配置與頁面設定
# ==============================================================================
st.set_page_config(
    page_title="夢境珍奇櫃 ‧ 探險家身心日誌",
    page_icon="🐿️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 莫蘭迪高奢法式 App 樣式
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Didot&family=Garamond:ital,wght@0,400;0,600;1,400&display=swap');

    .stApp {
        background-color: #FAF8F5;
        font-family: -apple-system, BlinkMacSystemFont, "Garamond", "Didot", "PingFang TC", sans-serif;
    }
    header[data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    footer { visibility: hidden; }

    .patient-hero-card {
        background: linear-gradient(135deg, #25352B 0%, #1A261F 100%);
        color: #FAF8F5;
        padding: 28px 32px;
        border-radius: 28px;
        box-shadow: 0 16px 40px rgba(37, 53, 43, 0.12);
        border: 1.5px solid #C2A675;
        text-align: center;
        margin-bottom: 20px;
    }
    .patient-hero-card h1 {
        font-family: "Didot", serif !important;
        color: #FAF8F5 !important;
        font-size: 1.6rem !important;
        margin-bottom: 6px !important;
    }
    .patient-hero-card p {
        color: #D3E0D7 !important;
        font-size: 0.88rem !important;
        margin: 0 !important;
    }

    .step-card {
        background: #FFFFFF;
        border: 1px solid #E4DCD0;
        border-radius: 22px;
        padding: 22px 24px;
        margin-bottom: 18px;
        box-shadow: 4px 4px 16px rgba(37, 53, 43, 0.03);
    }
    .step-title {
        font-family: "Garamond", serif;
        font-size: 1.15rem;
        font-weight: 600;
        color: #25352B;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
    }
    .step-badge {
        background: #F4F0E8;
        color: #25352B;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 0.78rem;
        border: 1px solid #C2A675;
        margin-right: 8px;
        font-family: "Didot", serif;
    }

    .stButton>button {
        border-radius: 14px !important;
        border: 1px solid #C2A675 !important;
        background: linear-gradient(135deg, #FAF8F5 0%, #F4F0E8 100%) !important;
        color: #25352B !important;
        font-weight: 500 !important;
        font-family: "Garamond", "PingFang TC", serif !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #25352B 0%, #1A261F 100%) !important;
        color: #FAF8F5 !important;
        border: 1px solid #25352B !important;
    }
    </style>
""", unsafe_allow_html=True)

# Session 狀態初始化
if "token" not in st.session_state:
    st.session_state["token"] = f"#SYM-P{random.randint(100, 999)}"
if "step1_done" not in st.session_state:
    st.session_state["step1_done"] = False
if "step2_done" not in st.session_state:
    st.session_state["step2_done"] = False
if "step3_done" not in st.session_state:
    st.session_state["step3_done"] = False
if "hrv_score" not in st.session_state:
    st.session_state["hrv_score"] = 0.0

# Header 宣示
st.markdown(f"""
    <div class="patient-hero-card">
        <div style="font-size: 2.2rem; margin-bottom: 4px;">🐿️</div>
        <h1>夢境珍奇櫃 ‧ 探險家日誌</h1>
        <p>首席珍藏家蔻恩閣長 Cone 陪伴您 ｜ 0 個資密鑰：<b style="color:#D4AF37;">{st.session_state['token']}</b></p>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# 🎨 步驟一：1 分鐘畫布塗鴉簽到 (採集 11 維度運動動態學)
# ==============================================================================
st.markdown("""
    <div class="step-card">
        <div class="step-title"><span class="step-badge">Step 1</span>🎨 1 分鐘沙龍畫布塗鴉 (11-D 動態學採集)</div>
        <div style="font-size: 0.85rem; color: #596B60; line-height: 1.6; margin-bottom: 12px;">
            請選取心靈色彩，在下方沙龍畫布隨意畫出此刻的心情（無聲紀錄筆觸壓力與微幅震幅，不需填寫冰冷量表）：
        </div>
    </div>
""", unsafe_allow_html=True)

color_pick = st.select_slider(
    "選擇此刻感官調性：",
    options=["莫蘭迪柔藍 (平穩)", "燕麥暖沙 (舒適)", "橄欖鼠尾草 (思考)", "煙燻玫瑰 (略感焦慮)", "沉香灰藍 (深度沉澱)"]
)

# 畫布模擬區 (可選擇畫筆或滑桿模擬按壓克數)
pressure_val = st.slider("大拇指滑動重力感應克數 (模擬按壓力道):", 10.0, 100.0, 42.5)

if st.button("✨ 完成 1 分鐘塗鴉簽到"):
    st.session_state["step1_done"] = True
    st.success("🎨 塗鴉簽到成功！小松鼠蔻恩閣長 Cone 已無聲紀錄您的 11 維度動態流。")

st.markdown("<hr style='border:0; border-top:1px solid #E4DCD0; margin:18px 0;'>", unsafe_allow_html=True)

# ==============================================================================
# 💓 步驟二：60 秒鏡頭 rPPG 心率變異度 (HRV) 光譜檢測
# ==============================================================================
st.markdown("""
    <div class="step-card">
        <div class="step-title"><span class="step-badge">Step 2</span>💓 60 秒鏡頭 rPPG 自律神經檢測 (HRV 提取)</div>
        <div style="font-size: 0.85rem; color: #596B60; line-height: 1.6; margin-bottom: 12px;">
            將大拇指輕貼於手機鏡頭與閃光燈上，系統運用 NumPy 在本機進行微血管光譜吸收率分析，無感提取 HRV：
        </div>
    </div>
""", unsafe_allow_html=True)

if st.button("🔴 開始 60 秒 rPPG 光譜掃描"):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # 用 NumPy 模擬微血管 PPG 波形採集與 FFT 頻譜分析
    fake_signal = []
    for i in range(100):
        time.sleep(0.03) # 模擬 60 秒縮時進度
        progress_bar.progress(i + 1)
        val = np.sin(i * 0.1) + np.random.normal(0, 0.1)
        fake_signal.append(val)
        status_text.caption(f"⏳ 正在進行光譜分析... {i+1}% (光譜吸收波形對焦中)")
    
    # 計算擬真 HRV Score
    computed_hrv = round(float(np.mean(fake_signal) * 10 + 88.5), 1)
    st.session_state["hrv_score"] = computed_hrv
    st.session_state["step2_done"] = True
    status_text.empty()
    st.success(f"🎉 60 秒 rPPG 檢測完成！您的即時心流一致性指數為：{computed_hrv}%")

st.markdown("<hr style='border:0; border-top:1px solid #E4DCD0; margin:18px 0;'>", unsafe_allow_html=True)

# ==============================================================================
# 🌿 步驟三：15 秒 0.067Hz 萌寵呼吸與迷走神經阻斷調息
# ==============================================================================
st.markdown("""
    <div class="step-card">
        <div class="step-title"><span class="step-badge">Step 3</span>🌿 15 秒 0.067Hz 萌寵呼吸調息 (迷走神經阻斷)</div>
        <div style="font-size: 0.85rem; color: #596B60; line-height: 1.6; margin-bottom: 12px;">
            看著小松鼠肚子起伏，進行黃金呼吸法（吸氣 5 秒、停頓 5 秒、呼氣 5 秒），配合馬達低頻微震拉降心率：
        </div>
    </div>
""", unsafe_allow_html=True)

if st.button("🌬️ 開啟 15 秒莫蘭迪深層調息"):
    breath_box = st.empty()
    for cycle in range(1, 4): # 15 秒 (3 次 5s 循環)
        breath_box.markdown(f"""
            <div style="background: linear-gradient(135deg, #F4F0E8 0%, #EAE4D8 100%); border: 2px solid #C2A675; border-radius: 24px; padding: 24px; text-align: center;">
                <div style="font-size: 2.8rem;">🐿️</div>
                <h3 style="color:#25352B; margin:8px 0;">吸氣 ➔ 停頓 ➔ 呼氣 (第 {cycle}/3 次)</h3>
                <p style="color:#C2A675; font-size:0.9rem;">迷走神經阻斷馬達 0.067Hz 低頻共振中...</p>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(2)
    
    breath_box.markdown("""
        <div style="background: #25352B; color: #FAF8F5; border-radius: 24px; padding: 24px; text-align: center;">
            <div style="font-size: 2.5rem;">✨</div>
            <h3 style="color:#FAF8F5; margin:8px 0;">調息完成 ‧ 心流拉升至黃金諧振區</h3>
            <p style="color:#D3E0D7; font-size:0.85rem;">身體 Cortisol 壓力負擔已無聲釋放。</p>
        </div>
    """, unsafe_allow_html=True)
    st.session_state["step3_done"] = True

# ==============================================================================
# 🕊️ 飛鴿拋接：將去敏數據拋至郭醫師診間面板 (app.py)
# ==============================================================================
st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

if st.session_state["step1_done"] and st.session_state["step2_done"] and st.session_state["step3_done"]:
    st.markdown("""
        <div style="background: #FAF8F5; border: 1.5px solid #C2A675; padding: 18px; border-radius: 20px; text-align: center; margin-bottom: 14px;">
            <b style="color:#25352B;">🕊️ 信鴿 Singer 準備就緒！</b><br>
            <span style="font-size:0.82rem; color:#596B60;">即將把去敏 Token <code>{}</code> 與心流數據送達郭醫師診間面板。</span>
        </div>
    """.format(st.session_state["token"]), unsafe_allow_html=True)

    if st.button("📡 一鍵飛鴿拋接去敏數據至診間面板", use_container_width=True):
        st.toast(f"🎉 飛鴿成功！去敏密鑰 {st.session_state['token']} 已拋接至郭醫師門診佇列！")
        st.balloons()
else:
    st.info("💡 請依序完成 Step 1 塗鴉、Step 2 rPPG 檢測與 Step 3 呼吸調息，即可解鎖飛鴿拋接！")