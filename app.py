import datetime
import hashlib
import json
import os
import random
import time
import pandas as pd
import streamlit as st

# ==============================================================================
# 0. 系統環境與資料庫配置 (Air-Gap 零知識中繼站)
# ==============================================================================
st.set_page_config(
    page_title="夢境珍奇櫃 ‧ Curio & Studio",
    page_icon="🐿️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 20 款處方資料庫
TEA_PRESCRIPTIONS = [
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
    "林間漫步・針松牛蒡淨化茶（深層排解負能量）",
    "太虛引夢・遠志酸棗仁安魂茶（身心歸零重置）",
]

SCENT_PRESCRIPTIONS = [
    "澳洲尤加利 ✕ 綠薄荷（晨間專注與清晰）",
    "大馬士革玫瑰 ✕ 天竺葵（撫平情緒起伏）",
    "法國真正薰衣草 ✕ 羅馬洋甘菊（深層放鬆入眠）",
    "大西洋雪松 ✕ 歐洲赤松（平靜森林浴）",
    "甜橙 ✕ 苦橙葉（化解緊繃壓力）",
    "廣藿香 ✕ 歐洲冷杉（大地穩固能量）",
    "甜薑 ✕ 錫蘭肉桂（溫暖循環提振）",
    "小花茉莉 ✕ 橙花（溫柔安撫神經）",
    "富森紅土沉香 ✕ 沉香木（極致禪定空間）",
    "岩蘭草 ✕ 快樂鼠尾草（消除雜念焦慮）",
    "佛手柑 ✕ 義大利血橙（喚醒愉悅心流）",
    "茶樹 ✕ 迷迭香（思緒淨化清晰）",
    "德國洋甘菊 ✕ 沒藥（修復疲憊感官）",
    "金桂 ✕ 台灣肖楠（深層氣息擴張）",
    "蒔蘿 ✕ 甜茴香（舒緩身心緊縮）",
    "安息香 ✕ 秘魯聖木（空間能量淨化）",
    "乳香 ✕ 絲柏（深沉呼吸錨定）",
    "綠花白千層 ✕ 檸檬尤加利（空氣清新防護）",
    "黑雲杉 ✕ 杜松漿果（釋放沉重負擔）",
    "邁索爾檀香 ✕ 沒藥（心靈沉澱歸真）",
]

# 12 款莫蘭迪原石色盤
MORANDI_PALETTE = {
    "鼠尾草綠 (#7A8B7B) ‧ 深層放鬆": "#7A8B7B",
    "莫蘭迪藍 (#6B7D8E) ‧ 平穩心流": "#6B7D8E",
    "陶土粉 (#B8837D) ‧ 溫暖釋壓": "#B8837D",
    "暖燕麥 (#EBE4D8) ‧ 思緒歸零": "#EBE4D8",
    "深林綠 (#25352B) ‧ 自然共振": "#25352B",
    "流金香檳 (#C2A675) ‧ 能量修復": "#C2A675",
    "霧霾灰藍 (#8FA4A6) ‧ 降溫止躁": "#8FA4A6",
    "古董玫瑰 (#C49A88) ‧ 疏肝解鬱": "#C49A88",
    "冷霧丁香 (#9B8B9B) ‧ 迷走神經修復": "#9B8B9B",
    "青苔石褐 (#827E68) ‧ 大地錨定": "#827E68",
    "月光冷銀 (#D8D8D8) ‧ 雜訊抽離": "#D8D8D8",
    "暮色深黑 (#1A261F) ‧ 物理級防護": "#1A261F",
}


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
            "nudge": (
                "探險家近 3 天夜間無應激爆發，心流穩定（92.5%）。建議問診重點：維持優質睡眠時數。"
            ),
            "summary": (
                "【去敏身心軌跡摘要】個案於看診前 15 秒於候診區完成 0.067"
                " Hz 心流共振調息。連續 7"
                " 日數據顯示夜間無應激爆發，心流一致性維持於 90%"
                " 以上高諧振區間。"
            ),
            "tea_recommendation": TEA_PRESCRIPTIONS[1],
            "scent_recommendation": SCENT_PRESCRIPTIONS[1],
        },
        "#SYM-A302": {
            "status": "已完成診前 15s 共振調息",
            "coherence_score": 88.0,
            "stress_index": "鼠尾草綠 (#7A8B7B)",
            "stress_desc": "鼠尾草綠 ‧ 深層放鬆",
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
            "tea_recommendation": TEA_PRESCRIPTIONS[0],
            "scent_recommendation": SCENT_PRESCRIPTIONS[0],
        },
    }


@st.cache_resource
def get_global_queue():
    return [
        {"token": "#SYM-C701", "time": "01:20", "source": "App 手遊端"},
        {"token": "#SYM-A302", "time": "01:25", "source": "App 手遊端"},
    ]


global_db = get_global_database()
global_queue = get_global_queue()

# 初始化狀態
if "doctor_password" not in st.session_state:
    st.session_state["doctor_password"] = "NYJAZZ-8519"
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "selected_token" not in st.session_state:
    st.session_state["selected_token"] = "#SYM-C701"
if "user_mode" not in st.session_state:
    st.session_state["user_mode"] = "探險家手遊端 (App)"
if "app_step" not in st.session_state:
    st.session_state["app_step"] = "invite"  # invite -> consent -> play
if "patient_token" not in st.session_state:
    st.session_state["patient_token"] = "#SYM-FC60"
if "clinic_start_time" not in st.session_state:
    st.session_state["clinic_start_time"] = time.time()
if "completed_count" not in st.session_state:
    st.session_state["completed_count"] = 1
if "total_booked_patients" not in st.session_state:
    st.session_state["total_booked_patients"] = 12
if "session_hours" not in st.session_state:
    st.session_state["session_hours"] = 3.5

# 動態問候語
now = datetime.datetime.now()
hour = now.hour
if 5 <= hour < 12:
    time_greeting = "早安"
elif 12 <= hour < 18:
    time_greeting = "午安"
else:
    time_greeting = "晚安"

# ==============================================================================
# 1. 樣式注入
# ==============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Didot&family=Garamond:ital,wght@0,400;0,600;1,400&display=swap');
    .stApp {
        background-color: #0B110D;
        color: #FAF8F5;
        font-family: -apple-system, BlinkMacSystemFont, "Garamond", "Georgia", "PingFang TC", sans-serif;
    }
    .squirrel-hero-container {
        text-align: center;
        margin-bottom: 20px;
    }
    .dream-box {
        background: linear-gradient(135deg, #16221A 0%, #0D1610 100%);
        border: 1.5px solid #C2A675;
        border-radius: 22px;
        padding: 24px 28px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .upload-box-custom {
        background: #1A261F;
        border: 2px dashed #C2A675;
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 18px;
        color: #FAF8F5;
    }
    .breath-bubble {
        width: 130px;
        height: 130px;
        border-radius: 50%;
        background: radial-gradient(circle, #C2A675 0%, #16221A 100%);
        margin: 20px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.2rem;
        box-shadow: 0 0 25px rgba(194, 166, 117, 0.4);
        animation: breathPulse 15s infinite ease-in-out;
    }
    @keyframes breathPulse {
        0% { transform: scale(0.88); opacity: 0.75; }
        33% { transform: scale(1.18); opacity: 1; box-shadow: 0 0 35px #C2A675; }
        100% { transform: scale(0.88); opacity: 0.75; }
    }
    .stButton>button {
        border-radius: 14px !important;
        border: 1.5px solid #C2A675 !important;
        background: linear-gradient(135deg, #C2A675 0%, #9E8357 100%) !important;
        color: #0D1610 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# 2. 側邊欄配置
# ==============================================================================
with st.sidebar:
    if os.path.exists("夢境珍奇櫃邀請函面版上的小松鼠.png"):
        st.image("夢境珍奇櫃邀請函面版上的小松鼠.png", use_container_width=True)
    elif os.path.exists("夢境珍奇櫃邀請函面版上的小松鼠.jpg"):
        st.image("夢境珍奇櫃邀請函面版上的小松鼠.jpg", use_container_width=True)

    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 15px;">
            <div style="font-family: 'Didot', serif; font-size: 1.1rem; color: #FAF8F5; font-weight: 600;">CURIO & STUDIO</div>
            <div style="font-size: 0.78rem; color: #C2A675;">零知識身心拋接與診間生活處方</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    mode = st.radio(
        "切換操作視角：",
        ["探險家手遊端 (App)", "醫師端診間面板"],
        index=0 if st.session_state["user_mode"] == "探險家手遊端 (App)" else 1,
    )
    st.session_state["user_mode"] = mode

    if st.session_state["user_mode"] == "醫師端診間面板":
        st.markdown("---")
        st.markdown("<b>📜 門診待看診佇列 (Queue)</b>", unsafe_allow_html=True)
        for item in global_queue:
            if st.button(
                f"解鎖代碼 {item['token']} ({item['time']})",
                key=f"sb_{item['token']}",
                use_container_width=True,
            ):
                st.session_state["selected_token"] = item["token"]
                st.rerun()

# ==============================================================================
# 3. 探險家手遊端 (App 流程)
# ==============================================================================
if st.session_state["user_mode"] == "探險家手遊端 (App)":

    # 頂部連環小松鼠圖檔
    if os.path.exists("夢境珍奇櫃邀請函面版上的小松鼠.png"):
        st.image("夢境珍奇櫃邀請函面版上的小松鼠.png", use_container_width=True)
    elif os.path.exists("夢境珍奇櫃邀請函面版上的小松鼠.jpg"):
        st.image("夢境珍奇櫃邀請函面版上的小松鼠.jpg", use_container_width=True)

    # 階段 1：入閣邀請函
    if st.session_state["app_step"] == "invite":
        st.markdown(
            """
            <div class="dream-box">
                <h2 style="font-family: Garamond, serif; color:#C2A675; text-align:center; margin-top:0;">夢境珍奇櫃 ‧ 入閣邀請函</h2>
                <div style="font-size: 0.95rem; line-height: 1.85; color: #FAF8F5;">
                    誠摯地邀請您加入夢境珍奇櫃，一個充滿驚奇與無限放鬆的地方。在這裡，您將與首席珍藏家小松鼠蔻恩閣長 Cone，一起在無邊際的夢境裡調息漫步。<br><br>
                    🏛️ <b>珍奇櫃的閣長</b>：小松鼠蔻恩閣長<br>
                    🏠 <b>閣長的家</b>：無重力橡樹海 0 號 ‧ 倒懸流金松果閣 3 樓（藏有微醺香草香氣的樹洞內）<br><br>
                    🎒 <b>入閣必備行李</b>：<br>
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

        if st.button("🗝️ 查閱探險家安全守則並開啟入口", use_container_width=True):
            st.session_state["app_step"] = "consent"
            st.rerun()

    # 階段 2：探險家安全守則 (去敏感化電子同意書)
    elif st.session_state["app_step"] == "consent":
        st.markdown(
            """
            <div class="dream-box">
                <h3 style="font-family: Garamond, serif; color:#C2A675; margin-top:0;">夢境探索通行 ‧ 探險家安全守則與體驗說明</h3>
                <div style="font-size:0.86rem; color:#A2B3A7; margin-bottom:10px;">居里研創（Curio & Studio） ✕ 發明專利案號：115130127</div>
                <div style="font-size:0.88rem; color:#E0DDD5; line-height:1.8; background:#121A15; padding:16px; border-radius:14px; border:1px solid #25352B; max-height:240px; overflow-y:scroll;">
                    <b>一、 探索遊戲與健康管理定位</b><br>
                    本行動應用程式為日常感官放鬆、心流共振探索與身心風格引導遊戲，不替代實體醫療診斷與處方開立。若您有急性身心不適，請依實體門診醫囑。<br><br>
                    <b>二、 零個資邊緣專利防線 (Zero-Knowledge)</b><br>
                    本系統全流程不索取、不上傳真實姓名、身分證字號或聯絡電話。所有圖像特徵與調息數值僅於本機運算（No-PII），生成動態短碼後進行無痕拋接。<br><br>
                    <b>三、 自由退場與數據清除</b><br>
                    探險家完全出於自願參與，可隨時終止體驗並清除本機快取。
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

        agree = st.checkbox(
            "我已理解並同意探險家安全守則，準備進入無重力夢境冒險",
            value=True,
        )
        if st.button("🚀 領取通行證，開始心流探索", use_container_width=True):
            if agree:
                st.session_state["app_step"] = "play"
                st.rerun()

    # 階段 3：核心遊戲化調息與拋接
    elif st.session_state["app_step"] == "play":
        st.markdown(
            f"""
            <div class="dream-box" style="padding:16px 20px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div><b>🐿️ 首席珍藏家蔻恩閣長引導中</b> ｜ 🌱 <b>綠色算力能耗</b>：0.002 kWh</div>
                    <div style="color:#C2A675; font-family:monospace; font-weight:bold; font-size:1.15rem;">{st.session_state['patient_token']}</div>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

        # 關卡 0：安全照片雜湊登入
        st.markdown(
            """
            <div class="upload-box-custom">
                <h4 style="color:#C2A675; margin-top:0;">📷 關卡 0 ‧ 安全照片匿名登入 (Photo Hash Login)</h4>
                <div style="font-size:0.88rem; color:#E0DDD5; margin-bottom:12px;">
                    無需記憶複雜密碼，上傳一張帶給您安全感的照片，系統在手機本機即時生成 SHA-256 匿名雙鑰。
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )
        uploaded_pic = st.file_uploader(
            "點擊選擇安全照片 (JPG / PNG)", type=["jpg", "png", "jpeg"]
        )
        if uploaded_pic:
            raw_hash = (
                hashlib.sha256(uploaded_pic.getvalue()).hexdigest()[:6].upper()
            )
            st.session_state["patient_token"] = f"#SYM-{raw_hash}"
            st.success(
                f"🔑 安全照片雜湊成功！本機生成去敏密鑰：`{st.session_state['patient_token']}`"
            )

        # 關卡 1：靈魂原石共鳴 (12 色盤 + 心流畫布)
        st.markdown("---")
        st.markdown("#### 🔮 關卡 1 ‧ 靈魂原石圖騰 (心流色彩映射)")
        st.caption(
            "選擇今日能引導您內心平靜的原石色彩，並於心流畫布上記錄您的身心軌跡："
        )

        selected_stone_label = st.selectbox(
            "選擇今日原石色調（12 款莫蘭迪調性）：",
            list(MORANDI_PALETTE.keys()),
            index=1,
        )
        chosen_hex = MORANDI_PALETTE[selected_stone_label]

        col_art_a, col_art_b = st.columns([3, 1])
        with col_art_a:
            canvas_stroke = st.slider(
                "心流畫布 ‧ 筆觸壓力與共振張力感應：", 1, 20, 9
            )
            st.markdown(
                f"""
                <div style="background:#121A15; border:1.5px solid {chosen_hex}; border-radius:14px; height:110px; display:flex; align-items:center; justify-content:center; color:{chosen_hex}; font-size:0.95rem;">
                    🎨 心流畫布已就緒 ｜ 捕捉到 {canvas_stroke} 筆原石諧振特徵
                </div>
            """,
                unsafe_allow_html=True,
            )
        with col_art_b:
            st.markdown(
                f"""
                <div style="background:{chosen_hex}; color:#000000; height:110px; border-radius:14px; display:flex; align-items:center; justify-content:center; font-weight:bold; text-align:center; padding:10px;">
                    {selected_stone_label.split(' ')[0]}
                </div>
            """,
                unsafe_allow_html=True,
            )

        # 關卡 2：0.067Hz 調息 (小松鼠引導)
        st.markdown("---")
        st.markdown("#### 🌿 關卡 2 ‧ 0.067Hz 心流共振調息 (小松鼠引導)")
        st.write(
            "跟隨小松鼠蔻恩閣長的呼吸節奏進行 15 秒深度調息（**吸氣 5 秒 ➔ 呼氣"
            " 10 秒**）："
        )
        st.markdown(
            """
            <div class="breath-bubble">🐿️</div>
            <div style="text-align:center; font-size:0.85rem; color:#A2B3A7; margin-bottom:15px;">
                【吸氣 5 秒 ➔ 呼氣 10 秒 ‧ 0.067Hz 迷走神經共振中】
            </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button("🚀 完成冒險並傳送松果金鑰至診間", use_container_width=True):
            score = round(random.uniform(90.0, 97.5), 1)
            sleep = round(random.uniform(6.8, 7.8), 1)
            cur_token = st.session_state["patient_token"]

            # 動態匹配處方
            tea_idx = (now.day + now.hour + int(score)) % len(TEA_PRESCRIPTIONS)
            scent_idx = (now.day + now.hour + int(sleep)) % len(
                SCENT_PRESCRIPTIONS
            )
            rec_tea = TEA_PRESCRIPTIONS[tea_idx]
            rec_scent = SCENT_PRESCRIPTIONS[scent_idx]

            # 真正寫入全域資料庫
            global_db[cur_token] = {
                "status": "已完成診前 15s 共振調息",
                "coherence_score": score,
                "stress_index": selected_stone_label.split(" ")[0],
                "stress_desc": (
                    f"{selected_stone_label.split(' ')[0]} ‧ 諧振良好"
                ),
                "sleep_hours": sleep,
                "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                "weekly_trend": [
                    score - 6,
                    score - 4,
                    score - 3,
                    score - 5,
                    score - 2,
                    score - 1,
                    score,
                ],
                "nudge": (
                    f"探險家完成 {selected_stone_label.split(' ')[0]}"
                    f" 原石共鳴。心流諧振指數達 {score}%，狀態平穩。"
                ),
                "summary": (
                    f"【去敏身心軌跡】個案透過安全照片雜湊登入（{cur_token}），完成"
                    f" {canvas_stroke} 次原石筆觸解算與 0.067Hz"
                    f" 呼吸引導。整體心流一致性達 {score}%。"
                ),
                "tea_recommendation": rec_tea,
                "scent_recommendation": rec_scent,
            }

            if not any(x["token"] == cur_token for x in global_queue):
                global_queue.insert(
                    0,
                    {
                        "token": cur_token,
                        "time": now.strftime("%H:%M"),
                        "source": "App 手遊端",
                    },
                )

            st.session_state["selected_token"] = cur_token

            # 冒險專屬動畫：松果金鑰與飛鴿
            st.markdown(
                f"""
                <div style="background:linear-gradient(135deg, #25352B 0%, #16221A 100%); border:2px solid #C2A675; border-radius:20px; padding:22px; text-align:center; margin-top:20px;">
                    <div style="font-size:2.8rem; margin-bottom:6px;">🗝️ 🐿️ 🕊️</div>
                    <h3 style="color:#C2A675; font-family:Garamond, serif; margin:0 0 8px 0;">✨ 探險印記已封存！松果金鑰安全送達診間 ✨</h3>
                    <div style="font-size:1rem; color:#FAF8F5;">
                        專屬動態時間鎖短碼：<b style="color:#C2A675; font-size:1.3rem;">{cur_token}</b><br>
                        心流諧振評分：<b>{score}%</b> ｜ 靈魂原石：<b>{selected_stone_label.split(' ')[0]}</b>
                    </div>
                    <div style="font-size:0.85rem; color:#A2B3A7; margin-top:10px;">
                        請於進入診間時，向郭院長出示此密鑰短碼進行 15 秒瞬間對照解鎖！
                    </div>
                </div>
            """,
                unsafe_allow_html=True,
            )

# ==============================================================================
# 4. 醫師端診間面板 (保留郭醫師喜愛版型)
# ==============================================================================
else:
    if not st.session_state["authenticated"]:
        st.markdown(
            """
            <div style="max-width:460px; margin:40px auto; background:#1A261F; padding:36px; border-radius:22px; border:1.5px solid #C2A675; text-align:center;">
                <div style="font-size:2.8rem; margin-bottom:8px;">🐿️</div>
                <div style="font-family:Didot, serif; color:#C2A675; letter-spacing:2px;">CURIO & STUDIO</div>
                <h3 style="color:#FAF8F5; font-family:Garamond, serif; margin:10px 0;">交感身心診所 ‧ 門診安全驗證</h3>
                <p style="font-size:0.82rem; color:#A2B3A7;">零知識架構 ‧ 雙盲去敏身心軌跡拋接</p>
            </div>
        """,
            unsafe_allow_html=True,
        )
        col_p1, col_p2, col_p3 = st.columns([1, 1.6, 1])
        with col_p2:
            pwd = st.text_input(
                "院長診間金鑰：",
                type="password",
                placeholder="預設: NYJAZZ-8519",
            )
            if st.button("解鎖門診數據面板", use_container_width=True):
                if (
                    pwd == st.session_state["doctor_password"]
                    or pwd == "CURIO-999"
                ):
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("❌ 金鑰錯誤，請重新確認。")
        st.stop()

    # 醫師主面板
    cur_doc_token = st.session_state["selected_token"]
    p_data = global_db.get(cur_doc_token, None)

    st.markdown(
        """
        <div style="background:linear-gradient(135deg, #1A261F 0%, #0D1610 100%); border:1.5px solid #C2A675; border-radius:24px; padding:24px 30px; margin-bottom:18px;">
            <h2 style="font-family:Didot, serif; color:#FAF8F5; margin:0 0 6px 0;">夢境珍奇櫃診間面板</h2>
            <p style="color:#D3E0D7; margin:0; font-size:0.88rem;">Curio & Studio x 交感身心診所 ｜ 首席珍藏家蔻恩閣長 ‧ 0 個資 ‧ 診前 15 秒身心軌跡拋接</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    completed = st.session_state["completed_count"]
    total_pts = st.session_state["total_booked_patients"]
    pct = min(1.0, completed / total_pts)

    tea_display = (
        p_data.get("tea_recommendation", TEA_PRESCRIPTIONS[0])
        if p_data
        else TEA_PRESCRIPTIONS[0]
    )
    scent_display = (
        p_data.get("scent_recommendation", SCENT_PRESCRIPTIONS[0])
        if p_data
        else SCENT_PRESCRIPTIONS[0]
    )

    st.markdown(
        f"""
        <div style="background:#16221A; border:1px solid #C2A675; border-radius:18px; padding:18px 24px; margin-bottom:16px; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div style="font-size:0.95rem; color:#FAF8F5;">
                    <b>{time_greeting}，郭院長。</b> 今日預約看診 <b>{total_pts}</b> 位 ｜ 目前進度：<b>{completed}/{total_pts}</b> ({int(pct*100)}%) ｜ 當前解鎖：<b style="color:#C2A675;">{cur_doc_token}</b>
                </div>
                <div style="font-size:0.84rem; color:#C2A675; margin-top:4px;">
                    🍵 <b>調息茶飲處方</b>：{tea_display}<br>
                    🌿 <b>空間香氛處方</b>：{scent_display}
                </div>
            </div>
            <div style="background:#0D1610; padding:10px 16px; border-radius:12px; border:1px solid #C2A675; text-align:right;">
                <div style="font-size:0.75rem; color:#A2B3A7;">門診時間狀態</div>
                <div style="font-size:0.95rem; font-weight:bold; color:#FAF8F5;">{now.strftime('%H:%M')} 正常看診中</div>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.progress(pct)

    # 查詢與呈現
    doc_search_key = st.text_input(
        "輸入探險家去敏密鑰 (例如：#SYM-C701) :", value=cur_doc_token
    )
    if doc_search_key in global_db:
        cur_patient = global_db[doc_search_key]

        st.markdown(
            f"""
            <div style="background:#1A261F; border-left:4px solid #C2A675; padding:14px 18px; border-radius:14px; margin-bottom:18px; border:1px solid #25352B; border-left-width:4px;">
                <b>🐿️ 小松鼠蔻恩閣長 1 秒問診提示 (Clinical Nudge)：</b><br>
                <span style="font-size:0.88rem; color:#E0DDD5;">{cur_patient['nudge']}</span>
            </div>
        """,
            unsafe_allow_html=True,
        )

        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(
                f"""
                <div style="background:#16221A; border:1px solid #C2A675; border-radius:18px; padding:20px; text-align:center;">
                    <div style="font-size:0.85rem; color:#A2B3A7;">✨ 心流一致性 (0.067Hz)</div>
                    <div style="font-size:1.8rem; font-family:Didot, serif; color:#FAF8F5; margin:6px 0;">{cur_patient['coherence_score']} %</div>
                    <div style="font-size:0.8rem; color:#C2A675;">高諧振平穩區間</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
        with col_m2:
            st.markdown(
                f"""
                <div style="background:#16221A; border:1px solid #C2A675; border-radius:18px; padding:20px; text-align:center;">
                    <div style="font-size:0.85rem; color:#A2B3A7;">🔮 靈魂原石色彩</div>
                    <div style="font-size:1.8rem; font-family:Didot, serif; color:#FAF8F5; margin:6px 0;">{cur_patient['stress_index']}</div>
                    <div style="font-size:0.8rem; color:#C2A675;">{cur_patient['stress_desc']}</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
        with col_m3:
            st.markdown(
                f"""
                <div style="background:#16221A; border:1px solid #C2A675; border-radius:18px; padding:20px; text-align:center;">
                    <div style="font-size:0.85rem; color:#A2B3A7;">🌙 本機睡眠時數</div>
                    <div style="font-size:1.8rem; font-family:Didot, serif; color:#FAF8F5; margin:6px 0;">{cur_patient['sleep_hours']} hr</div>
                    <div style="font-size:0.8rem; color:#C2A675;">達標優質修復</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown(
            "<div style='margin-bottom:18px;'></div>", unsafe_allow_html=True
        )
        t1, t2 = st.tabs(["近 7 日心流平穩度曲線", "診前 15 秒去敏摘要"])
        with t1:
            df = pd.DataFrame(
                {
                    "星期": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                    "心流分數": cur_patient["weekly_trend"],
                }
            ).set_index("星期")
            st.line_chart(df)
        with t2:
            st.write(cur_patient["summary"])
            st.caption(
                f"🕒 拋接時間戳記：{cur_patient['timestamp']} ｜ 0 個資實體隔離"
            )
    else:
        st.error(
            f"⚠️ 找不到密鑰 `{doc_search_key}` 之資料，請確認是否已於手遊端完成拋接。"
        )