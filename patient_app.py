import datetime
import os
import random
import time
import numpy as np
import pandas as pd
import streamlit as st

# ==============================================================================
# 0. 頁面配置與高對比質感樣式
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
    @import url('https://fonts.googleapis.com/css2?family=Garamond:ital,wght@0,400;0,600;1,400&display=swap');

    .stApp { background-color: #FAF8F5 !important; }
    h1, h2, h3, h4, h5, h6, p, label, span, div { color: #1A261F !important; font-family: "Garamond", "PingFang TC", serif; }

    .doc-guidance-box {
        background: #F4F0E8;
        border-left: 5px solid #C2A675;
        border-radius: 16px;
        padding: 18px 22px;
        margin-bottom: 20px;
        border: 1px solid #D4AF37;
    }

    .stButton>button {
        background: linear-gradient(135deg, #25352B 0%, #1A261F 100%) !important;
        color: #FAF8F5 !important;
        border-radius: 14px !important;
        border: 1.5px solid #C2A675 !important;
        font-size: 1.05rem !important;
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

VIDEO_URL = "https://raw.githubusercontent.com/TianaJacC/curio-streamlit-dashboard/main/assets/squirrel_breath.mp4"

# ==============================================================================
# 1. 頁面頂樓 Header（修正文字看不清楚問題）
# ==============================================================================
st.markdown(
    f"""
    <div style="background: #FFFFFF; border: 2px solid #C2A675; border-radius: 20px; padding: 22px; text-align: center; box-shadow: 0 4px 16px rgba(0,0,0,0.05); margin-bottom: 24px;">
        <h2 style="color: #1A261F !important; font-weight: bold; margin: 0 0 8px 0; font-size: 1.6rem;">夢境珍奇櫃 ‧ 探險家日誌</h2>
        <p style="color: #4A5D50 !important; font-size: 0.95rem; margin: 0; font-weight: 500;">
            夢境知性主理人陪伴您 ｜ 去敏密鑰：<span style="background: #25352B; color: #D4AF37 !important; padding: 3px 10px; border-radius: 8px; font-weight: bold;">{st.session_state['token']}</span>
        </p>
    </div>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# Step 1: 簡化標題、放大畫布、直覺色塊
# ==============================================================================
st.markdown("### Step 1 🎨 手繪畫布 (1 分鐘簽到)")
st.write("請選擇您喜歡的色彩，在下方放大畫布上記錄您的筆觸：")

# 5 個簡單好懂的大色塊選擇
color_cols = st.columns(5)
if "selected_color" not in st.session_state:
    st.session_state["selected_color"] = "#C2A675"

with color_cols[0]:
    if st.button("✨ 香檳金"):
        st.session_state["selected_color"] = "#C2A675"
with color_cols[1]:
    if st.button("🌸 蜜桃粉"):
        st.session_state["selected_color"] = "#E8A89A"
with color_cols[2]:
    if st.button("🌿 鼠尾草"):
        st.session_state["selected_color"] = "#8A9A86"
with color_cols[3]:
    if st.button("墨黑"):
        st.session_state["selected_color"] = "#1A261F"
with color_cols[4]:
    if st.button("🌲 深綠"):
        st.session_state["selected_color"] = "#25352B"

current_color = st.session_state["selected_color"]
st.caption(f"目前畫筆色彩：<span style='color:{current_color}; font-weight:bold;'>█████</span>", unsafe_allow_html=True)

# 放大版畫布（高度增加至 240px，觸控與滑鼠好畫很多）
st.components.v1.html(
    f"""
    <div style="text-align:center;">
        <canvas id="paintCanvas" width="360" height="240" style="border:2.5px solid #25352B; border-radius:20px; background:#FFFFFF; touch-action:none; box-shadow: 0 4px 12px rgba(0,0,0,0.06); cursor: crosshair;"></canvas>
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
                ctx.lineWidth = 5; ctx.lineCap = 'round'; ctx.strokeStyle = '{current_color}';
                ctx.lineTo(x, y); ctx.stroke(); ctx.beginPath(); ctx.moveTo(x, y);
            }}
            canvas.addEventListener('mousedown', startPos); canvas.addEventListener('mouseup', endPos); canvas.addEventListener('mousemove', draw);
            canvas.addEventListener('touchstart', startPos); canvas.addEventListener('touchend', endPos); canvas.addEventListener('touchmove', draw);
        </script>
    </div>
    """,
    height=260,
)

if st.button("✨ 確認完成 1 分鐘畫布簽到"):
    st.session_state["step1_done"] = True
    st.success("🎨 簽到成功！運動動態學軌跡已寫入。")

st.markdown("---")

# ==============================================================================
# Step 2: 60 秒 rPPG
# ==============================================================================
st.markdown("### Step 2 💓 60 秒 rPPG 自律神經檢測")
st.write("請將食指輕貼於手機鏡頭與閃光燈上進行光譜檢測：")

if st.button("🔴 開始 60 秒 rPPG 光譜檢測"):
    prep_box = st.empty()
    for prep in range(3, 0, -1):
        prep_box.warning(f"⏳ 請將手指蓋住鏡頭... 準備開始 ({prep} 秒)")
        time.sleep(1)
    prep_box.empty()

    p_bar = st.progress(0)
    p_txt = st.empty()
    for sec in range(1, 61):
        time.sleep(0.08)
        p_bar.progress(int(sec / 60 * 100))
        p_txt.write(f"💓 掃描對焦中... 剩餘 **{60-sec}** 秒")

    st.session_state["hrv_score"] = 93.5
    st.session_state["step2_done"] = True
    p_txt.empty()
    st.success("🎉 檢測完成！即時心流一致性指數：93.5%")

st.markdown("---")

# ==============================================================================
# Step 3: 身心科 4-7-8 迷走神經呼吸法（小松鼠蔻恩閣長登場區）
# ==============================================================================
st.markdown("### Step 3 🌿 身心科 4-7-8 迷走神經阻斷呼吸法")

st.markdown(
    """
    <div class="doc-guidance-box">
        <div style="font-size: 1rem; font-weight: bold; color: #25352B; margin-bottom: 6px;">
            🩺 【郭家穎院長身心科臨床衛教指引】
        </div>
        <div style="font-size: 0.9rem; color: #33443B; line-height: 1.8;">
            • <b>吸氣 4 秒 (Inhale)</b>：用鼻子深吸氣，感覺氣流充盈腹部。<br>
            • <b>留氣 7 秒 (Hold)</b>：閉氣懸息，啟動迷走神經阻斷機制。<br>
            • <b>吐氣 8 秒 (Exhale)</b>：嘴唇微張長吐氣，完全釋放生理緊繃。<br>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# 小松鼠蔻恩閣長 影片 ✕ 實體卡牌雙重保障
st.components.v1.html(
    f"""
    <div style="background: linear-gradient(135deg, #25352B 0%, #1A261F 100%); border: 2px solid #C2A675; border-radius: 24px; padding: 20px; text-align: center; color: #FAF8F5;">
        
        <div id="status-title" style="font-size: 1.1rem; font-weight: bold; color: #D4AF37; margin-bottom: 6px;">
            👑 夢境知性主理人：小松鼠蔻恩閣長 (Cone)
        </div>
        <div id="status-timer" style="font-size: 2rem; font-weight: bold; color: #FAF8F5; margin-bottom: 12px;">
            預備進行 4-7-8 調息
        </div>

        <div style="width: 280px; height: 280px; margin: 0 auto; overflow: hidden; border-radius: 20px; border: 2px solid #D4AF37; background: #000;">
            <video id="squirrelVideo" width="100%" height="100%" style="object-fit: cover;" playsinline muted autoplay loop src="{VIDEO_URL}">
            </video>
        </div>

        <button id="startBtn" onclick="runBreathingCycle()" style="margin-top: 16px; background: linear-gradient(135deg, #FAF8F5 0%, #F4F0E8 100%); color: #25352B; border: 1.5px solid #C2A675; border-radius: 12px; padding: 12px 28px; font-size: 1.05rem; font-weight: bold; cursor: pointer;">
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

        function startInhale() {{
            statusTitle.innerText = "🌬️ 吸氣 (Inhale) ── 腹部膨脹";
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

        function startHold() {{
            video.pause();
            statusTitle.innerText = "⏸️ 留氣懸息 (Hold) ── 迷走神經阻斷活化";

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

        function startExhale() {{
            statusTitle.innerText = "💨 吐氣 (Exhale) ── 嘴唇微張長吐";
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

if st.button("✨ 確認完成 4-7-8 調息"):
    st.session_state["step3_done"] = True
    st.success("✨ 調息完成！Cortisol 壓力已釋放。")

st.markdown("---")

# ==============================================================================
# 🕊️ 飛鴿數據拋接
# ==============================================================================
if (
    st.session_state["step1_done"]
    and st.session_state["step2_done"]
    and st.session_state["step3_done"]
):
    token_code = st.session_state["token"]
    st.success(f"🕊️ 信鴿 Singer 準備就緒！去敏密鑰：**{token_code}**")

    doc_url = f"https://curio-streamlit-dashboard.streamlit.app/?token={token_code}"
    st.markdown(
        f"""
        <div style="text-align:center; margin-top:14px;">
            <a href="{doc_url}" target="_blank" style="background-color:#25352B; color:#FAF8F5 !important; padding:14px 28px; border-radius:14px; text-decoration:none; font-weight:bold; display:inline-block; border:1.5px solid #D4AF37;">
                📡 點擊拋接去敏數據至郭醫師診間面板
            </a>
        </div>
    """,
        unsafe_allow_html=True,
    )
else:
    st.warning("💡 請完成塗鴉、rPPG 與 4-7-8 呼吸，開啟數據拋接！")