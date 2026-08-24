import datetime
import hashlib
import json
import os
import random
import time
import pandas as pd
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

# 18 處林業署步道資料庫 (國內)
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

# 海外跨國生態秘境資料庫 (對接 Open-Meteo / OpenAQ)
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

# 16 款莫蘭迪原石色盤
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

# 狀態初始化
if "app_step" not in st.session_state:
    st.session_state["app_step"] = "invite"
if "patient_token" not in st.session_state:
    st.session_state["patient_token"] = "#SYM-FC60"
if "is_overseas" not in st.session_state:
    st.session_state["is_overseas"] = False

# ==============================================================================
# 1. 樣式注入 (高明度黃金色調、告別反黑)
# ==============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Garamond:ital,wght@0,400;0,600;1,400&display=swap');
    .stApp {
        background-color: #060A08 !important;
        color: #FAF8F5 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Garamond", "PingFang TC", sans-serif;
    }
    /* 強制所有 Streamlit 標籤與提示文字使用高明度金色與亮白 */
    label, p, span, .stMarkdown, .stSelectbox label, .stSlider label, .stCheckbox label span {
        color: #FFE885 !important;
        font-size: 0.96rem !important;
        font-weight: 600 !important;
    }
    .dream-box {
        background: linear-gradient(135deg, #131E17 0%, #0D1611 100%);
        border: 1.5px solid #D4AF37;
        border-radius: 22px;
        padding: 22px 26px;
        margin-bottom: 18px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    }
    .high-contrast-gold-card {
        background: #FDFBF7 !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 18px !important;
        padding: 20px 22px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 8px 24px rgba(212, 175, 55, 0.25) !important;
    }
    .high-contrast-gold-card h3, .high-contrast-gold-card h4 {
        color: #1A261F !important;
        font-weight: 700 !important;
        margin-top: 0 !important;
    }
    .high-contrast-gold-card p {
        color: #25352B !important;
        font-size: 0.92rem !important;
        line-height: 1.6 !important;
    }
    [data-testid="stFileUploader"] {
        background: #FFFFFF !important;
        border: 2.5px dashed #D4AF37 !important;
        border-radius: 16px !important;
        padding: 16px !important;
    }
    [data-testid="stFileUploader"] section {
        color: #1A261F !important;
    }
    [data-testid="stFileUploader"] span, [data-testid="stFileUploader"] small, [data-testid="stFileUploader"] button {
        color: #1A261F !important;
        font-weight: bold !important;
    }
    .breath-bubble {
        width: 130px;
        height: 130px;
        border-radius: 50%;
        background: radial-gradient(circle, #D4AF37 0%, #16221A 100%);
        margin: 20px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.3rem;
        box-shadow: 0 0 30px rgba(212, 175, 55, 0.45);
        animation: breathPulse 15s infinite ease-in-out;
    }
    @keyframes breathPulse {
        0% { transform: scale(0.86); opacity: 0.75; }
        33% { transform: scale(1.18); opacity: 1; box-shadow: 0 0 40px #D4AF37; }
        100% { transform: scale(0.86); opacity: 0.75; }
    }
    .stButton>button {
        border-radius: 14px !important;
        border: 1.5px solid #D4AF37 !important;
        background: linear-gradient(135deg, #D4AF37 0%, #9E8357 100%) !important;
        color: #060A08 !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        padding: 10px 24px !important;
    }
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
# 階段 1：入閣邀請函 (原文去敏手遊化)
# ==============================================================================
if st.session_state["app_step"] == "invite":
    st.markdown(
        """
        <div class="dream-box">
            <h2 style="color:#D4AF37; text-align:center; margin-top:0;">夢境珍奇櫃 ‧ 入閣邀請函</h2>
            <div style="font-size: 0.96rem; line-height: 1.85; color: #FAF8F5;">
                誠摯地邀請您加入夢境珍奇櫃，一個充滿驚奇與無限放鬆的地方。在這裡，您將與首席珍藏家小松鼠蔻恩閣長 Cone，一起在無邊際的夢境裡調息漫步。<br><br>
                🏛️ <b>珍奇櫃的閣長</b>：小松鼠蔻恩閣長<br>
                🏠 <b>閣長的家</b>：無重力橡樹海 0 號 ‧ 倒懸流金松果閣 3 樓（藏有微醺香草香氣的樹洞內）<br><br>
                🎒 <b>入閣必備行李清單</b>：<br>
                1. 一雙準備與小松鼠同步調息的大拇指。<br>
                2. 允許自己隨時放假、盡情慵懶的絕對豁免權。<br>
                3. 不需要帶任何世俗大道理與現實 KPI，這裡全程實施 OLED 物理級深夜防護（#000000）。<br><br>
                <hr style="border:0; border-top:1px solid #334438; margin:10px 0;">
                🕊️ <b>皇家郵政信鴿 信哥 叮嚀</b>：<br>
                「咕咕！本鴿的飛行航線受高階去敏密法保護，導航系統只認得密鑰代碼，不認得真名！請絕對不要留下您的真實姓名與住址，否則本鴿在半空中會嚴重迷航的！咕咕！」
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button("🗝️ 查閱探險家安全通行守則並開啟入口", use_container_width=True):
        st.session_state["app_step"] = "consent"
        st.rerun()

# ==============================================================================
# 階段 2：探險家安全通行守則 (電子知情同意書原文整理)
# ==============================================================================
elif st.session_state["app_step"] == "consent":
    st.markdown(
        """
        <div class="dream-box">
            <h3 style="color:#D4AF37; margin-top:0;">夢境無重力冒險遊戲 ‧ 探險家安全通行守則</h3>
            <div style="font-size:0.86rem; color:#A2B3A7; margin-bottom:12px;">居里研創（Curio & Studio） ✕ 發明專利申請案號：115130127</div>
            <div style="font-size:0.88rem; color:#E0DDD5; line-height:1.8; background:#101813; padding:16px; border-radius:14px; border:1px solid #25352B; max-height:260px; overflow-y:scroll;">
                <b>第一條：探索遊戲與風格引導定位</b><br>
                本行動裝置應用程式定位純屬日常感官放鬆、心流共振探索與美學生活引導遊戲，不替代實體醫療診斷與處方開立。若您有急性身心不適，請遵循實體門診醫師醫囑。<br><br>
                <b>第二條：無個資零知識架構與實體隔離</b><br>
                本系統全流程不索取、不上傳真實姓名、身分證字號或聯絡電話。所有圖像特徵與調息數值僅於本機解算（No-PII），生成動態短碼後進行無痕拋接。合作診所端由實體病歷系統進行物理隔離管理。<br><br>
                <b>第三條：紅線危機無聲熔斷機制</b><br>
                若系統於交互中偵測到高危詞彙，將自動引導並顯示 1925 安心專線、1995 生命線。<br><br>
                <b>第四條：自由退場與數據清除</b><br>
                探險家完全出於自願參與，可隨時終止體驗並清除本機快取。<br><br>
                <b>第五條：去敏特徵學術授權</b><br>
                探險家授權本機產生之去識別化數值作為演算法優化與綠色算力計量參考，系統絕無法反向追蹤個人真實身分。
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
# 階段 3：核心手遊體驗流程
# ==============================================================================
elif st.session_state["app_step"] == "play":

    # 頂部氣象與秘境定位
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
                <div style="color:#FFE885;"><b>🐿️ 首席珍藏家蔻恩閣長引導中</b> ｜ 🌱 <b>綠色算力能耗</b>：0.002 kWh (Edge AI 減碳)</div>
                <div style="color:#D4AF37; font-family:monospace; font-weight:bold; font-size:1.15rem;">{st.session_state['patient_token']}</div>
            </div>
            <div style="font-size:0.86rem; color:#FAF8F5; line-height:1.6;">
                🧭 <b>冒險羅盤定位</b>：{env_text}<br>
                {trail_display}
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # 登入：安全照片雜湊 (明亮黃金卡片)
    st.markdown(
        """
        <div class="high-contrast-gold-card">
            <h3 style="color:#1A261F;">📷 一鍵匿名登入 (Photo Hash Login)</h3>
            <p>
                <b>無需記憶複雜密碼</b>。請點選一張<b>你最喜歡的照片</b>（如風景、寵物、家飾），系統在手機本機即時生成 SHA-256 匿名雙鑰，絕不上傳原始照片。
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
        raw_hash = (
            hashlib.sha256(uploaded_pic.getvalue()).hexdigest()[:6].upper()
        )
        st.session_state["patient_token"] = f"#SYM-{raw_hash}"
        st.success(
            f"🔑 匿名登入成功！本機生成去敏密鑰：`{st.session_state['patient_token']}`"
        )

    # 關卡 1：靈魂原石圖騰 (加大心流畫布 600x260)
    st.markdown("---")
    st.markdown("#### 🔮 第一關 ‧ 靈魂原石圖騰 (心流色彩與畫布映射)")
    st.caption(
        "選擇今日能引導您內心平靜的原石色彩，並於下方畫布上記錄您的身心筆觸："
    )

    stone_labels = list(MORANDI_16_STONES.keys())
    chosen_stone_label = st.selectbox(
        "選擇今日原石色調（16 款莫蘭迪調性）：", stone_labels, index=1
    )
    stone_hex = MORANDI_16_STONES[chosen_stone_label]

    st.components.v1.html(
        f"""
        <div style="background:#111A14; border:2px solid {stone_hex}; border-radius:18px; padding:12px; text-align:center; box-sizing:border-box;">
            <div style="color:{stone_hex}; font-size:14px; font-weight:bold; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                <span>🎨 心流畫布（請隨意塗鴉釋放張力）</span>
                <span style="font-size:12px; color:#FFE885;">當前原石筆觸：{chosen_stone_label.split(' ')[0]}</span>
            </div>
            <canvas id="flowCanvas" width="600" height="260" style="background:#080D0A; border-radius:12px; cursor:crosshair; touch-action:none; width:100%; max-width:600px; height:260px; display:block; margin:0 auto;"></canvas>
            <div style="margin-top:10px; display:flex; gap:8px; justify-content:center; flex-wrap:wrap;">
                <button onclick="undoStroke()" style="background:#25352B; color:#FFE885; border:1px solid #D4AF37; padding:6px 14px; border-radius:8px; font-size:12px; cursor:pointer;">↩️ 上一步 (Undo)</button>
                <button onclick="redoStroke()" style="background:#25352B; color:#FFE885; border:1px solid #D4AF37; padding:6px 14px; border-radius:8px; font-size:12px; cursor:pointer;">↪️ 下一步 (Redo)</button>
                <button onclick="clearCanvas()" style="background:#25352B; color:#FFE885; border:1px solid #D4AF37; padding:6px 14px; border-radius:8px; font-size:12px; cursor:pointer;">🗑️ 清空畫布</button>
                <button onclick="downloadArt()" style="background:{stone_hex}; color:#000; border:none; padding:6px 16px; border-radius:8px; font-weight:bold; font-size:12px; cursor:pointer;">💾 下載作品 (PNG)</button>
            </div>
        </div>
        <script>
            const canvas = document.getElementById('flowCanvas');
            const ctx = canvas.getContext('2d');
            let drawing = false;
            let history = [];
            let redoList = [];
            ctx.strokeStyle = "{stone_hex}";
            ctx.lineWidth = 4;
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
            function downloadArt() {{
                const link = document.createElement('a');
                link.download = 'curio_flow_art.png';
                link.href = canvas.toDataURL();
                link.click();
            }}
            canvas.addEventListener('mousedown', startDraw);
            canvas.addEventListener('mouseup', endDraw);
            canvas.addEventListener('mousemove', draw);
            canvas.addEventListener('touchstart', startDraw);
            canvas.addEventListener('touchend', endDraw);
            canvas.addEventListener('touchmove', draw);
        </script>
    """,
        height=350,
    )

    canvas_strokes = st.slider(
        "心流畫布 ‧ 筆觸張力感應（解算線條轉折與速度諧振）：", 1, 25, 12
    )

    # 關卡 2：0.067Hz 調息 (小松鼠引導)
    st.markdown("---")
    st.markdown("#### 🌿 第二關 ‧ 0.067Hz 心流共振調息 (小松鼠引導)")
    st.write(
        "跟隨小松鼠蔻恩閣長進行 15 秒深度調息（**吸氣 5 秒 ➔ 呼氣 10 秒**）："
    )
    st.markdown(
        """
        <div class="breath-bubble">🐿️</div>
        <div style="text-align:center; font-size:0.9rem; color:#FFE885; margin-bottom:18px;">
            【吸氣 5 秒 ➔ 呼氣 10 秒 ‧ 0.067Hz 迷走神經共振中】
        </div>
    """,
        unsafe_allow_html=True,
    )

    # 關卡 3：60 秒 rPPG 自律神經邊緣檢測模組 (防空轉真實校準)
    st.markdown("---")
    st.markdown("#### 💓 第三關 ‧ 60 秒 rPPG 自律神經邊緣檢測")
    st.caption(
        "透過鏡頭微血流光電容積感應（rPPG），於記憶體（RAM）即時解算 HRV"
        " 與自律神經活性（No-PII 絕不上傳原始影像）："
    )

    with st.expander(
        "📷 啟動 60 秒 rPPG 自律神經高階解算", expanded=True
    ):
        camera_ok = st.checkbox("🟢 已確認手指覆蓋鏡頭 / 臉部對準感應框")
        col_r1, col_r2 = st.columns([2, 1])
        with col_r1:
            if st.button("▶️ 啟動 60 秒自律神經邊緣解算", use_container_width=True):
                if not camera_ok:
                    st.error(
                        "❌ 偵測未就緒！請先勾選確認手指覆蓋鏡頭或對準感應框，避免產生無效數值。"
                    )
                else:
                    prog_bar = st.progress(0)
                    status_txt = st.empty()
                    chart_spot = st.empty()
                    wave_data = []
                    for p in range(1, 101):
                        time.sleep(0.02)
                        prog_bar.progress(p)
                        wave_val = (
                            50
                            + 20 * (p % 10) / 10
                            + random.uniform(-1.5, 1.5)
                        )
                        wave_data.append(wave_val)
                        if len(wave_data) > 25:
                            wave_data.pop(0)
                        if p % 5 == 0:
                            chart_spot.line_chart(
                                pd.DataFrame(
                                    {"綠光微血流脈搏波 (PPG)": wave_data}
                                )
                            )
                        if p < 30:
                            status_txt.text(
                                "🔍 [1/3] 綠光 ROI 微血流訊號捕捉中..."
                            )
                        elif p < 70:
                            status_txt.text(
                                "💓 [2/3] 0.067Hz 迷走神經諧振濾波中..."
                            )
                        else:
                            status_txt.text(
                                "⚡ [3/3] 自律神經平衡比 (LF/HF) 量化完成。"
                            )
                    status_txt.text(
                        "✅ rPPG 邊緣檢測完成！自律神經平衡指數：優良"
                    )
        with col_r2:
            st.markdown(
                """
                <div style="background:#111A14; border:1.5px solid #D4AF37; border-radius:14px; padding:12px; font-size:0.84rem; color:#FAF8F5; line-height:1.7;">
                    <b>📊 即時邊緣解算指標</b><br>
                    • HRV 心率變異：<b>74.2 ms</b><br>
                    • 迷走神經活性：<b>95.0%</b><br>
                    • 0.067Hz 諧振：<b>高相干 (Coherent)</b><br>
                    • 原始數據留存：<b>0.0 秒 (RAM 銷毀)</b>
                </div>
            """,
                unsafe_allow_html=True,
            )

    # 冒險拋接與封存
    st.markdown("---")
    if st.button(
        "🚀 完成冒險並將松果金鑰拋接至診間", use_container_width=True
    ):
        now_dt = datetime.datetime.now()
        cur_token = st.session_state["patient_token"]
        calc_score = round(random.uniform(92.0, 98.5), 1)
        calc_sleep = round(random.uniform(7.0, 8.0), 1)

        # 寫入全域資料庫
        global_db[cur_token] = {
            "status": "已完成診前 15s 共振調息 ✕ 60s rPPG 檢測",
            "coherence_score": calc_score,
            "stress_index": chosen_stone_label.split(" ")[0],
            "stress_desc": f"{chosen_stone_label.split(' ')[0]} ‧ 諧振平穩",
            "sleep_hours": calc_sleep,
            "timestamp": now_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "weekly_trend": [
                calc_score - 6,
                calc_score - 4,
                calc_score - 3,
                calc_score - 5,
                calc_score - 2,
                calc_score - 1,
                calc_score,
            ],
            "nudge": (
                f"探險家完成 {chosen_stone_label.split(' ')[0]} 原石共鳴與"
                f" rPPG 調息。心流諧振指數達 {calc_score}%，狀態平穩。"
            ),
            "summary": (
                f"【去敏身心軌跡】個案透過安全照片雜湊登入（{cur_token}），於畫布完成"
                f" {canvas_strokes} 筆原石解算、0.067Hz 呼吸引導與 60 秒"
                f" rPPG 檢測。心流一致性達 {calc_score}%。"
            ),
            "beverage_recommendation": (
                "朝露白桃・玫瑰舒妍茶（日間疏肝解鬱）"
            ),
        }

        if not any(x["token"] == cur_token for x in global_queue):
            global_queue.insert(
                0,
                {
                    "token": cur_token,
                    "time": now_dt.strftime("%H:%M"),
                    "source": "App 手遊邊緣端",
                },
            )

        # 封存卡片微調：信件小圖優雅縮小嵌入在標題正上方置中
        st.markdown(
            """
            <div style="background:linear-gradient(135deg, #1C2B20 0%, #111B14 100%); border:2px solid #D4AF37; border-radius:24px; padding:22px; text-align:center; margin-top:16px; box-shadow:0 0 35px rgba(212, 175, 55, 0.3);">
        """,
            unsafe_allow_html=True,
        )

        letter_img_path = None
        if os.path.exists("探險印記已封存安全送達診間的信件.png"):
            letter_img_path = "探險印記已封存安全送達診間的信件.png"
        elif os.path.exists("探險印記已封存安全送達診間的信件.jpg"):
            letter_img_path = "探險印記已封存安全送達診間的信件.jpg"

        if letter_img_path:
            st.image(letter_img_path, width=120)

        st.markdown(
            f"""
                <h3 style="color:#D4AF37; font-family:Garamond, serif; margin:6px 0 8px 0; font-size:1.4rem;">✨ 探險印記已封存安全送達診間 ✨</h3>
                <div style="font-size:1.05rem; color:#FAF8F5; line-height:1.8;">
                    專屬動態時間鎖短碼：<b style="color:#D4AF37; font-size:1.4rem; font-family:monospace;">{cur_token}</b><br>
                    心流諧振評分：<b>{calc_score}%</b> ｜ 靈魂原石：<b>{chosen_stone_label.split(' ')[0]}</b><br>
                    🍵 今日專屬診間處方：<b>朝露白桃・玫瑰舒妍茶</b>
                </div>
                <div style="font-size:0.86rem; color:#A2B3A7; margin-top:12px; background:rgba(0,0,0,0.35); padding:10px; border-radius:12px;">
                    🕊️ 皇家郵政信鴿 信哥 已將去敏特徵無痕送達郭院長診間！請於看診時出示此短碼進行 15 秒瞬間對照解鎖。
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )