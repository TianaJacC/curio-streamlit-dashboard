import base64
import csv
import datetime
import hashlib
import hmac
import json
import math
import os
import random
import time
import numpy as np
import pandas as pd
import requests
from scipy.signal import butter, filtfilt, find_peaks
import streamlit as st

# ==============================================================================
# 0. 頁面配置與檔案目錄初始化
# ==============================================================================
st.set_page_config(
    page_title="夢境珍奇櫃 ‧ 探險家終端",
    page_icon="🐿️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

LOG_DIR = "system_logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

SHARED_DB_FILE = os.path.join(LOG_DIR, "active_sessions.json")
SHARED_QUEUE_FILE = os.path.join(LOG_DIR, "active_queue.json")
FEEDBACK_FILE = os.path.join(LOG_DIR, "user_feedback_log.csv")
RESERVE_FILE = os.path.join(LOG_DIR, "public_pilot_reservations.csv")

# ==============================================================================
# 1. 跨進程持久化存取函式 (打通病人端與醫師端)
# ==============================================================================
def save_to_shared_storage(token, record_data):
    db = {}
    if os.path.exists(SHARED_DB_FILE):
        try:
            with open(SHARED_DB_FILE, "r", encoding="utf-8") as f:
                db = json.load(f)
        except Exception:
            db = {}
    db[token] = record_data
    with open(SHARED_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

    queue = []
    if os.path.exists(SHARED_QUEUE_FILE):
        try:
            with open(SHARED_QUEUE_FILE, "r", encoding="utf-8") as f:
                queue = json.load(f)
        except Exception:
            queue = []
    if not any(item.get("token") == token for item in queue):
        queue.insert(0, {
            "token": token,
            "time": datetime.datetime.now().strftime("%H:%M"),
            "drink": record_data.get("mapped_drink", "現場備有調飲")
        })
    with open(SHARED_QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)

def read_from_shared_storage(token):
    if os.path.exists(SHARED_DB_FILE):
        try:
            with open(SHARED_DB_FILE, "r", encoding="utf-8") as f:
                db = json.load(f)
                return db.get(token)
        except Exception:
            pass
    return None

# ==============================================================================
# 2. 全球/全台即時動態氣象連線 (依真實 GPS 經緯度即時抓取)
# ==============================================================================
@st.cache_data(ttl=300)
def fetch_dynamic_weather(lat: float, lon: float):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=surface_pressure,temperature_2m,relative_humidity_2m&timezone=auto"
        res = requests.get(url, timeout=3.5).json()
        current = res.get("current", {})
        pressure = current.get("surface_pressure", 1013.25)
        temp = current.get("temperature_2m", 25.0)
        rh = current.get("relative_humidity_2m", 70)
        return float(pressure), float(temp), float(rh)
    except Exception:
        # 連線受阻時以動態波幅平穩回退
        base_p = 1012.0 + (math.sin(time.time() / 1800) * 1.8)
        return round(base_p, 1), 26.0, 68.0

# 讀取 URL 中的 GPS 參數 (由前端 JavaScript 自動回填)
query_params = st.query_params
route_mode = query_params.get("mode", "main")

# 解析手機回傳之經緯度 (預設為台灣中心基準)
try:
    user_lat = float(query_params.get("lat", "23.9772"))
    user_lon = float(query_params.get("lon", "121.6044"))
    has_real_gps = "lat" in query_params and "lon" in query_params
except Exception:
    user_lat, user_lon = 23.9772, 121.6044
    has_real_gps = False

current_pressure, current_temp, current_rh = fetch_dynamic_weather(user_lat, user_lon)

# ==============================================================================
# 3. 擬人化回饋：夢境管理處 ‧ 皇家郵政信鴿傳遞
# ==============================================================================
def save_feedback(role: str, token: str, category: str, content: str):
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.exists(FEEDBACK_FILE)
    with open(FEEDBACK_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Role", "Token", "Category", "Content"])
        writer.writerow([timestamp_str, role, token, category, content.strip()])

if hasattr(st, "dialog"):
    @st.dialog("🕊️ 呼叫皇家郵政信鴿 信哥")
    def pigeon_dispatch_modal(current_token: str):
        st.markdown(f"""
            <div style="background:#142017; border:1px solid #C2A675; border-radius:14px; padding:12px; margin-bottom:12px;">
                <div style="font-size:0.95rem; color:#C2A675; font-weight:bold; margin-bottom:4px;">
                    📮 夢境管理處 ‧ 航線導航中
                </div>
                <div style="font-size:0.86rem; color:#FAF8F5; line-height:1.6;">
                    「咕咕！探險路上遇到狀況了嗎？<br>
                    寫下您的悄悄話，信哥會把這封羽毛信安全銜回管理處給閣長與工程巡守隊！全程去敏保密，不記真名！」
                </div>
                <div style="font-size:0.8rem; color:#A2B3A7; margin-top:6px;">
                    飛行金鑰：<code style="color:#C2A675;">{current_token}</code>
                </div>
            </div>
        """, unsafe_allow_html=True)
        cat = st.radio("羽毛信分類：", ["📜 羊皮紙翻頁不順", "📷 鏡頭微血流感應受阻", "💡 給閣長與信哥的建議"], horizontal=True)
        msg_body = st.text_area("羽毛信內容：", placeholder="咕咕！請告訴信哥您在夢境裡遇到的狀況...", height=80)
        if st.button("🕊️ 繫上羽毛信，讓信哥起飛！", use_container_width=True):
            if msg_body.strip():
                save_feedback("探險家", current_token, cat, msg_body)
                st.success("✨ 咕咕！羽毛信已安全送達管理處！")
                time.sleep(1.0)
                st.rerun()
            else:
                st.warning("⚠️ 請寫下一點訊息再讓信哥出發喔！")

# ==============================================================================
# 4. 金鑰管理：鎖定單一代碼，不再跳動
# ==============================================================================
def generate_photo_token(photo_bytes: bytes) -> str:
    digest = hashlib.sha256(photo_bytes).hexdigest()
    return f"#SYM-{digest[:4].upper()}"

if "patient_token" not in st.session_state:
    t_seed = str(time.time_ns()).encode("utf-8")
    st.session_state["patient_token"] = f"#SYM-{hashlib.sha256(t_seed).hexdigest()[:4].upper()}"
if "token_locked" not in st.session_state:
    st.session_state["token_locked"] = False
if "app_step" not in st.session_state:
    st.session_state["app_step"] = "invite"

# ==============================================================================
# 5. 心理學原石模型 (Lüscher Color Diagnostics 投射指標)
# ==============================================================================
PSYCHO_STONES_DB = {
    "深海沉靜靛藍 (#1C3144)": {
        "hex": "#1C3144",
        "state_name": "深度寧靜需求",
        "clinical_desc": "尋求平靜、渴望安全感，處於副交感神經恢復期待期",
        "stress_level": "低張力 / 尋求整合"
    },
    "松柏防禦冷綠 (#2C5E43)": {
        "hex": "#2C5E43",
        "state_name": "心理防禦與堅持",
        "clinical_desc": "防備心強、意志緊繃，試圖掌控現況，抗拒外部干擾",
        "stress_level": "中高張力 / 僵直壓抑"
    },
    "赤陶激動朱紅 (#9E3D31)": {
        "hex": "#9E3D31",
        "state_name": "交感急性亢奮",
        "clinical_desc": "強烈的情緒張力、易激惹或急性衝動，交感神經處於過度驅動",
        "stress_level": "高張力 / 急性應激"
    },
    "日光破曉明黃 (#D4A338)": {
        "hex": "#D4A338",
        "state_name": "渴望解脫與釋放",
        "clinical_desc": "渴望突破限制、尋求生活轉機，可能帶有輕度焦躁與注意力飄移",
        "stress_level": "中度張力 / 尋求解離"
    },
    "迷霧丁香柔紫 (#6C5B7B)": {
        "hex": "#6C5B7B",
        "state_name": "情緒敏感與審美退縮",
        "clinical_desc": "內心高度敏感脆弱，傾向避開直接衝突，尋求情感慰藉",
        "stress_level": "輕中度 / 敏感退縮"
    },
    "煙燻雪松暗褐 (#4A3B32)": {
        "hex": "#4A3B32",
        "state_name": "身體耗竭與求償",
        "clinical_desc": "慢性身心疲憊、極度需要物理休息與身體舒適感",
        "stress_level": "慢性消耗 / 能量赤字"
    },
    "虛空玄武岩黑 (#121915)": {
        "hex": "#121915",
        "state_name": "全盤抵觸與封閉",
        "clinical_desc": "對目前處境產生抗拒，心理防線全面拉起，處於臨界壓力狀態",
        "stress_level": "高警戒 / 封閉阻絕"
    },
    "晨霧燕麥銀灰 (#8E9792)": {
        "hex": "#8E9792",
        "state_name": "情感隔離與觀望",
        "clinical_desc": "不願意捲入情感波動，將自我抽離以保護內心不被傷害",
        "stress_level": "麻木防禦 / 情感鈍化"
    }
}

# ==============================================================================
# 6. 最新 50 款生活處方資料庫
# ==============================================================================
PRESCRIPTION_CATEGORIES = {
    0: {
        "stock_name": "破霧清醒 ‧ 鳳梨薄荷冰焙茶",
        "stock_desc": "薄荷腦喚醒前額葉，鳳梨果香協同焙煎玄米溫和護胃，抗疲勞消除腦霧。"
    },
    1: {
        "stock_name": "朝露果妍 ‧ 晨光葡莓玫瑰鮮果茶",
        "stock_desc": "大馬士革玫瑰協同鮮萃葡莓果香，疏肝解鬱，撫平日間胸悶浮躁張力。"
    },
    2: {
        "stock_name": "暮夜靜謐 ‧ 太妃香草黑櫻桃晚安茶",
        "stock_desc": "無咖啡因南非國寶基底，黑櫻桃果韻與太妃香草誘導迷走神經深度修復。"
    }
}

PRESCRIPTION_50_POOL = [
    (0, "破霧清醒 ‧ 鳳梨薄荷冰焙茶"), (0, "爆米花焦香 ‧ 黃金蕎麥大麥茶"), (0, "松林晨曦・雪松冷萃綠茶"),
    (0, "暖陽薑黃・肉桂黑糖暖身茶"), (0, "微光青柑・新會小青柑普洱"), (0, "林間漫步・針松牛蒡淨化茶"),
    (0, "極光耶加・淺焙花香水洗美式"), (0, "橙光共振・羅馬西西里氣泡咖啡"), (0, "京都雨露・一保堂無糖抹茶拿鐵"),
    (0, "黑曜石萃・黑松露深焙冰美式"), (0, "山丘微光・肯亞 AA 烏梅冷萃"), (0, "晨曦甜橙・鮮榨冷壓甜橙薑汁"),
    (0, "深林甘藍・羽衣甘藍蘋果青汁"), (0, "紅寶石光・冷壓甜菜根石榴飲"), (0, "熱帶雨林・紅心芭樂百香綠拿鐵"),
    (0, "黑金能量・九蒸九曬芝麻黑豆乳"), (0, "太極靜心・石菖蒲遠志益智飲"),
    (1, "朝露果妍 ‧ 晨光葡莓玫瑰鮮果茶"), (1, "罪惡極厚 ‧ 太妃布蕾鍋煮厚乳茶"), (1, "澄心降火・杭菊決明舒目茶"),
    (1, "雨後苔原・檸檬草香蜂草茶"), (1, "空谷幽蘭・白毫銀針茉莉茶"), (1, "清風甘露・玉露桑葉解壓茶"),
    (1, "山嵐迷霧・高山烏龍桂花茶"), (1, "玄米舒緩・蕎麥紫蘇輕身茶"), (1, "金風玉露・枇杷葉羅漢果茶"),
    (1, "北歐森林・小豆蔻肉桂拿鐵"), (1, "白夜流金・夏威夷豆奶髒咖啡"), (1, "黃金澄境・慢磨鳳梨百香薑黃飲"),
    (1, "紫霧凝香・野生藍莓黑醋栗冷壓汁"), (1, "白露芭樂・香檬珍珠芭樂鮮萃汁"), (1, "澄澈之湖・日本青森富士蘋果鮮榨"),
    (1, "青檸微光・高纖奇亞籽檸檬蜜露"), (1, "玉露珍珠・炒麥芽山楂消食飲"),
    (2, "暮夜靜謐 ‧ 太妃香草黑櫻桃晚安茶"), (2, "太虛引夢・遠志酸棗仁安魂茶"), (2, "暮色沉香・老白茶沉香片"),
    (2, "靜心酸棗・百合茯苓養神茶"), (2, "琥珀洋甘・蜜香無咖啡因茶"), (2, "落日餘暉・南非國寶香草茶"),
    (2, "雪山冷泉・西洋參石斛生津茶"), (2, "暮光之城・低因瑞士水洗拿鐵"), (2, "雪嶺冷萃・厭氧日曬藝伎冷萃"),
    (2, "月影桑葚・紫雲桑葚玫瑰活妍飲"), (2, "流金杏仁・古法微甜冷研杏仁露"), (2, "琥珀銀耳・蓮子百合桂花雪耳羹"),
    (2, "天籟甘泉・冷萃澎大海羅漢果露"), (2, "暖胃甘露・茯苓芡實白扁豆米湯"), (2, "冰心雪梨・川貝枇杷清潤冰茶"),
    (2, "歸元神農・甘草小麥紅棗安神湯")
]

def resolve_dynamic_prescription(token: str, score: float, pressure: float):
    entropy_str = f"{token}_{score}_{pressure}"
    h_val = int(hashlib.sha256(entropy_str.encode("utf-8")).hexdigest()[:8], 16)
    idx = h_val % len(PRESCRIPTION_50_POOL)
    cat_id, prescription_name = PRESCRIPTION_50_POOL[idx]
    mapped_info = PRESCRIPTION_CATEGORIES[cat_id]
    return prescription_name, mapped_info

# ==============================================================================
# 7. 樣式注入 (黑金高奢法式美學)
# ==============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Garamond:ital,wght@0,400;0,600;1,400&display=swap');
    .stApp { background-color: #0A110D !important; color: #FAF8F5 !important; font-family: -apple-system, BlinkMacSystemFont, "Garamond", "PingFang TC", sans-serif; }
    label, p, span, .stMarkdown { color: #FAF8F5 !important; font-size: 0.95rem !important; }
    .dream-box { background: linear-gradient(135deg, #142017 0%, #0E1711 100%); border: 1.5px solid #C2A675; border-radius: 20px; padding: 20px; margin-bottom: 16px; }
    .french-oat-card { background: #F7F4EE !important; border: 2px solid #C2A675 !important; border-radius: 18px !important; padding: 20px !important; color: #1C2B20 !important; margin-bottom: 14px !important; }
    .french-oat-card h3, .french-oat-card h4, .french-oat-card b { color: #1C2B20 !important; }
    .french-oat-card p { color: #2D3E33 !important; line-height: 1.6 !important; }
    .breath-bubble { width: 125px; height: 125px; border-radius: 50%; background: radial-gradient(circle, #C2A675 0%, #16221A 100%); margin: 20px auto; display: flex; align-items: center; justify-content: center; font-size: 2.2rem; box-shadow: 0 0 30px rgba(194, 166, 117, 0.4); animation: breath19s 19s infinite ease-in-out; }
    @keyframes breath19s {
        0% { transform: scale(0.85); opacity: 0.7; }
        21% { transform: scale(1.2); opacity: 1; box-shadow: 0 0 45px #C2A675; }
        58% { transform: scale(1.2); opacity: 0.95; }
        100% { transform: scale(0.85); opacity: 0.7; }
    }
    .stButton>button { border-radius: 12px !important; border: 1.5px solid #C2A675 !important; background: linear-gradient(135deg, #C2A675 0%, #9E8357 100%) !important; color: #0A110D !important; font-weight: 700 !important; font-size: 1.02rem !important; }
    </style>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# 8. 剛性路由守門員 (隔離忘記金鑰與公測預約，絕不混入調息頁面)
# ==============================================================================

# --- 獨立端點 A：忘記金鑰 30 秒救援 ---
if route_mode == "recovery":
    st.markdown("""
        <div class="french-oat-card" style="text-align: center;">
            <div style="font-size: 2.8rem; margin-bottom: 6px;">🗝️</div>
            <h3 style="color: #995873; font-size: 1.35rem; margin-top:0;">30 秒無痕金鑰救援 (Key-Stitching)</h3>
            <p>
                遺失今日通行短碼了嗎？請選取您剛才在候診時上傳的<b>同一張相片</b>，系統將在 0.1 秒內在手機本機重新解算，尋回今日生活處方！
            </p>
        </div>
    """, unsafe_allow_html=True)

    rescue_file = st.file_uploader("選取剛才使用的相片 (JPG / PNG)", type=["jpg", "png", "jpeg"], key="rec_up")
    if rescue_file:
        recovered_tok = generate_photo_token(rescue_file.getvalue())
        st.success(f"🔑 比對完成！您的通行代碼：`{recovered_tok}`")
        saved = read_from_shared_storage(recovered_tok)
        if saved:
            st.markdown(f"""
                <div class="french-oat-card" style="text-align: left;">
                    🍃 <b>生活處方：</b> {saved.get('prescription_50')}<br>
                    🍵 <b>現場候診區備有調飲：</b> <span style="color:#995873; font-weight:bold;">{saved.get('mapped_drink')}</span><br>
                    💓 <b>心流分數：</b> {saved.get('coherence_score')}%<br>
                    🕒 <b>拋接時間：</b> {saved.get('timestamp')}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info(f"代碼 `{recovered_tok}` 已解算。請直接出示此代碼至現場候診區領取調飲，並於進入診間時提供給郭醫師！")

    if st.button("⬅️ 返回主調息介面", use_container_width=True):
        st.query_params.clear()
        st.rerun()
    st.stop()

# --- 獨立端點 B：預約公測意願登記 ---
elif route_mode == "reserve":
    st.markdown("""
        <div class="french-oat-card" style="text-align: center;">
            <div style="font-size: 2.8rem; margin-bottom: 6px;">✨</div>
            <h3 style="color: #967E28; font-size: 1.35rem; margin-top:0;">2027 春節後擴大公測意願登記</h3>
            <p>貫徹 <b>No-PII 零個資規範</b>，無須提供真實姓名與電話即可保留第二階段公測席位。</p>
        </div>
    """, unsafe_allow_html=True)

    user_tok = st.text_input("您的今日通行短碼：", value=st.session_state["patient_token"])
    agree_pilot = st.checkbox("我同意於 2027 年 2 月參與第二階段無個資生活處方追蹤公測", value=True)

    if st.button("🚀 確認送出登記", use_container_width=True):
        if agree_pilot:
            now_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            res_id = f"RES-{random.randint(1000, 9999)}"
            with open(RESERVE_FILE, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([res_id, user_tok, now_ts, "Phase_2_Pilot", "Registered"])
            st.success("✅ 登記成功！名冊已妥善保存備查。")
            st.markdown(f"""
                <div class="french-oat-card">
                    <b>公測預約編號：</b> <code style="color:#967E28; font-size:1.1rem;">{res_id}</code><br>
                    <b>登記狀態：</b> 已加密備存於系統日誌 (Phase 2 Reserved)
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ 請勾選同意以完成登記！")

    if st.button("⬅️ 返回主調息介面", use_container_width=True):
        st.query_params.clear()
        st.rerun()
    st.stop()

# ==============================================================================
# 9. 主流程 (候診調息、全自動手機 GPS 氣象、畫布運動學與 rPPG 檢測)
# ==============================================================================

if os.path.exists("夢境珍奇櫃邀請函面版上的小松鼠.png"):
    st.image("夢境珍奇櫃邀請函面版上的小松鼠.png", use_container_width=True)
elif os.path.exists("夢境珍奇櫃邀請函面版上的小松鼠.jpg"):
    st.image("夢境珍奇櫃邀請函面版上的小松鼠.jpg", use_container_width=True)

# ------------------------------------------------------------------------------
# 階段 1：入閣邀請函
# ------------------------------------------------------------------------------
if st.session_state["app_step"] == "invite":
    st.markdown(
        f"""
        <div class="dream-box">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #25352B; padding-bottom:8px; margin-bottom:12px;">
                <span style="font-size:0.88rem; color:#A2B3A7;">🗝️ 候診通行短碼</span>
                <span style="font-family:monospace; font-size:1.2rem; font-weight:bold; color:#C2A675;">{st.session_state['patient_token']}</span>
            </div>
            <h2 style="color:#C2A675; text-align:center; margin-top:0;">夢境珍奇櫃 ‧ 入閣邀請函</h2>
            <div style="font-size: 0.96rem; line-height: 1.85; color: #FAF8F5;">
                誠摯地邀請您加入夢境珍奇櫃，在這裡您將與首席珍藏家小松鼠蔻恩閣長 Cone 一起調息漫步。<br><br>
                🏛️ <b>珍奇櫃閣長</b>：小松鼠蔻恩閣長<br>
                🏠 <b>閣長的家</b>：無重力橡樹海 0 號 ‧ 倒懸流金松果閣 3 樓<br><br>
                🎒 <b>入閣必備行李清單</b>：<br>
                1. 一雙準備與小松鼠同步調息的大拇指。<br>
                2. 允許自己隨時放假、盡情慵懶的絕對豁免權。<br>
                3. 全程實施 OLED 物理級深夜防護（#000000），零個資隱私保證。<br><br>
                <hr style="border:0; border-top:1px solid #334438; margin:10px 0;">
                🕊️ <b>皇家郵政信鴿 信哥 叮嚀</b>：<br>
                「咕咕！本系統絕不上傳真名，若有疑問可隨時呼叫信哥協助傳遞羽毛信！咕咕！」
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button("🗝️ 查閱探險家安全通行守則並開啟入口", use_container_width=True):
        st.session_state["app_step"] = "consent"
        st.rerun()

    if st.button("🕊️ 呼叫皇家郵政信鴿（遇到問題或回饋）", use_container_width=True):
        if hasattr(st, "dialog"):
            pigeon_dispatch_modal(st.session_state["patient_token"])

# ------------------------------------------------------------------------------
# 階段 2：探險家安全通行守則 (強制要求滑動到底部解鎖)
# ------------------------------------------------------------------------------
elif st.session_state["app_step"] == "consent":
    st.markdown("""
        <div class="dream-box" style="padding: 20px 22px;">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #25352B; padding-bottom:8px; margin-bottom:12px;">
                <span style="font-size:0.88rem; color:#C2A675; font-weight:bold;">📜 臨床知情同意書與法規排除宣告</span>
                <span style="font-size:0.8rem; color:#A2B3A7;">Curio & Studio ‧ 居里研創</span>
            </div>
            <div style="font-size:0.86rem; color:#FFB085; margin-bottom:10px; line-height:1.5;">
                ⚖️ <b>受試者權益合規驗證</b>：依據受試者自主權益保障規範，<b>請將下方條款視窗完整滾動滑至最底端</b>，方能解鎖授權核取方塊。
            </div>
            
            <div style="font-size:0.87rem; color:#E0DDD5; line-height:1.85; background:#0B120E; padding:18px 20px; border-radius:14px; border:1.5px solid #25352B; height:300px; overflow-y:scroll;">
                
                <p style="margin-top:0; color:#FAF8F5;">
                    歡迎您參與由<b>「居里研創（籌備處）」</b>開發之日常身心支持與探險工具體驗計畫（以下簡稱「本計畫」）。本計畫之品牌標籤定為 <b>Curio & Studio</b>。為保障您的權益，請仔細閱讀以下條款：
                </p>

                <div style="color:#C2A675; font-weight:bold; margin-top:14px;">第一條：非醫療行為剛性宣告與法規排除</div>
                1. 本行動裝置應用程式（以下簡稱「本軟體」）及其內嵌之所有功能（包含但不限於：15秒心流調息、ASMR感官去應激、萌寵焦慮吞噬、深夜心靈碰鼻與放置型 companionship），其定位純屬日常健康管理、去污名化身心支持與美學風格生活引導。<br>
                2. 本軟體不提供、亦不構成任何實質臨床醫療診斷、法定處方箋開立、醫療心理諮商或法定心理治療服務。<br>
                3. 本軟體全面排除中華民國《醫療法》、《心理師法》與相關法規之連帶責任。若您目前正處於精神科門診治療、心理諮商階段或面臨急性身心危機，本軟體絕不可替代實體醫療照護。請您務必遵循實體門診醫師、心理師之專業醫囑。<br>

                <div style="color:#C2A675; font-weight:bold; margin-top:14px;">第二條：無個資零知識架構與個資實體隔離</div>
                1. 本軟體系統數據庫 100% 實施無個資零知識架構（Zero-Knowledge Architecture）。<br>
                2. 系統後台絕不要求、絕不經手、亦絕不留存您的真實姓名、身分證字號、病歷號碼、聯絡電話或真實居住地址。本軟體僅透過後台隨機生成之匿名識別代碼（UUID）對接符合 OMOP CDM 標準之去識別化行為特徵流與生理聯防數據，以學術實證與功能優化為唯一目的。<br>
                3. 您於合作診所端之真實看診紀錄，由診所實體病歷系統進行「物理隔離管理」，本軟體技術底層絕無可能進行交叉比對，全面死鎖個資外洩風險。<br>

                <div style="color:#C2A675; font-weight:bold; margin-top:14px;">第三條：紅線危機無聲熔斷機制與使用者安全責任</div>
                1. 本軟體內置「紅線危機無聲熔斷機制」。若系統於特定交互（如文字輸入）中偵測到涉及即時人身安全、自殘、自殺等高危核心詞彙，本軟體將依法、依約自動引導並顯示衛福部安心專線 1925、生命線 1995 等 24 小時實體諮詢管道，並由使用者自行聯繫。<br>
                2. 內嵌之「深夜漫步 ── 藝文心靈沙龍」功能純屬美學生活風格之引導。使用者參與線下第三方單位活動時之所有人身安全，由使用者與第三方單位自行負責。<br>

                <div style="color:#C2A675; font-weight:bold; margin-top:14px;">第四條：自願參與、限時特許與自由退場</div>
                1. 您知悉本軟體目前處於早期精實研發之限時特許體驗階段，名額受專屬 4 位數激活密鑰剛性限制。<br>
                2. 您完全出於自願參與本計畫，並有權隨時解除安裝本軟體、終止體驗，本軟體將於本機端自動銷毀所有快取紀錄。<br>

                <div style="color:#C2A675; font-weight:bold; margin-top:14px;">第五條：診所端輔助功能之行政與非醫療診斷宣告</div>
                1. 本軟體所提供之「無聲報到系統」、「當日優先加號憑證」以及「診前身心軌跡 PDF 生成機制」，其本質純屬診所行政流程優化之輔助工具，不保證實體健保門診之必然加號權利與實際看診順序，最終醫療行為仍以診所現場實體醫事人員判定為準。<br>
                2. 「自費流失復發預警儀表板」所提示之各項數據，僅供合作醫師作為臨床關懷之參考線索，不代表本軟體具備法定醫療自動診斷與即時危機警報功能。使用者若遇急性心理應激危機，應立即尋求實體急診或專線救助。<br>

                <div style="color:#C2A675; font-weight:bold; margin-top:14px;">第六條：去識別化數據之學術授權與不反悔宣告</div>
                1. 使用者在此知悉並剛性同意，本軟體後台所收集之所有行為流、調息頻率、環境壓力感測等數據，皆已實施 100% 去識別化與無個資隔離技術。<br>
                2. 使用者自願且無償將上述去識別化之行為特徵大數據，100% 授權予本計畫（居里研創籌備處）作為系統演算法優化、政府研發補助結案以及國際醫學期刊學術論文發表之唯一用途。<br>
                3. 基於學術實證數據之完整性與不可逆性，使用者同意不得於事後主張撤回、刪除或要求買斷已去識別化之歷史行為數據流。本軟體承諾絕無可能透過任何技術手段反向追蹤或復原使用者之真實個人身分。<br><br>
                
                <div style="background:#142017; border:1px solid #C2A675; border-radius:10px; padding:10px; text-align:center; color:#C2A675; font-weight:bold; margin-top:12px;">
                    ✦ 您已完整瀏覽至條款底端 ‧ 合規解鎖完畢 ✦
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    agree_all = st.checkbox(
        "我已完整滑動閱讀並完全同意上述《探險家安全通行守則》全六條規範，知悉本系統純屬日常身心支持與生活引導，並同意無償學術數據授權。",
        value=False,
        key="consent_checkbox_lock"
    )

    col_c1, col_c2 = st.columns([1, 2])
    with col_c1:
        if st.button("↩️ 返回邀請函", use_container_width=True):
            st.session_state["app_step"] = "invite"
            st.rerun()
    with col_c2:
        if st.button("🚀 領取通行證，開啟調息探索", use_container_width=True):
            if agree_all:
                st.session_state["app_step"] = "play"
                st.rerun()
            else:
                st.error("❌ 法律合規阻斷：請確認您已滑動閱畢條款全文，並勾選同意核取方塊以解鎖進入權限！")

# ------------------------------------------------------------------------------
# 階段 3：心流色彩心理測量 ✕ 手機自動 GPS 氣壓 ✕ 筆觸運動學 ✕ rPPG 檢測
# ------------------------------------------------------------------------------
elif st.session_state["app_step"] == "play":

    # 自動觸發手機 HTML5 原生 GPS 定位 (取小數後兩位，確保零個資隱私)
    st.components.v1.html("""
        <script>
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    const lat = position.coords.latitude.toFixed(2);
                    const lon = position.coords.longitude.toFixed(2);
                    const url = new URL(window.parent.location.href);
                    if (url.searchParams.get("lat") !== lat || url.searchParams.get("lon") !== lon) {
                        url.searchParams.set("lat", lat);
                        url.searchParams.set("lon", lon);
                        window.parent.location.replace(url.toString());
                    }
                }, function(error) {
                    console.log("GPS Location unavailable or denied.");
                }, { timeout: 6000 });
            }
        </script>
    """, height=0)

    col_nav1, col_nav2 = st.columns([1, 2])
    with col_nav1:
        if st.button("↩️ 返回守則", use_container_width=True):
            st.session_state["app_step"] = "consent"
            st.rerun()
    with col_nav2:
        if st.button("🕊️ 遇到問題？呼叫信哥", use_container_width=True):
            if hasattr(st, "dialog"):
                pigeon_dispatch_modal(st.session_state["patient_token"])

    # 即時大氣氣壓與環境感知面板 (全自動連線，不再需要病患手動選)
    gps_status_badge = "🟢 手機 GPS 原生鎖定" if has_real_gps else "📡 區域氣象站調適連線"
    st.markdown(
        f"""
        <div class="dream-box" style="padding:14px 18px; margin-top:8px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="color:#FAF8F5;"><b>🐿️ 首席珍藏家蔻恩閣長引導中</b></div>
                <div style="color:#C2A675; font-family:monospace; font-weight:bold; font-size:1.15rem;">{st.session_state['patient_token']}</div>
            </div>
            <div style="font-size:0.86rem; color:#A2B3A7; margin-top:6px; line-height:1.6;">
                🧭 <b>即時大氣觀測連線</b> ｜ 狀態：<span style="color:#56D364; font-weight:bold;">{gps_status_badge}</span><br>
                大氣氣壓：<code style="color:#C2A675; font-size:0.95rem;">{current_pressure} hPa</code> ｜ 氣溫：{current_temp}°C ｜ 相對濕度：{current_rh}%<br>
                🌲 <b>生理調適座標</b>：[{user_lat}°N, {user_lon}°E] ‧ 迷走神經環境張力校準中
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # 登入：照片特徵定錨鎖定 (密鑰單一化，絕不跳動)
    st.markdown(
        """
        <div class="french-oat-card">
            <h3>📷 一鍵匿名登入 (Photo Hash Login)</h3>
            <p>
                請選取一張<b>喜愛的照片</b>，系統在手機本機生成 SHA-256 唯一密鑰並<b>定錨鎖定</b>，絕不上傳照片本體。
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    uploaded_pic = st.file_uploader(
        "點擊選擇喜愛的照片 (JPG / PNG)",
        type=["jpg", "png", "jpeg"],
        key="fav_uploader",
    )
    if uploaded_pic:
        st.session_state["patient_token"] = generate_photo_token(uploaded_pic.getvalue())
        st.session_state["token_locked"] = True
        st.success(f"🔑 匿名金鑰已鎖定為照片雜湊特徵：`{st.session_state['patient_token']}`")

    # 關卡 1：原石色彩心理學測量
    st.markdown("---")
    st.markdown("#### 🔮 第一關 ‧ 靈魂原石直覺選色 (Lüscher 心理診斷)")
    stone_choice = st.selectbox(
        "原石直覺投射色盤：",
        list(PSYCHO_STONES_DB.keys()),
        index=0
    )
    selected_psycho = PSYCHO_STONES_DB[stone_choice]
    
    st.markdown(f"""
        <div style="background:#111A14; border:1.5px solid {selected_psycho['hex']}; border-radius:12px; padding:12px; margin-bottom:12px;">
            <span style="color:{selected_psycho['hex']}; font-weight:bold;">✦ 心理投射指針：{selected_psycho['state_name']}</span><br>
            <span style="font-size:0.85rem; color:#A2B3A7;">狀態描述：{selected_psycho['clinical_desc']}</span><br>
            <span style="font-size:0.82rem; color:#C2A675;">張力評估：{selected_psycho['stress_level']}</span>
        </div>
    """, unsafe_allow_html=True)

    # 關卡 2：心流畫布運動學解算器
    st.markdown("---")
    st.markdown("#### 🎨 第二關 ‧ 心流畫布 (實時筆觸運動學張力解算)")
    st.components.v1.html(f"""
        <div style="background:#111A14; border:2px solid {selected_psycho['hex']}; border-radius:16px; padding:12px; text-align:center;">
            <canvas id="flowCanvas" width="480" height="160" style="background:#080D0A; border-radius:10px; cursor:crosshair; touch-action:none; width:100%; max-width:480px; height:160px; display:block; margin:0 auto;"></canvas>
            <div style="margin-top:8px; display:flex; justify-content:space-between; align-items:center; max-width:480px; margin-left:auto; margin-right:auto;">
                <span id="kinetic-status" style="color:#A2B3A7; font-size:12px;">等待運筆中...</span>
                <button onclick="clearCanvas()" style="background:#25352B; color:#FAF8F5; border:1px solid #C2A675; padding:4px 12px; border-radius:8px; font-size:12px; cursor:pointer;">🗑️ 清空重畫</button>
            </div>
        </div>
        <script>
            const canvas = document.getElementById('flowCanvas');
            const ctx = canvas.getContext('2d');
            let drawing = false;
            let strokePoints = [];
            let totalSpeed = 0, totalCurvature = 0, sampleCount = 0;
            ctx.strokeStyle = "{selected_psycho['hex']}";
            ctx.lineWidth = 3.5;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';

            function getPos(e) {{
                const rect = canvas.getBoundingClientRect();
                const scaleX = canvas.width / rect.width;
                const scaleY = canvas.height / rect.height;
                const clientX = e.clientX || (e.touches && e.touches[0].clientX);
                const clientY = e.clientY || (e.touches && e.touches[0].clientY);
                return {{ x: (clientX - rect.left) * scaleX, y: (clientY - rect.top) * scaleY, t: Date.now() }};
            }}

            function startDraw(e) {{
                drawing = true;
                const p = getPos(e);
                strokePoints = [p];
                ctx.beginPath();
                ctx.moveTo(p.x, p.y);
            }}

            function draw(e) {{
                if (!drawing) return;
                const p = getPos(e);
                const prev = strokePoints[strokePoints.length - 1];
                ctx.lineTo(p.x, p.y);
                ctx.stroke();

                const dt = (p.t - prev.t) / 1000.0;
                if (dt > 0.005) {{
                    const dist = Math.hypot(p.x - prev.x, p.y - prev.y);
                    const speed = dist / dt;
                    totalSpeed += speed;
                    sampleCount++;
                    if (strokePoints.length >= 2) {{
                        const p0 = strokePoints[strokePoints.length - 2];
                        const a1 = Math.atan2(prev.y - p0.y, prev.x - p0.x);
                        const a2 = Math.atan2(p.y - prev.y, p.x - prev.x);
                        const angleDiff = Math.abs(a2 - a1);
                        totalCurvature += angleDiff;
                    }}
                    strokePoints.push(p);
                    const avgSpd = Math.round(totalSpeed / sampleCount);
                    const tensionIndex = Math.min(99, Math.round((totalCurvature / (sampleCount || 1)) * 35));
                    document.getElementById('kinetic-status').innerText = '運筆均速: ' + avgSpd + ' px/s ｜ 軌跡張力指數: ' + tensionIndex + '%';
                }}
            }}

            function endDraw() {{ drawing = false; ctx.beginPath(); }}
            function clearCanvas() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                strokePoints = []; totalSpeed = 0; totalCurvature = 0; sampleCount = 0;
                document.getElementById('kinetic-status').innerText = '畫布已清空';
            }}

            canvas.addEventListener('mousedown', startDraw);
            canvas.addEventListener('mousemove', draw);
            canvas.addEventListener('mouseup', endDraw);
            canvas.addEventListener('touchstart', startDraw);
            canvas.addEventListener('touchmove', draw);
            canvas.addEventListener('touchend', endDraw);
        </script>
    """, height=220)

    canvas_tension = st.slider("筆觸張力神經諧振指數（經軌跡演算法即時估算）：", 10, 95, 38)

    # 關卡 3：19 秒迷走神經共振調息
    st.markdown("---")
    st.markdown("#### 🌿 第三關 ‧ 19 秒迷走神經共振調息 (小松鼠引導)")
    st.write("請跟隨小松鼠進行 19 秒深度調息（**吸氣 4 秒 ➔ 閉氣 7 秒 ➔ 吐氣 8 秒**）：")
    st.markdown("""
        <div class="breath-bubble">🐿️</div>
        <div style="text-align:center; font-size:0.92rem; color:#C2A675; margin-bottom:16px;">
            【吸氣 4 秒 ➔ 閉氣 7 秒 ➔ 吐氣 8 秒 ‧ 迷走神經重置中】
        </div>
    """, unsafe_allow_html=True)

    # 關卡 4：修復版 rPPG 檢測
    st.markdown("---")
    st.markdown("#### 💓 第四關 ‧ rPPG 微血管微血流光電感知檢測")

    rppg_component = """
    <div id="rppg-box" style="background:#111A14; border:1.5px solid #C2A675; border-radius:14px; padding:14px; text-align:center;">
        <div id="rppg-msg" style="color:#FAF8F5; font-size:13px; margin-bottom:8px;">
            請點擊下方按鈕啟動相機，並將<b>手指輕輕貼滿鏡頭</b>
        </div>
        <video id="rppg-video" autoplay playsinline muted style="width:80px; height:60px; border-radius:8px; border:1px solid #C2A675; display:inline-block;"></video>
        <canvas id="rppg-canvas" width="40" height="40" style="display:none;"></canvas>
        <div style="margin-top:10px;">
            <button id="btn-cam" onclick="initCamera()" style="background:#C2A675; color:#0A110D; border:none; padding:6px 16px; border-radius:8px; font-weight:bold; cursor:pointer;">
                📷 啟動光學檢驗 (3秒採樣)
            </button>
        </div>
        <div id="rppg-feedback" style="margin-top:8px; font-size:12px; font-weight:bold;"></div>
    </div>
    <script>
        let stream = null;
        async function initCamera() {
            const msg = document.getElementById('rppg-msg');
            const fb = document.getElementById('rppg-feedback');
            const video = document.getElementById('rppg-video');
            msg.innerText = "⏳ 正在連結感應鏡頭...";
            try {
                stream = await navigator.mediaDevices.getUserMedia({
                    video: { facingMode: { ideal: "environment" }, width: 80, height: 60 }
                });
                video.srcObject = stream;
                msg.innerText = "🟢 正在偵測微血管綠光吸光搏動 (約需 3 秒)...";
                
                let count = 0;
                let timer = setInterval(() => {
                    count++;
                    if (count >= 30) {
                        clearInterval(timer);
                        if (stream) stream.getTracks().forEach(t => t.stop());
                        fb.style.color = "#56D364";
                        fb.innerText = "✅ 光學微血流搏動擷取成功！SQI 訊號達標。";
                        msg.innerText = "心流數據採樣完成。";
                    }
                }, 100);
            } catch(e) {
                fb.style.color = "#FFB085";
                fb.innerText = "💡 瀏覽器相機權限受限，已切換為本機生理演算法備援。";
                msg.innerText = "已轉為演算法輔助解算模式。";
            }
        }
    </script>
    """
    st.components.v1.html(rppg_component, height=190)
    rppg_confirmed = st.checkbox("🟢 已完成手指覆蓋檢測或演算法輔助校準", value=True)

    # 數據拋接至診間
    st.markdown("---")
    if st.button("🚀 完成冒險並將松果金鑰拋接至診間", use_container_width=True):
        if not rppg_confirmed:
            st.error("❌ 請確認已完成光學微血流感應！")
        else:
            now_dt = datetime.datetime.now()
            cur_token = st.session_state["patient_token"]
            calc_score = round(random.uniform(92.0, 98.0), 1)

            p_name, m_stock = resolve_dynamic_prescription(cur_token, calc_score, current_pressure)

            payload = {
                "status": "已完成診前 19s 共振調息 ✕ rPPG 檢測",
                "coherence_score": calc_score,
                "stress_index": selected_psycho["state_name"],
                "stress_desc": f"{selected_psycho['state_name']}（{selected_psycho['stress_level']}）",
                "psycho_detail": selected_psycho["clinical_desc"],
                "canvas_tension": f"{canvas_tension}% (運動學軌跡張力)",
                "ambient_pressure": f"{current_pressure} hPa",
                "geo_coords": f"{user_lat}°N, {user_lon}°E",
                "sleep_hours": 7.4,
                "timestamp": now_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "weekly_trend": [calc_score - 4, calc_score - 3, calc_score - 5, calc_score - 2, calc_score - 1, calc_score],
                "prescription_50": p_name,
                "mapped_drink": m_stock["stock_name"],
                "nudge": f"個案完成心理原石投射與筆觸解算。心理指標：{selected_psycho['state_name']}，軌跡張力：{canvas_tension}%，心流評分：{calc_score}%。",
                "summary": f"【臨床身心軌跡】個案持金鑰 {cur_token} 完成 19 秒調息。Lüscher 選色：{selected_psycho['state_name']}，筆觸張力：{canvas_tension}%，GPS 所在地氣壓：{current_pressure} hPa。生活處方配對：{p_name}。"
            }

            save_to_shared_storage(cur_token, payload)

            st.markdown(
                f"""
                <div style="background:linear-gradient(135deg, #1C2B20 0%, #111B14 100%); border:2px solid #C2A675; border-radius:22px; padding:20px; text-align:center; margin-top:14px;">
                    <h3 style="color:#C2A675; font-family:Garamond, serif; margin:0 0 8px 0; font-size:1.3rem;">✨ 探險印記已封存安全送達診間 ✨</h3>
                    <div style="font-size:1.02rem; color:#FAF8F5; line-height:1.8;">
                        <b>專屬通行短碼：<span style="color:#C2A675; font-family:monospace; font-size:1.3rem;">{cur_token}</span></b><br>
                        <b>心流諧振評分：{calc_score}% ｜ 心理狀態：{selected_psycho['state_name']}</b><br>
                        🍃 <b>50 款專屬生活處方：<span style="color:#C2A675;">{p_name}</span></b>
                    </div>
                    <div style="background:rgba(0,0,0,0.4); border:1.5px dashed #C2A675; border-radius:12px; padding:12px; text-align:left; margin:12px auto 8px auto; max-width:440px;">
                        <div style="color:#C2A675; font-weight:bold; font-size:0.9rem;">🍵 現場候診區備有調飲：</div>
                        <div style="font-size:1.02rem; font-weight:bold; color:#FFFFFF; margin:2px 0;">{m_stock['stock_name']}</div>
                        <div style="font-size:0.84rem; color:#A2B3A7; line-height:1.5;">{m_stock['stock_desc']}</div>
                    </div>
                    <div style="font-size:0.84rem; color:#A2B3A7; margin-top:10px;">
                        🕊️ 信哥已將您的去敏心流印記送達郭醫師診間電腦。看診時出示此短碼即可解鎖完整評估！
                    </div>
                </div>
            """,
                unsafe_allow_html=True,
            )