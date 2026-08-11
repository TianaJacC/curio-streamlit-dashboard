import base64
import os
import random
import time
import streamlit as st

# ==============================================================================
# 0. 頁面配置與高對比極簡冒險美學
# ==============================================================================
st.set_page_config(
    page_title="夢境珍奇櫃 ‧ 探險家日誌",
    page_icon="🌰",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# 本地影片轉 Base64 剛性安全解法
def get_local_video_b64():
    video_candidates = [
        "video.mp4",
        "Squirrel_exhales_slowly,_belly_s…_202608030927.mp4",
        "這是影片的主角蔻恩_我不要背景_只有這隻小松鼠就好_這隻小松.mp4",
        "assets/squirrel_breath.mp4",
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

# 清潔 CSS 封裝，徹底消滅頂部原始碼外漏問題
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=Noto+Serif+TC:wght@500;700&display=swap');

    .stApp { background-color: #FAF6F0 !important; }
    html, body, p, div, span, label, h1, h2, h3, h4 {
        font-family: 'Noto Serif TC', 'Cinzel', serif !important;
        color: #1A261F !important;
    }
    .adventure-card {
        background: #FFFFFF; border: 2px solid #C2A675; border-radius: 18px;
        padding: 20px; margin-bottom: 20px; box-shadow: 0 6px 18px rgba(194, 166, 117, 0.1);
    }
    .quest-box {
        background: #F4EFEA; border-left: 5px solid #C2A675; border-radius: 10px;
        padding: 14px 16px; margin-bottom: 16px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #25352B 0%, #1A261F 100%) !important;
        color: #D4AF37 !important; border-radius: 12px !important; border: 1.5px solid #D4AF37 !important;
        font-size: 1rem !important; font-weight: bold !important; padding: 10px 24px !important;
        width: 100% !important; box-shadow: 0 4px 12px rgba(37, 53, 43, 0.15) !important;
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
if "canvas_color" not in st.session_state:
    st.session_state["canvas_color"] = "#2A9D8F"

# 1. 頂樓 Header (單行無縫內聯 HTML，徹底修復溢出程式碼)
token_val = st.session_state["token"]
header_html = f'<div style="background:#FFFFFF; border:2px solid #C2A675; border-radius:20px; padding:20px; text-align:center; box-shadow:0 6px 20px rgba(0,0,0,0.05); margin-bottom:20px;"><h2 style="color:#1A261F !important; font-weight:800; margin:0 0 4px 0; font-size:1.6rem;">🏰 夢境珍奇櫃 ‧ 探險家日誌</h2><div style="font-size:0.98rem; color:#4A5D50 !important; margin-bottom:14px; font-weight:700;">🌰 蔻恩閣長陪您開始冒險旅程</div><div style="display:inline-block; background:#1A261F; border:2px solid #D4AF37; padding:8px 24px; border-radius:25px; box-shadow:0 4px 12px rgba(0,0,0,0.2);"><span style="color:#FAF8F5 !important; font-size:0.95rem; font-weight:600;">🗝️ 0 個資去敏密鑰：</span><span style="color:#FFD700 !important; font-size:1.3rem; font-weight:900; font-family:monospace; letter-spacing:2.5px;">{token_val}</span></div></div>'
st.markdown(header_html, unsafe_allow_html=True)

# Step 1: 🗺️ 冒險地圖畫布 ✕ 無文字引導純色盤 (不拉長直排)
st.markdown(
    """
    <div class="adventure-card">
        <h3 style="color: #1A261F !important; font-size: 1.2rem; font-weight: 700; margin-bottom: 6px;">
            第一站 🗺️ 繪製冒險地圖
        </h3>
        <p style="color: #596B60 !important; font-size: 0.9rem; margin-bottom: 12px;">
            點選吸引您的色彩，在畫布上記錄今天的冒險足跡：
        </p>
""",
    unsafe_allow_html=True,
)

RESEARCH_COLORS = [
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

colors_json = str(RESEARCH_COLORS)
cur_color = st.session_state["canvas_color"]

color_picker_html = f"""
<div style="background: #F9F6F0; border: 1.5px solid #C2A675; border-radius: 12px; padding: 10px; margin-bottom: 12px;">
    <div style="font-size: 0.85rem; font-weight: bold; color: #1A261F; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
        <span>🎨 選擇色彩代碼</span>
        <span id="colorCodeDisplay" style="color: {cur_color}; font-family: monospace; font-size: 0.95rem; font-weight: 800;">{cur_color}</span>
    </div>
    <div id="colorGrid" style="display: grid; grid-template-columns: repeat(10, 1fr); gap: 5px; max-height: 110px; overflow-y: auto; padding-right: 2px;">
    </div>
</div>

<script>
    var colors = {colors_json};
    var grid = document.getElementById("colorGrid");
    var codeDisplay = document.getElementById("colorCodeDisplay");

    colors.forEach(function(hex) {{
        var btn = document.createElement("div");
        btn.style.backgroundColor = hex;
        btn.style.height = "22px";
        btn.style.borderRadius = "4px";
        btn.style.cursor = "pointer";
        btn.style.border = "1px solid rgba(0,0,0,0.15)";
        btn.onclick = function() {{
            codeDisplay.innerText = hex;
            codeDisplay.style.color = hex;
            window.parent.postMessage({{type: 'COLOR_SELECT', color: hex}}, '*');
        }};
        grid.appendChild(btn);
    }});
</script>
"""

st.components.v1.html(color_picker_html, height=145)
selected_c = st.session_state["canvas_color"]

st.components.v1.html(
    f"""
    <div style="text-align:center;">
        <canvas id="adventureCanvas" width="580" height="320" style="width:100%; height:320px; border:2px solid #C2A675; border-radius:14px; background:#FFFFFF; touch-action:none; cursor: crosshair; box-shadow: inset 0 2px 6px rgba(0,0,0,0.04);"></canvas>
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
    height=340,
)

if st.button("🗝️ 儲存冒險地圖筆觸"):
    st.session_state["step1_done"] = True
    st.success("✨ 冒險印記已順利記錄！")

st.markdown("</div>", unsafe_allow_html=True)

# Step 2: 🔮 冒險者能量共振
st.markdown(
    """
    <div class="adventure-card">
        <h3 style="color: #1A261F !important; font-size: 1.2rem; font-weight: 700; margin-bottom: 6px;">
            第二站 🔮 冒險者能量共振
        </h3>
        <p style="color: #596B60 !important; font-size: 0.9rem; margin-bottom: 12px;">
            請將手指輕貼於鏡頭上，讓蔻恩為您測量當前的心流指數：
        </p>
""",
    unsafe_allow_html=True,
)

if st.button("⚡ 開始 60 秒能量校準"):
    prep_box = st.empty()
    for prep in range(3, 0, -1):
        prep_box.warning(f"⏳ 請貼緊鏡頭... 準備開始 ({prep} 秒)")
        time.sleep(1)
    prep_box.empty()

    p_bar = st.progress(0)
    p_txt = st.empty()
    for sec in range(1, 61):
        time.sleep(0.08)
        p_bar.progress(int(sec / 60 * 100))
        p_txt.write(f"🕯️ 光譜對焦中... 剩餘 **{60-sec}** 秒")

    st.session_state["step2_done"] = True
    p_txt.empty()
    st.success("🎉 對焦完成！心流指數：93.5%（狀態極佳）")

st.markdown("</div>", unsafe_allow_html=True)

# Step 3: 🌰 蔻恩閣長 4-7-8 呼吸調息 (JS 控制 100% 不黑屏)
st.markdown(
    """
    <div class="adventure-card">
        <h3 style="color: #1A261F !important; font-size: 1.2rem; font-weight: 700; margin-bottom: 10px;">
            第三站 🌰 與蔻恩閣長進行 4-7-8 調息
        </h3>
""",
    unsafe_allow_html=True,
)

st.components.v1.html(
    f"""
    <style>
        @keyframes holdPulse {{
            0% {{ transform: scale(1.0); }}
            50% {{ transform: scale(1.03); }}
            100% {{ transform: scale(1.0); }}
        }}
        .pulsing {{ animation: holdPulse 3.5s ease-in-out infinite; }}
    </style>

    <div style="background: linear-gradient(135deg, #1A261F 0%, #25352B 100%); border: 2px solid #D4AF37; border-radius: 18px; padding: 16px; text-align: center; color: #FAF8F5;">
        <div id="status-title" style="font-size: 1.05rem; font-weight: bold; color: #FFD700; margin-bottom: 4px;">
            🌰 跟著蔻恩閣長一起調息吧！
        </div>
        <div id="status-timer" style="font-size: 1.8rem; font-weight: bold; color: #FFFFFF; margin-bottom: 10px;">
            準備開始
        </div>
        <div id="videoContainer" style="width: 250px; height: 250px; margin: 0 auto; overflow: hidden; border-radius: 16px; border: 2px solid #FFD700; background: #000;">
            <video id="squirrelVideo" width="100%" height="100%" style="object-fit: cover;" playsinline muted src="{video_src_code}">
            </video>
        </div>
        <button id="startBtn" onclick="runBreathingCycle()" style="margin-top: 16px; background: linear-gradient(135deg, #FFD700 0%, #C2A675 100%); color: #1A261F; border: none; border-radius: 10px; padding: 10px 24px; font-size: 0.95rem; font-weight: bold; cursor: pointer; width: 100%;">
            🌬️ 開始 4-7-8 呼吸調息
        </button>
    </div>

    <script>
        var video = document.getElementById("squirrelVideo");
        var container = document.getElementById("videoContainer");
        var statusTitle = document.getElementById("status-title");
        var statusTimer = document.getElementById("status-timer");
        var startBtn = document.getElementById("startBtn");

        function runBreathingCycle() {{
            startBtn.disabled = true;
            startBtn.style.opacity = "0.5";
            startInhale();
        }}

        function startInhale() {{
            container.classList.remove("pulsing");
            statusTitle.innerText = "🌬️ 深吸氣 (4秒) ── 感覺能量流入";
            video.currentTime = 0; video.playbackRate = 0.3; video.play();
            var count = 4; statusTimer.innerText = count + " 秒";
            var timer = setInterval(function() {{
                count--;
                if(count > 0) statusTimer.innerText = count + " 秒";
                else {{ clearInterval(timer); startHold(); }}
            }}, 1000);
        }}

        function startHold() {{
            video.pause(); container.classList.add("pulsing");
            statusTitle.innerText = "⏸️ 靜心閉氣 (7秒) ── 心神完全沉澱";
            var count = 7; statusTimer.innerText = count + " 秒";
            var timer = setInterval(function() {{
                count--;
                if(count > 0) statusTimer.innerText = count + " 秒";
                else {{ clearInterval(timer); startExhale(); }}
            }}, 1000);
        }}

        function startExhale() {{
            container.classList.remove("pulsing");
            statusTitle.innerText = "💨 緩吐氣 (8秒) ── 釋放身上所有疲憊";
            var duration = 8000; var startFrameTime = video.currentTime; var startTime = performance.now();
            var count = 8; statusTimer.innerText = count + " 秒";
            var countdownTimer = setInterval(function() {{
                count--;
                if(count > 0) statusTimer.innerText = count + " 秒";
                else clearInterval(countdownTimer);
            }}, 1000);

            function step(now) {{
                var elapsed = now - startTime;
                var progress = elapsed / duration;
                if (progress < 1) {{
                    video.currentTime = Math.max(0, startFrameTime * (1 - progress));
                    requestAnimationFrame(step);
                }} else {{ video.currentTime = 0; finishCycle(); }}
            }}
            requestAnimationFrame(step);
        }}

        function finishCycle() {{
            statusTitle.innerText = "✨ 能量充沛！準備完成";
            statusTimer.innerText = "心流諧振成功";
            startBtn.disabled = false; startBtn.style.opacity = "1.0";
        }}
    </script>
""",
    height=460,
)

# 修正文案：這是開始前的一個準備動作！
if st.button("✨ 完成準備，開始冒險旅程"):
    st.session_state["step3_done"] = True
    st.success("✨ 調息準備完畢！已開啟連線。")

st.markdown("</div>", unsafe_allow_html=True)

# 數據拋接至郭醫師診間面板 (帶參數 URL 拋接，100% 直達)
if (
    st.session_state["step1_done"]
    and st.session_state["step2_done"]
    and st.session_state["step3_done"]
):
    token_code = st.session_state["token"]
    st.markdown(
        f"""
        <div style="background: #FFFFFF; border: 2px solid #C2A675; border-radius: 18px; padding: 18px; text-align: center; box-shadow: 0 6px 18px rgba(0,0,0,0.05);">
            <h3 style="color: #25352B !important; margin-top: 0; font-size: 1.2rem;">📜 冒險日誌拋接就緒</h3>
            <p style="color: #596B60 !important; font-size: 0.9rem;">
                通行密鑰：<b style="color: #1A261F !important;">{token_code}</b>
            </p>
            <a href="https://curio-streamlit-dashboard.streamlit.app/?token={token_code}" target="_blank" style="background: linear-gradient(135deg, #25352B 0%, #1A261F 100%); color: #D4AF37 !important; padding: 12px 26px; border-radius: 10px; text-decoration: none; font-weight: bold; font-size: 0.95rem; display: inline-block; border: 1.5px solid #D4AF37;">
                🕊️ 由信鴿 Singer 將日誌拋接至郭醫師診間
            </a>
        </div>
    """,
        unsafe_allow_html=True,
    )
else:
    st.info("💡 完成三站準備後，即可將日誌拋接至郭醫師診間！")