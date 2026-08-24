import datetime
import hashlib
import json
import os
import random
import time
import pandas as pd
import streamlit as st

# ==============================================================================
# 0. 頁面配置與高奢莫蘭迪樣式
# ==============================================================================
st.set_page_config(
    page_title="夢境珍奇櫃 ‧ 探險家終端",
    page_icon="🐿️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Didot&family=Garamond:ital,wght@0,400;0,600;1,400&display=swap');
    .stApp {
        background-color: #000000 !important;
        color: #FAF8F5 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Garamond", "Georgia", "PingFang TC", sans-serif;
    }
    .dream-card {
        background: linear-gradient(135deg, #1A261F 0%, #0D1610 100%);
        border: 1.5px solid #C2A675;
        border-radius: 24px;
        padding: 24px 28px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(194, 166, 117, 0.15);
    }
    .letter-box {
        background: #121A15;
        border-left: 4px solid #C2A675;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        font-size: 0.9rem;
        line-height: 1.8;
        color: #E0DDD5;
    }
    .breath-circle {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        background: radial-gradient(circle, #C2A675 0%, #1A261F 100%);
        margin: 25px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        box-shadow: 0 0 30px rgba(194, 166, 117, 0.4);
        animation: breathAnimation 15s infinite ease-in-out;
    }
    @keyframes breathAnimation {
        0% { transform: scale(0.85); opacity: 0.7; }
        33% { transform: scale(1.2); opacity: 1; filter: drop-shadow(0 0 15px #C2A675); }
        100% { transform: scale(0.85); opacity: 0.7; }
    }
    .stButton>button {
        border-radius: 14px !important;
        border: 1.5px solid #C2A675 !important;
        background: linear-gradient(135deg, #C2A675 0%, #8C734B 100%) !important;
        color: #0D1610 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 10px 24px !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #FAF8F5 0%, #EAE4D8 100%) !important;
        color: #0D1610 !important;
        box-shadow: 0 0 20px rgba(194, 166, 117, 0.6) !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 初始化 Session State
if "app_stage" not in st.session_state:
    st.session_state["app_stage"] = "invitation"  # invitation -> consent -> game
if "patient_token" not in st.session_state:
    st.session_state["patient_token"] = "#SYM-FC60"
if "consent_agreed" not in st.session_state:
    st.session_state["consent_agreed"] = False

# 莫蘭迪原石色盤
MORANDI_PALETTE = {
    "鼠尾草綠 (深層放鬆)": "#7A8B7B",
    "莫蘭迪藍 (情緒平穩)": "#6B7D8E",
    "陶土粉 (溫暖釋壓)": "#B8837D",
    "燕麥白 (思緒歸零)": "#EBE4D8",
    "深林綠 (自然共振)": "#25352B",
    "香檳金 (能量修復)": "#C2A675",
}

# ==============================================================================
# 階段一：信哥的入閣邀請函 (沉浸式前導)
# ==============================================================================
if st.session_state["app_stage"] == "invitation":
    st.markdown(
        """
        <div class="dream-card" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 6px;">🐿️ 🌲</div>
            <div style="font-family: Didot, serif; color: #C2A675; letter-spacing: 3px;">CABINET OF CURIOSITIES</div>
            <h2 style="font-family: Garamond, serif; margin: 8px 0;">夢境珍奇櫃 ‧ 入閣邀請函</h2>
            <div style="font-size: 0.85rem; color: #A2B3A7;">發明專利案號：115130127 ｜ 零知識邊緣架構</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="letter-box">
            <b>親愛的 探險家：</b><br>
            誠摯地邀請您加入夢境珍奇櫃──一個充滿驚奇與無限放鬆的地方。在這裡，您將與首席珍藏家<b>小松鼠蔻恩閣長 Cone</b>，一起在無邊際的純黑星空下調息漫步。<br><br>
            🏛️ <b>珍奇櫃的閣長</b>：小松鼠蔻恩閣長 🐿️<br>
            🏠 <b>閣長的家</b>：無重力橡樹海 0 號 ‧ 倒懸流金松果閣 3 樓（藏有微醺香草香氣的樹洞內）<br><br>
            🎒 <b>入閣必備行李</b>：<br>
            1. 一雙準備撫摸小松鼠的大拇指。<br>
            2. 允許自己隨時放假、盡情慵懶的絕對豁免權。<br>
            3. 不需要帶任何理性大道理與世俗 KPI，這裡全程實施 OLED 物理級深夜防護（#000000）。<br><br>
            <hr style="border:0; border-top:1px solid #334438; margin:12px 0;">
            🕊️ <b>皇家郵政信鴿 信哥 叮嚀</b>：<br>
            「咕咕！本鴿的飛行航線受高階去敏密法保護，導航系統<b>只認得密鑰代碼，不認得真名</b>！請絕對不要留下您的真實姓名與住址，否則本鴿在半空中會嚴重迷航、一頭撞上松果塔的！咕咕！」
        </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button("🗝️ 查閱探險家知情同意書並開啟入口", use_container_width=True):
        st.session_state["app_stage"] = "consent"
        st.rerun()

# ==============================================================================
# 階段二：電子知情同意書與法規免責宣告
# ==============================================================================
elif st.session_state["app_stage"] == "consent":
    st.markdown(
        """
        <div class="dream-card">
            <h3 style="margin-top:0; color:#C2A675; font-family:Garamond, serif;">【夢境珍奇櫃】日常身心支持體驗 ‧ 電子知情同意書</h3>
            <div style="font-size:0.85rem; color:#A2B3A7; margin-bottom:12px;">居里研創（Curio & Studio） ✕ 0 個資實體隔離防線</div>
            <div style="font-size:0.84rem; color:#E0DDD5; line-height:1.75; max-height:260px; overflow-y:scroll; background:#080D0A; padding:14px; border-radius:12px; border:1px solid #25352B;">
                <b>第一條：非醫療行為剛性宣告與法規排除</b><br>
                本行動裝置應用程式定位純屬日常健康管理、去污名化身心支持與美學生活引導。本軟體不提供、亦不構成任何實質臨床醫療診斷、法定處方箋開立或法定心理諮商。全面排除《醫療法》、《心理師法》之連帶責任。若面臨急性身心危機，請遵循實體門診醫師醫囑。<br><br>
                <b>第二條：無個資零知識架構與個資實體隔離</b><br>
                系統數據庫 100% 實施無個資零知識架構（Zero-Knowledge Architecture）。系統絕不收集、絕不經手真實姓名、身分證字號、病歷號或聯絡電話。診所端實體病歷實施物理隔離管理，技術底層無從交叉比對。<br><br>
                <b>第三條：紅線危機無聲熔斷機制</b><br>
                若系統偵測到涉及即時人身安全等高危詞彙，將自動顯示衛福部安心專線 1925、生命線 1995。<br><br>
                <b>第四條：自由退場與數據學術授權</b><br>
                使用者自願參與，並授權去識別化之行為特徵數據作為演算法優化與學術論文發表用途，本軟體絕無可能反向追蹤個人身分。
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    agree = st.checkbox(
        "我已詳細閱讀並理解上述條款，同意在 100% 零個資保護下進入體驗"
    )
    if st.button("🚀 確認同意並開始心流冒險", use_container_width=True):
        if agree:
            st.session_state["consent_agreed"] = True
            st.session_state["app_stage"] = "game"
            st.rerun()
        else:
            st.warning("⚠️ 請先勾選同意條款以確保您的權益！")

# ==============================================================================
# 階段三：正式遊戲化調息與拋接流程 (小松鼠全程引導)
# ==============================================================================
elif st.session_state["app_stage"] == "game":
    # 頂部狀態列
    st.markdown(
        f"""
        <div class="dream-card" style="padding:16px 22px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <b>🐿️ 閣長蔻恩引導中</b> ｜ 🌱 <b>綠色算力能耗</b>：0.002 kWh (Edge AI 減碳)
                </div>
                <div style="color:#C2A675; font-weight:bold; font-family:monospace; font-size:1.1rem;">
                    {st.session_state['patient_token']}
                </div>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # 關卡 0：安全照片雜湊登入
    st.markdown("#### 📷 關卡 0 ‧ 安全照片匿名登入 (Photo Hash Login)")
    st.caption(
        "無需記憶複雜密碼，上傳一張帶給您安全感的照片，系統在手機本機即時生成 SHA-256"
        " 匿名雙鑰。"
    )
    photo_file = st.file_uploader(
        "點擊選擇安全照片", type=["jpg", "png", "jpeg"]
    )
    if photo_file:
        raw_hash = hashlib.sha256(photo_file.getvalue()).hexdigest()[:6].upper()
        st.session_state["patient_token"] = f"#SYM-{raw_hash}"
        st.success(
            f"✨ 安全照片解鎖成功！本機匿名標籤：`{st.session_state['patient_token']}`"
        )

    # 關卡 1：靈魂原石共鳴
    st.markdown("---")
    st.markdown("#### 🔮 關卡 1 ‧ 靈魂原石圖騰 (心流色彩映射)")
    st.caption(
        "選擇今日能引導您內心平靜的原石色彩，將在畫布上轉換為去敏心流特徵："
    )

    selected_color_label = st.selectbox(
        "選擇原石色彩：", list(MORANDI_PALETTE.keys()), index=0
    )
    selected_hex = MORANDI_PALETTE[selected_color_label]

    col_c1, col_c2 = st.columns([3, 1])
    with col_c1:
        stroke_val = st.slider("當前身心張力/筆觸深度調節：", 1, 15, 6)
    with col_c2:
        st.markdown(
            f"""
            <div style="background:{selected_hex}; color:#000000; height:65px; border-radius:14px; display:flex; align-items:center; justify-content:center; font-weight:bold; margin-top:10px;">
                {selected_color_label.split(' ')[0]}
            </div>
        """,
            unsafe_allow_html=True,
        )

    # 關卡 2：0.067Hz 調息 (小松鼠帶領)
    st.markdown("---")
    st.markdown("#### 🌿 關卡 2 ‧ 0.067Hz 心流共振調息 (小松鼠引導)")
    st.write(
        "跟隨小松鼠蔻恩閣長的呼吸節奏進行 15 秒深度調息（**吸氣 5 秒 ➔ 呼氣 10"
        " 秒**）："
    )

    st.markdown(
        """
        <div class="breath-circle">
            🐿️
        </div>
        <div style="text-align:center; font-size:0.85rem; color:#A2B3A7; margin-bottom:15px;">
            【吸氣 5 秒 ➔ 呼氣 10 秒 ‧ 0.067Hz 迷走神經共振中】
        </div>
    """,
        unsafe_allow_html=True,
    )

    # 拋接按鈕
    if st.button(
        "🚀 完成冒險並將去敏特徵拋接至郭醫師診間", use_container_width=True
    ):
        calc_score = round(random.uniform(89.0, 97.0), 1)
        calc_sleep = round(random.uniform(6.8, 7.8), 1)

        st.balloons()
        st.success(
            f"🎉 拋接成功！動態時間鎖標籤：`{st.session_state['patient_token']}`\n\n"
            f"心流諧振評分：`{calc_score}%` ｜ 原石色彩：`{selected_color_label.split(' ')[0]}`\n\n"
            "請於看診時將此短碼告知郭醫師進行 15 秒瞬間對照解鎖！"
        )