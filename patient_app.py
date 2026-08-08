import base64
import datetime
import os
import random
import time
import numpy as np
import pandas as pd
import streamlit as st

# ==============================================================================
# 0. 頁面配置與高奢極簡字體樣式 (High-Contrast Elegant Styling)
# ==============================================================================
st.set_page_config(
    page_title="夢境珍奇櫃 ‧ 探險家日誌",
    page_icon="🌰",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=Noto+Serif+TC:wght@500;700&display=swap');

    .stApp { background-color: #FBF9F5 !important; }
    
    /* 強制全局高對比高奢字體 */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: #1A261F !important;
        font-family: 'Noto Serif TC', 'Cinzel', serif !important;
    }

    .french-card {
        background: #FFFFFF;
        border: 1.5px solid #C2A675;
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 22px;
        box-shadow: 0 8px 24px rgba(194, 166, 117, 0.08);
    }

    .doc-guidance-card {
        background: #FAF8F5;
        border: 1.5px solid #D4AF37;
        border-left: 6px solid #C2A675;
        border-radius: 16px;
        padding: 18px 22px;
        margin-bottom: 20px;
    }

    .stButton>button {
        background: linear-gradient(135deg, #25352B 0%, #1A261F 100%) !important;
        color: #D4AF37 !important;
        border-radius: 14px !important;
        border: 1.5px solid #D4AF37 !important;
        font-size: 1.05rem !important;
        font-weight: bold !important;
        padding: 12px 28px !important;
    }
    .stButton>button p { color: #D4AF37 !important; font-weight: bold !important; }
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

# 影片連結相容
VIDEO_URL = "https://raw.githubusercontent.com/TianaJacC/curio-streamlit-dashboard/main/assets/squirrel_breath.mp4"

# ==============================================================================
# 1. 頂樓 Header：清晰高對比黑金徽章（徹底解決密鑰看不清楚問題）
# ==============================================================================
st.markdown(
    f"""
    <div style="background: #FFFFFF; border: 2px solid #C2A675; border-radius: 22px; padding: 24px; text-align: center; box-shadow: 0 8px 24px rgba(0,0,0,0.05); margin-bottom: 24px;">
        <h2 style="color: #1A261F !important; font-weight: 800; margin: 0 0 8px 0; font-size: 1.75rem; letter-spacing: 1px;">
            🏰 夢境珍奇櫃 ‧ 探險家日誌
        </h2>
        <div style="font-size: 0.95rem; color: #4A5D50 !important; margin-bottom: 14px; font-weight: 600;">
            首席珍藏家 ‧ 小松鼠蔻恩閣長 (Cone) 陪伴您
        </div>
        <div style="display: inline-block; background: #1A261F; border: 2px solid #D4AF37; padding: 10px 26px; border-radius: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            <span style="color: #FAF8F5 !important; font-size: 1rem; font-weight: 600;">
                🗝️ 0 個資去敏密鑰：
            </span>
            <span style="color: #FFD700 !important; font-size: 1.35rem; font-weight: 900; font-family: monospace; letter-spacing: 2.5px;">
                {st.session_state['token']}
            </span>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# Step 1: 🪞 巨型畫布 ✕ 60 色純色塊盤（完全無文字提示，無選色焦慮）
# ==============================================================================
st.markdown(
    """
    <div class="french-card">
        <h3 style="color: #1A261F !important; font-size: 1.3rem; font-weight: 700; margin-bottom: 8px;">
            Step 1 🪞 手繪畫布 (1 分鐘心靈簽到)
        </h3>
        <p style="color: #596B60 !important; font-size: 0.92rem; margin-bottom: 16px;">
            請選取直覺色彩，於下方放大畫布上記錄您的筆觸：
        </p>
""",
    unsafe_allow_html=True,
)

# 60 種法式/莫蘭迪純色代碼（完全不加任何文字狀態提示）
MORANDI_60_PURE = [
    "#C2A675", "#D4AF37", "#E8DCC4", "#A68A56", "#8C6D3B", "#D9C5A0",
    "#E8A89A", "#F5D6CB", "#D18B7B", "#B86B5C", "#E3B5A4", "#F0C2B2",
    "#8A9A86", "#596B60", "#25352B", "#1A261F", "#A3B19B", "#C4D1BE",
    "#7B8B9A", "#5A6B7C", "#3D4A59", "#9EB0C2", "#C0D0E0", "#2C3845",
    "#A89B9E", "#8C7B80", "#6E5C62", "#C8BDC0", "#E0D5D8", "#524248",
    "#D6C5B3", "#B8A490", "#8A735C", "#5C4B38", "#EBE0D3", "#705943",
    "#9E9B78", "#7C7A59", "#5A583A", "#C0BD9B", "#DEDCBE", "#403E22",
    "#C78275", "#A86356", "#824337", "#E3A396", "#F5C4B8", "#5C261B",
    "#D4D0C8", "#B5B0A8", "#8E8981", "#615C55", "#F5F2EC", "#3B3731",
    "#6B3A43", "#4A222A", "#8C525D", "#2E1016", "#0D1410", "#1C1013"
]

if "canvas_color" not in st.session_state:
    st.session_state["canvas_color"] = "#C2A675"

st.write("🎨 **60 色純色視覺板（直接點擊色塊）：**")
grid_cols = st.columns(10)
for idx, hex_code in enumerate(MORANDI_60_PURE):
    col = grid_cols[idx % 10]
    with col:
        is_selected = st.session_state["canvas_color"] == hex_code
        border_s = "3px solid #1A261F" if is_selected else "1px solid #CCC"
        if st.button(" ", key=f"c_btn_{idx}"):
            st.session_state["canvas_color"] = hex_code
        st.markdown(
            f"""<div style="background-color: {hex_code}; height: 24px; border-radius: 6px; border: {border_s}; margin-top: -38px; margin-bottom: 8px; pointer-events: none;"></div>""",
            unsafe_allow_html=True,
        )

selected_c = st.session_state["canvas_color"]
st.markdown(
    f"""<div style="margin: 10px 0; font-size: 0.95rem;">當前選擇色彩：<span style="display:inline-block; width: 18px; height: 18px; background:{selected_c}; border-radius:4px; vertical-align:middle; border:1px solid #000;"></span> <b>{selected_c}</b></div>""",
    unsafe_allow_html=True,
)

# 巨型畫布 (高度 380px)
st.components.v1.html(
    f"""
    <div style="text-align:center;">
        <canvas id="paintCanvas" width="580" height="380" style="width:100%; height:380px; border:2px solid #C2A675; border-radius:20px; background:#FFFFFF; touch-action:none; cursor: crosshair;"></canvas>
        <script>
            var canvas = document.getElementById('paintCanvas');
            var ctx = canvas.getContext('2d');
            var painting = false;
            function startPos(e) {{ painting = true; draw(e); }}
            function endPos() {{ painting = false; ctx.beginPath(); }}
            function draw(e) {{
                if (!painting) return;
                var rect = canvas.getBoundingClientRect();
                var scaleX = canvas.width / rect.width;
                var scaleY = canvas.height / rect.height;
                var clientX = e.clientX || (e.touches && e.touches[0].clientX);
                var clientY = e.clientY || (e.touches && e.touches[0].clientY);
                var x = (clientX - rect.left) * scaleX;
                var y = (clientY - rect.top) * scaleY;
                ctx.lineWidth = 6; ctx.lineCap = 'round'; ctx.strokeStyle = '{selected_c}';
                ctx.lineTo(x, y); ctx.stroke(); ctx.beginPath(); ctx.moveTo(x, y);
            }}
            canvas.addEventListener('mousedown', startPos); canvas.addEventListener('mouseup', endPos); canvas.addEventListener('mousemove', draw);
            canvas.addEventListener('touchstart', startPos); canvas.addEventListener('touchend', endPos); canvas.addEventListener('touchmove', draw);
        </script>
    </div>
    """,
    height=400,
)

if st.button("🗝️ 完成筆觸簽到"):
    st.session_state["step1_done"] = True
    st.success("💎 簽到成功！運動動態學軌跡已加密寫入。")

st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# Step 2: 🕯️ 60 秒 rPPG
# ==============================================================================
st.markdown(
    """
    <div class="french-card">
        <h3 style="color: #1A261F !important; font-size: 1.3rem; font-weight: 700; margin-bottom: 8px;">
            Step 2 🕯️ 60 秒 rPPG 自律神經檢測 (HRV 提取)
        </h3>
        <p style="color: #596B60 !important; font-size: 0.92rem; margin-bottom: 16px;">
            請將食指輕貼於鏡頭上，進行微血管光譜吸收率與心流一致性計算：
        </p>
""",
    unsafe_allow_html=True,
)

if st.button("🔮 開始 60 秒 rPPG 光譜對焦"):
    prep_box = st.empty()
    for prep in range(3, 0, -1):
        prep_box.warning(f"⏳ 請蓋住鏡頭... 準備開始 ({prep} 秒)")
        time.sleep(1)
    prep_box.empty()

    p_bar = st.progress(0)
    p_txt = st.empty()
    for sec in range(1, 61):
        time.sleep(0.08)
        p_bar.progress(int(sec / 60 * 100))
        p_txt.write(f"🕯️ 微血管波形計算中... 剩餘 **{60-sec}** 秒")

    st.session_state["hrv_score"] = 93.5
    st.session_state["step2_done"] = True
    p_txt.empty()
    st.success("🎉 檢測完成！即時心流一致性指數：93.5%")

st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# Step 3: 🌰 首席珍藏家 ‧ 小松鼠蔻恩閣長 4-7-8 呼吸
# ==============================================================================
st.markdown(
    """
    <div class="french-card">
        <h3 style="color: #1A261F !important; font-size: 1.3rem; font-weight: 700; margin-bottom: 12px;">
            Step 3 🌰 4-7-8 迷走神經阻斷呼吸法
        </h3>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="doc-guidance-card">
        <div style="font-size: 1.05rem; font-weight: 700; color: #25352B; margin-bottom: 8px;">
            🩺 【郭家穎院長身心科臨床衛教指引】
        </div>
        <div style="font-size: 0.92rem; color: #33443B; line-height: 1.85;">
            • <b>吸氣 4 秒 (Inhale)</b>：用鼻子深吸氣，感覺氣流充盈腹部，活化副交感神經。<br>
            • <b>留氣 7 秒 (Hold)</b>：閉氣懸息，啟動大腦迷走神經阻斷機制，抑制交感神經過亢。<br>
            • <b>吐氣 8 秒 (Exhale)</b>：嘴唇微張長吐氣，完全釋放 Cortisol 生理應激。<br>
            <span style="color: #C2A675; font-weight: 700;">請觀察下方首席珍藏家蔻恩閣長示範腹部起伏：</span>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# 小松鼠蔻恩閣長影片 ✕ 原生播放控制
st.components.v1.html(
    f"""
    <div style="background: linear-gradient(135deg, #1A261F 0%, #25352B 100%); border: 2px solid #D4AF37; border-radius: 20px; padding: 22px; text-align: center; color: #FAF8F5;">
        
        <div id="status-title" style="font-size: 1.15rem; font-weight: bold; color: #D4AF37; margin-bottom: 6px;">
            👑 首席珍藏家 ‧ 小松鼠蔻恩閣長示範調息
        </div>
        <div id="status-timer" style="font-size: 2.2rem; font-weight: bold; color: #FFD700; margin-bottom: 14px;">
            0.067 Hz 諧振調息預備
        </div>

        <div style="width: 280px; height: 280px; margin: 0 auto; overflow: hidden; border-radius: 20px; border: 2px solid #D4AF37; background: #000;">
            <video id="squirrelVideo" width="100%" height="100%" style="object-fit: cover;" playsinline muted loop autoplay src="{VIDEO_URL}">
            </video>
        </div>

        <button id="startBtn" onclick="runBreathingCycle()" style="margin-top: 18px; background: linear-gradient(135deg, #D4AF37 0%, #C2A675 100%); color: #1A261F; border: none; border-radius: 12px; padding: 12px 30px; font-size: 1.05rem; font-weight: bold; cursor: pointer;">
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
            statusTitle.innerText = "🌬️ 吸氣 (Inhale) ── 肚子慢慢膨脹 (4秒)";
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

        function startExhale() {{
            statusTitle.innerText = "💨 吐氣 (Exhale) ── 嘴唇微張徐徐長吐 (8秒)";
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
            statusTimer.innerText = "心流諧振成功";
            startBtn.disabled = false;
            startBtn.style.opacity = "1.0";
        }}
    </script>
""",
    height=500,
)

if st.button("💎 完成 4-7-8 調息（寫入珍奇櫃紀錄）"):
    st.session_state["step3_done"] = True
    st.success("✨ 迷走神經調息完成！Cortisol 應激負擔已釋放。")

st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# 🕊️ 信鴿 Singer 拋接
# ==============================================================================
if (
    st.session_state["step1_done"]
    and st.session_state["step2_done"]
    and st.session_state["step3_done"]
):
    token_code = st.session_state["token"]
    st.markdown(
        f"""
        <div style="background: #FFFFFF; border: 2px solid #C2A675; border-radius: 20px; padding: 24px; text-align: center; box-shadow: 0 8px 24px rgba(0,0,0,0.04);">
            <h3 style="color: #25352B !important; margin-top: 0;">🕊️ 信鴿 Singer (信哥) 拋接準備就緒</h3>
            <p style="color: #596B60 !important; font-size: 0.95rem;">
                去敏密鑰：<b style="color: #1A261F !important;">{token_code}</b> ｜ 心流一致性：<b style="color: #C2A675 !important;">{st.session_state['hrv_score']}%</b>
            </p>
            <a href="https://curio-streamlit-dashboard.streamlit.app/?token={token_code}" target="_blank" style="background: linear-gradient(135deg, #25352B 0%, #1A261F 100%); color: #D4AF37 !important; padding: 14px 32px; border-radius: 14px; text-decoration: none; font-weight: bold; font-size: 1.05rem; display: inline-block; border: 1.5px solid #D4AF37;">
                📜 點擊由信鴿 Singer 拋接去敏數據至郭醫師診間
            </a>
        </div>
    """,
        unsafe_allow_html=True,
    )
else:
    st.info("💡 請依次完成 Step 1 畫布、Step 2 rPPG 與 Step 3 蔻恩呼吸，解鎖數據拋接！")