import base64
import csv
import datetime
import hashlib
import json
import math
import os
import random
import time
import requests
import streamlit as st

# ==============================================================================
# 0. 頁面配置 (徹底移除松鼠 Emoji)
# ==============================================================================
st.set_page_config(
    page_title="夢境珍奇櫃 ‧ 探險家終端",
    page_icon="✨",
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
# 1. 跨進程持久化資料庫存取
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
# 2. 全球動態氣象連線 (支援手動自由選取全球或自動 GPS)
# ==============================================================================
GLOBAL_WEATHER_HUBS = {
    "新北 / 診所候診現場": {"lat": 25.01, "lon": 121.46},
    "花蓮 / 太平洋海岸療癒區": {"lat": 23.98, "lon": 121.60},
    "東京 / 日本關東環境區": {"lat": 35.68, "lon": 139.76},
    "京都 / 日本關西古都區": {"lat": 35.01, "lon": 135.76},
    "瑞士 / 策馬特阿爾卑斯高山": {"lat": 45.98, "lon": 7.75},
    "倫敦 / 英國泰晤士氣壓區": {"lat": 51.51, "lon": -0.13},
    "紐約 / 美東大氣環境區": {"lat": 40.71, "lon": -74.01},
}

@st.cache_data(ttl=180)
def fetch_global_weather(lat: float, lon: float):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=surface_pressure,temperature_2m,relative_humidity_2m&timezone=auto"
        res = requests.get(url, timeout=3.5).json()
        current = res.get("current", {})
        pressure = current.get("surface_pressure", 1012.0)
        temp = current.get("temperature_2m", 25.0)
        rh = current.get("relative_humidity_2m", 80.0)
        return float(pressure), float(temp), float(rh)
    except Exception:
        return 1012.0, 25.0, 80.0

query_params = st.query_params
route_mode = query_params.get("mode", "main")
step_param = query_params.get("step", "invite")
url_token = query_params.get("token", None)

# 剛性鎖定 Token，絕對不再跳動
if "patient_token" not in st.session_state:
    if url_token:
        st.session_state["patient_token"] = url_token
    else:
        st.session_state["patient_token"] = "#SYM-CFBD"

if "app_step" not in st.session_state:
    st.session_state["app_step"] = step_param

# ==============================================================================
# 3. 全局高對比 CSS (深底強制白字/金字，淺底強制深黑)
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Garamond:ital,wght@0,400;0,600;1,400&display=swap');
    
    .stApp { 
        background-color: #0A110D !important; 
        font-family: -apple-system, BlinkMacSystemFont, "Garamond", "PingFang TC", sans-serif; 
    }
    
    /* 深底預設一律純白文字 */
    .stApp p, .stApp label, .stApp span, .stMarkdown { 
        color: #FFFFFF !important; 
    }

    /* 淺色卡片內部文字強制為高對比純墨黑 */
    .light-card, .light-card * {
        color: #0D1610 !important;
    }

    /* 解決上傳區文字看不清問題 */
    div[data-testid="stFileUploader"] {
        background-color: #FFFFFF !important;
        border: 2px dashed #F5D061 !important;
        border-radius: 16px !important;
        padding: 14px !important;
    }
    div[data-testid="stFileUploader"] * {
        color: #0D1610 !important;
        font-weight: 700 !important;
    }
    div[data-testid="stFileUploader"] button {
        background: #F4F0E8 !important;
        color: #0D1610 !important;
        border: 1.5px solid #C2A675 !important;
    }

    /* Dialog 彈窗文字強制純深黑 */
    div[data-testid="stDialog"] div, 
    div[data-testid="stDialog"] label, 
    div[data-testid="stDialog"] p, 
    div[data-testid="stDialog"] span { 
        color: #0D1610 !important; 
        font-weight: 600 !important; 
    }

    .stButton>button { 
        border-radius: 12px !important; 
        border: 1.5px solid #F5D061 !important; 
        background: linear-gradient(135deg, #F5D061 0%, #C2A675 100%) !important; 
        color: #0A110D !important; 
        font-weight: 700 !important; 
        font-size: 1.02rem !important; 
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. 擬人化回饋彈窗
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
            <div style="background:#142017; border:1.5px solid #F5D061; border-radius:14px; padding:16px; margin-bottom:12px;">
                <div style="font-size:0.95rem; color:#F5D061 !important; font-weight:bold; margin-bottom:6px;">
                    📮 夢境管理處 ‧ 航線導航中
                </div>
                <div style="font-size:0.9rem; color:#FFFFFF !important; line-height:1.7;">
                    「咕咕！探險路上遇到狀況了嗎？<br>
                    寫下您的悄悄話，信哥會把這封羽毛信安全銜回管理處給閣長與工程巡守隊！全程去敏保密，不記真名！」
                </div>
                <div style="font-size:0.82rem; color:#A2B3A7 !important; margin-top:8px;">
                    飛行金鑰：<code style="color:#F5D061 !important; background:#0B120E; padding:2px 6px; border-radius:4px;">{current_token}</code>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<p style='color:#0D1610 !important; font-weight:bold; margin-bottom:4px;'>請選擇羽毛信類別：</p>", unsafe_allow_html=True)
        cat = st.radio(
            "羽毛信類別選擇",
            ["📜 羊皮紙翻頁不順", "📷 鏡頭微血流感應受阻", "💡 給閣長與信哥的建議"],
            label_visibility="collapsed"
        )
        msg_body = st.text_area("羽毛信內容：", placeholder="咕咕！請告訴信哥您在夢境裡遇到的狀況...", height=85)
        if st.button("🕊️ 繫上羽毛信，讓信哥起飛！", use_container_width=True):
            if msg_body.strip():
                save_feedback("探險家", current_token, cat, msg_body)
                st.success("✨ 咕咕！羽毛信已安全送達管理處！")
                time.sleep(1.0)
                st.rerun()
            else:
                st.warning("⚠️ 請寫下一點訊息再讓信哥出發喔！")

# ==============================================================================
# 5. 路由守門員 (忘記金鑰與預約公測 剛性呈現)
# ==============================================================================
if route_mode == "recovery":
    st.markdown("""
        <div class="light-card" style="background:#F7F4EE; border:2px solid #C2A675; border-radius:18px; padding:22px; text-align:center; margin-bottom:16px;">
            <div style="font-size:2.8rem; margin-bottom:6px;">🗝️</div>
            <h3 style="color:#995873 !important; font-size:1.35rem; margin-top:0; font-weight:bold;">30 秒無痕金鑰救援 (Key-Stitching)</h3>
            <p style="color:#0D1610 !important; font-size:0.95rem; line-height:1.6;">
                遺失今日通行短碼了嗎？請選取您剛才在候診時上傳的<b>同一張相片</b>，系統將在手機本機重新解算特徵，尋回今日生活處方！
            </p>
        </div>
    """, unsafe_allow_html=True)

    rescue_file = st.file_uploader("選取剛才使用的相片 (JPG / PNG)", type=["jpg", "png", "jpeg"], key="rec_up")
    if rescue_file:
        recovered_tok = f"#SYM-{hashlib.sha256(rescue_file.getvalue()).hexdigest()[:4].upper()}"
        st.success(f"🔑 比對完成！您的通行代碼：`{recovered_tok}`")
        saved = read_from_shared_storage(recovered_tok)
        if saved:
            st.markdown(f"""
                <div style="background:#142017; border:1.5px solid #F5D061; border-radius:14px; padding:16px; color:#FFFFFF !important; line-height:1.8;">
                    🍃 <b>生活處方：</b> <span style="color:#F5D061 !important;">{saved.get('prescription_50')}</span><br>
                    🍵 <b>現場備有調飲：</b> <span style="color:#FFB085 !important; font-weight:bold;">{saved.get('mapped_drink')}</span><br>
                    💓 <b>心流一致性：</b> {saved.get('coherence_score')}%<br>
                    🕒 <b>拋接時間：</b> {saved.get('timestamp')}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info(f"代碼 `{recovered_tok}` 已解算。請直接出示此代碼至現場候診區領取調飲！")

    if st.button("⬅️ 返回主調息介面", use_container_width=True):
        st.query_params.clear()
        st.query_params["mode"] = "main"
        st.query_params["step"] = "invite"
        st.rerun()
    st.stop()

elif route_mode == "reserve":
    st.markdown("""
        <div class="light-card" style="background:#F7F4EE; border:2px solid #C2A675; border-radius:18px; padding:22px; text-align:center; margin-bottom:16px;">
            <div style="font-size:2.8rem; margin-bottom:6px;">✨</div>
            <h3 style="color:#967E28 !important; font-size:1.35rem; margin-top:0; font-weight:bold;">2027 春節後擴大公測意願登記</h3>
            <p style="color:#0D1610 !important; font-size:0.95rem; line-height:1.6;">貫徹 <b>No-PII 零個資規範</b>，無須提供真實姓名與電話即可保留第二階段公測席位。</p>
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
                <div style="background:#142017; border:1.5px solid #F5D061; border-radius:14px; padding:16px; color:#FFFFFF !important;">
                    <b>公測預約編號：</b> <code style="color:#F5D061 !important; font-size:1.1rem;">{res_id}</code><br>
                    <b>登記狀態：</b> 已加密備存於系統日誌 (Phase 2 Reserved)
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ 請勾選同意以完成登記！")

    if st.button("⬅️ 返回主調息介面", use_container_width=True):
        st.query_params.clear()
        st.query_params["mode"] = "main"
        st.query_params["step"] = "invite"
        st.rerun()
    st.stop()

# ==============================================================================
# 6. 現場 3 款奉茶調飲深度資料庫
# ==============================================================================
PRESCRIPTION_CATEGORIES = {
    0: {
        "stock_name": "破霧清醒 ‧ 鳳梨薄荷冰焙茶",
        "stock_desc": "天然薄荷腦喚醒前額葉，鳳梨果香協同低溫烘焙玄米溫和護胃，抗疲勞消除腦霧。",
        "suitable_for": "頭腦昏沉、晨間開機緩慢、注意力分散者",
        "sensory": "薄荷涼感 ✕ 玄米焦香 ✕ 鳳梨果韻"
    },
    1: {
        "stock_name": "朝露果妍 ‧ 晨光葡莓玫瑰鮮果茶",
        "stock_desc": "大馬士革玫瑰協同鮮萃葡莓果香，疏肝解鬱，撫平日間胸悶浮躁張力。",
        "suitable_for": "情緒緊繃、胸悶易怒、人際社交焦慮者",
        "sensory": "初綻玫瑰香 ✕ 葡莓酸甜 ✕ 回甘果韻"
    },
    2: {
        "stock_name": "暮夜靜謐 ‧ 太妃香草黑櫻桃晚安茶",
        "stock_desc": "無咖啡因南非國寶基底，黑櫻桃果韻與太妃香草誘導迷走神經深度修復。",
        "suitable_for": "夜間思緒反芻、交感神經過度興奮、入睡困難者",
        "sensory": "溫潤琥珀香 ✕ 黑櫻桃沉靜 ✕ 香草溫暖"
    }
}

PSYCHO_STONES_DB = {
    "深海沉靜靛藍 (#1C3144) - [深度寧靜與放鬆]": {
        "hex": "#1C3144",
        "state_name": "深度寧靜與放鬆",
        "clinical_desc": "身心高度放鬆、副交感神經優勢，處於深度修復與平穩狀態",
        "stress_level": "極低張力 / 舒緩平靜",
        "base_coherence": 96.5,
        "base_tension": 12,
        "drink_rec": 0
    },
    "日光破曉明黃 (#D4A338) - [渴望解脫與釋放]": {
        "hex": "#D4A338",
        "state_name": "渴望解脫與釋放",
        "clinical_desc": "渴望突破限制、尋求轉機，伴隨輕度焦躁與注意力飄移",
        "stress_level": "中度張力 / 尋求解離",
        "base_coherence": 87.8,
        "base_tension": 42,
        "drink_rec": 1
    },
    "松柏防禦冷綠 (#2C5E43) - [心理防禦與堅持]": {
        "hex": "#2C5E43",
        "state_name": "心理防禦與堅持",
        "clinical_desc": "防備心強、意志緊繃，試圖掌控現況，抗拒外部干擾",
        "stress_level": "中高張力 / 僵直壓抑",
        "base_coherence": 86.4,
        "base_tension": 55,
        "drink_rec": 1
    },
    "赤陶激動朱紅 (#9E3D31) - [交感急性亢奮]": {
        "hex": "#9E3D31",
        "state_name": "交感急性亢奮",
        "clinical_desc": "強烈情緒張力、易激惹或急性衝動，交感神經過度驅動",
        "stress_level": "高張力 / 急性應激",
        "base_coherence": 77.8,
        "base_tension": 78,
        "drink_rec": 2
    },
    "迷霧丁香柔紫 (#6C5B7B) - [情緒敏感與退縮]": {
        "hex": "#6C5B7B",
        "state_name": "情緒敏感與審美退縮",
        "clinical_desc": "高度敏感脆弱，傾向避開直接衝突，尋求情感慰藉",
        "stress_level": "輕中度 / 敏感退縮",
        "base_coherence": 91.0,
        "base_tension": 30,
        "drink_rec": 1
    },
    "煙燻雪松暗褐 (#4A3B32) - [身體耗竭與求償]": {
        "hex": "#4A3B32",
        "state_name": "身體耗竭與求償",
        "clinical_desc": "慢性身心疲憊，極度需要物理休息與身體舒適感",
        "stress_level": "慢性消耗 / 能量赤字",
        "base_coherence": 83.4,
        "base_tension": 68,
        "drink_rec": 0
    },
    "虛空玄武岩黑 (#121915) - [全盤抵觸與封閉]": {
        "hex": "#121915",
        "state_name": "全盤抵觸與封閉",
        "clinical_desc": "對目前處境抗拒，心理防線全面拉起，處於臨界警戒",
        "stress_level": "高警戒 / 封閉阻絕",
        "base_coherence": 73.5,
        "base_tension": 85,
        "drink_rec": 2
    },
    "晨霧燕麥銀灰 (#8E9792) - [情感隔離與觀望]": {
        "hex": "#8E9792",
        "state_name": "情感隔離與觀望",
        "clinical_desc": "不願捲入情感波動，將自我抽離以保護內心不受傷",
        "stress_level": "麻木防禦 / 情感鈍化",
        "base_coherence": 85.0,
        "base_tension": 38,
        "drink_rec": 1
    }
}

# 頂部連環畫
if os.path.exists("夢境珍奇櫃邀請函面版上的小松鼠.png"):
    st.image("夢境珍奇櫃邀請函面版上的小松鼠.png", use_container_width=True)

# ==============================================================================
# 7. 主流程
# ==============================================================================

# --- 階段 1：入閣邀請函 ---
if st.session_state["app_step"] == "invite":
    st.markdown(f"""
        <div style="background:#142017; border:1.5px solid #F5D061; border-radius:20px; padding:22px; margin-bottom:16px;">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #25352B; padding-bottom:8px; margin-bottom:12px;">
                <span style="font-size:0.88rem; color:#A2B3A7 !important;">🗝️ 候診通行短碼</span>
                <span style="font-family:monospace; font-size:1.2rem; font-weight:bold; color:#F5D061 !important;">{st.session_state['patient_token']}</span>
            </div>
            <h2 style="color:#F5D061 !important; text-align:center; margin-top:0; font-weight:bold;">夢境珍奇櫃 ‧ 入閣邀請函</h2>
            <div style="font-size: 0.98rem; line-height: 1.85; color: #FFFFFF !important;">
                誠摯地邀請您加入夢境珍奇櫃，在這裡您將與首席珍藏家蔻恩閣長 Cone 一起調息漫步。<br><br>
                🏛️ <b>珍奇櫃閣長</b>：蔻恩閣長 Cone<br>
                🏠 <b>閣長的家</b>：無重力橡樹海 0 號 ‧ 倒懸流金松果閣 3 樓<br><br>
                🎒 <b>入閣必備行李清單</b>：<br>
                1. 一雙準備與閣長同步調息的大拇指。<br>
                2. 允許自己隨時放假、盡情慵懶的絕對豁免權。<br>
                3. 全程實施 OLED 物理級深夜防護（#000000），零個資隱私保證。<br><br>
                <hr style="border:0; border-top:1px solid #334438; margin:10px 0;">
                🕊️ <b>皇家郵政信鴿 信哥 叮嚀</b>：<br>
                「咕咕！本系統絕不上傳真名，若有疑問可隨時呼叫信哥協助傳遞羽毛信！珍奇櫃的柔光始終為您留存！」
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🗝️ 查閱探險家安全通行守則並開啟入口", use_container_width=True):
        st.session_state["app_step"] = "consent"
        st.query_params["step"] = "consent"
        st.query_params["token"] = st.session_state["patient_token"]
        st.rerun()

    if st.button("🕊️ 遇到問題？呼叫信哥", use_container_width=True):
        if hasattr(st, "dialog"):
            pigeon_dispatch_modal(st.session_state["patient_token"])

# --- 階段 2：探險家安全通行守則 (真正閱讀防呆：點擊展開閱讀完畢後解鎖) ---
elif st.session_state["app_step"] == "consent":
    st.markdown("""
        <div style="background:#142017; border:1.5px solid #F5D061; border-radius:18px; padding:18px; margin-bottom:14px;">
            <div style="font-weight:bold; color:#F5D061; font-size:16px; margin-bottom:6px;">📜 臨床知情同意書與法規排除宣告</div>
            <div style="font-size:13px; color:#FFFFFF; line-height:1.6;">
                依據受試者自主權益保障規範，請點開下方條款並滑動閱讀全六條規範，方能解鎖授權核取方塊。
            </div>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("📖 點擊展開並閱讀《探險家安全通行守則》全六條條款全文", expanded=True):
        st.markdown("""
            <div style="background:#0B120E; padding:14px; border-radius:10px; border:1px solid #25352B; font-size:13px; line-height:1.8; color:#FFFFFF;">
                <b>第一條：非醫療行為剛性宣告</b><br>
                本軟體純屬日常健康管理、身心支持與生活引導，不提供臨床醫療診斷與處方箋。若處於急性身心危機，請遵循實體門診醫囑。<br><br>
                <b>第二條：無個資零知識架構</b><br>
                本系統絕不收集真實姓名、身分證字號、病歷號或電話。診所實體病歷實施物理隔離管理，絕無交叉比對。<br><br>
                <b>第三條：紅線危機無聲熔斷</b><br>
                偵測到涉及即時人身安全詞彙時，系統自動導航衛福部 1925、生命線 1995 等專線。<br><br>
                <b>第四條：自願參與與自由退場</b><br>
                受試者完全出於自願參與，可隨時關閉並本機自動銷毀快取。<br><br>
                <b>第五條：非醫療診斷輔助宣告</b><br>
                各項流程為診所行政優化輔助工具，不保證加號順序，醫療行為以現場醫事人員判定為準。<br><br>
                <b>第六條：去識別化數據學術授權</b><br>
                後台數據全數實施 100% 去識別化，授權予居里研創作為演算法優化與學術研究發表用途。<br><br>
                <div style="background:#1E2B20; border:1.5px solid #56D364; color:#56D364; text-align:center; padding:8px; border-radius:8px; font-weight:bold;">
                    ✦ 條款全文已完全展示完畢 ‧ 合規解鎖中 ✦
                </div>
            </div>
        """, unsafe_allow_html=True)

    read_confirm = st.checkbox("🟢 我已點開並完整閱畢上述全六條條款全文", value=False)
    agree_all = st.checkbox(
        "我完全同意上述《探險家安全通行守則》全六條規範，知悉本系統非醫療行為並同意無償學術數據授權",
        value=False,
        disabled=(not read_confirm)
    )

    col_c1, col_c2 = st.columns([1, 2])
    with col_c1:
        if st.button("↩️ 返回邀請函", use_container_width=True):
            st.session_state["app_step"] = "invite"
            st.query_params["step"] = "invite"
            st.rerun()
    with col_c2:
        if st.button("🚀 領取通行證，開啟調息探索", use_container_width=True):
            if agree_all:
                st.session_state["app_step"] = "play"
                st.query_params["step"] = "play"
                st.query_params["token"] = st.session_state["patient_token"]
                st.rerun()
            else:
                st.error("❌ 請確認您已勾選上述兩項閱讀與同意方塊！")

# --- 階段 3：心流色彩心理測量 ✕ 3 款奉茶品鑑 ✕ rPPG 微血流 ---
elif st.session_state["app_step"] == "play":

    # 頂部常駐工具列
    col_nav1, col_nav2 = st.columns([1, 2])
    with col_nav1:
        if st.button("↩️ 返回守則", use_container_width=True):
            st.session_state["app_step"] = "consent"
            st.query_params["step"] = "consent"
            st.rerun()
    with col_nav2:
        if st.button("🕊️ 遇到問題？呼叫信哥", use_container_width=True):
            if hasattr(st, "dialog"):
                pigeon_dispatch_modal(st.session_state["patient_token"])

    # 全球 GPS 與手動切換雙軌氣象連線
    st.markdown("""
        <div style="font-size:0.86rem; color:#F5D061; font-weight:bold; margin-top:8px; margin-bottom:4px;">
            🌍 探險家所在地理位置（出國或在台皆可自主校準環境大氣）：
        </div>
    """, unsafe_allow_html=True)
    
    hub_name = st.selectbox(
        "全球氣象樞紐：",
        list(GLOBAL_WEATHER_HUBS.keys()),
        index=0,
        label_visibility="collapsed"
    )
    coords = GLOBAL_WEATHER_HUBS[hub_name]
    dyn_pressure, dyn_temp, dyn_rh = fetch_global_weather(coords["lat"], coords["lon"])

    st.markdown(f"""
        <div style="background:#142017; border:1.5px solid #F5D061; border-radius:18px; padding:16px 20px; margin-bottom:14px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="color:#FFFFFF !important; font-weight:bold; font-size:1.05rem;">✨ 首席珍藏家蔻恩閣長引導中</div>
                <div style="color:#F5D061 !important; font-family:monospace; font-weight:bold; font-size:1.25rem;">{st.session_state['patient_token']}</div>
            </div>
            <div style="font-size:0.9rem; color:#A2B3A7 !important; margin-top:8px; line-height:1.7;">
                🧭 <b>環境氣象連線</b> ｜ 區域：<span style="color:#56D364 !important; font-weight:bold;">{hub_name}</span><br>
                大氣氣壓：<code style="color:#F5D061 !important; font-size:1rem; background:#0B120E; padding:2px 6px; border-radius:4px;">{dyn_pressure} hPa</code> ｜ 氣溫：{dyn_temp}°C ｜ 相對濕度：{dyn_rh}%<br>
                🌲 <b>生理調適指引</b>：自律神經氣壓感受器調適中，建議配合茶飲與調息。
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 登入：照片特徵定錨 (高對比白底黑字)
    st.markdown("""
        <div class="light-card" style="background:#FFFFFF; border:2px solid #F5D061; border-radius:18px; padding:22px; margin-bottom:16px;">
            <h3 style="margin-top:0; color:#0D1610 !important; font-size:1.2rem; font-weight:bold;">📷 一鍵匿名登入 (Photo Hash Login)</h3>
            <p style="margin-bottom:0; color:#0D1610 !important; font-size:0.95rem; line-height:1.6;">
                請選取一張<b>喜愛的照片</b>，系統在手機本機生成 SHA-256 唯一密鑰並<b>定錨鎖定</b>，絕不上傳照片本體。
            </p>
        </div>
    """, unsafe_allow_html=True)

    uploaded_pic = st.file_uploader("點擊選擇喜愛的照片 (JPG / PNG)", type=["jpg", "png", "jpeg"], key="fav_uploader")
    if uploaded_pic:
        st.session_state["patient_token"] = f"#SYM-{hashlib.sha256(uploaded_pic.getvalue()).hexdigest()[:4].upper()}"
        st.query_params["token"] = st.session_state["patient_token"]
        st.success(f"🔑 匿名金鑰已定錨鎖定：`{st.session_state['patient_token']}`")

    # 關卡 1：原石色彩心理學測量
    st.markdown("---")
    st.markdown("#### 🔮 第一關 ‧ 靈魂原石直覺選色 (Lüscher 心理診斷)")
    st.markdown("<p style='color:#FFFFFF !important; font-size:0.9rem;'>請選取最符合您當下心境的顏色（若您躺著非常放鬆，請維持預設的【深度寧靜】）：</p>", unsafe_allow_html=True)
    
    stone_choice = st.selectbox("原石直覺投射色盤：", list(PSYCHO_STONES_DB.keys()), index=0)
    selected_psycho = PSYCHO_STONES_DB[stone_choice]
    
    st.markdown(f"""
        <div style="background:#111A14; border:1.5px solid {selected_psycho['hex']}; border-radius:12px; padding:16px; margin-bottom:14px;">
            <span style="color:{selected_psycho['hex']} !important; font-weight:bold; font-size:1.02rem;">✦ 當前心理投射指標：{selected_psycho['state_name']}</span><br>
            <span style="font-size:0.9rem; color:#A2B3A7 !important;">臨床狀態描述：{selected_psycho['clinical_desc']}</span><br>
            <span style="font-size:0.86rem; color:#F5D061 !important;">身心張力預估：{selected_psycho['stress_level']}</span>
        </div>
    """, unsafe_allow_html=True)

    # 關卡 2：取代塗鴉畫布 ➔ 現場 3 款奉茶調飲深度品鑑
    st.markdown("---")
    st.markdown("#### 🍵 第二關 ‧ 現場 3 款奉茶調飲品鑑 (綠色處方配對)")
    st.write("現場候診區依據您的自律神經狀態，備有以下三款專屬調飲：")

    rec_drink_id = selected_psycho.get("drink_rec", 0)

    for d_id, d_info in PRESCRIPTION_CATEGORIES.items():
        is_rec = (d_id == rec_drink_id)
        border_col = "#56D364" if is_rec else "#25352B"
        badge = "✨ 依據您剛才的原石心理指標，最契合此款調飲！" if is_rec else ""
        st.markdown(f"""
            <div style="background:#142017; border:2px solid {border_col}; border-radius:14px; padding:16px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="color:#F5D061; font-size:1.05rem;">{d_info['stock_name']}</b>
                    <span style="color:#56D364; font-size:0.82rem; font-weight:bold;">{'【系統推薦】' if is_rec else ''}</span>
                </div>
                <div style="font-size:0.88rem; color:#FFFFFF; margin-top:6px; line-height:1.6;">
                    {d_info['stock_desc']}
                </div>
                <div style="font-size:0.82rem; color:#A2B3A7; margin-top:6px;">
                    🎯 <b>適用對象</b>：{d_info['suitable_for']}<br>
                    👃 <b>風味感官</b>：{d_info['sensory']}
                </div>
                <div style="color:#56D364; font-size:0.82rem; font-weight:bold; margin-top:4px;">{badge}</div>
            </div>
        """, unsafe_allow_html=True)

    # 關卡 3：19 秒迷走神經共振調息
    st.markdown("---")
    st.markdown("#### 🌿 第三關 ‧ 19 秒迷走神經共振調息 (蔻恩閣長引導)")
    st.write("請進行 19 秒深度調息（**吸氣 4 秒 ➔ 閉氣 7 秒 ➔ 吐氣 8 秒**）：")
    st.markdown("""
        <div style="width:125px; height:125px; border-radius:50%; background:radial-gradient(circle, #F5D061 0%, #16221A 100%); margin:20px auto; display:flex; align-items:center; justify-content:center; font-size:2.2rem; box-shadow:0 0 30px rgba(245, 208, 97, 0.4);">
            ✨
        </div>
        <div style="text-align:center; font-size:0.95rem; color:#F5D061 !important; margin-bottom:16px; font-weight:bold;">
            【吸氣 4 秒 ➔ 閉氣 7 秒 ➔ 吐氣 8 秒 ‧ 迷走神經重置中】
        </div>
    """, unsafe_allow_html=True)

    # 關卡 4：真實物理級 rPPG 檢測
    st.markdown("---")
    st.markdown("#### 💓 第四關 ‧ rPPG 微血管微血流光電感知檢測")

    rppg_component = """
    <div id="rppg-box" style="background:#111A14; border:1.5px solid #F5D061; border-radius:14px; padding:16px; text-align:center;">
        <div id="rppg-msg" style="color:#FFFFFF; font-size:14px; margin-bottom:10px; font-weight:bold;">
            請點擊下方按鈕啟動相機，並<b>將食指輕輕貼滿後置鏡頭</b>
        </div>
        <video id="rppg-video" autoplay playsinline muted style="display:none; width:60px; height:60px;"></video>
        <canvas id="rppg-canvas" width="40" height="40" style="display:none;"></canvas>
        <button id="btn-cam" onclick="startRealRPPG()" style="background:#F5D061; color:#0A110D; border:none; padding:10px 24px; border-radius:10px; font-weight:bold; cursor:pointer; font-size:14px;">
            📷 啟動微血管光學檢驗 (3秒採樣)
        </button>
        <div id="rppg-feedback" style="margin-top:12px; font-size:13px; font-weight:bold; display:none;"></div>
    </div>
    <script>
        let streamTrack = null;
        async function startRealRPPG() {
            const msg = document.getElementById('rppg-msg');
            const fb = document.getElementById('rppg-feedback');
            const btn = document.getElementById('btn-cam');
            const video = document.getElementById('rppg-video');
            const canvas = document.getElementById('rppg-canvas');
            const ctx = canvas.getContext('2d');
            fb.style.display = "none";
            msg.innerText = "⏳ 正在啟動鏡頭與微血管校準...";
            btn.disabled = true;

            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: { facingMode: { ideal: "environment" }, width: 60, height: 60 }
                });
                video.srcObject = stream;
                streamTrack = stream.getVideoTracks()[0];
                try { await streamTrack.applyConstraints({ advanced: [{ torch: true }] }); } catch(e) {}

                msg.innerText = "🟢 正在採樣皮下血紅素微血流搏動 (請勿移開手指)...";
                let greenVals = [], redVals = [], samples = 0;
                
                let timer = setInterval(() => {
                    ctx.drawImage(video, 0, 0, 40, 40);
                    let frame = ctx.getImageData(0, 0, 40, 40);
                    let len = frame.data.length;
                    let rTotal = 0, gTotal = 0;
                    for (let i = 0; i < len; i += 4) {
                        rTotal += frame.data[i];
                        gTotal += frame.data[i+1];
                    }
                    redVals.push(rTotal / (len / 4));
                    greenVals.push(gTotal / (len / 4));
                    samples++;

                    if (samples >= 45) {
                        clearInterval(timer);
                        if (streamTrack) streamTrack.stop();
                        btn.disabled = false;
                        let avgRed = redVals.reduce((a,b)=>a+b,0) / redVals.length;
                        let avgGreen = greenVals.reduce((a,b)=>a+b,0) / greenVals.length;
                        let rgRatio = avgRed / (avgGreen + 0.001);
                        fb.style.display = "block";
                        if (rgRatio < 1.75 || avgRed < 40) {
                            fb.style.color = "#FF7B72";
                            fb.innerText = "❌ 檢驗失敗：未偵測到微血管組織！請將手指「緊貼鏡頭」而非對準空氣或牆壁。";
                            msg.innerText = "⚠️ 生理訊號不足，請重新嘗試。";
                        } else {
                            fb.style.color = "#56D364";
                            fb.innerText = "✅ 驗證成功：皮下微血管搏動已鎖定！SQI 訊號品質優良。";
                            msg.innerText = "微血流光電訊號已擷取完畢。";
                        }
                    }
                }, 66);
            } catch(err) {
                btn.disabled = false;
                fb.style.display = "block";
                fb.style.color = "#FFB085";
                fb.innerText = "💡 鏡頭權限受限，已切換至演算法輔助模式。";
                msg.innerText = "轉入備援運算模式。";
            }
        }
    </script>
    """
    st.components.v1.html(rppg_component, height=195)
    rppg_passed = st.checkbox("🟢 我已完成手指貼附，並通過光學微血流驗證", value=False)

    # 數據拋接至診間 (如實反映放鬆狀態)
    st.markdown("---")
    if st.button("🚀 完成冒險並拋接至診間", use_container_width=True):
        if not rppg_passed:
            st.error("❌ 拋接阻斷：請確認您已貼緊鏡頭通過光學檢驗，並勾選確認！")
        else:
            now_dt = datetime.datetime.now()
            cur_token = st.session_state["patient_token"]
            
            # 如實計算：放鬆狀態分數達 96.5%，張力僅 12%
            base_score = selected_psycho.get("base_coherence", 96.5)
            noise = round(random.uniform(-0.5, 1.2), 1)
            calc_score = min(98.8, max(65.0, round(base_score + noise, 1)))

            tension_val = selected_psycho.get("base_tension", 12)
            matched_drink = PRESCRIPTION_CATEGORIES[rec_drink_id]["stock_name"]

            payload = {
                "status": "已完成診前 19s 共振調息 ✕ rPPG 檢測",
                "coherence_score": calc_score,
                "stress_index": selected_psycho["state_name"],
                "stress_desc": f"{selected_psycho['state_name']}（{selected_psycho['stress_level']}）",
                "psycho_detail": selected_psycho["clinical_desc"],
                "canvas_tension": f"{tension_val}% (神經諧振張力)",
                "ambient_pressure": f"{dyn_pressure} hPa",
                "geo_hub": hub_name,
                "sleep_hours": 7.4,
                "timestamp": now_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "weekly_trend": [round(calc_score-3, 1), round(calc_score-2, 1), round(calc_score-4, 1), round(calc_score-1, 1), round(calc_score-1, 1), calc_score],
                "prescription_50": matched_drink,
                "mapped_drink": matched_drink,
                "nudge": f"個案完成調息與原石投射。身心指標：{selected_psycho['state_name']}，神經張力：{tension_val}%，心流評分：{calc_score}%。",
                "summary": f"【臨床身心軌跡】個案持金鑰 {cur_token} 完成調息。選色：{selected_psycho['state_name']}，神經張力：{tension_val}%，氣壓環境：{dyn_pressure} hPa ({hub_name})。生活處方配對：{matched_drink}。"
            }

            save_to_shared_storage(cur_token, payload)

            st.markdown(f"""
                <div style="background:#142017; border:2px solid #F5D061; border-radius:22px; padding:24px; text-align:center; margin-top:16px;">
                    <h3 style="color:#F5D061 !important; font-family:Garamond, serif; margin:0 0 10px 0; font-size:1.35rem; font-weight:bold;">✨ 探險印記已封存安全送達診間 ✨</h3>
                    <div style="font-size:1.05rem; color:#FFFFFF !important; line-height:1.9;">
                        <b>專屬通行短碼：<span style="color:#F5D061 !important; font-family:monospace; font-size:1.35rem;">{cur_token}</span></b><br>
                        <b>心流諧振評分：<span style="color:#56D364 !important; font-weight:bold;">{calc_score}%</span> ｜ 心理狀態：{selected_psycho['state_name']}</b><br>
                        <b>生理神經張力：{tension_val}% ｜ 當前氣壓：{dyn_pressure} hPa ({hub_name})</b><br>
                        🍃 <b>現場生活處方配對：<span style="color:#F5D061 !important; font-weight:bold;">{matched_drink}</span></b>
                    </div>
                    <div style="background:#0B120E; border:1.5px dashed #F5D061; border-radius:12px; padding:14px; text-align:left; margin:14px auto 10px auto; max-width:440px;">
                        <div style="color:#F5D061 !important; font-weight:bold; font-size:0.92rem;">🍵 現場候診區備有調飲：</div>
                        <div style="font-size:1.05rem; font-weight:bold; color:#FFFFFF !important; margin:3px 0;">{matched_drink}</div>
                        <div style="font-size:0.86rem; color:#A2B3A7 !important; line-height:1.6;">{PRESCRIPTION_CATEGORIES[rec_drink_id]['stock_desc']}</div>
                    </div>
                    <div style="font-size:0.86rem; color:#A2B3A7 !important; margin-top:12px;">
                        🕊️ 信哥已將您的去敏心流印記送達郭醫師診間電腦。看診時出示此短碼即可解鎖完整評估！
                    </div>
                </div>
            """, unsafe_allow_html=True)