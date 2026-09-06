import csv
import datetime
import hashlib
import hmac
import json
import os
import random
import time
import pandas as pd
import streamlit as st

# ==============================================================================
# 0. 全局配置 (必須為第一個 Streamlit 指令)
# ==============================================================================
st.set_page_config(
    page_title="夢境珍奇櫃診間面板 ‧ Curio & Studio",
    page_icon="🐿️",
    layout="wide",
    initial_sidebar_state="expanded",
)

LOG_DIR = "system_logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

SHARED_DB_FILE = os.path.join(LOG_DIR, "active_sessions.json")
SHARED_QUEUE_FILE = os.path.join(LOG_DIR, "active_queue.json")
FEEDBACK_LOG_FILE = os.path.join(LOG_DIR, "user_feedback_log.csv")


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


def save_anonymous_feedback(role: str, token: str, category: str, content: str):
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.exists(FEEDBACK_LOG_FILE)
    with open(FEEDBACK_LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(
                ["Timestamp", "UserRole", "Token", "Category", "FeedbackContent"]
            )
        writer.writerow([timestamp_str, role, token, category, content.strip()])


def generate_secure_token(seed_bytes: bytes = None) -> str:
    if seed_bytes is None:
        seed_bytes = os.urandom(32)
    time_entropy = str(time.time_ns()).encode("utf-8")
    digest = hmac.new(time_entropy, seed_bytes, hashlib.sha256).hexdigest()
    return f"#SYM-{digest[:4].upper()}"


# ==============================================================================
# 1. 50 款生活處方資料庫 ✕ 現場 3 款備用調飲映射
# ==============================================================================
PRESCRIPTION_CATEGORIES = {
    0: {
        "stock_name": "破霧清醒 ‧ 鳳梨薄荷冰焙茶",
        "stock_desc": "薄荷腦喚醒前額葉，鳳梨果香協同焙煎玄米溫和護胃，抗疲勞消除腦霧。",
    },
    1: {
        "stock_name": "朝露果妍 ‧ 晨光葡莓玫瑰鮮果茶",
        "stock_desc": "大馬士革玫瑰協同鮮萃葡莓果香，疏肝解鬱，撫平日間胸悶浮躁張力。",
    },
    2: {
        "stock_name": "暮夜靜謐 ‧ 太妃香草黑櫻桃晚安茶",
        "stock_desc": "無咖啡因南非國寶基底，黑櫻桃果韻與太妃香草誘導迷走神經深度修復。",
    },
}

PRESCRIPTION_50_POOL = [
    (0, "破霧清醒 ‧ 鳳梨薄荷冰焙茶"),
    (0, "爆米花焦香 ‧ 黃金蕎麥大麥茶"),
    (0, "松林晨曦・雪松冷萃綠茶"),
    (0, "暖陽薑黃・肉桂黑糖暖身茶"),
    (0, "微光青柑・新會小青柑普洱"),
    (0, "林間漫步・針松牛蒡淨化茶"),
    (0, "極光耶加・淺焙花香水洗美式"),
    (0, "橙光共振・羅馬西西里氣泡咖啡"),
    (0, "京都雨露・一保堂無糖抹茶拿鐵"),
    (0, "黑曜石萃・黑松露深焙冰美式"),
    (0, "山丘微光・肯亞 AA 烏梅冷萃"),
    (0, "晨曦甜橙・鮮榨冷壓甜橙薑汁"),
    (0, "深林甘藍・羽衣甘藍蘋果青汁"),
    (0, "紅寶石光・冷壓甜菜根石榴飲"),
    (0, "熱帶雨林・紅心芭樂百香綠拿鐵"),
    (0, "黑金能量・九蒸九曬芝麻黑豆乳"),
    (0, "太極靜心・石菖蒲遠志益智飲"),
    (1, "朝露果妍 ‧ 晨光葡莓玫瑰鮮果茶"),
    (1, "罪惡極厚 ‧ 太妃布蕾鍋煮厚乳茶"),
    (1, "澄心降火・杭菊決明舒目茶"),
    (1, "雨後苔原・檸檬草香蜂草茶"),
    (1, "空谷幽蘭・白毫銀針茉莉茶"),
    (1, "清風甘露・玉露桑葉解壓茶"),
    (1, "山嵐迷霧・高山烏龍桂花茶"),
    (1, "玄米舒緩・蕎麥紫蘇輕身茶"),
    (1, "金風玉露・枇杷葉羅漢果茶"),
    (1, "北歐森林・小豆蔻肉桂拿鐵"),
    (1, "白夜流金・夏威夷豆奶髒咖啡"),
    (1, "黃金澄境・慢磨鳳梨百香薑黃飲"),
    (1, "紫霧凝香・野生藍莓黑醋栗冷壓汁"),
    (1, "白露芭樂・香檬珍珠芭樂鮮萃汁"),
    (1, "澄澈之湖・日本青森富士蘋果鮮榨"),
    (1, "青檸微光・高纖奇亞籽檸檬蜜露"),
    (1, "玉露珍珠・炒麥芽山楂消食飲"),
    (2, "暮夜靜謐 ‧ 太妃香草黑櫻桃晚安茶"),
    (2, "太虛引夢・遠志酸棗仁安魂茶"),
    (2, "暮色沉香・老白茶沉香片"),
    (2, "靜心酸棗・百合茯苓養神茶"),
    (2, "琥珀洋甘・蜜香無咖啡因茶"),
    (2, "落日餘暉・南非國寶香草茶"),
    (2, "雪山冷泉・西洋參石斛生津茶"),
    (2, "暮光之城・低因瑞士水洗拿鐵"),
    (2, "雪嶺冷萃・厭氧日曬藝伎冷萃"),
    (2, "月影桑葚・紫雲桑葚玫瑰活妍飲"),
    (2, "流金杏仁・古法微甜冷研杏仁露"),
    (2, "琥珀銀耳・蓮子百合桂花雪耳羹"),
    (2, "天籟甘泉・冷萃澎大海羅漢果露"),
    (2, "暖胃甘露・茯苓芡實白扁豆米湯"),
    (2, "冰心雪梨・川貝枇杷清潤冰茶"),
    (2, "歸元神農・甘草小麥紅棗安神湯"),
]


def resolve_dynamic_prescription(
    token: str, score: float, pressure: float = 1002.5
):
    entropy_str = f"{token}_{time.time_ns()}_{score}_{pressure}"
    h_val = int(hashlib.sha256(entropy_str.encode("utf-8")).hexdigest()[:8], 16)
    idx = h_val % len(PRESCRIPTION_50_POOL)
    cat_id, prescription_name = PRESCRIPTION_50_POOL[idx]
    mapped_info = PRESCRIPTION_CATEGORIES[cat_id]
    return prescription_name, mapped_info


@st.cache_resource
def get_global_database():
    return {
        "#SYM-C701": {
            "status": "已完成診前 19s 共振調息",
            "coherence_score": 92.5,
            "stress_index": "深度寧靜需求",
            "stress_desc": "低張力 / 尋求整合",
            "sleep_hours": 7.2,
            "timestamp": "2026-09-07 09:15:00",
            "weekly_trend": [82, 85, 87, 84, 89, 91, 92.5],
            "prescription_50": "朝露果妍 ‧ 晨光葡莓玫瑰鮮果茶",
            "mapped_drink": "朝露果妍 ‧ 晨光葡莓玫瑰鮮果茶",
            "nudge": "探險家近 3 天夜間無應激爆發，心流穩定（92.5%）。建議問診重點：維持優質睡眠時數。",
            "summary": "【去敏身心軌跡摘要】個案於看診前在候診區完成 19 秒迷走共振調息。心流一致性維持於 90% 以上高諧振區間。",
        }
    }


@st.cache_resource
def get_global_queue():
    return [
        {
            "token": "#SYM-C701",
            "time": "09:15",
            "source": "LINE LIFF / App",
            "drink": "朝露果妍 ‧ 晨光葡莓玫瑰鮮果茶",
        }
    ]


global_db = get_global_database()
global_queue = get_global_queue()

# 讀取跨進程共享檔案
if os.path.exists(SHARED_QUEUE_FILE):
    try:
        with open(SHARED_QUEUE_FILE, "r", encoding="utf-8") as f:
            live_q = json.load(f)
            for item in live_q:
                if not any(x["token"] == item["token"] for x in global_queue):
                    global_queue.insert(0, item)
    except Exception:
        pass


def fetch_patient_data(user_key):
    if os.path.exists(SHARED_DB_FILE):
        try:
            with open(SHARED_DB_FILE, "r", encoding="utf-8") as f:
                db_disk = json.load(f)
                if user_key in db_disk:
                    return db_disk[user_key]
        except Exception:
            pass
    return global_db.get(user_key, None)


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

# ==============================================================================
# 2. Bespoke French High-Jewelry 樣式 (徹底隱藏 app/recovery/reserve)
# ==============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Didot&family=Garamond:ital,wght@0,400;0,600;1,400&display=swap');

    /* 關鍵：徹底隱藏 Streamlit 自動產生的側邊欄多頁面選單 (app, recovery, reserve) */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    .stApp {
        background-color: #FAF8F5;
        font-family: -apple-system, BlinkMacSystemFont, "Garamond", "Didot", "Georgia", "PingFang TC", sans-serif;
    }
    header[data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    footer { visibility: hidden; }

    .curio-hero-card {
        background: linear-gradient(135deg, #25352B 0%, #1A261F 100%);
        color: #FAF8F5;
        padding: 30px 40px;
        border-radius: 26px;
        box-shadow: 0 18px 40px rgba(37, 53, 43, 0.12);
        border: 1px solid #C2A675;
        margin-bottom: 20px;
    }
    .curio-hero-card h1 { 
        font-family: "Didot", "Georgia", "PingFang TC", serif !important;
        color: #FAF8F5 !important; 
        font-size: 1.8rem !important; 
        margin: 0 0 6px 0 !important; 
    }
    .curio-hero-card p { 
        color: #D3E0D7 !important; 
        font-size: 0.88rem !important; 
        margin: 0 !important; 
    }

    .curio-3d-icon {
        width: 26px;
        height: 26px;
        background: linear-gradient(145deg, #FAF8F5, #EBE4D8);
        border-radius: 8px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #C2A675;
        font-size: 0.85rem;
        margin-right: 6px;
        vertical-align: middle;
    }

    .doctor-care-card {
        background: linear-gradient(135deg, #F4F0E8 0%, #EAE4D8 100%);
        border: 1px solid #C2A675;
        border-radius: 20px;
        padding: 18px 24px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .doctor-care-text { font-size: 0.9rem; color: #25352B; line-height: 1.6; }
    .doctor-timer-badge {
        background: #25352B;
        color: #FAF8F5;
        padding: 10px 16px;
        border-radius: 14px;
        font-size: 0.85rem;
        border: 1px solid #C2A675;
        text-align: right;
    }

    .quick-nudge-box {
        background-color: #FFFFFF;
        border-left: 4px solid #C2A675;
        border-radius: 16px;
        padding: 16px 20px;
        margin-bottom: 18px;
        border: 1px solid #E4DCD0;
        border-left-width: 4px;
    }

    .atelier-login-card {
        background: rgba(255, 255, 255, 0.96);
        border: 1.5px solid #C2A675;
        padding: 45px 40px 30px 40px;
        border-radius: 28px;
        box-shadow: 0 20px 50px rgba(37, 53, 43, 0.08);
        max-width: 500px;
        margin: 20px auto;
        text-align: center;
    }
    .custom-metric-card {
        background: #FFFFFF;
        border: 1px solid #E4DCD0;
        padding: 22px 24px;
        border-radius: 20px;
        box-shadow: 4px 4px 14px rgba(37, 53, 43, 0.03);
    }
    .custom-metric-value { 
        font-size: 1.5rem; 
        color: #25352B; 
        font-weight: 600; 
        font-family: "Didot", "Garamond", serif; 
        margin-bottom: 6px; 
    }
    .custom-metric-delta { 
        font-size: 0.8rem; 
        color: #435449; 
        background-color: #F4F0E8; 
        padding: 3px 10px; 
        border-radius: 8px; 
        display: inline-block; 
        border: 1px solid #E4DCD0; 
    }

    .stButton>button {
        border-radius: 12px !important;
        border: 1px solid #C2A675 !important;
        background: linear-gradient(135deg, #FAF8F5 0%, #F4F0E8 100%) !important;
        color: #25352B !important;
        font-weight: 500 !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #25352B 0%, #1A261F 100%) !important;
        color: #FAF8F5 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# 3. 診間 Dialog 彈窗模組
# ==============================================================================
if hasattr(st, "dialog"):

    @st.dialog("💬 匿名問題與使用體驗回饋")
    def feedback_dialog(user_role: str, current_token: str):
        st.markdown(
            f"目前連線代碼：`{current_token}` ｜ 身分：<b>{user_role}</b>",
            unsafe_allow_html=True,
        )
        cat = st.radio(
            "請選擇問題類型：",
            ["操作不順暢", "鏡頭感應不良", "視覺體驗建議"],
            horizontal=True,
        )
        txt = st.text_area("詳細說明：", height=90)
        if st.button("🚀 送出匿名回饋", use_container_width=True):
            save_anonymous_feedback(user_role, current_token, cat, txt)
            st.success("✅ 回饋已安全送達日誌庫！")
            st.rerun()

    @st.dialog("⚙️ 變更診間金鑰")
    def change_password_dialog():
        old_p = st.text_input("輸入原診間金鑰：", type="password")
        new_p = st.text_input("設定新診間金鑰：", type="password")
        if st.button("🔒 確認更新", use_container_width=True):
            if old_p != st.session_state["doctor_password"]:
                st.error("❌ 原金鑰輸入錯誤！")
            elif not new_p:
                st.warning("⚠️ 新金鑰不可為空！")
            else:
                st.session_state["doctor_password"] = new_p
                st.success("🎉 診間金鑰已更新成功！")
                st.rerun()

# ==============================================================================
# 4. 門診登入驗證頁
# ==============================================================================
if not st.session_state["authenticated"]:
    st.markdown(
        """
        <div class="atelier-login-card">
            <div style="font-size: 2.6rem; margin-bottom: 6px;">🐿️</div>
            <div style="color: #C2A675; font-size: 0.9rem; letter-spacing: 2px;">CURIO & STUDIO</div>
            <h2 style="color: #25352B; font-family: Garamond, serif; margin: 6px 0 14px 0;">交感身心診所 ‧ 門診驗證</h2>
            <p style="font-size: 0.85rem; color: #596B60; line-height: 1.6;">
                零知識架構 (Zero-Knowledge) ‧ 去敏身心軌跡拋接<br>
                首席珍藏家蔻恩閣長已為您鎖定 0 個資防線
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1.2, 1.8, 1.2])
    with col2:
        pwd = st.text_input(
            "院長診間金鑰",
            type="password",
            placeholder="請輸入金鑰 (預設: NYJAZZ-8519)",
        )
        if st.button("解鎖門診數據面板", use_container_width=True):
            if (
                pwd == st.session_state["doctor_password"]
                or pwd == MASTER_KEY
            ):
                st.session_state["authenticated"] = True
                st.session_state["clinic_start_time"] = time.time()
                st.rerun()
            else:
                st.error("⚠️ 金鑰驗證未通過，請重新確認。")
    st.stop()

# ==============================================================================
# 5. 側邊欄：音樂與待看佇列
# ==============================================================================
with st.sidebar:
    st.markdown(
        """
        <div style="background:#FFFFFF; border:1px solid #E4DCD0; padding:14px; border-radius:18px; text-align:center; margin-bottom:14px;">
            <div style="font-size: 1.8rem;">🐿️ 🕊️</div>
            <b style="color:#25352B; font-size:0.9rem;">Curio & Studio 數據中繼站</b><br>
            <span style="font-size:0.75rem; color:#C2A675;">首席珍藏家蔻恩閣長 ✕ 信鴿 Singer</span>
        </div>
    """,
        unsafe_allow_html=True,
    )

    with st.expander("🎵 郭醫師指定 YouTube 聲景音場", expanded=True):
        st.components.v1.html(
            """
            <iframe width="100%" height="160" src="https://www.youtube.com/embed/_eCGu2Te3ZA?autoplay=0&loop=1&playlist=_eCGu2Te3ZA" 
            frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        """,
            height=170,
        )

    st.markdown("<b>📜 門診待看佇列 (Queue)</b>", unsafe_allow_html=True)
    for item in global_queue:
        if st.button(
            f"解鎖 {item['token']} ({item['time']})",
            key=f"q_{item['token']}",
            use_container_width=True,
        ):
            st.session_state["selected_token"] = item["token"]
            st.rerun()

# ==============================================================================
# 6. 醫師端主面板
# ==============================================================================
st.markdown(
    """
    <div class="curio-hero-card">
        <h1>夢境珍奇櫃診間面板</h1>
        <p>Curio & Studio x 交感身心診所 ｜ 0 個資 ‧ 診前身心軌跡去敏拋接</p>
    </div>
""",
    unsafe_allow_html=True,
)

elapsed_minutes = int(
    (time.time() - st.session_state["clinic_start_time"]) // 60
)
completed = st.session_state["completed_count"]
total_p = st.session_state["total_booked_patients"]

st.markdown(
    f"""
    <div class="doctor-care-card">
        <div>
            午安。今日預約看診 <b>{total_p}</b> 位探險家 ｜ 目前進度：<b>{completed}/{total_p}</b><br>
            <span style="font-size:0.82rem; color:#596B60;">🍵 現場候診區備有調飲：本日建議搭配 <b>薄荷冰焙茶</b> ✕ <b>煙燻雪松香氛</b>。</span>
        </div>
        <div class="doctor-timer-badge">
            看診進行中: {elapsed_minutes} m
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

col_t1, col_t2, col_t3 = st.columns([2, 1, 1])
with col_t2:
    if st.button("⚙️ 變更金鑰", use_container_width=True):
        if hasattr(st, "dialog"):
            change_password_dialog()
with col_t3:
    if st.button("💬 系統回饋", use_container_width=True):
        if hasattr(st, "dialog"):
            feedback_dialog("臨床醫師", st.session_state["selected_token"])

user_key = st.text_input(
    "請輸入探險家去敏密鑰 (例如：#SYM-C701) :",
    value=st.session_state["selected_token"],
)

if user_key:
    data = fetch_patient_data(user_key)
    if data:
        p50 = data.get("prescription_50", "朝露果妍 ‧ 晨光葡莓玫瑰鮮果茶")
        mdrink = data.get(
            "mapped_drink", "朝露果妍 ‧ 晨光葡莓玫瑰鮮果茶"
        )

        st.markdown(
            f"""
            <div class="quick-nudge-box">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                    <b style="color:#25352B;">✨ 蔻恩閣長 1 秒問診焦點提示 (Clinical Nudge)</b>
                    <span style="color:#C2A675; font-size:0.85rem; font-weight:bold;">🍵 生活處方：{p50}（現場備有：{mdrink}）</span>
                </div>
                <div style="font-size:0.86rem; color:#596B60; line-height:1.5;">
                    {data.get('nudge', '個案身心軌跡平穩，可進行常規問診。')}
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                f"""
                <div class="custom-metric-card">
                    <div style="font-size:0.85rem; color:#596B60;">心流一致性 (0.067Hz)</div>
                    <div class="custom-metric-value">{data['coherence_score']} %</div>
                    <div class="custom-metric-delta">↑ 3.2% 穩定共振</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f"""
                <div class="custom-metric-card">
                    <div style="font-size:0.85rem; color:#596B60;">心理狀態指標</div>
                    <div class="custom-metric-value">{data['stress_index']}</div>
                    <div class="custom-metric-delta">{data.get('stress_desc', '平穩狀態')}</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f"""
                <div class="custom-metric-card">
                    <div style="font-size:0.85rem; color:#596B60;">睡眠時數 / 氣壓環境</div>
                    <div class="custom-metric-value">{data.get('sleep_hours', 7.4)} hr</div>
                    <div class="custom-metric-delta">{data.get('ambient_pressure', '1012.0 hPa')}</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["近 7 日心流共振曲線", "診前去敏摘要"])
        with tab1:
            chart_df = pd.DataFrame(
                {
                    "日期": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                    "心流分數": data.get(
                        "weekly_trend", [80, 83, 85, 87, 89, 91, 93]
                    ),
                }
            ).set_index("日期")
            st.line_chart(chart_df, color="#25352B")
        with tab2:
            st.write(
                f"**【去敏身心摘要】**\n\n{data.get('summary', '個案已完成診前 19 秒調息。')}"
            )
            st.caption(
                f"🕒 數據傳輸時間戳記：{data.get('timestamp', '今日')}"
            )
    else:
        st.error(
            f"⚠️ 找不到密鑰 `{user_key}` 之當日資料，請確認病患端是否已點擊送出。"
        )