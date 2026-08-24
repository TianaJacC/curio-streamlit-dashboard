import datetime
import hashlib
import json
import os
import random
import time
import pandas as pd
import streamlit as st

# ==============================================================================
# 0. 頁面配置與高奢莫蘭迪黑金調性
# ==============================================================================
st.set_page_config(
    page_title="夢境珍奇櫃 ‧ 探險家終端",
    page_icon="🐿️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 50 款診間生活處方飲品庫
BEVERAGE_PRESCRIPTIONS = [
    "破霧清醒・薄荷焙香玄米茶（晨間專注開機）",
    "朝露白桃・玫瑰舒妍茶（日間疏肝解鬱）",
    "暮夜靜謐・香草琥珀晚安茶（夜間助眠安神）",
    "松林晨曦・雪松冷萃綠茶（清空大腦雜訊）",
    "澄心降火・杭菊決明舒目茶（降肝火與眼壓）",
    "雨後苔原・檸檬草香蜂草茶（化解胸悶氣鬱）",
    "暖陽薑黃・肉桂黑糖暖身茶（溫陽驅寒驅疲）",
    "空谷幽蘭・白毫銀針茉莉茶（撫平呼吸急促）",
    "暮色沉香・老白茶沉香片（深度迷走神經錨定）",
    "靜心酸棗・百合茯苓養神茶（安撫思緒過載）",
    "微光青柑・新會小青柑普洱（理氣健脾化濕）",
    "清風甘露・玉露桑葉解壓茶（淨化神經疲憊）",
    "琥珀洋甘・蜜香無咖啡因茶（舒緩胃部緊縮）",
    "山嵐迷霧・高山烏龍桂花茶（擴張胸腔呼吸量）",
    "玄米舒緩・蕎麥紫蘇輕身茶（化濕理氣輕盈）",
    "落日餘暉・南非國寶香草茶（釋放整日疲勞）",
    "雪山冷泉・西洋參石斛生津茶（滋陰降虛火）",
    "金風玉露・枇杷葉羅漢果茶（潤肺順氣利咽）",
    "林間漫步・針松牛蒡淨化茶（深層代謝負能量）",
    "太虛引夢・遠志酸棗仁安魂茶（身心歸零重置）",
    "極光耶加・淺焙花香水洗美式（喚醒大腦靈感）",
    "雪嶺冷萃・厭氧日曬藝伎冷萃（平息煩躁思緒）",
    "焦糖迷霧・燕麥奶海鹽拿鐵（溫潤血糖安全感）",
    "暮光之城・低因瑞士水洗拿鐵（無負擔咖啡香氣）",
    "橙光共振・羅馬西西里氣泡咖啡（打破午後倦怠）",
    "京都雨露・一保堂無糖抹茶拿鐵（茶胺酸冷靜專注）",
    "黑曜石萃・黑松露深焙冰美式（快速重啟運作）",
    "北歐森林・小豆蔻肉桂拿鐵（提升末梢循環）",
    "山丘微光・肯亞 AA 烏梅冷萃（酸甜明亮生津）",
    "白夜流金・夏威夷豆奶髒咖啡 (Dirty)（多層次放鬆）",
    "晨曦甜橙・鮮榨冷壓甜橙薑汁（高維生素 C 抗氧化）",
    "深林甘藍・羽衣甘藍蘋果青汁（補充鎂離子負荷）",
    "紅寶石光・冷壓甜菜根石榴飲（舒張血管改善循環）",
    "黃金澄境・慢磨鳳梨百香薑黃飲（抗發炎緩解緊繃）",
    "紫霧凝香・野生藍莓黑醋栗冷壓汁（修復視神經疲勞）",
    "白露芭樂・香檬珍珠芭樂鮮萃汁（穩定午後情緒）",
    "澄澈之湖・日本青森富士蘋果鮮榨（純淨溫柔慰藉）",
    "青檸微光・高纖奇亞籽檸檬蜜露（改善自律神經緊縮）",
    "熱帶雨林・紅心芭樂百香綠拿鐵（淨化腸道身心）",
    "月影桑葚・紫雲桑葚玫瑰活妍飲（滋陰養血抗壓）",
    "流金杏仁・古法微甜冷研杏仁露（潤肺平喘深呼吸）",
    "琥珀銀耳・蓮子百合桂花雪耳羹（植物多醣體修復）",
    "黑金能量・九蒸九曬芝麻黑豆乳（滋補熬夜腦霧）",
    "天籟甘泉・冷萃澎大海羅漢果露（放鬆發聲肌群）",
    "大地沉香・葛根枳椇子醒神飲（緩解頸椎悶脹）",
    "玉露珍珠・炒麥芽山楂消食飲（舒緩壓力性胃脹）",
    "暖胃甘露・茯苓芡實白扁豆米湯（健脾溫和護胃）",
    "冰心雪梨・川貝枇杷清潤冰茶（清心潤燥平息內熱）",
    "太極靜心・石菖蒲遠志益智飲（開竅寧神清空雜念）",
    "歸元神農・甘草小麥紅棗安神湯（平息情緒波動）",
]

# 16 款莫蘭迪原石色彩庫
MORANDI_16_STONES = {
    "鼠尾草綠 (#7A8B7B) ‧ 深層放鬆": "#7A8B7B",
    "莫蘭迪藍 (#6B7D8E) ‧ 平穩心流": "#6B7D8E",
    "陶土粉 (#B8837D) ‧ 溫暖釋壓": "#B8837D",
    "暖燕麥 (#EBE4D8) ‧ 思緒歸零": "#EBE4D8",
    "深林綠 (#25352B) ‧ 大地共振": "#25352B",
    "流金香檳 (#C2A675) ‧ 能量修復": "#C2A675",
    "霧霾灰藍 (#8FA4A6) ‧ 降溫止躁": "#8FA4A6",
    "古董玫瑰 (#C49A88) ‧ 疏肝解鬱": "#C49A88",
    "冷霧丁香 (#9B8B9B) ‧ 迷走神經錨定": "#9B8B9B",
    "青苔石褐 (#827E68) ‧ 深度穩定": "#827E68",
    "月光冷銀 (#D8D8D8) ‧ 雜訊抽離": "#D8D8D8",
    "煙燻雪松 (#4A3B32) ‧ 屏障防護": "#4A3B32",
    "日落赤陶 (#A35D4D) ‧ 驅散陰鬱": "#A35D4D",
    "初生嫩芽 (#A2B38F) ‧ 生機復甦": "#A2B38F",
    "深海暮光 (#2B3A42) ‧ 潛意識探索": "#2B3A42",
    "暮色純黑 (#000000) ‧ 物理級防禦": "#000000",
}

# 全域中繼資料庫
@st.cache_resource
def get_global_database():
    return {
        "#SYM-C701": {
            "status": "已完成診前 15s 共振調息",
            "coherence_score": 92.5,
            "stress_index": "莫蘭迪藍 (#6B7D8E)",
            "stress_desc": "莫蘭迪藍 ‧ 平穩心流",
            "sleep_hours": 7.2,
            "timestamp": "2026-08-25 01:20:15",
            "weekly_trend": [82, 85, 87, 84, 89, 91, 92.5],
            "nudge": "探險家心流穩定（92.5%），夜間無應激爆發。建議問診重點：維持優質睡眠時數。",
            "summary": "【去敏身心軌跡摘要】個案於看診前 15 秒於候診區完成 0.067 Hz 心流共振調息。連續 7 日數據顯示心流維持於 90% 以上高諧振區間。",
            "beverage_recommendation": BEVERAGE_PRESCRIPTIONS[1],
        }
    }

@st.cache_resource
def get_global_queue():
    return [{"token": "#SYM-C701", "time": "01:20", "source": "App 手遊端"}]

global_db = get_global_database()
global_queue = get_global_queue()

# 狀態管理
if "app_step" not in st.session_state:
    st.session_state["app_step"] = "invite"  # invite -> consent -> play
if "patient_token" not in st.session_state:
    st.session_state["patient_token"] = "#SYM-FC60"

# ==============================================================================
# 1. 樣式注入 (高對比、奢華質感、告別死黑看不清)
# ==============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Didot&family=Garamond:ital,wght@0,400;0,600;1,400&display=swap');
    .stApp {
        background-color: #060A08 !important;
        color: #FAF8F5 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Garamond", "Georgia", "PingFang TC", sans-serif;
    }
    .dream-box {
        background: linear-gradient(135deg, #131E17 0%, #0D1611 100%);
        border: 1.5px solid #C2A675;
        border-radius: 24px;
        padding: 24px 28px;
        margin-bottom: 20px;
        box-shadow: 0 12px 36px rgba(0,0,0,0.6);
    }
    /* 高對比上傳區 */
    .high-contrast-card {
        background: #F4F0E8 !important;
        border: 2px solid #C2A675 !important;
        border-radius: 20px !important;
        padding: 22px 24px !important;
        color: #1A261F !important;
        margin-bottom: 20px !important;
        box-shadow: 0 8px 24px rgba(194, 166, 117, 0.2) !important;
    }
    .high-contrast-card h4 {
        color: #1A261F !important;
        font-family: "Garamond", serif !important;
        font-weight: 600 !important;
        margin-top: 0 !important;
        font-size: 1.25rem !important;
    }
    .high-contrast-card p {
        color: #3B4D40 !important;
        font-size: 0.92rem !important;
        line-height: 1.6 !important;
    }
    .breath-bubble {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        background: radial-gradient(circle, #C2A675 0%, #16221A 100%);
        margin: 22px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        box-shadow: 0 0 30px rgba(194, 166, 117, 0.45);
        animation: breathPulse 15s infinite ease-in-out;
    }
    @keyframes breathPulse {
        0% { transform: scale(0.86); opacity: 0.75; }
        33% { transform: scale(1.18); opacity: 1; box-shadow: 0 0 40px #C2A675; }
        100% { transform: scale(0.86); opacity: 0.75; }
    }
    .stButton>button {
        border-radius: 14px !important;
        border: 1.5px solid #C2A675 !important;
        background: linear-gradient(135deg, #C2A675 0%, #9E8357 100%) !important;
        color: #060A08 !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        padding: 12px 28px !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #FAF8F5 0%, #EAE4D8 100%) !important;
        color: #060A08 !important;
        box-shadow: 0 0 22px rgba(194, 166, 117, 0.7) !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 頂部小松鼠連環畫 (承接 ➔ 封存 ➔ 回饋)
if os.path.exists("夢境珍奇櫃邀請函面版上的小松鼠.png"):
    st.image("夢境珍奇櫃邀請函面版上的小松鼠.png", use_container_width=True)
elif os.path.exists("夢境珍奇櫃邀請函面版上的小松鼠.jpg"):
    st.image("夢境珍奇櫃邀請函面版上的小松鼠.jpg", use_container_width=True)

# ==============================================================================
# 階段 1：入閣邀請函 (沉浸式手遊世界觀)
# ==============================================================================
if st.session_state["app_step"] == "invite":
    st.markdown(
        """
        <div class="dream-box">
            <h2 style="font-family: Garamond, serif; color:#C2A675; text-align:center; margin-top:0;">夢境珍奇櫃 ‧ 入閣邀請函</h2>
            <div style="font-size: 0.96rem; line-height: 1.85; color: #FAF8F5;">
                誠摯地邀請您加入夢境珍奇櫃，一個充滿驚奇與無限放鬆的地方。在這裡，您將與首席珍藏家小松鼠蔻恩閣長 Cone，一起在無邊際的夢境裡調息漫步。<br><br>
                🏛️ <b>珍奇櫃的閣長</b>：小松鼠蔻恩閣長<br>
                🏠 <b>閣長的家</b>：無重力橡樹海 0 號 ‧ 倒懸流金松果閣 3 樓（藏有微醺香草香氣的樹洞內）<br><br>
                🎒 <b>入閣必備行李清單</b>：<br>
                1. 一雙準備與小松鼠同步調息的大拇指。<br>
                2. 允許自己隨時放假、盡情慵懶的絕對豁免權。<br>
                3. 不需要帶任何世俗大道理與現實 KPI，這裡全程實施 OLED 物理級深夜防護（#000000）。<br><br>
                <hr style="border:0; border-top:1px solid #334438; margin:12px 0;">
                🕊️ <b>皇家郵政信鴿 信哥 叮嚀</b>：<br>
                「咕咕！本鴿的飛行航線受高階去敏密法保護，導航系統只認得密鑰代碼，不認得真名！請絕對不要留下您的真實姓名與住址，否則本鴿在半空中會嚴重迷航的！咕咕！」
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button("🗝️ 查閱探險家安全守則並開啟入口", use_container_width=True):
        st.session_state["app_step"] = "consent"
        st.rerun()

# ==============================================================================
# 階段 2：探險家安全守則 (去敏感化電子同意書)
# ==============================================================================
elif st.session_state["app_step"] == "consent":
    st.markdown(
        """
        <div class="dream-box">
            <h3 style="font-family: Garamond, serif; color:#C2A675; margin-top:0;">夢境無重力冒險遊戲 ‧ 探險家安全通行守則</h3>
            <div style="font-size:0.86rem; color:#A2B3A7; margin-bottom:12px;">居里研創（Curio & Studio） ✕ 發明專利申請案號：115130127</div>
            <div style="font-size:0.88rem; color:#E0DDD5; line-height:1.8; background:#101813; padding:16px; border-radius:14px; border:1px solid #25352B; max-height:250px; overflow-y:scroll;">
                <b>一、 探索遊戲與健康管理定位</b><br>
                本行動應用程式為日常感官放鬆、心流共振探索與身心美學風格引導遊戲，不替代實體醫療診斷與處方開立。若您有急性身心不適，請依實體門診醫囑。<br><br>
                <b>二、 零個資邊緣專利防線 (Zero-Knowledge)</b><br>
                本系統全流程不索取、不上傳真實姓名、身分證字號或聯絡電話。所有圖像特徵與調息數值僅於本機解算（No-PII），生成動態短碼後進行無痕拋接。<br><br>
                <b>三、 自由退場與數據清除</b><br>
                探險家完全出於自願參與，可隨時終止體驗並清除本機快取。<br><br>
                <b>四、 去敏特徵學術授權</b><br>
                探險家授權本機產生之去識別化數值作為演算法優化與綠色算力計量參考，系統絕無法反向追蹤個人真實身分。
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    agree = st.checkbox("我已理解並同意探險家安全守則，準備進入無重力夢境冒險", value=True)
    if st.button("🚀 領取通行證，開始心流探索", use_container_width=True):
        if agree:
            st.session_state["app_step"] = "play"
            st.rerun()
        else:
            st.warning("⚠️ 請先勾選同意守則以確保您的權益！")

# ==============================================================================
# 階段 3：核心遊戲化調息與拋接流程
# ==============================================================================
elif st.session_state["app_step"] == "play":
    st.markdown(
        f"""
        <div class="dream-box" style="padding:16px 22px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div><b>🐿️ 首席珍藏家蔻恩閣長引導中</b> ｜ 🌱 <b>綠色算力能耗</b>：0.002 kWh (Edge AI 減碳)</div>
                <div style="color:#C2A675; font-family:monospace; font-weight:bold; font-size:1.15rem;">{st.session_state['patient_token']}</div>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # 關卡 0：安全照片雜湊登入 (高對比溫潤卡片)
    st.markdown(
        """
        <div class="high-contrast-card">
            <h4>📷 關卡 0 ‧ 安全照片匿名登入 (Photo Hash Login)</h4>
            <p>
                <b>無需記憶複雜密碼</b>。請點選一張帶給您安全感的照片（如風景、寵物、家飾），系統在手機本機即時生成 SHA-256 匿名雙鑰，絕不上傳原始照片。
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    uploaded_pic = st.file_uploader(
        "點擊選擇安全照片 (JPG / PNG)",
        type=["jpg", "png", "jpeg"],
        key="photo_hash_uploader",
    )
    if uploaded_pic:
        raw_hash = hashlib.sha256(uploaded_pic.getvalue()).hexdigest()[:6].upper()
        st.session_state["patient_token"] = f"#SYM-{raw_hash}"
        st.success(f"🔑 安全照片雜湊成功！本機生成去敏密鑰：`{st.session_state['patient_token']}`")

    # 關卡 1：靈魂原石共鳴 (16 色盤 + 心流畫布)
    st.markdown("---")
    st.markdown("#### 🔮 關卡 1 ‧ 靈魂原石圖騰 (心流色彩與畫布映射)")
    st.caption("選擇今日能引導您內心平靜的原石色彩，並於畫布上記錄您的身心筆觸：")

    chosen_stone_label = st.selectbox(
        "選擇今日原石色調（16 款莫蘭迪調性）：",
        list(MORANDI_16_STONES.keys()),
        index=1,
    )
    stone_hex = MORANDI_16_STONES[chosen_stone_label]

    col_art_1, col_art_2 = st.columns([3, 1])
    with col_art_1:
        canvas_strokes = st.slider("心流畫布 ‧ 筆觸壓力與共振張力感應：", 1, 25, 12)
        st.markdown(
            f"""
            <div style="background:#101813; border:2px dashed {stone_hex}; border-radius:14px; height:120px; display:flex; align-items:center; justify-content:center; color:{stone_hex}; font-size:0.95rem; text-align:center; padding:10px;">
                🎨 心流畫布已就緒 ｜ 已捕捉 {canvas_strokes} 筆心流原石筆觸<br>
                <span style="font-size:0.8rem; color:#A2B3A7;">（邊緣演算法自動解算壓力諧振特徵）</span>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with col_art_2:
        st.markdown(
            f"""
            <div style="background:{stone_hex}; color:{'#FFFFFF' if stone_hex in ['#000000', '#25352B', '#4A3B32', '#2B3A42'] else '#000000'}; height:120px; border-radius:14px; display:flex; align-items:center; justify-content:center; font-weight:bold; text-align:center; padding:12px; border:1px solid #C2A675;">
                {chosen_stone_label.split(' ')[0]}
            </div>
        """,
            unsafe_allow_html=True,
        )

    # 關卡 2：0.067Hz 調息 (小松鼠全程引導)
    st.markdown("---")
    st.markdown("#### 🌿 關卡 2 ‧ 0.067Hz 心流共振調息 (小松鼠引導)")
    st.write("跟隨小松鼠蔻恩閣長進行 15 秒深度調息（**吸氣 5 秒 ➔ 呼氣 10 秒**）：")

    st.markdown(
        """
        <div class="breath-bubble">🐿️</div>
        <div style="text-align:center; font-size:0.88rem; color:#C2A675; margin-bottom:18px;">
            【吸氣 5 秒 ➔ 呼氣 10 秒 ‧ 0.067Hz 迷走神經共振中】
        </div>
    """,
        unsafe_allow_html=True,
    )

    # 冒險拋接與數據封存
    if st.button("🚀 完成冒險並將松果金鑰拋接至診間", use_container_width=True):
        now_dt = datetime.datetime.now()
        cur_token = st.session_state["patient_token"]
        calc_score = round(random.uniform(91.0, 98.2), 1)
        calc_sleep = round(random.uniform(6.8, 8.0), 1)

        # 50 款飲品動態匹配運算
        drink_idx = (now_dt.day + now_dt.hour + int(calc_score)) % len(BEVERAGE_PRESCRIPTIONS)
        rec_drink = BEVERAGE_PRESCRIPTIONS[drink_idx]

        # 寫入共享資料庫 (保證醫師端 100% 抓得到)
        global_db[cur_token] = {
            "status": "已完成診前 15s 共振調息",
            "coherence_score": calc_score,
            "stress_index": chosen_stone_label.split(" ")[0],
            "stress_desc": f"{chosen_stone_label.split(' ')[0]} ‧ 諧振良好",
            "sleep_hours": calc_sleep,
            "timestamp": now_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "weekly_trend": [
                calc_score - 7,
                calc_score - 4,
                calc_score - 3,
                calc_score - 5,
                calc_score - 2,
                calc_score - 1,
                calc_score,
            ],
            "nudge": f"探險家完成 {chosen_stone_label.split(' ')[0]} 原石共鳴。心流諧振指數達 {calc_score}%，狀態極佳。",
            "summary": f"【去敏身心軌跡】個案透過安全照片雜湊登入（{cur_token}），於畫布完成 {canvas_strokes} 筆原石特徵解算與 0.067Hz 呼吸引導。心流一致性達 {calc_score}%。",
            "beverage_recommendation": rec_drink,
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

        # 專屬冒險光效與飛鴿傳送信號
        st.markdown(
            f"""
            <div style="background:linear-gradient(135deg, #1C2B20 0%, #111B14 100%); border:2px solid #C2A675; border-radius:24px; padding:26px; text-align:center; margin-top:22px; box-shadow:0 0 35px rgba(194, 166, 117, 0.3);">
                <div style="font-size:3rem; margin-bottom:8px;">🗝️ 🐿️ 🕊️</div>
                <h3 style="color:#C2A675; font-family:Garamond, serif; margin:0 0 10px 0; font-size:1.45rem;">✨ 探險印記已封存！松果金鑰安全送達診間 ✨</h3>
                <div style="font-size:1.05rem; color:#FAF8F5; line-height:1.8;">
                    專屬動態時間鎖短碼：<b style="color:#C2A675; font-size:1.4rem; font-family:monospace;">{cur_token}</b><br>
                    心流諧振評分：<b>{calc_score}%</b> ｜ 靈魂原石：<b>{chosen_stone_label.split(' ')[0]}</b><br>
                    🍵 今日專屬診間處方：<b>{rec_drink}</b>
                </div>
                <div style="font-size:0.86rem; color:#A2B3A7; margin-top:14px; background:rgba(0,0,0,0.3); padding:10px; border-radius:12px;">
                    🕊️ 皇家郵政信鴿 信哥 已安全將數據拋接至郭院長診間！請於看診時出示此短碼進行 15 秒瞬間對照解鎖。
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )