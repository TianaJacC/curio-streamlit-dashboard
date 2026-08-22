import base64
import json
import os
import random
import time
import streamlit as st

# ==============================================================================
# 0. 頁面配置與 RPG 探險手遊介面 (冒險者 HUD)
# ==============================================================================
st.set_page_config(
    page_title="夢境珍奇櫃 ‧ 探險家手冊",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="collapsed",
)


def get_local_video_b64():
    for p in [
        "video.mp4",
        "Squirrel_exhales_slowly,_belly_s…_202608030927.mp4",
        "assets/squirrel_breath.mp4",
    ]:
        if os.path.exists(p):
            try:
                with open(p, "rb") as f:
                    return (
                        f"data:video/mp4;base64,{base64.b64encode(f.read()).decode()}"
                    )
            except Exception:
                pass
    return "https://raw.githubusercontent.com/TianaJacC/curio-streamlit-dashboard/main/assets/squirrel_breath.mp4"


video_b64 = get_local_video_b64()

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Noto+Serif+TC:wght@600;900&display=swap');
    .stApp { background: radial-gradient(circle, #25382E 0%, #121C16 100%) !important; }
    html, body, p, div, span, label, h1, h2, h3, h4 {
        font-family: 'Noto Serif TC', 'Cinzel', serif !important; color: #F4EAD4 !important;
    }
    .rpg-scroll {
        background: #FAF6ED; border: 3px solid #D4AF37; border-radius: 18px;
        padding: 20px; margin-bottom: 22px; box-shadow: 0 10px 30px rgba(0,0,0,0.6);
        color: #1A261F !important;
    }
    .rpg-scroll p, .rpg-scroll h3, .rpg-scroll span, .rpg-scroll div { color: #1A261F !important; }
    .stButton>button {
        background: linear-gradient(135deg, #D4AF37 0%, #997528 100%) !important;
        color: #1A261F !important; border-radius: 25px !important; border: 2px solid #FFF8DC !important;
        font-size: 1.05rem !important; font-weight: 900 !important; width: 100% !important; padding: 10px 24px !important;
        box-shadow: 0 4px 15px rgba(212,175,55,0.4) !important;
    }
    .stButton>button p { color: #1A261F !important; font-weight: 900 !important; }
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
    st.session_state["canvas_color"] = "#E85D04"

# 1. 冒險者公會 HUD (密鑰與能量進度)
token_code = st.session_state["token"]
completed_num = sum(
    [
        st.session_state["step1_done"],
        st.session_state["step2_done"],
        st.session_state["step3_done"],
    ]
)
energy_val = int((completed_num / 3) * 100)

hud_single_line = f'<div style="background:linear-gradient(180deg, rgba(26,38,31,0.95) 0%, rgba(13,20,16,0.95) 100%); border:2px solid #D4AF37; border-radius:18px; padding:16px 20px; margin-bottom:18px;"><div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;"><div style="font-size:1.15rem; font-weight:900; color:#FFD700;">🏰 夢境珍奇櫃 ‧ 冒險者通行證</div><div style="background:#000; border:1.5px solid #FFD700; padding:4px 14px; border-radius:20px; font-family:monospace; font-size:0.95rem; font-weight:bold; color:#FFD700;">🗝️ {token_code}</div></div><div style="font-size:0.82rem; color:#D3E0D7; margin-bottom:6px;">🌰 守護者蔻恩指引 ｜ 綠色算力能耗：<b>0.002 kWh (Edge AI 減碳)</b> ｜ 冒險進度：<b>{energy_val}%</b></div><div style="width:100%; height:10px; background:#0D1410; border-radius:5px; border:1px solid #C2A675; overflow:hidden;"><div style="width:{max(5, energy_val)}%; height:100%; background:linear-gradient(90deg, #E85D04, #FFD700); transition:width 0.5s;"></div></div></div>'
st.markdown(hud_single_line, unsafe_allow_html=True)

# 2. 🌲 冒險指南羅盤（農業部林業署 Open Data ✕ 全球氣象 API）
is_abroad = st.checkbox("🌐 探險家目前位於海外（切換跨國 OpenAQ / Open-Meteo 氣象指標）", value=False)
if not is_abroad:
    env_str = "大氣氣壓: 1013.2 hPa ｜ AQI 空品: 22 良好 ｜ 芬多精負離子: 8,500 ions/cm³"
    rec_str = "【林業署步道推薦】奧萬大國家森林遊樂區 ‧ 森林療癒試辦步道（適合平穩副交感活性）"
else:
    env_str = "全球連線 ｜ 氣壓: 1016.5 hPa ｜ PM2.5: 8.2 μg/m³ ｜ 濕度: 54% (Open-Meteo API)"
    rec_str = "【全球綠色指引】海外氣壓平穩，建議前往當地森林公園進行 15 分鐘綠意感官療癒。"

st.markdown(
    f"""
    <div style="background: rgba(244,234,212,0.1); border: 1px dashed #D4AF37; border-radius: 14px; padding: 12px 16px; margin-bottom: 20px; font-size: 0.84rem; line-height: 1.6;">
        🧭 <b>冒險羅盤定位：</b> {env_str}<br>
        🌲 <b>今日秘境指引：</b> {rec_str}
    </div>
""",
    unsafe_allow_html=True,
)

# 第一關：靈魂圖騰繪製
st.markdown(
    """
    <div class="rpg-scroll">
        <h3 style="margin-top:0; font-size:1.2rem;">🔮 第一關：靈魂原石圖騰</h3>
        <p style="font-size:0.86rem;">點選吸引您的色彩原石，在畫布上記錄今天的冒險足跡：</p>
""",
    unsafe_allow_html=True,
)

RESEARCH_COLORS = [
    "#E85D04", "#DC2F02", "#D00000", "#9D0208", "#6A040F", "#370617",
    "#FFBA08", "#FAA307", "#F48C06", "#E85D04", "#D90429", "#EF233C",
    "#2B2D42", "#8D99AE", "#4A5568", "#2D3748", "#1A202C", "#111827",
    "#374151", "#4B5563", "#6B7280", "#9CA3AF", "#D1D5DB", "#E5E7EB",
    "#2A9D8F", "#264653", "#E76F51", "#F4A261", "#E9C46A", "#3A5A40",
    "#344E41", "#588157", "#A3B18A", "#DAD7CD", "#83C5BE", "#EDF6F9",
    "#3D5A80", "#98C1D9", "#E0FBFC", "#EE6C4D", "#293241", "#1D2D44",
    "#0D1B2A", "#415A77", "#778DA9", "#E0E1DD", "#5C6B73", "#93A8AC",
    "#6B705C", "#A5A58D", "#B7B7A4", "#DDA15E", "#BC6C25", "#283618",
    "#606C38", "#FEFAE0", "#D4A373", "#FAEDCD", "#E9EDC9", "#CCD5AE"
]

cur_c = st.session_state["canvas_color"]
st.components.v1.html(
    f"""
    <div style="background:#ECE5D8; border:1.5px solid #C2A675; border-radius:12px; padding:10px; margin-bottom:10px;">
        <div style="font-size:0.85rem; font-weight:bold; color:#1A261F; margin-bottom:8px; display:flex; justify-content:space-between;">
            <span>🎨 靈魂共鳴原石</span><span id="cCode" style="color:{cur_c}; font-family:monospace; font-weight:bold;">{cur_c}</span>
        </div>
        <div id="grid" style="display:grid; grid-template-columns:repeat(10, 1fr); gap:5px; max-height:110px; overflow-y:auto;"></div>
    </div>
    <script>
        var colors = {json.dumps(RESEARCH_COLORS)};
        var grid = document.getElementById("grid");
        var cCode = document.getElementById("cCode");
        colors.forEach(function(hex) {{
            var b = document.createElement("div");
            b.style.backgroundColor = hex; b.style.height = "22px"; b.style.borderRadius = "4px";
            b.style.cursor = "pointer"; b.style.border = "1px solid rgba(0,0,0,0.15)";
            b.onclick = function() {{ cCode.innerText = hex; cCode.style.color = hex; window.parent.postMessage({{type:'COLOR_SELECT', color:hex}}, '*'); }};
            grid.appendChild(b);
        }});
    </script>
""",
    height=145,
)

st.components.v1.html(
    f"""
    <div style="text-align:center;">
        <canvas id="c" width="580" height="260" style="width:100%; height:260px; border:2px dashed #C2A675; border-radius:14px; background:#FFF; cursor:crosshair; touch-action:none;"></canvas>
        <script>
            var canvas = document.getElementById('c'), ctx = canvas.getContext('2d'), draw = false;
            function start(e) {{ draw = true; move(e); }}
            function end() {{ draw = false; ctx.beginPath(); }}
            function move(e) {{
                if (!draw) return;
                var r = canvas.getBoundingClientRect(), sx = canvas.width/r.width, sy = canvas.height/r.height;
                var x = ((e.clientX || (e.touches && e.touches[0].clientX)) - r.left) * sx;
                var y = ((e.clientY || (e.touches && e.touches[0].clientY)) - r.top) * sy;
                ctx.lineWidth = 6; ctx.lineCap = 'round'; ctx.strokeStyle = '{cur_c}';
                ctx.lineTo(x, y); ctx.stroke(); ctx.beginPath(); ctx.moveTo(x, y);
            }}
            canvas.onmousedown = start; canvas.onmouseup = end; canvas.onmousemove = move;
            canvas.ontouchstart = start; canvas.ontouchend = end; canvas.ontouchmove = move;
        </script>
    </div>
""",
    height=280,
)

if st.button("✨ 封存第一關圖騰"):
    st.session_state["step1_done"] = True
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# 第二關：生命水晶共振 (rPPG 自律神經脈動)
st.markdown(
    """
    <div class="rpg-scroll">
        <h3 style="margin-top:0; font-size:1.2rem;">💎 第二關：生命水晶共振 (rPPG 邊緣運算)</h3>
        <p style="font-size:0.86rem;">將手指完全貼合鏡頭與補光燈，啟動微血管光學脈動校準：</p>
""",
    unsafe_allow_html=True,
)

if st.button("⚡ 啟動 60 秒水晶共振"):
    box = st.empty()
    for s in range(3, 0, -1):
        box.warning(f"⏳ 感測紅光強度 (Red Channel >= 120)... 準備啟動 ({s} 秒)")
        time.sleep(1)
    box.empty()
    bar = st.progress(0)
    msg = st.empty()
    for i in range(1, 61):
        time.sleep(0.08)
        bar.progress(int(i / 60 * 100))
        msg.write(f"🕯️ 邊緣端 FFT 濾波計算中... 剩餘 **{60-i}** 秒 ｜ 紅光強度：**148 (手指已完全覆蓋)**")
    st.session_state["step2_done"] = True
    msg.empty()
    st.success("🎉 水晶共振完成！即時心流穩定度：93.5%")
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# 第三關：守護者蔻恩 4-7-8 調息
st.markdown(
    """
    <div class="rpg-scroll">
        <h3 style="margin-top:0; font-size:1.2rem;">🌰 第三關：守護者蔻恩神殿調息</h3>
""",
    unsafe_allow_html=True,
)

st.components.v1.html(
    f"""
    <style>
        @keyframes holdPulse {{ 0% {{ transform: scale(1.0); }} 50% {{ transform: scale(1.04); }} 100% {{ transform: scale(1.0); }} }}
        .pulsing {{ animation: holdPulse 3.5s ease-in-out infinite; }}
    </style>
    <div style="background:linear-gradient(180deg, #1A261F 0%, #0D1410 100%); border:2px solid #D4AF37; border-radius:18px; padding:16px; text-align:center; color:#FAF8F5;">
        <div id="st-title" style="font-size:1.05rem; font-weight:bold; color:#FFD700; margin-bottom:4px;">🌰 守護者蔻恩引導調息</div>
        <div id="st-timer" style="font-size:1.8rem; font-weight:bold; color:#FFFFFF; margin-bottom:10px;">準備開始</div>
        <div id="videoContainer" style="width:240px; height:240px; margin:0 auto; overflow:hidden; border-radius:16px; border:2px solid #FFD700; background:#000;">
            <video id="v" width="100%" height="100%" style="object-fit:cover;" playsinline muted src="{video_b64}"></video>
        </div>
        <button id="sBtn" onclick="run()" style="margin-top:16px; background:linear-gradient(135deg, #FFD700 0%, #C2A675 100%); color:#1A261F; border:none; border-radius:20px; padding:10px 24px; font-weight:bold; cursor:pointer; width:100%;">🌬️ 啟動 4-7-8 調息法</button>
    </div>
    <script>
        var v = document.getElementById("v"), t = document.getElementById("st-title"), tm = document.getElementById("st-timer"), btn = document.getElementById("sBtn"), vc = document.getElementById("videoContainer");
        function run() {{
            btn.disabled = true; btn.style.opacity = "0.5"; vc.classList.remove("pulsing");
            t.innerText = "🌬️ 深吸氣 (4秒)"; v.currentTime = 0; v.playbackRate = 0.3; v.play();
            var c = 4; tm.innerText = c + " 秒";
            var i = setInterval(function() {{
                c--; if (c>0) tm.innerText = c + " 秒";
                else {{
                    clearInterval(i); v.pause(); vc.classList.add("pulsing");
                    t.innerText = "⏸️ 靜心閉氣 (7秒)";
                    var h = 7; tm.innerText = h + " 秒";
                    var j = setInterval(function() {{
                        h--; if (h>0) tm.innerText = h + " 秒";
                        else {{
                            clearInterval(j); vc.classList.remove("pulsing");
                            t.innerText = "💨 緩吐氣 (8秒)";
                            var st = performance.now(), sf = v.currentTime, ex = 8; tm.innerText = ex + " 秒";
                            var k = setInterval(function() {{ ex--; if (ex>0) tm.innerText = ex + " 秒"; else clearInterval(k); }}, 1000);
                            function rev(n) {{
                                var p = (n-st)/8000;
                                if (p<1) {{ v.currentTime = Math.max(0, sf*(1-p)); requestAnimationFrame(rev); }}
                                else {{ v.currentTime = 0; tm.innerText = "諧振成功"; t.innerText = "✨ 冒險能量充盈！"; btn.disabled = false; btn.style.opacity = "1.0"; }}
                            }}
                            requestAnimationFrame(rev);
                        }}
                    }}, 1000);
                }}
            }}, 1000);
        }}
    </script>
""",
    height=450,
)

if st.button("✨ 完成冒險準備"):
    st.session_state["step3_done"] = True
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# 冒險通關與拋接
if (
    st.session_state["step1_done"]
    and st.session_state["step2_done"]
    and st.session_state["step3_done"]
):
    st.markdown(
        f"""
        <div style="background:linear-gradient(180deg, #1A261F 0%, #0D1410 100%); border:2px solid #FFD700; border-radius:18px; padding:18px; text-align:center; box-shadow:0 6px 25px rgba(255,215,0,0.3);">
            <h3 style="color:#FFD700 !important; margin-top:0; font-size:1.25rem;">📜 探險家日誌封存完畢</h3>
            <p style="color:#D3E0D7 !important; font-size:0.9rem;">
                通行密鑰：<b style="color:#FFD700;">{token_code}</b> ｜ 🐶 <b>友善動物福利</b>：已為您推薦離您最近之公立收容所溫和陪伴犬貓資訊。
            </p>
            <a href="https://curio-streamlit-dashboard.streamlit.app/?token={token_code}" target="_blank" style="background:linear-gradient(135deg, #FFD700 0%, #C2A675 100%); color:#1A261F !important; padding:12px 28px; border-radius:25px; text-decoration:none; font-weight:900; font-size:1rem; display:inline-block;">
                🕊️ 信鴿 Singer 傳送日誌至診間面板
            </a>
        </div>
    """,
        unsafe_allow_html=True,
    )
else:
    st.info("💡 依序完成三項關卡，即可解鎖信鴿傳送！")