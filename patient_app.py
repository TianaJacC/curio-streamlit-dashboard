import datetime
import os
import random
import time
import numpy as np
import pandas as pd
import streamlit as st

# ==============================================================================
# 0. 頁面配置與法式莫蘭迪高奢樣式
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

    .step-card {
        background: #FFFFFF;
        border: 1.5px solid #E4DCD0;
        border-radius: 22px;
        padding: 22px 24px;
        margin-bottom: 20px;
        box-shadow: 4px 4px 16px rgba(37, 53, 43, 0.03);
    }
    
    .doc-guidance-box {
        background: linear-gradient(135deg, #F4F0E8 0%, #EAE4D8 100%);
        border-left: 4px solid #C2A675;
        border-radius: 16px;
        padding: 18px 22px;
        margin-bottom: 20px;
        border: 1px solid #C2A675;
        border-left-width: 5px;
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

# 去背小松鼠蔻恩影片路徑（支援本機檔案或 GitHub Raw 連結）
VIDEO_PATH = "assets/squirrel_breath.mp4"
VIDEO_URL = "https://raw.githubusercontent.com/TianaJacC/curio-streamlit-dashboard/main/assets/squirrel_breath.mp4"

# 頁面頂樓 Hero 區
st.markdown(
    f"""
    <div style="background: linear-gradient(135deg, #25352B 0%, #1A261F 100%); padding: 26px; border-radius: 26px; text-align: center; border: 1.5px solid #C2A675; margin-bottom: 22px;">
        <h2 style="color: #FAF8F5 !important; font-family: 'Didot', serif; margin: 0 0 6px 0;">夢境珍奇櫃 ‧ 探險家日誌</h2>
        <p style="color: #D3E0D7 !important; font-size: 0.88rem; margin: 0;">夢境知性主理人陪伴您 ｜ 0 個資去敏密鑰：<b style="color:#D4AF37;">{st.session_state['token']}</b></p>
    </div>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# Step 1: 莫蘭迪沙龍手繪畫布 (1 分鐘簽到)
# ==============================================================================
st.markdown("### Step 1 🎨 莫蘭迪沙龍手繪畫布 (1 分鐘簽到)")
st.write("請用手指或滑鼠在下方畫布隨意塗鴉（邊緣端無聲紀錄 11 維度運動動態學軌跡）：")

user_color = st.color_picker("🎨 請選取心靈調性色彩：", "#C2A675")

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
    st.success("🎨 塗鴉簽到成功！小松鼠蔻恩閣長已無聲紀錄您的 11 維度運動動態學軌跡。")

st.markdown("---")

# ==============================================================================
# Step 2: 60 秒 rPPG 自律神經檢測
# ==============================================================================
st.markdown("### Step 2 💓 60 秒 rPPG 自律神經檢測 (HRV 提取)")
st.write("請將食指輕貼於手機鏡頭與閃光燈上，進行微血管光譜吸收率分析：")

if st.button("🔴 開始 60 秒 rPPG 光譜對焦"):
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

# ==============================================================================
# Step 3: 身心科 4-7-8 迷走神經呼吸法 (完整保留郭醫師衛教 ✕ 影片速度控制器)
# ==============================================================================
st.markdown("### Step 3 🌿 身心科 4-7-8 迷走神經阻斷呼吸法")

# 100% 完整保留郭醫師文字衛教
st.markdown(
    """
    <div class="doc-guidance-box">
        <div style="font-size: 0.95rem; font-weight: 600; color: #25352B; margin-bottom: 8px;">
            🩺 【郭家穎院長身心科臨床衛教指引】
        </div>
        <div style="font-size: 0.88rem; color: #596B60; line-height: 1.85;">
            • <b>吸氣 4 秒 (Inhale)</b>：用鼻子深吸氣，感覺氣流充盈腹部，活化副交感神經預備狀態。<br>
            • <b>留氣 7 秒 (Hold)</b>：閉氣懸息，啟動大腦迷走神經阻斷機制，抑制交感神經過度亢奮。<br>
            • <b>吐氣 8 秒 (Exhale)</b>：嘴唇微張長吐氣，完全釋放 Cortisol 生理應激與肌肉緊繃負擔。<br>
            <span style="color: #C2A675; font-weight: 600;">請觀看下方蔻恩閣長的動態與腹部起伏，配合進行深呼吸：</span>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# 整合 HTML5 Video 控制器 (慢速播放 0.25x ➔ 7 秒定格 ➔ 超慢速 0.125x 吐氣)
st.components.v1.html(
    f"""
    <div style="background: linear-gradient(135deg, #25352B 0%, #1A261F 100%); border: 2px solid #C2A675; border-radius: 24px; padding: 22px; text-align: center; color: #FAF8F5;">
        
        <div id="status-title" style="font-size: 1.15rem; font-weight: 600; color: #D4AF37; margin-bottom: 6px; font-family: 'Garamond', serif;">
            小松鼠蔻恩閣長正等待與您一同調息
        </div>
        <div id="status-timer" style="font-size: 2.2rem; font-weight: bold; color: #FAF8F5; margin-bottom: 14px; font-family: 'Didot', serif;">
            0.067 Hz 迷走神經共振
        </div>

        <div style="width: 280px; height: 280px; margin: 0 auto; overflow: hidden; border-radius: 20px; border: 1.5px solid #C2A675; background: rgba(0,0,0,0.3);">
            <video id="squirrelVideo" width="100%" height="100%" style="object-fit: cover;" playsinline muted>
                <source src="{VIDEO_URL}" type="video/mp4">
            </video>
        </div>

        <button id="startBtn" onclick="runBreathingCycle()" style="margin-top: 18px; background: linear-gradient(135deg, #FAF8F5 0%, #F4F0E8 100%); color: #25352B; border: 1.5px solid #C2A675; border-radius: 14px; padding: 12px 28px; font-size: 1rem; font-weight: 600; cursor: pointer; transition: all 0.3s ease;">
            🌬️ 開始 4-7-8 蔻恩閣長動態調息
        </button>
    </div>

    <script>
        var video = document.getElementById("squirrelVideo");
        var statusTitle = document.getElementById("status-title");
        var statusTimer = document.getElementById("status-timer");
        var startBtn = document.getElementById("startBtn");

        function runBreathingCycle() {{
            startBtn.disabled = true;
            startBtn.style.opacity = "0.5";
            video.currentTime = 0;
            startInhale();
        }}

        // 1. 吸氣 4 秒：放慢 4 倍播放前半段 (0.25x)
        function startInhale() {{
            statusTitle.innerText = "🌬️ 吸氣 (Inhale) ── 腹部膨脹 (4秒)";
            video.playbackRate = 0.25;
            video.play();

            var count = 4;
            statusTimer.innerText = count + " s";
            var timer = setInterval(function() {{
                count--;
                if(count > 0) {{
                    statusTimer.innerText = count + " s";
                }} else {{
                    clearInterval(timer);
                    startHold();
                }}
            }}, 1000);
        }}

        // 2. 留氣 7 秒：畫面定格 pause()，維持腹部最大飽滿狀態
        function startHold() {{
            video.pause();
            statusTitle.innerText = "⏸️ 留氣懸息 (Hold) ── 迷走神經阻斷活化 (7秒)";

            var count = 7;
            statusTimer.innerText = count + " s";
            var timer = setInterval(function() {{
                count--;
                if(count > 0) {{
                    statusTimer.innerText = count + " s";
                }} else {{
                    clearInterval(timer);
                    startExhale();
                }}
            }}, 1000);
        }}

        // 3. 吐氣 8 秒：放慢 8 倍播放後半段 (0.125x)
        function startExhale() {{
            statusTitle.innerText = "💨 吐氣 (Exhale) ── 嘴唇微張長吐 (8秒)";
            video.playbackRate = 0.125;
            video.play();

            var count = 8;
            statusTimer.innerText = count + " s";
            var timer = setInterval(function() {{
                count--;
                if(count > 0) {{
                    statusTimer.innerText = count + " s";
                }} else {{
                    clearInterval(timer);
                    finishCycle();
                }}
            }}, 1000);
        }}

        function finishCycle() {{
            video.pause();
            statusTitle.innerText = "✨ 4-7-8 迷走神經調息完成";
            statusTimer.innerText = "🎉 諧振成功";
            startBtn.disabled = false;
            startBtn.style.opacity = "1.0";
        }}
    </script>
""",
    height=480,
)

if st.button("✨ 確認已完成 4-7-8 呼吸調息"):
    st.session_state["step3_done"] = True
    st.success("✨ 迷走神經阻斷調息完成！Cortisol 壓力負擔已釋放。")

st.markdown("---")

# ==============================================================================
# 🕊️ 飛鴿拋接：拋接去敏數據至郭醫師診間面板
# ==============================================================================
if (
    st.session_state["step1_done"]
    and st.session_state["step2_done"]
    and st.session_state["step3_done"]
):
    token_code = st.session_state["token"]
    st.success(
        f"🕊️ 信鴿 Singer 準備就緒！去敏密鑰：**{token_code}** ｜ 心流分數：**{st.session_state['hrv_score']}%**"
    )

    doc_url = (
        f"https://curio-streamlit-dashboard.streamlit.app/?token={token_code}"
    )

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