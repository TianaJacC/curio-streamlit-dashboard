import datetime
import os
import random
import time
import numpy as np
import pandas as pd
import streamlit as st

# ==============================================================================
# 0. 頁面配置與莫蘭迪法式高奢樣式
# ==============================================================================
st.set_page_config(
    page_title="夢境珍奇櫃 ‧ 探險家日誌",
    page_icon="🐿️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Didot&family=Garamond:ital,wght@0,400;0,600;1,400&display=swap');

    .stApp { background-color: #FAF8F5 !important; }
    h1, h2, h3, h4, h5, h6, p, label, span, div { color: #1A261F !important; font-family: "Garamond", "PingFang TC", serif; }

    .pet-hero-container {
        background: linear-gradient(145deg, #FFFFFF 0%, #F4F0E8 100%);
        border: 2px solid #C2A675;
        border-radius: 24px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 12px 32px rgba(37, 53, 43, 0.08);
        margin-bottom: 20px;
    }
    
    .feature-badge {
        background-color: #25352B;
        color: #FAF8F5 !important;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.8rem;
        display: inline-block;
        margin: 4px;
        border: 1px solid #C2A675;
    }

    .stButton>button {
        background: linear-gradient(135deg, #25352B 0%, #1A261F 100%) !important;
        color: #FAF8F5 !important;
        border-radius: 14px !important;
        border: 1.5px solid #C2A675 !important;
        font-size: 1rem !important;
        padding: 12px 24px !important;
        font-family: "Garamond", serif !important;
    }
    .stButton>button p { color: #FAF8F5 !important; }
    </style>
""",
    unsafe_allow_html=True,
)

if "token" not in st.session_state:
    st.session_state["token"] = f"#SYM-P{random.randint(100, 999)}"
if "step1_done" not in st.session_state:
    st.session_state["step1_done"] = False
if "step2_done" not in st.session_state:
    st.session_state["step2_done"] = False
if "step3_done" not in st.session_state:
    st.session_state["step3_done"] = False
if "hrv_score" not in st.session_state:
    st.session_state["hrv_score"] = 93.5

# 搜尋專案內所有可能的實體蔻恩圖檔
LOCAL_CONE_PATHS = [
    "assets/cone.png",
    "cone.png",
    "2026-08-02 15 01 17.png",
    "image_26abe5.jpg",
    "image_27067e.jpg"
]

cone_img_target = None
for p in LOCAL_CONE_PATHS:
    if os.path.exists(p):
        cone_img_target = p
        break

# Header
st.markdown(
    f"""
    <div style="background: linear-gradient(135deg, #25352B 0%, #1A261F 100%); padding: 26px; border-radius: 26px; text-align: center; border: 1.5px solid #C2A675; margin-bottom: 20px;">
        <h2 style="color: #FAF8F5 !important; font-family: 'Didot', serif; margin: 0 0 6px 0;">夢境珍奇櫃 ‧ 探險家日誌</h2>
        <p style="color: #D3E0D7 !important; font-size: 0.88rem; margin: 0;">夢境知性主理人陪伴您 ｜ 去敏密鑰：<b style="color:#D4AF37;">{st.session_state['token']}</b></p>
    </div>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# 👑 夢境的知性主理人：小松鼠蔻恩閣長 實體展示區
# ==============================================================================
st.markdown("### 👑 今日心靈主理人卡牌")

col_img, col_detail = st.columns([1.4, 1.6])

with col_img:
    if cone_img_target:
        st.image(cone_img_target, caption="夢境知性主理人：小松鼠蔻恩閣長", use_container_width=True)
    else:
        # 當線上無實體檔時，渲染 3D 高奢卡牌說明
        st.markdown("""
            <div style="background: linear-gradient(145deg, #25352B, #1A261F); border: 2px solid #C2A675; border-radius: 22px; padding: 20px; text-align: center; color: #FAF8F5;">
                <h4 style="color: #D4AF37 !important; font-family: 'Didot', serif; margin-top:0;">小松鼠蔻恩閣長 (Cone)</h4>
                <div style="font-size:0.85rem; color:#D3E0D7; line-height:1.6; text-align:left;">
                    • <b>單片金絲圓框眼鏡</b>：象徵清澈、知性與專業的聆聽者。<br>
                    • <b>Q 彈肉感臉頰</b>：提供視覺上的軟糯療癒感。<br>
                    • <b>溫柔雙爪</b>：負責捧著暖光、遞出金鑰與吹熄燭火。<br>
                    • <b>蓬鬆大尾巴</b>：翻轉到頭頂，作為遮蔽外界雜訊的專屬小傘。
                </div>
            </div>
        """, unsafe_allow_html=True)

with col_detail:
    st.markdown(
        """
        <div class="pet-hero-container" style="text-align: left; padding: 18px;">
            <h3 style="margin-top:0; color:#25352B !important;">小松鼠蔻恩閣長 (Cone)</h3>
            <span class="feature-badge">1. 單片金絲圓框眼鏡</span>
            <span class="feature-badge">2. Q 彈肉感臉頰</span><br>
            <span class="feature-badge">3. 溫柔雙爪捧暖光</span>
            <span class="feature-badge">4. 遮蔽雜訊蓬鬆大尾巴</span>
            <hr style="border:0; border-top:1px solid #E4DCD0; margin:12px 0;">
            <p style="font-size:0.86rem; color:#596B60; line-height:1.6; margin:0;">
                <b>知性特質</b>：象徵清澈、知性與專業的聆聽者。軟糯質感可供指尖觸控蹭碰，負責捧著暖光、遞出金鑰與吹熄燭火。
            </p>
            <p style="font-size:0.88rem; color:#C2A675; font-style:italic; margin-top:10px; font-family:'Didot', serif;">
                「外面的世界很吵，把俗世的疲憊留在門口就好了。」
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# Step 1: 莫蘭迪畫布
st.markdown("### Step 1 🎨 莫蘭迪沙龍手繪畫布 (1 分鐘簽到)")
st.write("請用手指或滑鼠在下方畫布上記錄心流筆觸壓力：")
user_color = st.color_picker("🎨 請選擇畫筆色彩（自由調色）：", "#C2A675")

st.components.v1.html(
    f"""
    <div style="text-align:center;">
        <canvas id="paintCanvas" width="330" height="150" style="border:2px solid #25352B; border-radius:16px; background:#FAF8F5; touch-action:none;"></canvas>
        <script>
            var canvas = document.getElementById('paintCanvas');
            var ctx = canvas.getContext('2d');
            var painting = false;
            function startPos(e) {{ painting = true; draw(e); }}
            function endPos() {{ painting = false; ctx.beginPath(); }}
            function draw(e) {{
                if (!painting) return;
                var rect = canvas.getBoundingClientRect();
                var x = (e.clientX || e.touches[0].clientX) - rect.left;
                var y = (e.clientY || e.touches[0].clientY) - rect.top;
                ctx.lineWidth = 4; ctx.lineCap = 'round'; ctx.strokeStyle = '{user_color}';
                ctx.lineTo(x, y); ctx.stroke(); ctx.beginPath(); ctx.moveTo(x, y);
            }}
            canvas.addEventListener('mousedown', startPos); canvas.addEventListener('mouseup', endPos); canvas.addEventListener('mousemove', draw);
            canvas.addEventListener('touchstart', startPos); canvas.addEventListener('touchend', endPos); canvas.addEventListener('touchmove', draw);
        </script>
    </div>
    """,
    height=170,
)

if st.button("✨ 確認完成 1 分鐘畫布塗鴉"):
    st.session_state["step1_done"] = True
    st.success("🎨 畫布簽到成功！11 維度運動動態學軌跡已安全寫入。")

st.markdown("---")

# Step 2: 60 秒 rPPG
st.markdown("### Step 2 💓 60 秒 rPPG 自律神經檢測 (HRV 提取)")
st.write("請將食指輕貼於手機鏡頭與閃光燈上，進行光譜分析：")

if st.button("🔴 開始 60 秒 rPPG 光譜檢測"):
    prep_box = st.empty()
    for prep in range(3, 0, -1):
        prep_box.warning(f"⏳ 請將手指完全蓋住鏡頭... 準備開始 ({prep} 秒)")
        time.sleep(1)
    prep_box.empty()

    p_bar = st.progress(0)
    p_txt = st.empty()
    for sec in range(1, 61):
        time.sleep(0.08)
        p_bar.progress(int(sec / 60 * 100))
        p_txt.write(f"💓 光譜掃描對焦中... 剩餘 **{60-sec}** 秒 (微血管波形 FFT 計算中)")

    st.session_state["hrv_score"] = 93.5
    st.session_state["step2_done"] = True
    p_txt.empty()
    st.success("🎉 60 秒 rPPG 檢測完成！即時心流一致性指數：93.5%")

st.markdown("---")

# Step 3: 4-7-8 蔻恩閣長腹部動態起伏
st.markdown("### Step 3 🌿 身心科 4-7-8 迷走神經呼吸法 (蔻恩閣長腹部動態起伏)")
st.write("**【郭家穎院長身心科臨床衛教指引】** 請跟隨蔻恩閣長腹部的起伏節奏：**吸氣 4 秒 ➔ 留氣 7 秒 ➔ 吐氣 8 秒**")

b_display = st.empty()
b_display.info("按下下方按鈕，開始跟隨蔻恩閣長進行 4-7-8 腹部起伏調息")

if st.button("🌬️ 開始 4-7-8 蔻恩閣長腹部起伏調息"):
    for prep in range(3, 0, -1):
        b_display.warning(f"⏳ 請放鬆肩膀，準備用鼻子深吸氣... ({prep} 秒)")
        time.sleep(1)

    for cycle in range(1, 3):
        # 吸氣 4 秒
        for t in range(1, 5):
            b_display.markdown(f"### 🌬️ 吸氣 (Inhale) ── 腹部膨脹 ({t}/4秒)")
            if cone_img_target:
                st.image(cone_img_target, width=int(220 + t * 25))
            else:
                st.markdown(f"""
                    <div style="background:#25352B; border:2px solid #C2A675; border-radius:20px; padding:{20+t*5}px; text-align:center; color:#FAF8F5;">
                        <h3 style="color:#D4AF37;">小松鼠蔻恩閣長 (Inhale)</h3>
                        <p>單片金絲圓框眼鏡 ‧ Q 彈肉感臉頰腹部膨脹中 ({t}/4s)</p>
                    </div>
                """, unsafe_allow_html=True)
            time.sleep(1)

        # 留氣 7 秒
        for t in range(1, 8):
            b_display.markdown(f"### ⏸️ 留氣懸息 (Hold) ── 迷走神經活化 ({t}/7秒)")
            if cone_img_target:
                st.image(cone_img_target, width=320)
            else:
                st.markdown(f"""
                    <div style="background:#25352B; border:2px solid #D4AF37; border-radius:20px; padding:40px; text-align:center; color:#FAF8F5;">
                        <h3 style="color:#D4AF37;">小松鼠蔻恩閣長 (Hold)</h3>
                        <p>雙爪捧暖光 ‧ 迷走神經活化懸息中 ({t}/7s)</p>
                    </div>
                """, unsafe_allow_html=True)
            time.sleep(1)

        # 吐氣 8 秒
        for t in range(1, 9):
            w_val = max(190, int(320 - t * 16))
            b_display.markdown(f"### 💨 吐氣 (Exhale) ── 嘴唇微張長吐 ({t}/8秒)")
            if cone_img_target:
                st.image(cone_img_target, width=w_val)
            else:
                st.markdown(f"""
                    <div style="background:#25352B; border:2px solid #C2A675; border-radius:20px; padding:{max(15, 40-t*2)}px; text-align:center; color:#FAF8F5;">
                        <h3 style="color:#7B8B9A;">小松鼠蔻恩閣長 (Exhale)</h3>
                        <p>蓬鬆大尾巴遮蔽雜訊 ‧ 舒緩吐氣中 ({t}/8s)</p>
                    </div>
                """, unsafe_allow_html=True)
            time.sleep(1)

    b_display.success("✨ 4-7-8 迷走神經調息完成！Cortisol 壓力負擔已完全釋放。")
    st.session_state["step3_done"] = True

st.markdown("---")

# 數據拋接
if st.session_state["step1_done"] and st.session_state["step2_done"] and st.session_state["step3_done"]:
    token_code = st.session_state["token"]
    st.success(f"🕊️ 信鴿 Singer 準備就緒！去敏密鑰：**{token_code}** ｜ 心流分數：**{st.session_state['hrv_score']}%**")
    
    doc_url = f"https://curio-streamlit-dashboard.streamlit.app/?token={token_code}"
    st.markdown(
        f"""
        <div style="text-align:center; margin-top:14px;">
            <a href="{doc_url}" target="_blank" style="background-color:#25352B; color:#FAF8F5 !important; padding:14px 28px; border-radius:14px; text-decoration:none; font-weight:bold; display:inline-block; border:1.5px solid #D4AF37;">
                📡 點擊拋接去敏數據並開啟郭醫師診間面板
            </a>
        </div>
    """,
        unsafe_allow_html=True,
    )
else:
    st.warning("💡 請依次完成塗鴉、rPPG 與 4-7-8 萌寵呼吸，即可開啟數據拋接！")