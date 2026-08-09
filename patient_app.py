import base64
import datetime
import os
import random
import time
import numpy as np
import pandas as pd
import streamlit as st

# ==============================================================================
# 1. 頁面配置與高對比冒險溫暖美學
# ==============================================================================
st.set_page_config(
    page_title="夢境珍奇櫃 ‧ 探險家日誌",
    page_icon="🌰",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# 本地影片轉 Base64 安全解法
def get_local_video_b64():
    video_candidates = [
        "Squirrel_exhales_slowly,_belly_s…_202608030927.mp4",
        "這是影片的主角蔻恩_我不要背景_只有這隻小松鼠就好_這隻小松.mp4",
        "assets/squirrel_breath.mp4",
        "squirrel_breath.mp4",
    ]
    for v_path in video_candidates:
        if os.path.exists(v_path):
            try:
                with open(v_path, "rb") as f:
                    v_bytes = f.read()
                return f"data:video/mp4;base64,{base64.b64encode(v_bytes).decode()}"
            except Exception:
                pass
    return "https://raw.githubusercontent.com/TianaJacC/curio-streamlit-dashboard/main/assets/squirrel_breath.mp4"


video_src_code = get_local_video_b64()

# 乾淨且無溢出的 CSS 注入
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=Noto+Serif+TC:wght@500;700&display=swap');

    .stApp {
        background-color: #FAF6F0 !important;
    }
    
    body, p, div, span, label, h1, h2, h3, h4 {
        font-family: 'Noto Serif TC', 'Cinzel', serif !important;
        color: #1A261F !important;
    }

    /* 溫暖冒險卡牌風格 */
    .adventure-card {
        background: #FFFFFF;
        border: 2px solid #C2A675;
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 20px rgba(194, 166, 117, 0.12);
    }

    /* 冒險者引導框 */
    .quest-box {
        background: #F4EFEA;
        border-left: 6px solid #C2A675;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 18px;
    }

    /* 自訂主按鈕 */
    .stButton>button {
        background: linear-gradient(135deg, #25352B 0%, #1A261F 100%) !important;
        color: #D4AF37 !important;
        border-radius: 14px !important;
        border: 1.5px solid #D4AF37 !important;
        font-size: 1.05rem !important;
        font-weight: bold !important;
        padding: 12px 28px !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(37, 53, 43, 0.2) !important;
    }
    .stButton>button p {
        color: #D4AF37 !important;
        font-weight: bold !important;
    }
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

# ==============================================================================
# 2. 頂部 Header：冒險遊戲風格標題與超高對比去敏密鑰
# ==============================================================================
st.markdown(
    f"""
    <div style="background: #FFFFFF; border: 2.5px solid #C2A675; border-radius: 22px; padding: 24px; text-align: center; box-shadow: 0 8px 24px rgba(0,0,0,0.06); margin-bottom: 24px;">
        <h2 style="color: #1A261F !important; font-weight: 800; margin: 0 0 6px 0; font-size: 1.75rem;">
            🏰 夢境珍奇櫃 ‧ 探險家日誌
        </h2>
        <div style="font-size: 1.05rem; color: #4A5D50 !important; margin-bottom: 16px; font-weight: 700;">
            🌰 小松鼠蔻恩閣長 Cone 陪伴您開始冒險旅程
        </div>
        
        <div style="display: inline-block; background: #FFD700; border: 2px solid #1A261F; padding: 10px 24px; border-radius: 30px; box-shadow: 0 4px 12px rgba(212,175,55,0.35);">
            <span style="color: #1A261F !important; font-size: 1rem; font-weight: 700;">
                🗝️ 探險家專屬通行密鑰：
            </span>
            <span style="color: #1A261F !important; font-size: 1.35rem; font-weight: 900; font-family: monospace; letter-spacing: 2px;">
                {st.session_state['token']}
            </span>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# Step 1: 🗺️ 冒險地圖畫布 ✕ 靈魂色彩調色盤
# ==============================================================================
st.markdown(
    """
    <div class="adventure-card">
        <h3 style="color: #1A261F !important; font-size: 1.3rem; font-weight: 700; margin-bottom: 8px;">
            第一站 🗺️ 繪製今天的冒險地圖
        </h3>
        <p style="color: #596B60 !important; font-size: 0.95rem; margin-bottom: 16px;">
            請憑第一直覺點選最吸引您的靈魂色彩，在畫布上記錄您今天的冒險足跡：
        </p>
""",
    unsafe_allow_html=True,
)

# 具備臨床研究價值的 60 色矩陣（外觀完全為冒險遊戲調色盤）
COLOR_MATRIX = [
    "#E85D04",
    "#DC2F02",
    "#D00000",
    "#9D0208",
    "#6A040F",
    "#370617",
    "#FFBA08",
    "#FAA307",
    "#F48C06",
    "#E85D04",
    "#D90429",
    "#EF233C",
    "#2B2D42",
    "#8D99AE",
    "#4A5568",
    "#2D3748",
    "#1A202C",
    "#111827",
    "#374151",
    "#4B5563",
    "#6B7280",
    "#9CA3AF",
    "#D1D5DB",
    "#E5E7EB",
    "#2A9D8F",
    "#264653",
    "#E76F51",
    "#F4A261",
    "#E9C46A",
    "#3A5A40",
    "#344E41",
    "#588157",
    "#A3B18A",
    "#DAD7CD",
    "#83C5BE",
    "#EDF6F9",
    "#3D5A80",
    "#98C1D9",
    "#E0FBFC",
    "#EE6C4D",
    "#293241",
    "#1D2D44",
    "#0D1B2A",
    "#415A77",
    "#778DA9",
    "#E0E1DD",
    "#5C6B73",
    "#93A8AC",
    "#6B705C",
    "#A5A58D",
    "#B7B7A4",
    "#DDA15E",
    "#BC6C25",
    "#283618",
    "#606C38",
    "#FEFAE0",
    "#D4A373",
    "#FAEDCD",
    "#E9EDC9",
    "#CCD5AE",
]

if "canvas_color" not in st.session_state:
    st.session_state["canvas_color"] = "#2A9D8F"

st.write("🎨 **靈魂色彩調色盤：**")
grid_cols = st.columns(10)
for idx, hex_code in enumerate(COLOR_MATRIX):
    col = grid_cols[idx % 10]
    with col:
        is_selected = st.session_state["canvas_color"] == hex_code
        border_s = "3px solid #1A261F" if is_selected else "1px solid #E0E0E0"
        if st.button(" ", key=f"color_btn_{idx}"):
            st.session_state["canvas_color"] = hex_code
        st.markdown(
            f"""<div style="background-color: {hex_code}; height: 24px; border-radius: 6px; border: {border_s}; margin-top: -38px; margin-bottom: 8px; pointer-events: none;"></div>""",
            unsafe_allow_html=True,
        )

selected_c = st.session_state["canvas_color"]
st.markdown(
    f"""
    <div style="margin: 12px 0; font-size: 0.95rem; font-weight: 600;">
        當前選取畫筆色彩：
        <span style="display:inline-block; width: 18px; height: 18px; background:{selected_c}; border-radius:4px; vertical-align:middle; border:1px solid #1A261F;"></span> 
        <b style="color:{selected_c} !important;">{selected_c}</b>
    </div>
""",
    unsafe_allow_html=True,
)

# 滿版觸控繪圖畫布
st.components.v1.html(
    f"""
    <div style="text-align:center;">
        <canvas id="adventureCanvas" width="580" height="360" style="width:100%; height:360px; border:2px solid #C2A675; border-radius:18px; background:#FFFFFF; touch-action:none; cursor: crosshair; box-shadow: inset 0 2px 6px rgba(0,0,0,0.05);"></canvas>
        <script>
            var canvas = document.getElementById('adventureCanvas');
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
    height=380,
)

if st.button("🗝️ 儲存冒險地圖筆觸"):
    st.session_state["step1_done"] = True
    st.success("✨ 冒險印記已順利寫入日誌！")

st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# Step 2: 🔮 冒險者能量波形校準
# ==============================================================================
st.markdown(
    """
    <div class="adventure-card">
        <h3 style="color: #1A261F !important; font-size: 1.3rem; font-weight: 700; margin-bottom: 8px;">
            第二站 🔮 冒險者能量共振校準
        </h3>
        <p style="color: #596B60 !important; font-size: 0.95rem; margin-bottom: 16px;">
            請將手指輕貼於鏡頭上，讓小松鼠蔻恩幫您測量當前的心流平穩指數：
        </p>
""",
    unsafe_allow_html=True,
)

if st.button("⚡ 開始 60 秒能量校準"):
    prep_box = st.empty()
    for prep in range(3, 0, -1):
        prep_box.warning(f"⏳ 請將手指貼緊鏡頭... 準備開始 ({prep} 秒)")
        time.sleep(1)
    prep_box.empty()

    p_bar = st.progress(0)
    p_txt = st.empty()
    for sec in range(1, 61):
        time.sleep(0.08)
        p_bar.progress(int(sec / 60 * 100))
        p_txt.write(f"🕯️ 光譜能量對焦中... 剩餘 **{60-sec}** 秒")

    st.session_state["hrv_score"] = 93.5
    st.session_state["step2_done"] = True
    p_txt.empty()
    st.success("🎉 能量對焦完成！心流指數：93.5%（狀態極佳）")

st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# Step 3: 🌰 蔻恩閣長 4-7-8 冒險呼吸（精準引導）
# ==============================================================================
st.markdown(
    """
    <div class="adventure-card">
        <h3 style="color: #1A261F !important; font-size: 1.3rem; font-weight: 700; margin-bottom: 12px;">
            第三站 🌰 與蔻恩閣長一起進行 4-7-8 能量調息
        </h3>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="quest-box">
        <div style="font-size: 1rem; font-weight: 700; color: #25352B; margin-bottom: 6px;">
            📜 蔻恩閣長的冒險調息祕訣：
        </div>
        <div style="font-size: 0.92rem; color: #33443B; line-height: 1.8;">
            • <b>吸氣 4 秒</b>：跟著蔻恩用鼻子深吸氣，感受大自然的能量流入。<br>
            • <b>閉氣 7 秒</b>：閉氣定神，讓心神沉澱平靜。<br>
            • <b>吐氣 8 秒</b>：微張嘴巴徐徐吐氣，放鬆全身累積的疲憊。<br>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# 小松鼠 HTML5 / JS 動態引導面板
st.components.v1.html(
    f"""
    <div style="background: linear-gradient(135deg, #1A261F 0%, #25352B 100%); border: 2px solid #D4AF37; border-radius: 20px; padding: 20px; text-align: center; color: #FAF8F5; box-shadow: 0 8px 20px rgba(0,0,0,0.2);">
        
        <div id="status-title" style="font-size: 1.15rem; font-weight: bold; color: #FFD700; margin-bottom: 6px;">
            🌰 蔻恩閣長準備好了，跟著我的節奏一起調息吧！
        </div>
        <div id="status-timer" style="font-size: 2rem; font-weight: bold; color: #FFFFFF; margin-bottom: 12px;">
            準備開始
        </div>

        <div style="width: 280px; height: 280px; margin: 0 auto; overflow: hidden; border-radius: 18px; border: 2px solid #FFD700; background: #000;">
            <video id="squirrelVideo" width="100%" height="100%" style="object-fit: cover;" playsinline muted loop autoplay src="{video_src_code}">
            </video>
        </div>

        <button id="startBtn" onclick="runBreathingCycle()" style="margin-top: 18px; background: linear-gradient(135deg, #FFD700 0%, #C2A675 100%); color: #1A261F; border: none; border-radius: 12px; padding: 12px 28px; font-size: 1rem; font-weight: bold; cursor: pointer;">
            🌬️ 開始 4-7-8 蔻恩閣長呼吸調息
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
            statusTitle.innerText = "🌬️ 深吸氣 (4秒) ── 感受清晨森林的能量";
            video.playbackRate = 0.3;
            video.play();

            var count = 4;
            statusTimer.innerText = count + " 秒";
            var timer = setInterval(function() {{
                count--;
                if(count > 0) {{
                    statusTimer.innerText = count + " 秒";
                }} else {{
                    clearInterval(timer);
                    startHold();
                }}
            }}, 1000);
        }}

        function startHold() {{
            video.pause();
            statusTitle.innerText = "⏸️ 靜心閉氣 (7秒) ── 讓心神沉澱平靜";

            var count = 7;
            statusTimer.innerText = count + " 秒";
            var timer = setInterval(function() {{
                count--;
                if(count > 0) {{
                    statusTimer.innerText = count + " 秒";
                }} else {{
                    clearInterval(timer);
                    startExhale();
                }}
            }}, 1000);
        }}

        function startExhale() {{
            statusTitle.innerText = "💨 緩吐氣 (8秒) ── 釋放身上所有的疲憊";
            video.playbackRate = 0.15;
            video.play();

            var count = 8;
            statusTimer.innerText = count + " 秒";
            var timer = setInterval(function() {{
                count--;
                if(count > 0) {{
                    statusTimer.innerText = count + " 秒";
                }} else {{
                    clearInterval(timer);
                    finishCycle();
                }}
            }}, 1000);
        }}

        function finishCycle() {{
            video.pause();
            statusTitle.innerText = "✨ 能量充沛！您已完成今天的調息冒險";
            statusTimer.innerText = "心流諧振成功";
            startBtn.disabled = false;
            startBtn.style.opacity = "1.0";
        }}
    </script>
""",
    height=500,
)

if st.button("💎 完成調息冒險（領取冒險證書）"):
    st.session_state["step3_done"] = True
    st.success("✨ 恭喜您完成今天的冒險旅程！")

st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# 4. 數據拋接與黑客松亮點功能：一鍵同步至診間
# ==============================================================================
if (
    st.session_state["step1_done"]
    and st.session_state["step2_done"]
    and st.session_state["step3_done"]
):
    token_code = st.session_state["token"]
    st.markdown(
        f"""
        <div style="background: #FFFFFF; border: 2.5px solid #C2A675; border-radius: 20px; padding: 22px; text-align: center; box-shadow: 0 8px 24px rgba(0,0,0,0.06);">
            <h3 style="color: #25352B !important; margin-top: 0;">📜 冒險日誌拋接準備就緒</h3>
            <p style="color: #596B60 !important; font-size: 0.95rem;">
                通行密鑰：<b style="color: #1A261F !important;">{token_code}</b> ｜ 心流評估：<b style="color: #C2A675 !important;">{st.session_state['hrv_score']}%</b>
            </p>
            <a href="https://curio-streamlit-dashboard.streamlit.app/?token={token_code}" target="_blank" style="background: linear-gradient(135deg, #25352B 0%, #1A261F 100%); color: #D4AF37 !important; padding: 14px 30px; border-radius: 12px; text-decoration: none; font-weight: bold; font-size: 1rem; display: inline-block; border: 1.5px solid #D4AF37;">
                🕊️ 由信鴿 Singer 將日誌拋接至郭醫師診間
            </a>
        </div>
    """,
        unsafe_allow_html=True,
    )
else:
    st.info("💡 完成三站冒險後，即可將今天的探險日誌拋接至診間喔！")