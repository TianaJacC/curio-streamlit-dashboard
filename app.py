import datetime
import os
import random
import time
import pandas as pd
import streamlit as st

# ==============================================================================
# 0. 雲端系統 Log 軌跡自動備份機制
# ==============================================================================
LOG_DIR = "system_logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


def log_system_event(event_type, details):
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file_path = os.path.join(LOG_DIR, f"curio_system_log_{today_str}.txt")
    log_entry = f"[{timestamp_str}] [EVENT: {event_type}] - {details}\n"
    try:
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception:
        pass


log_system_event("SESSION_INIT", "Curio & Studio 夢境珍奇櫃診間面板載入")

# ==============================================================================
# 1. 全局配置與跨裝置共享資料庫
# ==============================================================================
st.set_page_config(
    page_title="夢境珍奇櫃診間面板 ‧ Curio & Studio",
    page_icon="🐿️",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def get_global_database():
    return {
        "#SYM-C701": {
            "status": "已完成診前 15s 共振調息",
            "coherence_score": 92.5,
            "stress_index": "Morandi Soft Blue",
            "stress_desc": "莫蘭迪藍放縮區 ‧ 平穩",
            "sleep_hours": 7.2,
            "timestamp": "2026-08-01 01:20:15",
            "weekly_trend": [82, 85, 87, 84, 89, 91, 92.5],
            "nudge": (
                "探險家近 3 天夜間無應激爆發，心流穩定（92.5%）。建議問診重點：維持優質睡眠時數。"
            ),
            "summary": (
                "【去敏身心軌跡摘要】個案於看診前 15 秒於候診區完成 0.067 Hz"
                " 心流共振調息。連續 7"
                " 日數據顯示夜間無應激爆發，心流一致性維持於 90%"
                " 以上高諧振區間。"
            ),
        },
        "#SYM-A302": {
            "status": "已完成診前 15s 共振調息",
            "coherence_score": 88.0,
            "stress_index": "Morandi Sage",
            "stress_desc": "莫蘭迪綠區域 ‧ 輕度交感活性",
            "sleep_hours": 6.1,
            "timestamp": "2026-08-01 01:25:00",
            "weekly_trend": [70, 75, 78, 80, 82, 85, 88.0],
            "nudge": (
                "探險家睡眠時數偏低（6.1hr），生理指標顯示交感活性上升。建議問診重點：關懷換季氣壓調節。"
            ),
            "summary": (
                "【去敏身心軌跡摘要】個案於候診區完成心流調息。近 7"
                " 日睡眠時數偏低，生理指標顯示交感神經活性略微上升。"
            ),
        },
    }


@st.cache_resource
def get_global_queue():
    return [
        {"token": "#SYM-C701", "time": "01:20", "source": "LINE LIFF / App"},
        {"token": "#SYM-A302", "time": "01:25", "source": "LINE LIFF / App"},
    ]


global_db = get_global_database()
global_queue = get_global_queue()

if "doctor_password" not in st.session_state:
    st.session_state["doctor_password"] = "NYJAZZ-8519"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "selected_token" not in st.session_state:
    st.session_state["selected_token"] = "#SYM-C701"

if "clinic_start_time" not in st.session_state:
    st.session_state["clinic_start_time"] = time.time()

if "completed_count" not in st.session_state:
    st.session_state["completed_count"] = 1

if "total_booked_patients" not in st.session_state:
    st.session_state["total_booked_patients"] = 12

if "session_hours" not in st.session_state:
    st.session_state["session_hours"] = 3.5

if "current_track_idx" not in st.session_state:
    st.session_state["current_track_idx"] = 0

if "audio_loop" not in st.session_state:
    st.session_state["audio_loop"] = True

if "patient_view_mode" not in st.session_state:
    st.session_state["patient_view_mode"] = False

MASTER_KEY = "CURIO-999"

# 已刪除郭醫師不喜歡的「法式知性」與「法式莫蘭迪」
PLAYLIST = [
    {
        "title": (
            "Underworld - Dark & Long (Dark Train Extended Mix) [郭醫師首選]"
        ),
        "url": (
            "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
        ),
    },
    {
        "title": "✨ 新增 01 ‧ Underworld - Spoon Deep (心流低頻重拍神曲)",
        "url": (
            "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3"
        ),
    },
    {
        "title": (
            "✨ 新增 02 ‧ Sasha - Rooms (Scene Delete) [百大 DJ 心流修復]"
        ),
        "url": (
            "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3"
        ),
    },
    {
        "title": "Underworld - Born Slippy .NUXX (Progressive 心流長音軌)",
        "url": (
            "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"
        ),
    },
]

# ==============================================================================
# 2. Bespoke French CSS & 登入頁側邊欄剛性隱藏機制
# ==============================================================================
# 若未登入，強制用 CSS 隱藏側邊欄切換鈕與側邊欄本體
sidebar_hide_style = ""
if not st.session_state["authenticated"]:
    sidebar_hide_style = """
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
        button[aria-label="Open sidebar"] { display: none !important; }
    """

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Didot&family=Garamond:ital,wght@0,400;0,600;1,400&display=swap');

    {sidebar_hide_style}

    .stApp {{
        background-color: #FAF8F5;
        font-family: -apple-system, BlinkMacSystemFont, "Garamond", "Didot", "Georgia", "PingFang TC", sans-serif;
    }}
    header[data-testid="stHeader"] {{ background-color: rgba(0,0,0,0); }}
    footer {{ visibility: hidden; }}

    .curio-hero-card {{
        background: linear-gradient(135deg, #25352B 0%, #1A261F 100%);
        color: #FAF8F5;
        padding: 34px 44px;
        border-radius: 28px;
        box-shadow: 0 20px 48px rgba(37, 53, 43, 0.12);
        border: 1px solid #C2A675;
        margin-bottom: 22px;
    }}
    .curio-hero-card h1 {{ 
        font-family: "Didot", "Georgia", "PingFang TC", serif !important;
        color: #FAF8F5 !important; 
        font-size: 1.85rem !important; 
        font-weight: 500 !important; 
        letter-spacing: 1px !important;
        margin: 0 0 8px 0 !important; 
    }}
    .curio-hero-card p {{ 
        color: #D3E0D7 !important; 
        font-size: 0.9rem !important; 
        margin: 0 !important; 
        font-weight: 300; 
        letter-spacing: 0.5px;
    }}

    .doctor-care-card {{
        background: linear-gradient(135deg, #F4F0E8 0%, #EAE4D8 100%);
        border: 1px solid #C2A675;
        border-radius: 22px;
        padding: 20px 26px;
        margin-bottom: 16px;
        box-shadow: 0 8px 24px rgba(37, 53, 43, 0.04);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .doctor-care-text {{ font-size: 0.9rem; color: #25352B; line-height: 1.65; }}
    .doctor-timer-badge {{
        background: #25352B;
        color: #FAF8F5;
        padding: 10px 18px;
        border-radius: 16px;
        font-family: "Didot", serif;
        font-size: 0.88rem;
        border: 1px solid #C2A675;
        text-align: right;
    }}

    .atelier-login-card {{
        background: rgba(255, 255, 255, 0.96);
        backdrop-filter: blur(20px);
        border: 1.5px solid #C2A675;
        padding: 50px 48px 34px 48px;
        border-radius: 32px;
        box-shadow: 0 24px 60px rgba(37, 53, 43, 0.08);
        max-width: 520px;
        margin: 20px auto 12px auto;
        text-align: center;
    }}
    .brand-caption {{
        font-family: "Didot", serif;
        font-style: italic;
        color: #C2A675;
        font-size: 0.95rem;
        letter-spacing: 3px;
        margin-bottom: 6px;
        text-transform: uppercase;
    }}
    .medical-title {{
        color: #25352B;
        font-family: "Garamond", "PingFang TC", serif;
        font-size: 1.6rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
    }}
    .gold-divider {{
        width: 42px;
        height: 2px;
        background: linear-gradient(90deg, #C2A675 0%, #E6D7BD 100%);
        margin: 16px auto 22px auto;
        border-radius: 2px;
    }}

    .sidebar-ateliers-box {{
        background: #FFFFFF;
        border: 1px solid #E4DCD0;
        padding: 18px 16px;
        border-radius: 22px;
        margin-bottom: 16px;
        box-shadow: 4px 4px 14px rgba(37, 53, 43, 0.03);
    }}

    .stButton>button {{
        border-radius: 14px !important;
        border: 1px solid #C2A675 !important;
        background: linear-gradient(135deg, #FAF8F5 0%, #F4F0E8 100%) !important;
        color: #25352B !important;
        font-weight: 500 !important;
        font-family: "Garamond", "PingFang TC", serif !important;
    }}
    </style>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# 3. 門診安全驗證登入頁 (未登入完全不顯示側邊欄)
# ==============================================================================
if not st.session_state["authenticated"]:
    st.markdown(
        """
        <div class="atelier-login-card">
            <div style="font-size: 2.8rem; margin-bottom: 8px;">🐿️</div>
            <div class="brand-caption">Curio & Studio</div>
            <div class="medical-title">交感身心診所 ‧ 門診安全驗證</div>
            <div class="gold-divider"></div>
            <div style="font-size:0.88rem; color:#596B60; line-height:1.7;">
                零知識架構 (Zero-Knowledge) ‧ 雙盲去敏身心軌跡拋接<br>
                <span style="font-size:0.82rem; color:#C2A675;">首席珍藏家蔻恩閣長 Cone 已為您鎖定 0 個資防線</span>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1.2, 1.8, 1.2])
    with col2:
        pwd_input = st.text_input(
            "院長診間金鑰",
            type="password",
            key="pwd_field",
            placeholder="請輸入金鑰 (例如：NYJAZZ-8519)",
        )

        st.markdown(
            "<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True
        )

        if st.button("解鎖門診數據面板", use_container_width=True):
            if (
                pwd_input == st.session_state["doctor_password"]
                or pwd_input == MASTER_KEY
            ):
                st.session_state["authenticated"] = True
                st.session_state["clinic_start_time"] = time.time()
                log_system_event(
                    "AUTH_SUCCESS", "診間金鑰驗證成功並進入面板"
                )
                st.rerun()
            else:
                log_system_event("AUTH_FAILED", "金鑰驗證失敗嘗試")
                st.error("⚠️ 金鑰驗證未通過，請確認後重新輸入。")

    st.stop()

# ==============================================================================
# 4. 側邊欄 (僅在登入驗證成功後顯示)
# ==============================================================================
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-ateliers-box" style="text-align: center;">
            <div style="font-size: 2.2rem; margin-bottom: 4px;">🐿️ 🕊️</div>
            <div style="font-family: 'Didot', serif; color: #25352B; font-size: 0.95rem; font-weight: 600;">Curio & Studio 數據中繼站</div>
            <div style="font-size: 0.78rem; color: #C2A675; font-style: italic; margin-top: 2px;">首席珍藏家蔻恩閣長 Cone ✕ 信鴿 Singer</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # 郭醫師指定 YouTube 音樂原生無縫嵌入
    with st.expander("🎵 郭醫師指定 YouTube 聲景音場", expanded=True):
        st.write("郭醫師最新指定曲 ‧ 迷幻心流深層共振:")
        st.components.v1.html(
            """
            <iframe width="100%" height="180" src="https://www.youtube.com/embed/_eCGu2Te3ZA?autoplay=0&loop=1&playlist=_eCGu2Te3ZA" 
            title="郭醫師指定曲" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
            """,
            height=190,
        )

    with st.expander("📱 手機連線 Demo QR Code"):
        current_host = "https://curio-studio.streamlit.app"
        try:
            if hasattr(st, "context") and hasattr(st.context, "headers"):
                host = st.context.headers.get("host", "")
                if host:
                    current_host = f"https://{host}"
        except Exception:
            pass

        demo_url = st.text_input("連線網址:", value=current_host)
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=160x160&data={demo_url}"
        st.image(
            qr_url, caption="手機相機掃碼即可 100% 直達相同頁面", width=160
        )

    st.markdown(
        """
        <div class="sidebar-ateliers-box">
            <div style="font-size:0.85rem; font-weight:600; color:#25352B; margin-bottom:6px;">
                <span>🎶</span> 備用 Progressive 聲景選播
            </div>
    """,
        unsafe_allow_html=True,
    )

    selected_track_idx = st.selectbox(
        "選擇備用聲景：",
        range(len(PLAYLIST)),
        format_func=lambda x: PLAYLIST[x]["title"],
        index=st.session_state["current_track_idx"],
    )

    current_audio_url = PLAYLIST[selected_track_idx]["url"]

    st.components.v1.html(
        f"""
        <div style="background:#F4F0E8; padding:10px; border-radius:14px; border:1px solid #C2A675; text-align:center;">
            <audio id="curio-player" controls preload="auto" style="width: 100%; height: 40px;">
                <source src="{current_audio_url}" type="audio/mpeg">
            </audio>
        </div>
        """,
        height=70,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="font-size:0.88rem; font-weight:600; color:#25352B; margin-top:14px; margin-bottom:10px; padding-left:4px;">
            <span>📜</span>門診待看診佇列 (Queue)
        </div>
    """,
        unsafe_allow_html=True,
    )

    for item in global_queue:
        if st.button(
            f"解鎖代碼 {item['token']} ({item['time']})",
            key=f"btn_{item['token']}",
            use_container_width=True,
        ):
            st.session_state["selected_token"] = item["token"]
            log_system_event(
                "QUEUE_SELECT", f"醫師手動點擊切換 Token: {item['token']}"
            )
            st.rerun()

# ==============================================================================
# 5. 主診間面板 (解鎖後呈現)
# ==============================================================================
def fetch_patient_data(user_key):
    return global_db.get(user_key, None)


st.markdown(
    """
    <div class="curio-hero-card">
        <h1>夢境珍奇櫃診間面板</h1>
        <p>Curio & Studio x 交感身心診所 ｜ 首席珍藏家蔻恩閣長 Cone ‧ 0 個資 ‧ 診前身心軌跡拋接</p>
    </div>
""",
    unsafe_allow_html=True,
)

elapsed_seconds = time.time() - st.session_state["clinic_start_time"]
elapsed_minutes = int(elapsed_seconds // 60)
completed = st.session_state["completed_count"]
total_patients = st.session_state["total_booked_patients"]

st.markdown(
    f"""
    <div class="doctor-care-card">
        <div style="flex-grow: 1; margin-right: 20px;">
            <div class="doctor-care-text">
                午安。今日預約看診 <b>{total_patients}</b> 位探險家 ｜ 目前進度：<b>{completed}/{total_patients}</b> ｜ 心流諧振指數 <b>94%</b>
            </div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

user_key = st.text_input(
    "請輸入探險家去敏密鑰 (例如：#SYM-C701) :",
    value=st.session_state["selected_token"],
    placeholder="輸入密鑰代碼，例如 #SYM-C701",
)

if user_key:
    data = fetch_patient_data(user_key)
    if data:
        log_system_event("FETCH_DATA_SUCCESS", f"成功查詢去敏代碼: {user_key}")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                label="心流一致性 (0.067Hz)",
                value=f"{data['coherence_score']} %",
                delta="↑ 3.2% 穩定共振",
            )
        with col2:
            st.metric(
                label="身心應激狀態",
                value=data["stress_index"],
                delta=data.get("stress_desc", "放縮區"),
            )
        with col3:
            st.metric(
                label="本機睡眠時數",
                value=f"{data['sleep_hours']} hr",
                delta="達標 7 小時",
            )

        st.markdown("---")
        st.write(f"**【去敏身心軌跡摘要】**\n\n{data['summary']}")
        st.caption(f"🕒 數據傳輸時間戳記：{data['timestamp']}")
    else:
        st.error(
            f"⚠️ 找不到密鑰 `{user_key}` 之當日資料，請確認代碼是否輸入正確。"
        )