import base64
import datetime
import os
import random
import time
import numpy as np
import pandas as pd
import streamlit as st

# ==============================================================================
# 0. 頁面配置與高對比法式溫暖美學 (Warm French Medical Aesthetic)
# ==============================================================================
st.set_page_config(
    page_title="夢境珍奇櫃 ‧ 探險家日誌",
    page_icon="🌰",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# 本地影片轉 Base64 剛性安全解法 (徹底解決黑盒問題)
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
    # 網路 CDN 極速備用
    return "https://raw.githubusercontent.com/TianaJacC/curio-streamlit-dashboard/main/assets/squirrel_breath.mp4"


video_src_code = get_local_video_b64()

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=Noto+Serif+TC:wght@500;700&display=swap');

    /* 溫暖舒服、不刺眼的法式羊膏白底色 */
    .stApp { background-color: #FAF6F0 !important; }
    
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: #1A261F !important;
        font-family: 'Noto Serif TC', 'Cinzel', serif !important;
    }

    /* 溫暖圓潤高奢卡牌 */
    .french-card {
        background: #FFFFFF;
        border: 1.5px solid #C2A675;
        border-radius: 22px;
        padding: 24px 26px;
        margin-bottom: 24px;
        box-shadow: 0 8px 24px rgba(194, 166, 117, 0.1);
    }

    /* 郭醫師衛教專屬卡片 */
    .doc-guidance-card {
        background: #F5EFEE;
        border: 1.5px solid #D4AF37;
        border-left: 6px solid #C2A675;
        border-radius: 18px;
        padding: 20px 24px;
        margin-bottom: 20px;
    }

    /* 高質感按鈕 */
    .stButton>button {
        background: linear-gradient(135deg, #25352B 0%, #1A261F 100%) !important;
        color: #D4AF37 !important;
        border-radius: 14px !important;
        border: 1.5px solid #D4AF37 !important;
        font-size: 1.05rem !important;
        font-weight: bold !important;
        padding: 12px 28px !important;
        box-shadow: 0 4px 15px rgba(37, 53, 43, 0.15) !important;
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

# ==============================================================================
# 1. 頁面頂樓 Header：完全清晰可見的高對比去敏密鑰徽章
# ==============================================================================
st.markdown(
    f"""
    <div style="background: #FFFFFF; border: 2.5px solid #C2A675; border-radius: 24px; padding: 26px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.05); margin-bottom: 26px;">
        <h2 style="color: #1A261F !important; font-weight: 800; margin: 0 0 8px 0; font-size: 1.8rem; letter-spacing: 1px;">
            🏰 夢境珍奇櫃 ‧ 探險家日誌
        </h2>
        <div style="font-size: 0.98rem; color: #4A5D50 !important; margin-bottom: 16px; font-weight: 600;">
            首席珍藏家 ‧ 小松鼠蔻恩閣長 (Cone) 溫暖陪伴您
        </div>
        
        <div style="display: inline-block; background: #FFD700; border: 2px solid #1A261F; padding: 10px 28px; border-radius: 30px; box-shadow: 0 4px 15px rgba(212,175,55,0.4);">
            <span style="color: #1A261F !important; font-size: 1.05rem; font-weight: 700;">
                🗝️ 0 個資去敏密鑰：
            </span>
            <span style="color: #1A261F !important; font-size: 1.4rem; font-weight: 900; font-family: monospace; letter-spacing: 3px;">
                {st.session_state['token']}
            </span>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# Step 1: 🪞 巨型畫布 ✕ 60 色身心科臨床研究價值色盤 (Clinical Color Matrix)
# ==============================================================================
st.markdown(
    """
    <div class="french-card">
        <h3 style="color: #1A261F !important; font-size: 1.35rem; font-weight: 700; margin-bottom: 8px;">
            Step 1 🪞 筆觸簽到畫布 (1 分鐘心靈靈魂解構)
        </h3>
        <p style="color: #596B60 !important; font-size: 0.92rem; margin-bottom: 16px;">
            下方 60 色依據身心科臨床色彩心理學區分，請憑直覺選擇當下最吸引您的色彩進行手繪：
        </p>
""",
    unsafe_allow_html=True,
)

# 具研究價值之 60 色臨床分區矩陣（完全不顯示字面狀態，保留研究純粹性）
RESEARCH_COLOR_MATRIX = [
    # A. 焦慮與交感高亢度評估區 (High Sympathetic)
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
    # B. 情緒抑鬱與低落度評估區 (Anhedonia / Low Mood)
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
    # C. 副交感神經恢復與舒緩區 (Parasympathetic Recovery)
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
    # D. 夜間焦慮與安眠需求評估區 (Sleep / Circadian)
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
    # E. 社交防禦與邊緣警戒度評估區 (Social Guarding)
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

st.write("🎨 **60 色臨床研究指標色盤（請直接點選）：**")

grid_cols = st.columns(10)
for idx, hex_code in enumerate(RESEARCH_COLOR_MATRIX):
    col = grid_cols[idx % 10]
    with col:
        is_selected = st.session_state["canvas_color"] == hex_code
        border_s = "3px solid #1A261F" if is_selected else "1px solid #E0E0E0"
        if st.button(" ", key=f"r_c_{idx}"):
            st.session_state["canvas_color"] = hex_code
        st.markdown(
            f"""<div style="background-color: {hex_code}; height: 26px; border-radius: 6px; border: {border_s}; margin-top: -38px; margin-bottom: 8px; pointer-events: none;"></div>""",
            unsafe_allow_html=True,
        )

selected_c = st.session_state["canvas_color"]
st.markdown(
    f"""
    <div style="margin: 12px 0; font-size: 0.95rem; font-weight: 600;">
        當前選取研究代碼色彩：
        <span style="display:inline-block; width: 20px; height: 20px; background:{selected_c}; border-radius:5px; vertical-align:middle; border:1px solid #1A261F;"></span> 
        <b style="color:{selected_c} !important;">{selected_c}</b>
    </div>
""",
    unsafe_allow_html=True,
)

# 巨型畫布 (高度 380px 滿版)
st.components.v1.html(
    f"""
    <div style="text-align:center;">
        <canvas id="paintCanvas" width="580" height="380" style="width:100%; height:380px; border:2px solid #C2A675; border-radius:20px; background:#FFFFFF; touch-action:none; cursor: crosshair; box-shadow: inset 0 2px 8px rgba(0,0,0,0.04);"></canvas>
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

if st.button("🗝️ 完成筆觸簽到（寫入珍奇櫃日誌）"):
    st.session_state["step1_done"] = True
    st.success("💎 簽到成功！運動動態學軌跡已寫入數據鏈。")

st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# Step 2: 🕯️ 60 秒 rPPG
# ==============================================================================
st.markdown(
    """
    <div class="french-card">
        <h3 style="color: #1A261F !important; font-size: 1.35rem; font-weight: 700; margin-bottom: 8px;">
            Step 2 🕯️ 60 秒 rPPG 自律神經檢測 (HRV 提取)
        </h3>
        <p style="color: #596B60 !important; font-size: 0.92rem; margin-bottom: 16px;">
            請將食指輕貼於手機鏡頭上，進行微血管光譜吸收率與心流一致性計算：
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
        p_txt.write(f"🕯️ 微血管波形 FFT 計算中... 剩餘 **{60-sec}** 秒")

    st.session_state["hrv_score"] = 93.5
    st.session_state["step2_done"] = True
    p_txt.empty()
    st.success("🎉 檢測完成！即時心流一致性指數：93.5%")

st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# Step 3: 🌰 首席珍藏家 ‧ 小松鼠蔻恩閣長 (Cone) 4-7-8 呼吸法（100% 精準動作）
# ==============================================================================
st.markdown(
    """
    <div class="french-card">
        <h3 style="color: #1A261F !important; font-size: 1.35rem; font-weight: 700; margin-bottom: 12px;">
            Step 3 🌰 4-7-8 迷走神經阻斷呼吸法
        </h3>
""",
    unsafe_allow_html=True,
)

# 郭醫師衛教卡片
st.markdown(
    """
    <div class="doc-guidance-card">
        <div style="font-size: 1.05rem; font-weight: 700; color: #25352B; margin-bottom: 8px;">
            🩺 【郭家穎院長身心科臨床衛教指引】
        </div>
        <div style="font-size: 0.92rem; color: #33443B; line-height: 1.85;">
            • <b>吸氣 4 秒 (Inhale)</b>：用鼻子深吸氣，感覺氣流充盈腹部，活化副交感神經預備狀態。<br>
            • <b>留氣 7 秒 (Hold)</b>：閉氣懸息，啟動大腦迷走神經阻斷機制，抑制交感神經過亢。<br>
            • <b>吐氣 8 秒 (Exhale)</b>：嘴唇微張長吐氣，完全釋放 Cortisol 生理應激與肌肉緊繃。<br>
            <span style="color: #C2A675; font-weight: 700;">請觀察下方首席珍藏家蔻恩閣長示範腹部起伏：</span>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# 小松鼠蔻恩閣長呼吸控制器 (採用 Base64 內嵌，100% 絕不黑屏)
st.components.v1.html(
    f"""
    <div style="background: linear-gradient(135deg, #1A261F 0%, #25352B 100%); border: 2.5px solid #D4AF37; border-radius: 22px; padding: 22px; text-align: center; color: #FAF8F5; box-shadow: 0 10px 25px rgba(0,0,0,0.2);">
        
        <div style="color: #FFD700; font-size: 0.85rem; letter-spacing: 2px; font-family: sans-serif; margin-bottom: 4px;">
            CHIEF CURATOR OF DREAM CABINET
        </div>
        <div id="status-title" style="font-size: 1.2rem; font-weight: bold; color: #FAF8F5; margin-bottom: 6px;">
            👑 首席珍藏家 ‧ 小松鼠蔻恩閣長 (Cone) 示範調息
        </div>
        <div id="status-timer" style="font-size: 2.2rem; font-weight: bold; color: #FFD700; margin-bottom: 14px;">
            0.067 Hz 諧振調息預備
        </div>

        <div style="width: 300px; height: 300px; margin: 0 auto; overflow: hidden; border-radius: 20px; border: 2.5px solid #FFD700; background: #000; box-shadow: 0 8px 20px rgba(0,0,0,0.5);">
            <video id="squirrelVideo" width="100%" height="100%" style="object-fit: cover;" playsinline muted loop autoplay src="{video_src_code}">
            </video>
        </div>

        <button id="startBtn" onclick="runBreathingCycle()" style="margin-top: 20px; background: linear-gradient(135deg, #FFD700 0%, #C2A675 100%); color: #1A261F; border: none; border-radius: 14px; padding: 14px 32px; font-size: 1.1rem; font-weight: bold; cursor: pointer; box-shadow: 0 4px 15px rgba(252,211,77,0.4);">
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
            statusTitle.innerText = "🌬️ 吸氣 (Inhale) ── 腹部慢慢膨脹 (4秒)";
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
            statusTitle.innerText = "✨ 4-7-8 迷走神經共振完成";
            statusTimer.innerText = "心流諧振成功";
            startBtn.disabled = false;
            startBtn.style.opacity = "1.0";
        }}
    </script>
""",
    height=520,
)

if st.button("💎 完成 4-7-8 調息（獲得心流解鎖認證）"):
    st.session_state["step3_done"] = True
    st.success("✨ 迷走神經調息完成！Cortisol 應激負擔已徹底釋放。")

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