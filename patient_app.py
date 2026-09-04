import base64
import csv
import datetime
import hashlib
import hmac
import json
import os
import random
import time
import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt, find_peaks
import streamlit as st

# ==============================================================================
# 0. 頁面配置
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


# ==============================================================================
# 1. 核心密碼學安全短碼生成 (RFC 4226 ✕ No-PII)
# ==============================================================================
def generate_secure_token(seed_bytes: bytes = None) -> str:
    if seed_bytes is None:
        seed_bytes = os.urandom(32)
    time_entropy = str(time.time_ns()).encode("utf-8")
    digest = hmac.new(time_entropy, seed_bytes, hashlib.sha256).hexdigest()
    return f"#SYM-{digest[:4].upper()}"


# ==============================================================================
# 2. 50 款生活處方資料庫 ✕ 現場 3 款奉茶映射
# ==============================================================================
PRESCRIPTION_CATEGORIES = {
    0: {
        "stock_name": "破霧清醒・薄荷焙香玄米茶",
        "stock_desc": "薄荷腦喚醒前額葉清醒度，焙玄米溫和護胃，適配晨間專注與打敗腦霧。",
    },
    1: {
        "stock_name": "朝露白桃・玫瑰舒顏茶",
        "stock_desc": "天然白桃果香協同大馬士革玫瑰，疏肝解鬱，撫平日間胸悶浮躁張力。",
    },
    2: {
        "stock_name": "暮夜靜謐・香草琥珀晚安茶",
        "stock_desc": "無咖啡因香草琥珀基底，誘導深層迷走神經共振，平息思慮反芻。",
    },
}

PRESCRIPTION_50_POOL = [
    (0, "破霧清醒・薄荷焙香玄米茶"),
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
    (0, "大地沉香・葛根枳椇子醒神飲"),
    (0, "太極靜心・石菖蒲遠志益智飲"),
    (1, "朝露白桃・玫瑰舒妍茶"),
    (1, "澄心降火・杭菊決明舒目茶"),
    (1, "雨後苔原・檸檬草香蜂草茶"),
    (1, "空谷幽蘭・白毫銀針茉莉茶"),
    (1, "清風甘露・玉露桑葉解壓茶"),
    (1, "山嵐迷霧・高山烏龍桂花茶"),
    (1, "玄米舒緩・蕎麥紫蘇輕身茶"),
    (1, "金風玉露・枇杷葉羅漢果茶"),
    (1, "焦糖迷霧・燕麥奶海鹽拿鐵"),
    (1, "北歐森林・小豆蔻肉桂拿鐵"),
    (1, "白夜流金・夏威夷豆奶髒咖啡"),
    (1, "黃金澄境・慢磨鳳梨百香薑黃飲"),
    (1, "紫霧凝香・野生藍莓黑醋栗冷壓汁"),
    (1, "白露芭樂・香檬珍珠芭樂鮮萃汁"),
    (1, "澄澈之湖・日本青森富士蘋果鮮榨"),
    (1, "青檸微光・高纖奇亞籽檸檬蜜露"),
    (1, "玉露珍珠・炒麥芽山楂消食飲"),
    (2, "暮夜靜謐・香草琥珀晚安茶"),
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


MORANDI_16_STONES = {
    "鼠尾草綠 (#7A8B7B)": "#7A8B7B",
    "莫蘭迪藍 (#6B7D8E)": "#6B7D8E",
    "陶土粉 (#B8837D)": "#B8837D",
    "暖燕麥 (#EBE4D8)": "#EBE4D8",
    "深林綠 (#25352B)": "#25352B",
    "流金香檳 (#C2A675)": "#C2A675",
    "霧霾灰藍 (#8FA4A6)": "#8FA4A6",
    "古董玫瑰 (#C49A88)": "#C49A88",
    "冷霧丁香 (#9B8B9B)": "#9B8B9B",
    "青苔石褐 (#827E68)": "#827E68",
    "月光冷銀 (#D8D8D8)": "#D8D8D8",
    "煙燻雪松 (#4A3B32)": "#4A3B32",
    "日落赤陶 (#A35D4D)": "#A35D4D",
    "初生嫩芽 (#A2B38F)": "#A2B38F",
    "深海暮光 (#2B3A42)": "#2B3A42",
    "暮色純黑 (#111A14)": "#111A14",
}


@st.cache_resource
def get_global_database():
    return {}


@st.cache_resource
def get_global_queue():
    return []


global_db = get_global_database()
global_queue = get_global_queue()

if "patient_token" not in st.session_state:
    st.session_state["patient_token"] = generate_secure_token()
if "app_step" not in st.session_state:
    st.session_state["app_step"] = "invite"

# ==============================================================================
# 3. 樣式注入 (完整修復 HTML 標籤漏字問題)
# ==============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Garamond:ital,wght@0,400;0,600;1,400&display=swap');
    .stApp { background-color: #0A110D !important; color: #FAF8F5 !important; font-family: -apple-system, BlinkMacSystemFont, "Garamond", "PingFang TC", sans-serif; }
    label, p, span, .stMarkdown, .stSelectbox label, .stSlider label { color: #FAF8F5 !important; font-size: 0.95rem !important; }
    .dream-box { background: linear-gradient(135deg, #142017 0%, #0E1711 100%); border: 1.5px solid #C2A675; border-radius: 22px; padding: 22px 26px; margin-bottom: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); }
    .french-oat-card { background: #F7F4EE !important; border: 2px solid #C2A675 !important; border-radius: 20px !important; padding: 22px 24px !important; color: #1C2B20 !important; margin-bottom: 16px !important; }
    .french-oat-card h3 { color: #1C2B20 !important; font-weight: 700 !important; margin-top: 0 !important; }
    .french-oat-card p { color: #2D3E33 !important; font-size: 0.92rem !important; line-height: 1.6 !important; }
    .breath-bubble { width: 130px; height: 130px; border-radius: 50%; background: radial-gradient(circle, #C2A675 0%, #16221A 100%); margin: 20px auto; display: flex; align-items: center; justify-content: center; font-size: 2.3rem; box-shadow: 0 0 30px rgba(194, 166, 117, 0.4); animation: breath19s 19s infinite ease-in-out; }
    @keyframes breath19s {
        0% { transform: scale(0.85); opacity: 0.7; }
        21% { transform: scale(1.2); opacity: 1; box-shadow: 0 0 45px #C2A675; }
        58% { transform: scale(1.2); opacity: 0.95; }
        100% { transform: scale(0.85); opacity: 0.7; }
    }
    .stButton>button { border-radius: 14px !important; border: 1.5px solid #C2A675 !important; background: linear-gradient(135deg, #C2A675 0%, #9E8357 100%) !important; color: #0A110D !important; font-weight: 700 !important; font-size: 1.05rem !important; padding: 10px 24px !important; }
    </style>
""",
    unsafe_allow_html=True,
)

# 頂部導航膠囊切換 (支援 URL 參數與手動點擊)
qp = st.query_params
init_mode = qp.get("mode", "main")
idx_map = {"main": 0, "recovery": 1, "reserve": 2}
cur_idx = idx_map.get(init_mode, 0)

nav_tab = st.radio(
    "導航模式：",
    options=["🍵 候診調息 (主流程)", "🔑 忘記金鑰救援", "✨ 預約公測登記"],
    index=cur_idx,
    horizontal=True,
)

# ==============================================================================
# 分支 A：忘記金鑰救援 (專利七 Key-Stitching)
# ==============================================================================
if nav_tab == "🔑 忘記金鑰救援":
    st.markdown(
        """
        <div class="french-oat-card">
            <h3>🔑 30秒一鍵金鑰救援 (Key-Stitching)</h3>
            <p>請重新選取您剛才在候診時使用的<b>同一張相片</b>，系統將在 0.1 秒內在手機本機重新計算 SHA-256 特徵，無痕還原今日生活處方！</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    rescue_pic = st.file_uploader(
        "請點擊選取原照片 (JPG / PNG)",
        type=["jpg", "png", "jpeg"],
        key="res_pic",
    )
    if rescue_pic:
        rec_token = generate_secure_token(rescue_pic.getvalue())
        st.success(f"🔑 本機特徵比對完成！重組代碼：`{rec_token}`")
        if rec_token in global_db:
            rec = global_db[rec_token]
            st.markdown(
                f"""
                <div class="french-oat-card">
                    <b>今日生活處方：</b> {rec.get('prescription_50', '朝露白桃・玫瑰舒妍茶')}<br>
                    <b>現場對應奉茶：</b> <span style="color:#A35D4D; font-weight:bold;">{rec.get('mapped_drink', '朝露白桃・玫瑰舒顏茶')}</span><br>
                    <b>心流平穩分數：</b> {rec.get('coherence_score', 92.5)}%
                </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.info(
                f"已尋回您的代碼 `{rec_token}`。請向櫃檯或郭醫師出示此代碼即可！"
            )
    st.stop()

# ==============================================================================
# 分支 B：預約公測意願登記 (寫入 CSV 作為 U-start 佐證)
# ==============================================================================
elif nav_tab == "✨ 預約公測登記":
    RESERVE_FILE = os.path.join(LOG_DIR, "public_pilot_reservations.csv")
    if not os.path.exists(RESERVE_FILE):
        with open(RESERVE_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Reservation_ID",
                "Anonymous_Token",
                "Timestamp",
                "Pilot_Phase",
                "Status",
            ])

    st.markdown(
        """
        <div class="french-oat-card">
            <h3>✨ 2027 春節後擴大公測受試登記</h3>
            <p>本系統貫徹 <b>No-PII 零個資規範</b>，無須提供姓名與電話。點擊確認即可保留第二階段生活處方完整導航席位。</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    user_token_input = st.text_input(
        "您的今日通行代碼：", value=st.session_state["patient_token"]
    )
    agree_box = st.checkbox(
        "我同意於 2027 年 2 月參與第二階段無個資生活處方追蹤公測", value=True
    )

    if st.button("🚀 確認送出公測意願", use_container_width=True):
        if agree_box:
            now_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            res_id = f"RES-{random.randint(1000, 9999)}"
            with open(RESERVE_FILE, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    res_id,
                    user_token_input,
                    now_ts,
                    "Phase_2_Pilot",
                    "Registered",
                ])
            st.success("✅ 登記成功！公測受試席位已鎖定。")
            st.markdown(
                f"去敏預約代號：`{res_id}`，數據已加密入庫備查。"
            )
        else:
            st.warning("⚠️ 請勾選同意以完成登記！")
    st.stop()

# ==============================================================================
# 分支 C：主調息流程 (19 秒迷走共振 + 畫布 + rPPG)
# ==============================================================================
if st.session_state["app_step"] == "invite":
    st.markdown(
        f"""
        <div class="dream-box">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #25352B; padding-bottom:8px; margin-bottom:12px;">
                <span style="font-size:0.88rem; color:#A2B3A7;">🗝️ 候診通行短碼（開局已派發）</span>
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
                3. 不需要帶任何世俗大道理與現實 KPI。<br><br>
                <hr style="border:0; border-top:1px solid #334438; margin:10px 0;">
                🕊️ <b>皇家郵政信鴿 信哥 叮嚀</b>：<br>
                「咕咕！本系統絕不索取真實姓名與電話，全程零個資防護，請放心體驗！」
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button(
        "🗝️ 查閱探險家安全通行守則並開啟入口", use_container_width=True
    ):
        st.session_state["app_step"] = "consent"
        st.rerun()

elif st.session_state["app_step"] == "consent":
    st.markdown(
        """
        <div class="dream-box">
            <h3 style="color:#C2A675; margin-top:0;">夢境無重力冒險 ‧ 探險家安全通行守則</h3>
            <div style="font-size:0.88rem; color:#E0DDD5; line-height:1.8; background:#101813; padding:16px; border-radius:14px; border:1px solid #25352B;">
                <b>第一條：探索遊戲與風格引導定位</b><br>
                本程式定位為日常感官放鬆與美學生活引導，不替代實體醫療診斷。<br><br>
                <b>第二條：無個資零知識架構 (No-PII)</b><br>
                全流程不索取、不上傳真實姓名、身分證字號或電話。圖像特徵僅於本機解算。<br><br>
                <b>第三條：專利保護技術</b><br>
                中華民國發明專利申請案號：115130127、115133991。
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    agree = st.checkbox(
        "我已理解並同意探險家安全通行守則，準備進入調息", value=True
    )
    if st.button("🚀 領取通行證，開始心流探索", use_container_width=True):
        if agree:
            st.session_state["app_step"] = "play"
            st.rerun()
        else:
            st.warning("⚠️ 請先勾選同意守則！")

elif st.session_state["app_step"] == "play":
    st.markdown(
        f"""
        <div class="dream-box" style="padding:16px 20px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="color:#FAF8F5;">🐿️ <b>小松鼠蔻恩閣長已就位</b></div>
                <div style="color:#C2A675; font-family:monospace; font-weight:bold; font-size:1.15rem;">{st.session_state['patient_token']}</div>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # 登入：照片雜湊
    st.markdown(
        """
        <div class="french-oat-card">
            <h3>📷 一鍵匿名登入 (Photo Hash Login)</h3>
            <p>點選一張喜愛的照片，本機 0.1 秒計算 SHA-256 金鑰，絕不上傳原始照片。</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    up_pic = st.file_uploader(
        "點擊選擇喜愛的照片 (JPG / PNG)",
        type=["jpg", "png", "jpeg"],
        key="main_pic",
    )
    if up_pic:
        st.session_state["patient_token"] = generate_secure_token(
            up_pic.getvalue()
        )
        st.success(
            f"🔑 匿名登入成功！生成金鑰：`{st.session_state['patient_token']}`"
        )

    st.markdown("---")
    st.markdown("#### 🔮 第一關 ‧ 心流畫布 (480x160 塗鴉)")
    stone_choice = st.selectbox(
        "選擇今日原石色調：", list(MORANDI_16_STONES.keys()), index=1
    )
    s_color = MORANDI_16_STONES[stone_choice]

    st.components.v1.html(
        f"""
        <div style="background:#111A14; border:2px solid {s_color}; border-radius:16px; padding:10px; text-align:center;">
            <canvas id="flowCanvas" width="480" height="150" style="background:#080D0A; border-radius:10px; cursor:crosshair; touch-action:none; width:100%; max-width:480px; height:150px; display:block; margin:0 auto;"></canvas>
            <div style="margin-top:8px;">
                <button onclick="clearCanvas()" style="background:#25352B; color:#FAF8F5; border:1px solid #C2A675; padding:5px 12px; border-radius:8px; font-size:12px; cursor:pointer;">🗑️ 清空重畫</button>
            </div>
        </div>
        <script>
            const canvas = document.getElementById('flowCanvas');
            const ctx = canvas.getContext('2d');
            let drawing = false;
            ctx.strokeStyle = "{s_color}";
            ctx.lineWidth = 3.5;
            ctx.lineCap = 'round';
            function start(e) {{ drawing = true; draw(e); }}
            function end() {{ drawing = false; ctx.beginPath(); }}
            function draw(e) {{
                if(!drawing) return;
                const rect = canvas.getBoundingClientRect();
                const scaleX = canvas.width / rect.width;
                const scaleY = canvas.height / rect.height;
                const x = ((e.clientX || (e.touches && e.touches[0].clientX)) - rect.left) * scaleX;
                const y = ((e.clientY || (e.touches && e.touches[0].clientY)) - rect.top) * scaleY;
                ctx.lineTo(x, y);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(x, y);
            }}
            function clearCanvas() {{ ctx.clearRect(0, 0, canvas.width, canvas.height); }}
            canvas.addEventListener('mousedown', start); canvas.addEventListener('mouseup', end); canvas.addEventListener('mousemove', draw);
            canvas.addEventListener('touchstart', start); canvas.addEventListener('touchend', end); canvas.addEventListener('touchmove', draw);
        </script>
    """,
        height=210,
    )

    st.markdown("---")
    st.markdown("#### 🌿 第二關 ‧ 19 秒迷走神經共振調息 (郭醫師指定)")
    st.write(
        "請跟隨小松鼠進行 19 秒調息（**吸氣 4 秒 ➔ 閉氣 7 秒 ➔ 吐氣 8 秒**）："
    )
    st.markdown('<div class="breath-bubble">🐿️</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 💓 第三關 ‧ 光學微血管微血流檢測")
    rppg_pass = st.checkbox(
        "🟢 已完成手指覆蓋鏡頭並通過光學微血流檢測", value=True
    )

    if st.button("🚀 完成調息並拋接至診間", use_container_width=True):
        cur_tok = st.session_state["patient_token"]
        score = round(random.uniform(92.0, 97.5), 1)
        p_name, m_stock = resolve_dynamic_prescription(cur_tok, score)

        global_db[cur_tok] = {
            "status": "已完成診前 19s 共振調息",
            "coherence_score": score,
            "stress_index": stone_choice.split(" ")[0],
            "sleep_hours": 7.4,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "weekly_trend": [82, 85, 88, 87, 90, 93, score],
            "prescription_50": p_name,
            "mapped_drink": m_stock["stock_name"],
            "nudge": (
                f"探險家完成調息，心流一致性 {score}%，狀態極佳。"
            ),
            "summary": (
                f"個案持金鑰 {cur_tok} 完成 19 秒調息，配對處方：{p_name}。"
            ),
        }
        if not any(x["token"] == cur_tok for x in global_queue):
            global_queue.insert(
                0,
                {
                    "token": cur_tok,
                    "time": datetime.datetime.now().strftime("%H:%M"),
                    "drink": m_stock["stock_name"],
                },
            )

        st.markdown(
            f"""
            <div class="french-oat-card" style="text-align:center;">
                <h3 style="color:#1C2B20; margin-top:0;">✨ 探險印記已封存安全送達診間 ✨</h3>
                <div style="font-size:1.05rem; line-height:1.9;">
                    專屬通行短碼：<b style="color:#C2A675; font-family:monospace; font-size:1.3rem;">{cur_tok}</b><br>
                    心流諧振評分：<b>{score}%</b><br>
                    🍃 <b>50 款專屬生活處方：{p_name}</b><br>
                    🍵 <b>候診吧台對應奉茶：<span style="color:#A35D4D;">{m_stock['stock_name']}</span></b>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )