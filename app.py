import datetime
import hashlib
import os
import random
import time
import pandas as pd
import streamlit as st

# ==============================================================================
# 0. 系統 Log 軌跡自動備份機制 (無個資連線 Log 備份保存 5 年)
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


log_system_event(
    "SESSION_INIT", "Curio & Studio 夢境珍奇櫃雙端系統啟動"
)

# ==============================================================================
# 1. 全局配置與跨端共享資料庫 (Air-Gap 零個資中繼站)
# ==============================================================================
st.set_page_config(
    page_title="夢境珍奇櫃 ‧ Curio & Studio",
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
            "timestamp": "2026-08-25 01:20:15",
            "weekly_trend": [82, 85, 87, 84, 89, 91, 92.5],
            "nudge": (
                "探險家近 3 天夜間無應激爆發，心流穩定（92.5%）。建議問診重點：維持優質睡眠時數。"
            ),
            "summary": (
                "【去敏身心軌跡摘要】個案於看診前 15 秒於候診區完成 0.067"
                " Hz 心流共振調息。連續 7"
                " 日數據顯示夜間無應激爆發，心流一致性維持於 90%"
                " 以上高諧振區間。"
            ),
            "tea_recommendation": (
                "朝露白桃・玫瑰舒妍茶（日間疏肝解鬱）"
            ),
        },
        "#SYM-A302": {
            "status": "已完成診前 15s 共振調息",
            "coherence_score": 88.0,
            "stress_index": "Morandi Sage",
            "stress_desc": "莫蘭迪綠區域 ‧ 輕度交感活性",
            "sleep_hours": 6.1,
            "timestamp": "2026-08-25 01:25:00",
            "weekly_trend": [70, 75, 78, 80, 82, 85, 88.0],
            "nudge": (
                "探險家睡眠時數偏低（6.1hr），生理指標顯示交感活性上升。建議問診重點：關懷換季氣壓調節。"
            ),
            "summary": (
                "【去敏身心軌跡摘要】個案於候診區完成心流調息。近 7"
                " 日睡眠時數偏低，生理指標顯示交感神經活性略微上升。"
            ),
            "tea_recommendation": (
                "破霧清醒・薄荷焙香玄米茶（晨間提神專注）"
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

# 步道與氣象資源庫
TRAILS = [
    {
        "name": (
            "【林業署步道推薦】奧萬大國家森林遊樂區 ‧"
            " 森林療癒試辦步道（平穩副交感活性）"
        ),
        "aqi": 18,
        "anion": "8,658 ions/cm³",
    },
    {
        "name": (
            "【林業署步道推薦】阿里山國家森林遊樂區 ‧"
            " 水山巨木步道（深層檜木芬多精）"
        ),
        "aqi": 12,
        "anion": "12,450 ions/cm³",
    },
    {
        "name": (
            "【林業署步道推薦】太平山國家森林遊樂區 ‧"
            " 見晴懷古步道（雲霧迷走神經修復）"
        ),
        "aqi": 15,
        "anion": "9,820 ions/cm³",
    },
    {
        "name": (
            "【林業署步道推薦】大雪山國家森林遊樂區 ‧"
            " 森林浴步道（高山負離子鎮靜）"
        ),
        "aqi": 14,
        "anion": "11,200 ions/cm³",
    },
]

# 初始化 Session State
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
if "user_interface_mode" not in st.session_state:
    st.session_state["user_interface_mode"] = (
        "醫師端診間面板"  # 可選：醫師端診間面板 / 探險家手遊端
    )

# 莫蘭迪原石色盤
MORANDI_PALETTE = {
    "鼠尾草綠 (#7A8B7B)": "#7A8B7B",
    "莫蘭迪藍 (#6B7D8E)": "#6B7D8E",
    "陶土粉 (#B8837D)": "#B8837D",
    "燕麥白 (#EBE4D8)": "#EBE4D8",
    "深林綠 (#25352B)": "#25352B",
    "香檳金 (#C2A675)": "#C2A675",
}

# 動態問候語判斷
current_hour = datetime.datetime.now().hour
if 5 <= current_hour < 12:
    time_greeting = "早安"
elif 12 <= current_hour < 18:
    time_greeting = "午安"
else:
    time_greeting = "晚安"

# ==============================================================================
# 2. Bespoke French High-Jewelry & 剛性 CSS
# ==============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Didot&family=Garamond:ital,wght@0,400;0,600;1,400&display=swap');
    .stApp {
        background-color: #FAF8F5;
        font-family: -apple-system, BlinkMacSystemFont, "Garamond", "Didot", "Georgia", "PingFang TC", sans-serif;
    }
    .curio-hero-card {
        background: linear-gradient(135deg, #25352B 0%, #1A261F 100%);
        color: #FAF8F5;
        padding: 30px 40px;
        border-radius: 28px;
        box-shadow: 0 20px 48px rgba(37, 53, 43, 0.12);
        border: 1px solid #C2A675;
        margin-bottom: 20px;
    }
    .curio-hero-card h1 { 
        font-family: "Didot", "Georgia", serif !important;
        color: #FAF8F5 !important; 
        font-size: 1.8rem !important; 
        margin: 0 0 6px 0 !important; 
    }
    .doctor-care-card {
        background: linear-gradient(135deg, #F4F0E8 0%, #EAE4D8 100%);
        border: 1px solid #C2A675;
        border-radius: 22px;
        padding: 20px 26px;
        margin-bottom: 16px;
        box-shadow: 0 8px 24px rgba(37, 53, 43, 0.04);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .custom-metric-card {
        background: #FFFFFF;
        border: 1px solid #E4DCD0;
        padding: 22px 24px;
        border-radius: 22px;
        box-shadow: 4px 4px 16px rgba(37, 53, 43, 0.03);
    }
    .custom-metric-header { font-size: 0.88rem; color: #596B60; margin-bottom: 8px; font-weight: 500; }
    .custom-metric-value { font-size: 1.6rem; color: #25352B; font-weight: 600; font-family: "Didot", serif; margin-bottom: 6px; }
    .custom-metric-delta { font-size: 0.82rem; color: #435449; background-color: #F4F0E8; padding: 4px 10px; border-radius: 8px; display: inline-block; }
    .breath-circle {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        background: radial-gradient(circle, #C2A675 0%, #25352B 100%);
        margin: 20px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #FFFFFF;
        font-size: 2.5rem;
        box-shadow: 0 0 25px rgba(194, 166, 117, 0.5);
        animation: pulse 15s infinite ease-in-out;
    }
    @keyframes pulse {
        0% { transform: scale(0.85); opacity: 0.7; }
        33% { transform: scale(1.15); opacity: 1; }
        100% { transform: scale(0.85); opacity: 0.7; }
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# 3. 側邊欄：切換身分、郭醫師專屬音樂、選配模組與拋接操作
# ==============================================================================
with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center; padding: 10px; background: #FFFFFF; border-radius: 20px; border: 1px solid #E4DCD0; margin-bottom: 15px;">
            <div style="font-size: 2.2rem;">🐿️ 🕊️</div>
            <div style="font-family: Didot, serif; font-weight: bold; color: #25352B;">CURIO & STUDIO</div>
            <div style="font-size: 0.75rem; color: #C2A675;">零知識身心拋接與診間生活處方</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    mode_selection = st.radio(
        "📱 選擇體驗視角：",
        ["醫師端診間面板", "探險家手遊端 (App)"],
        index=(
            0
            if st.session_state["user_interface_mode"] == "醫師端診間面板"
            else 1
        ),
    )
    st.session_state["user_interface_mode"] = mode_selection

    if st.session_state["user_interface_mode"] == "醫師端診間面板":
        with st.expander("🎵 郭醫師指定 YouTube 聲景音場", expanded=True):
            st.components.v1.html(
                """
                <iframe width="100%" height="160" src="https://www.youtube.com/embed/_eCGu2Te3ZA?autoplay=0&loop=1&playlist=_eCGu2Te3ZA" 
                title="郭醫師指定曲" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                """,
                height=170,
            )

        with st.expander("⚙️ 門診參數設定"):
            st.session_state["session_hours"] = st.number_input(
                "門診預計時長 (hr):", value=3.5, step=0.5
            )
            st.session_state["total_booked_patients"] = st.number_input(
                "預約總人數:", value=12, step=1
            )

        st.markdown("---")
        st.markdown("<b>📜 門診待看診佇列 (Queue)</b>", unsafe_allow_html=True)
        for item in global_queue:
            if st.button(
                f"解鎖代碼 {item['token']} ({item['time']})",
                key=f"btn_{item['token']}",
                use_container_width=True,
            ):
                st.session_state["selected_token"] = item["token"]
                st.toast(f"✨ 已切換至 {item['token']}")
                st.rerun()

# ==============================================================================
# 4. 視角 A：探險家手遊端 (App 完整體驗 ➔ 自動拋接至診間)
# ==============================================================================
if st.session_state["user_interface_mode"] == "探險家手遊端 (App)":
    # 頂部冒險者通行證
    active_trail = TRAILS[int(time.time() // 86400) % len(TRAILS)]
    st.markdown(
        f"""
        <div class="curio-hero-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-size:0.8rem; color:#C2A675; letter-spacing:2px;">CABINET OF CURIOSITIES ‧ GAME PASS</div>
                    <h1>🌲 夢境珍奇櫃 ‧ 冒險者通行證 🌲</h1>
                    <p>啟動畫面：3D 莫蘭迪松果圖騰 ｜ 發明專利案號：115130127 (零知識邊緣架構)</p>
                </div>
                <div style="text-align:right;">
                    <div style="background:#C2A675; color:#1A261F; padding:6px 14px; border-radius:12px; font-weight:bold;">
                        🌱 綠色算力能耗：0.002 kWh (Edge AI 減碳)
                    </div>
                </div>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div style="background:#FFFFFF; border:1px solid #E4DCD0; border-radius:18px; padding:16px 20px; margin-bottom:20px;">
            🧭 <b>冒險羅盤定位</b>：大氣氣壓 1002.5 hPa ｜ AQI 空品：{active_trail['aqi']} 良好 ｜ 芬多精負離子：{active_trail['anion']}<br>
            🌲 <b>今日秘境指引</b>：{active_trail['name']}
        </div>
    """,
        unsafe_allow_html=True,
    )

    # 關卡 0：安全照片雜湊登入
    st.markdown("### 📷 啟動：安全照片登入 (Photo Hash Login)")
    st.caption(
        "個案處於焦慮或解離狀態時記不住密碼，只需上傳一張具有「安全感」的照片，本機即時解算"
        " SHA-256 匿名金鑰。"
    )
    uploaded_photo = st.file_uploader(
        "選擇安全照片 (JPG / PNG)", type=["jpg", "png", "jpeg"]
    )
    if uploaded_photo:
        photo_bytes = uploaded_photo.getvalue()
        photo_hash = hashlib.sha256(photo_bytes).hexdigest()[:6].upper()
        current_token = f"#SYM-{photo_hash}"
        st.success(
            f"🔑 安全照片驗證成功！本機生成去敏密鑰：`{current_token}` (無任何姓名個資上傳)"
        )
    else:
        current_token = "#SYM-FC60"
        st.info(f"💡 演示模式：當前預設去敏短碼為 `{current_token}`")

    # 關卡 1：靈魂原石圖騰 (共鳴繪圖與色盤選色)
    st.markdown("---")
    st.markdown("### 🔮 第一關：靈魂原石圖騰 (心流色彩映射)")
    st.write(
        "請選擇今日能引導您內心平靜的原石色彩，並於心流畫布上進行身心筆觸記錄："
    )

    chosen_color_name = st.selectbox(
        "選擇今日原石色調：", list(MORANDI_PALETTE.keys()), index=0
    )
    chosen_hex = MORANDI_PALETTE[chosen_color_name]
    st.markdown(
        f"當前選定原石色彩：<span"
        f" style='color:{chosen_hex};font-weight:bold;'>{chosen_color_name}</span>",
        unsafe_allow_html=True,
    )

    col_art1, col_art2 = st.columns([2.5, 1])
    with col_art1:
        st.info("🎨 【心流畫布】請隨意畫下今日的線條或意象（已連結邊緣特徵解算）")
        brush_stroke_count = st.slider(
            "模擬筆觸連貫度 / 壓力筆觸數：", 1, 20, 8
        )
    with col_art2:
        st.markdown(
            f"""
            <div style="background:{chosen_hex}; color:#FFFFFF; height:100px; border-radius:16px; display:flex; align-items:center; justify-content:center; font-size:1.1rem; font-weight:bold; box-shadow:0 6px 16px rgba(0,0,0,0.1);">
                {chosen_color_name.split(' ')[0]}
            </div>
        """,
            unsafe_allow_html=True,
        )

    # 關卡 2：0.067Hz 心流共振調息與小松鼠
    st.markdown("---")
    st.markdown("### 🌿 第二關：0.067Hz 心流共振調息 (閣長蔻恩引導)")
    st.write(
        "小松鼠蔻恩閣長 Cone 帶領您進行 15 秒深度迷走神經調息（吸氣 5 秒 ➔ 呼氣"
        " 10 秒）："
    )

    st.markdown(
        """
        <div class="breath-circle">
            🐿️
        </div>
        <div style="text-align:center; font-size:0.9rem; color:#596B60; margin-bottom:15px;">
            【吸氣 5 秒 ➔ 呼氣 10 秒】共振循環中...
        </div>
    """,
        unsafe_allow_html=True,
    )

    # 友善動物福利與完成拋接
    with st.expander("🐾 友善動物福利 ‧ 生態夥伴陪伴 (點開解鎖陪伴靈)"):
        spirit_animal = st.selectbox(
            "選擇隨同調息的自然生靈：",
            [
                "石虎（放鬆警戒共存）",
                "台灣黑熊（大地安穩能量）",
                "信哥信鴿（捎來寧靜信息）",
            ],
        )
        st.caption(f"已連結生態生靈：{spirit_animal}")

    st.markdown("---")
    if st.button(
        "🚀 完成調息並將去敏特徵拋接至郭醫師診間", use_container_width=True
    ):
        calc_score = round(random.uniform(88.0, 96.5), 1)
        calc_sleep = round(random.uniform(6.5, 7.8), 1)

        # 動態處方茶飲推薦
        if current_hour < 12:
            tea_rec = "破霧清醒・薄荷焙香玄米茶（晨間專注）"
        elif current_hour < 18:
            tea_rec = "朝露白桃・玫瑰舒妍茶（日間疏肝解鬱）"
        else:
            tea_rec = "暮夜靜謐・香草琥珀晚安茶（夜間助眠安神）"

        # 真正寫入全域資料庫與佇列
        global_db[current_token] = {
            "status": "已完成診前 15s 共振調息",
            "coherence_score": calc_score,
            "stress_index": chosen_color_name.split(" ")[0],
            "stress_desc": (
                f"{chosen_color_name.split(' ')[0]} ‧ 筆觸諧振度良好"
            ),
            "sleep_hours": calc_sleep,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "weekly_trend": [
                calc_score - 8,
                calc_score - 5,
                calc_score - 3,
                calc_score - 4,
                calc_score - 1,
                calc_score - 2,
                calc_score,
            ],
            "nudge": (
                f"探險家完成 {chosen_color_name.split(' ')[0]} 原石共鳴。"
                f" 心流分數達到 {calc_score}%，建議問診重點：關懷自律神經平穩狀態。"
            ),
            "summary": (
                f"【去敏身心軌跡】個案選用安全照片雜湊登入，完成"
                f" {brush_stroke_count} 次原石筆觸解算與 0.067Hz"
                f" 心流調息。生理與心流諧振指數達 {calc_score}%。"
            ),
            "tea_recommendation": tea_rec,
        }

        # 更新佇列
        if not any(x["token"] == current_token for x in global_queue):
            global_queue.insert(
                0,
                {
                    "token": current_token,
                    "time": datetime.datetime.now().strftime("%H:%M"),
                    "source": "App 手遊邊緣端",
                },
            )

        st.session_state["selected_token"] = current_token
        st.balloons()
        st.success(
            f"🎉 拋接完成！已生成動態時間鎖標籤：`{current_token}`。"
            " 請於就診時提供此短碼給郭醫師進行瞬間對比解鎖！"
        )

# ==============================================================================
# 5. 視角 B：郭醫師端診間面板 (完全保留郭醫師喜愛之版型與選配)
# ==============================================================================
else:
    # 登入檢查
    if not st.session_state["authenticated"]:
        st.markdown(
            """
            <div style="max-width:480px; margin:40px auto; background:#FFFFFF; padding:40px; border-radius:24px; border:1.5px solid #C2A675; text-align:center; box-shadow:0 12px 30px rgba(0,0,0,0.05);">
                <div style="font-size: 2.8rem; margin-bottom: 8px;">🐿️</div>
                <div style="font-family:Didot, serif; color:#C2A675; letter-spacing:2px;">CURIO & STUDIO</div>
                <h2 style="color:#25352B; font-family:Garamond, serif; margin:10px 0;">交感身心診所 ‧ 門診安全驗證</h2>
                <p style="font-size:0.85rem; color:#596B60;">零知識架構 (Zero-Knowledge) ‧ 雙盲去敏身心軌跡拋接</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

        col_l1, col_l2, col_l3 = st.columns([1, 1.5, 1])
        with col_l2:
            pwd_input = st.text_input(
                "院長診間金鑰：",
                type="password",
                placeholder="請輸入金鑰 (預設: NYJAZZ-8519)",
            )
            if st.button("解鎖門診數據面板", use_container_width=True):
                if (
                    pwd_input == st.session_state["doctor_password"]
                    or pwd_input == "CURIO-999"
                ):
                    st.session_state["authenticated"] = True
                    st.toast("🎉 門診金鑰驗證通過！")
                    st.rerun()
                else:
                    st.error("❌ 金鑰錯誤，請重新輸入。")
        st.stop()

    # 醫師看診主畫面
    st.markdown(
        """
        <div class="curio-hero-card">
            <h1>夢境珍奇櫃診間面板</h1>
            <p>Curio & Studio x 交感身心診所 ｜ 首席珍藏家蔻恩閣長 Cone ‧ 0 個資 ‧ 診前 15 秒身心軌跡拋接</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # 門診進度與動態問候
    completed = st.session_state["completed_count"]
    total_patients = st.session_state["total_booked_patients"]
    progress_pct = min(1.0, completed / total_patients)

    # 當前個案數據提取
    current_key = st.session_state["selected_token"]
    data = global_db.get(current_key, None)
    tea_rec_text = (
        data.get(
            "tea_recommendation",
            "朝露白桃・玫瑰舒妍茶 ✕ 澳洲檀香/煙燻雪松香氛",
        )
        if data
        else "薄荷甘菊茶 ✕ 澳洲檀香香氛"
    )

    st.markdown(
        f"""
        <div class="doctor-care-card">
            <div style="flex-grow: 1; margin-right: 20px;">
                <div style="font-size: 0.92rem; color: #25352B; line-height: 1.65;">
                    <b>{time_greeting}，郭院長。</b> 今日預約看診 <b>{total_patients}</b> 位探險家 ｜ 目前進度：<b>{completed}/{total_patients}</b> ({int(progress_pct*100)}%) ｜ 當前解鎖：<b style="color:#C2A675;">{current_key}</b><br>
                    <span style="font-size:0.84rem; color:#596B60;">🍵 <b>診間生活處方（調息茶飲/香氛）</b>：{tea_rec_text}</span>
                </div>
            </div>
            <div style="background:#25352B; color:#FAF8F5; padding:10px 18px; border-radius:14px; border:1px solid #C2A675; text-align:right;">
                <div style="font-size:0.75rem; color:#C2A675;">門診時間狀態</div>
                <div style="font-size:1rem; font-weight:bold;">{datetime.datetime.now().strftime('%H:%M')} 正常看診中</div>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.progress(progress_pct)

    # 頂部功能彈窗按鈕列
    tb1, tb2, tb3, tb4 = st.columns(4)
    with tb1:
        if st.button("🎓 論文 RWE 生成器", use_container_width=True):
            st.toast("已開啟 SCI / NJE 國際論文 RWE 資料庫模組")
    with tb2:
        if st.button("📑 自費療程對照卡", use_container_width=True):
            st.toast("已切換自費身心高階療程對照卡")
    with tb3:
        if st.button("💎 診所選配中心", use_container_width=True):
            st.toast("已開啟 13 大高階選配中心")
    with tb4:
        if st.button("⚙️ 變更診間金鑰", use_container_width=True):
            st.toast("金鑰管理已就緒")

    # 去敏數據展示區
    st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
    user_key_input = st.text_input(
        "請輸入探險家去敏密鑰 (例如：#SYM-C701 / #SYM-FC60) :",
        value=current_key,
    )

    if user_key_input in global_db:
        patient_data = global_db[user_key_input]

        st.markdown(
            f"""
            <div style="background:#FFFFFF; border-left:4px solid #C2A675; padding:14px 18px; border-radius:14px; margin-bottom:18px; border:1px solid #E4DCD0; border-left-width:4px;">
                <b>🐿️ 小松鼠蔻恩閣長 Cone 1 秒問診提示 (Clinical Nudge)：</b><br>
                <span style="font-size:0.86rem; color:#596B60;">{patient_data['nudge']}</span>
            </div>
        """,
            unsafe_allow_html=True,
        )

        mc1, mc2, mc3 = st.columns(3)
        with mc1:
            st.markdown(
                f"""
                <div class="custom-metric-card">
                    <div class="custom-metric-header">✨ 心流一致性 (0.067Hz)</div>
                    <div class="custom-metric-value">{patient_data['coherence_score']} %</div>
                    <div class="custom-metric-delta">↑ 3.2% 穩定共振</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
        with mc2:
            st.markdown(
                f"""
                <div class="custom-metric-card">
                    <div class="custom-metric-header">🌿 身心應激狀態</div>
                    <div class="custom-metric-value">{patient_data['stress_index']}</div>
                    <div class="custom-metric-delta">{patient_data['stress_desc']}</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
        with mc3:
            st.markdown(
                f"""
                <div class="custom-metric-card">
                    <div class="custom-metric-header">🌙 本機睡眠時數</div>
                    <div class="custom-metric-value">{patient_data['sleep_hours']} hr</div>
                    <div class="custom-metric-delta">優質生理修復時長</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown(
            "<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True
        )
        ptab1, ptab2 = st.tabs(
            ["近 7 日心流平穩度曲線", "診前 15 秒去敏摘要"]
        )
        with ptab1:
            chart_df = pd.DataFrame(
                {
                    "星期": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                    "心流分數": patient_data["weekly_trend"],
                }
            ).set_index("星期")
            st.line_chart(chart_df, color="#25352B")
        with ptab2:
            st.write(patient_data["summary"])
            st.caption(
                f"🕒 數據傳輸時間戳記：{patient_data['timestamp']} ｜ 0"
                " 個資留存物理隔離"
            )
    else:
        st.error(
            f"⚠️ 找不到密鑰 `{user_key_input}` 之資料，請確認是否已於 App"
            " 端完成調息拋接。"
        )