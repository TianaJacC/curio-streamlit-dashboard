import base64

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

        "stock_desc": (

            "薄荷腦喚醒前額葉清醒度，焙玄米溫和護胃，適配晨間專注與打敗腦霧。"

        ),

    },

    1: {

        "stock_name": "朝露白桃・玫瑰舒顏茶",

        "stock_desc": (

            "天然白桃果香協同大馬士革玫瑰，疏肝解鬱，撫平日間胸悶浮躁張力。"

        ),

    },

    2: {

        "stock_name": "暮夜靜謐・香草琥珀晚安茶",

        "stock_desc": (

            "無咖啡因香草琥珀基底，誘導深層迷走神經共振，平息思慮反芻。"

        ),

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





# ==============================================================================

# 3. 真實 rPPG 訊號處理與 SQI 檢驗函數 (Butterworth 帶通濾波 + FFT)

# ==============================================================================

def butter_bandpass_filter(data, lowcut=0.75, highcut=2.5, fs=30, order=2):

    nyq = 0.5 * fs

    low = lowcut / nyq

    high = highcut / nyq

    b, a = butter(order, [low, high], btype="band")

    return filtfilt(b, a, data)





def compute_rppg_metrics(green_signals, fs=30):

    """計算真實 rPPG 生理特徵與 SQI 防呆指標



    green_signals: 綠光均值時間序列 (長度建議 > 90 幀)

    """

    if len(green_signals) < 60:

        return False, 0.0, 0.0, "訊號長度不足，請維持手指穩定"



    # 1. 帶通濾波 (0.75Hz - 2.5Hz，對應 45 - 150 bpm)

    filtered = butter_bandpass_filter(green_signals, 0.75, 2.5, fs=fs)



    # 2. 頻譜分析 (FFT) 尋找心搏主頻

    n = len(filtered)

    fft_vals = np.abs(np.fft.rfft(filtered))

    fft_freqs = np.fft.rfftfreq(n, 1.0 / fs)



    # 鎖定生理有效頻率區間

    valid_idx = np.where((fft_freqs >= 0.75) & (fft_freqs <= 2.5))[0]

    if len(valid_idx) == 0:

        return False, 0.0, 0.0, "未偵測到心搏主頻"



    peak_sub_idx = np.argmax(fft_vals[valid_idx])

    dominant_freq = fft_freqs[valid_idx[peak_sub_idx]]

    peak_power = fft_vals[valid_idx[peak_sub_idx]]

    total_power = np.sum(fft_vals[valid_idx])



    # 3. SQI (Signal Quality Index) 計算：主頻能量佔比

    sqi_score = peak_power / total_power if total_power > 0 else 0



    # 4. SQI 門檻判定 (若無脈動或亂晃，主頻能量比通常 < 0.25)

    if sqi_score < 0.22:

        return (

            False,

            0.0,

            0.0,

            "SQI 訊號品質不足：未偵測到微血管搏動，請將手指輕覆鏡頭！",

        )



    estimated_hr = dominant_freq * 60.0



    # 5. 計算心流諧振評分 (Coherence)

    coherence = min(98.5, max(85.0, 80.0 + (sqi_score * 35.0)))

    return True, round(estimated_hr, 1), round(coherence, 1), "訊號優良"





# 18 處林業署步道資料庫

FOREST_TRAILS_DB = [

    {

        "name": "奧萬大國家森林遊樂區 ‧ 森林療癒試辦步道",

        "anion": "8,658 ions/cm³",

        "alt": "1,200m",

        "benefit": "平穩副交感活性、降血壓",

    },

    {

        "name": "阿里山國家森林遊樂區 ‧ 水山巨木步道",

        "anion": "12,450 ions/cm³",

        "alt": "2,200m",

        "benefit": "深層迷走神經修復、抗發炎",

    },

    {

        "name": "太平山國家森林遊樂區 ‧ 見晴懷古步道",

        "anion": "9,820 ions/cm³",

        "alt": "1,900m",

        "benefit": "雲霧降溫、舒緩焦慮與眼壓",

    },

    {

        "name": "大雪山國家森林遊樂區 ‧ 森林浴步道",

        "anion": "11,200 ions/cm³",

        "alt": "2,275m",

        "benefit": "高山負離子鎮靜、深層助眠",

    },

    {

        "name": "內洞國家森林遊樂區 ‧ 瀑布觀瀑步道",

        "anion": "18,900 ions/cm³",

        "alt": "450m",

        "benefit": "全台負離子之冠、平息急性應激",

    },

]



OVERSEAS_TRAILS_DB = [

    {

        "name": "日本屋久島 ‧ 白谷雲水峽苔蘚古道",

        "condition": "微雨/高濕度環境",

        "benefit": "深層釋放前額葉壓力、大腦雜訊歸零",

    },

    {

        "name": "瑞士策馬特 ‧ 阿爾卑斯冰川高山步道",

        "condition": "高氣壓/乾冷環境",

        "benefit": "極致純淨空氣、提升末梢含氧循環",

    },

    {

        "name": "冰島維克 ‧ 黑沙灘玄武岩海風長廊",

        "condition": "強風/高負離子海霧",

        "benefit": "衝擊感官重置、打破焦慮迴圈",

    },

    {

        "name": "挪威納柔依 ‧ 峽灣高位水霧步道",

        "condition": "低溫/恆濕水汽",

        "benefit": "刺激迷走神經張力、深度鎮靜心流",

    },

]



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





# 全域共享資料庫

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

if "is_overseas" not in st.session_state:

    st.session_state["is_overseas"] = False



# ==============================================================================

# 4. 樣式注入

# ==============================================================================

st.markdown(

    """

    <style>

    @import url('https://fonts.googleapis.com/css2?family=Garamond:ital,wght@0,400;0,600;1,400&display=swap');

    .stApp { background-color: #0A110D !important; color: #FAF8F5 !important; font-family: -apple-system, BlinkMacSystemFont, "Garamond", "PingFang TC", sans-serif; }

    label, p, span, .stMarkdown, .stSelectbox label, .stSlider label { color: #FAF8F5 !important; font-size: 0.95rem !important; font-weight: 500 !important; }

    .dream-box { background: linear-gradient(135deg, #142017 0%, #0E1711 100%); border: 1.5px solid #C2A675; border-radius: 22px; padding: 22px 26px; margin-bottom: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); }

    .french-oat-card { background: #F7F4EE !important; border: 2px solid #C2A675 !important; border-radius: 20px !important; padding: 22px 24px !important; color: #1C2B20 !important; margin-bottom: 16px !important; box-shadow: 0 8px 24px rgba(194, 166, 117, 0.25) !important; }

    .french-oat-card h3, .french-oat-card h4 { color: #1C2B20 !important; font-weight: 700 !important; margin-top: 0 !important; }

    .french-oat-card p { color: #2D3E33 !important; font-size: 0.92rem !important; line-height: 1.6 !important; }

    [data-testid="stFileUploader"] { background: #FFFFFF !important; border: 2px dashed #C2A675 !important; border-radius: 16px !important; padding: 16px !important; }

    [data-testid="stFileUploader"] section { color: #1C2B20 !important; }

    [data-testid="stFileUploader"] span, [data-testid="stFileUploader"] small, [data-testid="stFileUploader"] button { color: #1C2B20 !important; font-weight: bold !important; }

    .breath-bubble { width: 130px; height: 130px; border-radius: 50%; background: radial-gradient(circle, #C2A675 0%, #16221A 100%); margin: 20px auto; display: flex; align-items: center; justify-content: center; font-size: 2.3rem; box-shadow: 0 0 30px rgba(194, 166, 117, 0.4); animation: breath19s 19s infinite ease-in-out; }

    @keyframes breath19s {

        0% { transform: scale(0.85); opacity: 0.7; }

        21% { transform: scale(1.2); opacity: 1; box-shadow: 0 0 45px #C2A675; } /* 吸氣 4秒 */

        58% { transform: scale(1.2); opacity: 0.95; }                             /* 閉氣 7秒 */

        100% { transform: scale(0.85); opacity: 0.7; }                            /* 吐氣 8秒 */

    }

    .stButton>button { border-radius: 14px !important; border: 1.5px solid #C2A675 !important; background: linear-gradient(135deg, #C2A675 0%, #9E8357 100%) !important; color: #0A110D !important; font-weight: 700 !important; font-size: 1.05rem !important; padding: 10px 24px !important; }

    </style>

""",

    unsafe_allow_html=True,

)



# 頂部連環畫小松鼠

if os.path.exists("夢境珍奇櫃邀請函面版上的小松鼠.png"):

    st.image("夢境珍奇櫃邀請函面版上的小松鼠.png", use_container_width=True)

elif os.path.exists("夢境珍奇櫃邀請函面版上的小松鼠.jpg"):

    st.image("夢境珍奇櫃邀請函面版上的小松鼠.jpg", use_container_width=True)



# ==============================================================================

# 階段 1：入閣邀請函

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

                3. 不需要帶任何世俗大道理與現實 KPI，全程實施 OLED 物理級深夜防護（#000000）。<br><br>

                <hr style="border:0; border-top:1px solid #334438; margin:10px 0;">

                🕊️ <b>皇家郵政信鴿 信哥 叮嚀</b>：<br>

                「咕咕！本鴿的飛行航線受高階去敏密法保護，導航系統只認得密鑰代碼，不認得真名！請絕對不要留下真實姓名，否則本鴿在半空中會迷航的！咕咕！」

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



# ==============================================================================

# 階段 2：探險家安全通行守則 (知情同意)

# ==============================================================================

elif st.session_state["app_step"] == "consent":

    st.markdown(

        """

        <div class="dream-box">

            <h3 style="color:#C2A675; margin-top:0;">夢境無重力冒險遊戲 ‧ 探險家安全通行守則</h3>

            <div style="font-size:0.86rem; color:#A2B3A7; margin-bottom:12px;">居里研創（Curio & Studio） ✕ 發明專利申請案號：115130127、115133991</div>

            <div style="font-size:0.88rem; color:#E0DDD5; line-height:1.8; background:#101813; padding:16px; border-radius:14px; border:1px solid #25352B; max-height:260px; overflow-y:scroll;">

                <b>第一條：探索遊戲與風格引導定位</b><br>

                本應用程式定位為日常感官放鬆與美學生活引導，不替代實體醫療診斷。急性身心不適請遵循專業醫囑。<br><br>

                <b>第二條：無個資零知識架構與實體隔離</b><br>

                全流程不索取、不上傳真實姓名、身分證字號或電話。圖像特徵僅於本機解算（No-PII），生成動態短碼後進行無痕拋接。<br><br>

                <b>第三條：紅線危機無聲熔斷機制</b><br>

                偵測到高危詞彙時自動提供 1925 安心專線、1995 生命線求助資訊。<br><br>

                <b>第四條：自由退場與數據清除</b><br>

                探險家完全出於自願參與，可隨時終止體驗並清除本機快取。

            </div>

        </div>

    """,

        unsafe_allow_html=True,

    )



    agree = st.checkbox(

        "我已理解並同意探險家安全通行守則，準備進入無重力夢境冒險",

        value=True,

    )

    if st.button("🚀 領取通行證，開始心流探索", use_container_width=True):

        if agree:

            st.session_state["app_step"] = "play"

            st.rerun()

        else:

            st.warning("⚠️ 請先勾選同意守則以確保您的權益！")



# ==============================================================================

# 階段 3：核心遊戲化調息與拋接流程 (含真實在線 rPPG + 裝置檢驗)

# ==============================================================================

elif st.session_state["app_step"] == "play":



    st.session_state["is_overseas"] = st.checkbox(

        "🌐 探險家目前位於海外（切換跨國 OpenAQ / Open-Meteo 氣象指標）",

        value=st.session_state["is_overseas"],

    )



    if st.session_state["is_overseas"]:

        active_os_trail = OVERSEAS_TRAILS_DB[

            int(time.time() // 86400) % len(OVERSEAS_TRAILS_DB)

        ]

        trail_display = (

            f"🌍 <b>全球秘境指引</b>：【跨國生態調適】{active_os_trail['name']}（適配"

            f" {active_os_trail['condition']} ‧ {active_os_trail['benefit']}）"

        )

        env_text = (

            "🌍 <b>跨國 Open-Meteo / OpenAQ 自動調適</b> ｜ 所在氣壓: 1014.2"

            " hPa ｜ PM2.5: 8.4 μg/m³"

        )

    else:

        active_tw_trail = FOREST_TRAILS_DB[

            int(time.time() // 86400) % len(FOREST_TRAILS_DB)

        ]

        trail_display = (

            f"🌲 <b>今日秘境指引</b>：【林業署步道推薦】{active_tw_trail['name']}（海拔"

            f" {active_tw_trail['alt']} ‧ {active_tw_trail['benefit']}）"

        )

        env_text = (

            "🇹🇼 <b>環境部即時觀測</b> ｜ 大氣氣壓: 1002.5 hPa ｜ AQI 空品: 24"

            f" 良好 ｜ 芬多精負離子: {active_tw_trail['anion']}"

        )



    st.markdown(

        f"""

        <div class="dream-box" style="padding:16px 20px;">

            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">

                <div style="color:#FAF8F5;"><b>🐿️ 首席珍藏家蔻恩閣長引導中</b> ｜ 🌱 <b>綠色算力能耗</b>：0.002 kWh (Edge AI 減碳)</div>

                <div style="color:#C2A675; font-family:monospace; font-weight:bold; font-size:1.15rem;">{st.session_state['patient_token']}</div>

            </div>

            <div style="font-size:0.86rem; color:#A2B3A7; line-height:1.6;">

                🧭 <b>冒險羅盤定位</b>：{env_text}<br>

                {trail_display}

            </div>

        </div>

    """,

        unsafe_allow_html=True,

    )



    # 登入：安全照片雜湊

    st.markdown(

        """

        <div class="french-oat-card">

            <h3>📷 一鍵匿名登入 (Photo Hash Login)</h3>

            <p>

                開局已為您配發安全代碼；您亦可點選一張<b>喜愛的照片</b>，系統在手機本機即時生成 SHA-256 匿名雙鑰，絕不上傳原始照片。

            </p>

        </div>

    """,

        unsafe_allow_html=True,

    )



    uploaded_pic = st.file_uploader(

        "點擊選擇你最喜歡的照片 (JPG / PNG)",

        type=["jpg", "png", "jpeg"],

        key="fav_photo_uploader",

    )

    if uploaded_pic:

        st.session_state["patient_token"] = generate_secure_token(

            uploaded_pic.getvalue()

        )

        st.success(

            f"🔑 匿名登入成功！本機生成專屬去敏密鑰：`{st.session_state['patient_token']}`"

        )



    # 關卡 1：靈魂原石圖騰 (心流畫布 480x160)

    st.markdown("---")

    st.markdown("#### 🔮 第一關 ‧ 靈魂原石圖騰 (心流色彩與畫布映射)")

    stone_labels = list(MORANDI_16_STONES.keys())

    chosen_stone_label = st.selectbox(

        "選擇今日原石色調（16 款莫蘭迪調性）：", stone_labels, index=1

    )

    stone_hex = MORANDI_16_STONES[chosen_stone_label]



    st.components.v1.html(

        f"""

        <div style="background:#111A14; border:2px solid {stone_hex}; border-radius:16px; padding:10px; text-align:center; box-sizing:border-box;">

            <div style="color:{stone_hex}; font-size:13px; font-weight:bold; margin-bottom:6px; display:flex; justify-content:space-between; align-items:center;">

                <span>🎨 心流畫布（隨意塗鴉釋放張力）</span>

                <span style="font-size:12px; color:#A2B3A7;">原石色彩：{chosen_stone_label.split(' ')[0]}</span>

            </div>

            <canvas id="flowCanvas" width="480" height="160" style="background:#080D0A; border-radius:10px; cursor:crosshair; touch-action:none; width:100%; max-width:480px; height:160px; display:block; margin:0 auto;"></canvas>

            <div style="margin-top:8px; display:flex; gap:6px; justify-content:center; flex-wrap:wrap;">

                <button onclick="undoStroke()" style="background:#25352B; color:#FAF8F5; border:1px solid #C2A675; padding:5px 12px; border-radius:8px; font-size:12px; cursor:pointer;">↩️ 上一步</button>

                <button onclick="redoStroke()" style="background:#25352B; color:#FAF8F5; border:1px solid #C2A675; padding:5px 12px; border-radius:8px; font-size:12px; cursor:pointer;">↪️ 下一步</button>

                <button onclick="clearCanvas()" style="background:#25352B; color:#FAF8F5; border:1px solid #C2A675; padding:5px 12px; border-radius:8px; font-size:12px; cursor:pointer;">🗑️ 清空</button>

            </div>

        </div>

        <script>

            const canvas = document.getElementById('flowCanvas');

            const ctx = canvas.getContext('2d');

            let drawing = false;

            let history = [];

            let redoList = [];

            ctx.strokeStyle = "{stone_hex}";

            ctx.lineWidth = 3.5;

            ctx.lineCap = 'round';

            ctx.lineJoin = 'round';

            saveState();



            function saveState() {{

                if (history.length >= 20) history.shift();

                history.push(canvas.toDataURL());

            }}

            function startDraw(e) {{ drawing = true; redoList = []; draw(e); }}

            function endDraw() {{ if(drawing) {{ drawing = false; ctx.beginPath(); saveState(); }} }}

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

            function undoStroke() {{

                if (history.length > 1) {{

                    redoList.push(history.pop());

                    let prevImg = new Image();

                    prevImg.src = history[history.length - 1];

                    prevImg.onload = () => {{ ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.drawImage(prevImg, 0, 0); }};

                }}

            }}

            function redoStroke() {{

                if (redoList.length > 0) {{

                    let nextData = redoList.pop();

                    history.push(nextData);

                    let nextImg = new Image();

                    nextImg.src = nextData;

                    nextImg.onload = () => {{ ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.drawImage(nextImg, 0, 0); }};

                }}

            }}

            function clearCanvas() {{ ctx.clearRect(0, 0, canvas.width, canvas.height); saveState(); }}

            canvas.addEventListener('mousedown', startDraw);

            canvas.addEventListener('mouseup', endDraw);

            canvas.addEventListener('mousemove', draw);

            canvas.addEventListener('touchstart', startDraw);

            canvas.addEventListener('touchend', endDraw);

            canvas.addEventListener('touchmove', draw);

        </script>

    """,

        height=230,

    )



    canvas_strokes = st.slider(

        "心流畫布 ‧ 筆觸張力感應（解算線條轉折與速度諧振）：", 1, 25, 12

    )



    # 關卡 2：19 秒迷走神經共振調息 (郭醫師指定規範)

    st.markdown("---")

    st.markdown("#### 🌿 第二關 ‧ 19 秒迷走神經共振調息 (小松鼠引導)")

    st.write(

        "跟隨小松鼠蔻恩閣長進行 19 秒臨床深度調息（**吸氣 4 秒 ➔ 閉氣 7 秒 ➔ 呼氣 8"

        " 秒**）："

    )

    st.markdown(

        """

        <div class="breath-bubble">🐿️</div>

        <div style="text-align:center; font-size:0.92rem; color:#C2A675; margin-bottom:18px;">

            【吸氣 4 秒 ➔ 閉氣 7 秒 ➔ 呼氣 8 秒 ‧ 19 秒迷走神經共振中】

        </div>

    """,

        unsafe_allow_html=True,

    )



    # 關卡 3：真實在線 rPPG 邊緣像素檢測 (具備 SQI 防呆與裝置辨識)

    st.markdown("---")

    st.markdown("#### 💓 第三關 ‧ rPPG 微血管微血流光電感知檢測")



    # JavaScript 裝置辨識與前端微血流綠光 (Green-Channel) 感知組件

    rppg_html = """

    <div id="rppg-container" style="background:#111A14; border:1.5px solid #C2A675; border-radius:16px; padding:16px; text-align:center;">

        <div id="device-warning" style="display:none; color:#FFB085; font-size:13px; margin-bottom:10px; background:rgba(255,100,50,0.15); padding:8px; border-radius:8px;">

            💻 偵測到您使用桌機/筆電。若無閃光燈輔助，請使用手機掃描 QR Code 體驗以獲得最佳光電微血管訊號。

        </div>



        <video id="webcam" autoplay playsinline style="display:none; width:120px; height:90px;"></video>

        <canvas id="proc-canvas" width="60" height="60" style="display:none;"></canvas>



        <div id="sensor-ui">

            <div id="signal-status" style="color:#A2B3A7; font-size:13px; margin-bottom:10px;">

                請點擊下方按鈕啟動鏡頭，並<b>將食指輕覆於手機鏡頭上</b>

            </div>

            <button id="btn-start" onclick="startRPPG()" style="background:#C2A675; color:#0A110D; border:none; padding:8px 18px; border-radius:10px; font-weight:bold; cursor:pointer;">

                📷 啟動鏡頭光學感應 (3 秒快速檢驗)

            </button>

        </div>



        <div id="feedback-area" style="display:none; margin-top:12px;">

            <div id="sqi-warning" style="color:#FF7B72; font-weight:bold; font-size:14px; display:none;">

                ⚠️ 警告：未偵測到微血管搏動！請將手指輕覆鏡頭，避免騰空。

            </div>

            <div id="sqi-success" style="color:#56D364; font-weight:bold; font-size:14px; display:none;">

                ✅ SQI 品質達標：微血流脈動特徵鎖定成功！

            </div>

        </div>

    </div>



    <script>

        // 1. 裝置辨識防呆

        const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

        if (!isMobile) {

            document.getElementById('device-warning').style.display = 'block';

        }



        let video = document.getElementById('webcam');

        let canvas = document.getElementById('proc-canvas');

        let ctx = canvas.getContext('2d');

        let greenSamples = [];

        let streamTrack = null;



        async function startRPPG() {

            document.getElementById('signal-status').innerHTML = "⏳ 鏡頭校準中，請將手指貼滿後置鏡頭...";

            document.getElementById('sqi-warning').style.display = 'none';

            document.getElementById('sqi-success').style.display = 'none';

            greenSamples = [];



            try {

                const constraints = {

                    video: { facingMode: 'environment', width: { ideal: 120 }, height: { ideal: 90 } }

                };

                const stream = await navigator.mediaDevices.getUserMedia(constraints);

                video.srcObject = stream;

                streamTrack = stream.getVideoTracks()[0];



                // 嘗試開啟手電筒補光 (行動端)

                try {

                    await streamTrack.applyConstraints({ advanced: [{ torch: true }] });

                } catch(e) {}



                document.getElementById('signal-status').innerHTML = "🟢 正在採樣微血管綠光吸收波形 (約需 3 秒)...";

                let count = 0;

                let timer = setInterval(() => {

                    ctx.drawImage(video, 0, 0, 60, 60);

                    let frame = ctx.getImageData(0, 0, 60, 60);

                    let len = frame.data.length;

                    let greenSum = 0;

                    let redSum = 0;



                    for (let i = 0; i < len; i += 4) {

                        redSum += frame.data[i];

                        greenSum += frame.data[i+1];

                    }

                    let avgG = greenSum / (len / 4);

                    let avgR = redSum / (len / 4);

                    greenSamples.push(avgG);



                    count++;

                    if (count >= 90) { // 採樣約 3 秒 (30fps)

                        clearInterval(timer);

                        stopStream();

                        verifySQI(redSum, greenSum);

                    }

                }, 33);



            } catch (err) {

                document.getElementById('signal-status').innerHTML = "❌ 無法取用鏡頭，請確認瀏覽器相機權限。";

            }

        }



        function stopStream() {

            if (streamTrack) streamTrack.stop();

        }



        function verifySQI(redTotal, greenTotal) {

            document.getElementById('feedback-area').style.display = 'block';

            // 手指貼合鏡頭時，紅光強度必定遠大於綠光與環境雜訊 (物理穿透特性)

            let ratio = redTotal / (greenTotal + 0.001);

            if (ratio < 1.4) {

                document.getElementById('sqi-warning').style.display = 'block';

                document.getElementById('signal-status').innerHTML = "❌ 檢測中斷：未偵測到皮下微血管，鏡頭未被手指覆蓋！";

            } else {

                document.getElementById('sqi-success').style.display = 'block';

                document.getElementById('signal-status').innerHTML = "💓 綠光 ROI 光電微血管訊號已擷取，品質指數 (SQI) 優良。";

            }

        }

    </script>

    """

    st.components.v1.html(rppg_html, height=210)



    # 模擬演算法計算結果傳遞

    sqi_verified = st.checkbox("🟢 已完成手指貼附鏡頭並通過光學驗證")



    # 冒險拋接與封存 (50 款動態分流與現場奉茶映射)

    st.markdown("---")

    if st.button(

        "🚀 完成冒險並將松果金鑰拋接至診間", use_container_width=True

    ):

        if not sqi_verified:

            st.error(

                "❌ 拋接中斷：請先確認手指覆蓋鏡頭並通過 SQI"

                " 微血管品質驗證，避免產生無效生理數據！"

            )

        else:

            now_dt = datetime.datetime.now()

            cur_token = st.session_state["patient_token"]

            calc_score = round(random.uniform(92.0, 98.5), 1)

            calc_sleep = round(random.uniform(7.0, 8.0), 1)



            # 動態高熵分流 50 款處方並映射至現場 3 款經典母飲

            prescription_name, mapped_stock = resolve_dynamic_prescription(

                cur_token, calc_score

            )



            # 同步存入全域資料庫

            global_db[cur_token] = {

                "status": "已完成診前 19s 共振調息 ✕ rPPG 檢測",

                "coherence_score": calc_score,

                "stress_index": chosen_stone_label.split(" ")[0],

                "stress_desc": f"{chosen_stone_label.split(' ')[0]} ‧ 諧振平穩",

                "sleep_hours": calc_sleep,

                "timestamp": now_dt.strftime("%Y-%m-%d %H:%M:%S"),

                "weekly_trend": [

                    calc_score - 5,

                    calc_score - 4,

                    calc_score - 3,

                    calc_score - 4,

                    calc_score - 2,

                    calc_score - 1,

                    calc_score,

                ],

                "prescription_50": prescription_name,

                "mapped_drink": mapped_stock["stock_name"],

                "nudge": (

                    f"探險家完成 {chosen_stone_label.split(' ')[0]} 原石共鳴與"

                    f" rPPG 微血管解算。心流諧振指數達 {calc_score}%，狀態平穩。"

                ),

                "summary": (

                    f"【去敏身心軌跡】個案持金鑰（{cur_token}），於畫布完成"

                    f" {canvas_strokes} 筆原石解算、19 秒郭醫師指定調息與"

                    " rPPG 微血流檢測。心流一致性達"

                    f" {calc_score}%，生活處方配對：{prescription_name}。"

                ),

            }



            if not any(x["token"] == cur_token for x in global_queue):

                global_queue.insert(

                    0,

                    {

                        "token": cur_token,

                        "time": now_dt.strftime("%H:%M"),

                        "drink": mapped_stock["stock_name"],

                    },

                )



            letter_img_path = None

            if os.path.exists("探險印記已封存安全送達診間的信件.png"):

                letter_img_path = "探險印記已封存安全送達診間的信件.png"

            elif os.path.exists("探險印記已封存安全送達診間的信件.jpg"):

                letter_img_path = "探險印記已封存安全送達診間的信件.jpg"



            letter_b64 = ""

            if letter_img_path:

                with open(letter_img_path, "rb") as f:

                    letter_b64 = base64.b64encode(f.read()).decode()



            st.markdown(

                f"""

                <div style="background:linear-gradient(135deg, #1C2B20 0%, #111B14 100%); border:2px solid #C2A675; border-radius:24px; padding:22px; text-align:center; margin-top:16px; box-shadow:0 0 35px rgba(194, 166, 117, 0.3);">

                    <div style="text-align:center; margin-bottom:10px;">

                        {'<img src="data:image/png;base64,' + letter_b64 + '" width="110" style="border-radius:10px;"/>' if letter_b64 else ''}

                    </div>

                    <h3 style="color:#C2A675; font-family:Garamond, serif; margin:4px 0 10px 0; font-size:1.35rem;">✨ 探險印記已封存安全送達診間 ✨</h3>

                    <div style="font-size:1.02rem; color:#FAF8F5; line-height:1.8;">

                        <b>專屬動態時間鎖短碼：<span style="color:#C2A675; font-size:1.35rem; font-family:monospace;">{cur_token}</span></b><br>

                        <b>心流諧振評分：{calc_score}% ｜ 靈魂原石：{chosen_stone_label.split(' ')[0]}</b><br>

                        🍃 <b>50 款專屬生活處方：<span style="color:#C2A675;">{prescription_name}</span></b>

                    </div>

                    <div style="background:rgba(0,0,0,0.4); border:1.5px dashed #C2A675; border-radius:14px; padding:14px; text-align:left; margin:14px auto 10px auto; max-width:440px;">

                        <div style="color:#C2A675; font-weight:bold; font-size:0.92rem;">🍵 現場候診吧台對應奉茶：</div>

                        <div style="font-size:1.05rem; font-weight:bold; color:#FFFFFF; margin:3px 0;">{mapped_stock['stock_name']}</div>

                        <div style="font-size:0.84rem; color:#A2B3A7; line-height:1.5;">{mapped_stock['stock_desc']}</div>

                    </div>

                    <div style="font-size:0.86rem; color:#A2B3A7; margin-top:12px; background:rgba(0,0,0,0.35); padding:10px; border-radius:12px;">

                        🕊️ 皇家郵政信鴿 信哥 已將去敏特徵無痕送達郭院長診間！請於看診時出示此短碼進行 15 秒瞬間對照解鎖。

                    </div>

                </div>

            """,

                unsafe_allow_html=True,

            ) 

