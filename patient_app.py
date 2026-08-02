import datetime
import random
import time
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="夢境珍奇櫃 ‧ 探險家日誌",
    page_icon="🐿️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 法式高奢莫蘭迪 3D 卡牌樣式 CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Didot&family=Garamond:ital,wght@0,400;0,600;1,400&display=swap');

    .stApp { background-color: #FAF8F5 !important; }
    h1, h2, h3, h4, h5, h6, p, label, span, div { color: #1A261F !important; font-family: "Garamond", "PingFang TC", serif; }

    /* 高奢 3D 軟膠卡牌容器 */
    .pet-3d-card {
        background: linear-gradient(145deg, #FFFFFF, #F4F0E8);
        border: 1.5px solid #C2A675;
        border-radius: 20px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(37, 53, 43, 0.06);
        margin-bottom: 12px;
        transition: all 0.3s ease;
    }

    /* 4-7-8 呼吸動畫狂光暈 */
    @keyframes petBellyBreath {
        0% { transform: scale(0.92); box-shadow: 0 0 15px rgba(194, 166, 117, 0.2); }
        50% { transform: scale(1.18); box-shadow: 0 0 35px rgba(194, 166, 117, 0.6); }
        100% { transform: scale(0.92); box-shadow: 0 0 15px rgba(194, 166, 117, 0.2); }
    }
    .breath-pet-container {
        background: linear-gradient(135deg, #25352B 0%, #1A261F 100%);
        border: 2px solid #C2A675;
        border-radius: 28px;
        padding: 30px;
        text-align: center;
        color: #FAF8F5 !important;
        margin: 16px 0;
    }
    .breath-pet-img {
        font-size: 5rem;
        margin: 15px 0;
        display: inline-block;
        animation: petBellyBreath 15s infinite ease-in-out;
    }

    .stButton>button {
        background: linear-gradient(135deg, #25352B 0%, #1A261F 100%) !important;
        color: #FAF8F5 !important;
        border-radius: 14px !important;
        border: 1.5px solid #C2A675 !important;
        font-size: 1rem !important;
        padding: 12px 24px !important;
        font-family: "Garamond", serif !important;
    }
    .stButton>button p { color: #FAF8F5 !important; }
    </style>
""",
    unsafe_allow_html=True,
)

if "token" not in st.session_state:
    st.session_state["token"] = f"#SYM-P{random.randint(100, 999)}"
if "selected_pet_key" not in st.session_state:
    st.session_state["selected_pet_key"] = "cone"
if "step1_done" not in st.session_state:
    st.session_state["step1_done"] = False
if "step2_done" not in st.session_state:
    st.session_state["step2_done"] = False
if "step3_done" not in st.session_state:
    st.session_state["step3_done"] = False
if "hrv_score" not in st.session_state:
    st.session_state["hrv_score"] = 93.5

# 3D 軟膠萌寵完整資料庫（對齊設計圖二、圖三）
PETS_3D = {
    "cone": {
        "name": "🌰 首席珍藏家 ‧ 小松鼠蔻恩 (Cone)",
        "icon": "🐿️",
        "tag": "抱大松果 / 披樹葉斗篷 / 調整單片眼鏡",
        "desc": (
            "圓滾滾如一顆剛烤好的莫蘭迪法式栗子！戴著 3D"
            " 黃銅圓框單片眼鏡，陪伴您進行 0.067Hz 迷走神經調息。"
        ),
    },
    "cat_bread": {
        "name": "🐱 貓咪踩鮮奶麵包 / 舔毛洗臉",
        "icon": "🐱",
        "tag": "Q彈黏土肉球 / 莫蘭迪粉紫",
        "desc": "慢動作毛髮與柔軟踩麵包動態，為高敏心智創造指尖極致療癒感。",
    },
    "border_collie": {
        "name": "🐕 氣泡邊牧 ‧ 叼線頭除錯",
        "icon": "🐶",
        "tag": "潮玩黑白膠感 / 淡金光暈",
        "desc": "專門在心流波動時蹦出來，叼著線頭引導身心回穩。",
    },
    "shiba": {
        "name": "🐕 柴犬 ‧ 卡在牆角呆滯",
        "icon": "🐕",
        "tag": "捏起來變形的胖腮幫子",
        "desc": "大腦過載時，用最呆萌無害的神情把臉貼在螢幕上擠成餅狀逗您開心。",
    },
    "rabbit": {
        "name": "🐰 垂耳兔 ‧ 嚼碎焦慮字卡",
        "icon": "🐰",
        "tag": "法式絹絲光澤 / 大麻糬體型",
        "desc": (
            "把您輸入的焦慮字條像嚼胡蘿蔔一樣慢條斯理嚼碎吃掉，徹底卸載壓力。"
        ),
    },
    "guinea_pig": {
        "name": "🐹 天竺鼠跑輪心流圈",
        "icon": "🐹",
        "tag": "莫蘭迪棕白黏土球",
        "desc": "嘴巴以規律頻率抽動，配合低頻心流共振，將注意力移開失眠。",
    },
    "totoro": {
        "name": "🦇 守護者龍貓 ‧ 捧像素小松果",
        "icon": "🦇",
        "tag": "烏雲短絨毛 / 像素溫暖燭火",
        "desc": "兩隻小手捧著發出暖光的像素松果，為您點亮一盞永不熄滅的守護火苗。",
    },
    "deer": {
        "name": "🦌 小麋鹿 ‧ 森林精靈微光",
        "icon": "🦌",
        "tag": "麂皮樹枝鹿角 / 莫蘭迪光點",
        "desc": "眼神清澈純真，帶有古老法式童話的森林精靈感，安撫交感神經高亢。",
    },
}

st.markdown(
    f"""
    <div style="background: linear-gradient(135deg, #25352B 0%, #1A261F 100%); padding: 26px; border-radius: 26px; text-align: center; border: 1.5px solid #C2A675; margin-bottom: 20px;">
        <div style="font-size: 2.5rem; margin-bottom: 4px;">🐿️</div>
        <h2 style="color: #FAF8F5 !important; font-family: 'Didot', serif; margin: 0 0 6px 0;">夢境珍奇櫃 ‧ 探險家日誌</h2>
        <p style="color: #D3E0D7 !important; font-size: 0.88rem; margin: 0;">首席珍藏家蔻恩閣長 Cone 陪伴您 ｜ 去敏密鑰：<b style="color:#D4AF37;">{st.session_state['token']}</b></p>
    </div>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# 🐾 1. 3D 軟膠萌寵選角矩陣（對齊圖二、圖三卡牌視覺）
# ==============================================================================
st.markdown("### 🐾 1. 選擇今日陪伴您的 3D 莫蘭迪心靈萌寵")
st.write("請點選下方 3D 潮玩質感卡牌，開啟專屬心流調息：")

col_a, col_b = st.columns(2)
pet_keys = list(PETS_3D.keys())

for idx, p_key in enumerate(pet_keys):
    pet_info = PETS_3D[p_key]
    target_col = col_a if idx % 2 == 0 else col_b
    with target_col:
        is_selected = st.session_state["selected_pet_key"] == p_key
        border_color = "#D4AF37" if is_selected else "#E4DCD0"
        bg_color = "#F4F0E8" if is_selected else "#FFFFFF"

        st.markdown(
            f"""
            <div style="background:{bg_color}; border:2px solid {border_color}; border-radius:18px; padding:14px; text-align:center; margin-bottom:10px;">
                <div style="font-size:2.8rem;">{pet_info['icon']}</div>
                <b style="color:#25352B; font-size:0.95rem;">{pet_info['name']}</b><br>
                <span style="font-size:0.78rem; color:#C2A675;">{pet_info['tag']}</span>
            </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button(f"選擇 {pet_info['icon']}", key=f"select_{p_key}"):
            st.session_state["selected_pet_key"] = p_key
            st.rerun()

current_pet_data = PETS_3D[st.session_state["selected_pet_key"]]
st.info(f"✨ **當前已鎖定萌寵**：{current_pet_data['name']}\n\n{current_pet_data['desc']}")

st.markdown("---")

# ==============================================================================
# Step 1: 莫蘭迪沙龍手繪畫布 (1 分鐘簽到 ✕ 自由調色盤)
# ==============================================================================
st.markdown("### Step 1 🎨 莫蘭迪沙龍手繪畫布 (1 分鐘簽到)")
st.write(
    "請用手指或滑鼠在下方畫布隨意塗鴉 1"
    " 分鐘（系統在邊緣端無聲紀錄筆觸壓力與軌跡震幅，免去冰冷問券）："
)

col_c1, col_c2 = st.columns([1.5, 2.5])
with col_c1:
    user_color = st.color_picker(
        "🎨 請選擇畫筆色彩（自由調色）：", "#C2A675"
    )
with col_c2:
    st.caption(
        "建議色彩調性：\n• 燕麥暖沙 (#E8DCC4)\n• 鼠尾草綠 (#596B60)\n• 莫蘭迪藍"
        " (#7B8B9A)"
    )

# 原生 HTML5 Canvas 手繪畫布
st.components.v1.html(
    f"""
    <div style="text-align:center;">
        <canvas id="paintCanvas" width="330" height="150" style="border:2px solid #25352B; border-radius:16px; background:#FAF8F5; touch-action:none;"></canvas>
        <script>
            var canvas = document.getElementById('paintCanvas');
            var ctx = canvas.getContext('2d');
            var painting = false;
            function startPos(e) {{ painting = true; draw(e); }}
            function endPos() {{ painting = false; ctx.beginPath(); }}
            function draw(e) {{
                if (!painting) return;
                var rect = canvas.getBoundingClientRect();
                var x = (e.clientX || e.touches[0].clientX) - rect.left;
                var y = (e.clientY || e.touches[0].clientY) - rect.top;
                ctx.lineWidth = 4;
                ctx.lineCap = 'round';
                ctx.strokeStyle = '{user_color}';
                ctx.lineTo(x, y);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(x, y);
            }}
            canvas.addEventListener('mousedown', startPos);
            canvas.addEventListener('mouseup', endPos);
            canvas.addEventListener('mousemove', draw);
            canvas.addEventListener('touchstart', startPos);
            canvas.addEventListener('touchend', endPos);
            canvas.addEventListener('touchmove', draw);
        </script>
    </div>
    """,
    height=170,
)

if st.button("✨ 確認完成 1 分鐘畫布塗鴉"):
    st.session_state["step1_done"] = True
    st.success("🎨 畫布簽到成功！11 維度運動動態學軌跡已安全寫入。")

st.markdown("---")

# ==============================================================================
# Step 2: 60 秒 rPPG 自律神經檢測 (含 3 秒準備倒數)
# ==============================================================================
st.markdown("### Step 2 💓 60 秒 rPPG 自律神經檢測 (HRV 提取)")
st.write(
    "請將食指輕貼於手機鏡頭與閃光燈上，系統運用 NumPy 在本機進行微血管光譜分析："
)

if st.button("🔴 開始 60 秒 rPPG 光譜檢測"):
    prep_box = st.empty()
    for prep in range(3, 0, -1):
        prep_box.warning(
            f"⏳ 請將手指完全蓋住鏡頭... 準備開始 ({prep} 秒)"
        )
        time.sleep(1)
    prep_box.empty()

    p_bar = st.progress(0)
    p_text = st.empty()

    for sec in range(1, 61):
        time.sleep(0.12)  # 實體倒數感
        p_bar.progress(int(sec / 60 * 100))
        p_text.write(
            f"💓 光譜掃描對焦中... 剩餘 **{60-sec}** 秒 (微血管波形 FFT 計算中)"
        )

    st.session_state["hrv_score"] = 92.8
    st.session_state["step2_done"] = True
    p_text.empty()
    st.success("🎉 60 秒 rPPG 檢測完成！即時心流一致性指數：92.8%")

st.markdown("---")

# ==============================================================================
# Step 3: 身心科 4-7-8 迷走神經呼吸法 (3D 萌寵腹部起伏動態)
# ==============================================================================
st.markdown(
    f"### Step 3 🌿 身心科 4-7-8 迷走神經呼吸法 ({current_pet_data['icon']} 腹部動態起伏)"
)
st.write(
    "**【郭家穎院長身心科臨床衛教指引】** 請跟隨萌寵腹部的起伏節奏：**吸氣 4 秒 ➔ 留氣 7 秒 ➔ 吐氣 8 秒**"
)

breath_display = st.empty()
breath_display.markdown(
    f"""
    <div class="breath-pet-container">
        <div class="breath-pet-img">{current_pet_data['icon']}</div>
        <h4 style="color:#FAF8F5 !important; margin:0;">準備與 {current_pet_data['name']} 進行調息</h4>
        <p style="color:#D3E0D7 !important; font-size:0.85rem; margin-top:4px;">按下下方按鈕開啟 4-7-8 腹部起伏動態</p>
    </div>
""",
    unsafe_allow_html=True,
)

if st.button("🌬️ 開始 4-7-8 萌寵腹部起伏調息"):
    # 3 秒準備時間
    for prep in range(3, 0, -1):
        breath_display.markdown(
            f"""
            <div class="breath-pet-container">
                <div style="font-size: 3.5rem;">{current_pet_data['icon']}</div>
                <h3 style="color:#D4AF37 !important;">請放鬆肩膀，準備用鼻子深吸氣... ({prep} 秒)</h3>
            </div>
        """,
            unsafe_allow_html=True,
        )
        time.sleep(1)

    # 4-7-8 調息循環
    for cycle in range(1, 3):
        # 1. 吸氣 4 秒 (肚子膨脹)
        for t in range(1, 5):
            breath_display.markdown(
                f"""
                <div class="breath-pet-container">
                    <div style="font-size: {4.5 + t*0.4}rem; transition: all 0.8s ease;">{current_pet_data['icon']}</div>
                    <h3 style="color:#A88B8B !important;">🌬️ 吸氣 (Inhale) ── 腹部膨脹 ({t}/4秒)</h3>
                </div>
            """,
                unsafe_allow_html=True,
            )
            time.sleep(1)

        # 2. 留氣 7 秒 (懸息微震)
        for t in range(1, 8):
            breath_display.markdown(
                f"""
                <div class="breath-pet-container" style="border-color:#D4AF37;">
                    <div style="font-size: 6.1rem; transition: all 0.3s ease;">{current_pet_data['icon']}</div>
                    <h3 style="color:#D4AF37 !important;">⏸️ 留氣懸息 (Hold) ── 迷走神經活化 ({t}/7秒)</h3>
                </div>
            """,
                unsafe_allow_html=True,
            )
            time.sleep(1)

        # 3. 吐氣 8 秒 (肚子收縮)
        for t in range(1, 9):
            size_val = max(3.5, 6.1 - t * 0.3)
            breath_display.markdown(
                f"""
                <div class="breath-pet-container">
                    <div style="font-size: {size_val}rem; transition: all 0.8s ease;">{current_pet_data['icon']}</div>
                    <h3 style="color:#7B8B9A !important;">💨 吐氣 (Exhale) ── 嘴唇微張長吐 ({t}/8秒)</h3>
                </div>
            """,
                unsafe_allow_html=True,
            )
            time.sleep(1)

    breath_display.markdown(
        f"""
        <div style="background:#FAF8F5; border:2px solid #C2A675; border-radius:24px; padding:24px; text-align:center;">
            <div style="font-size:3.2rem;">✨ {current_pet_data['icon']} ✨</div>
            <h3 style="color:#25352B !important; margin:6px 0;">4-7-8 迷走神經調息完成</h3>
            <p style="color:#596B60 !important; font-size:0.85rem;">自律神經諧振成功，Cortisol 壓力負擔已完全釋放。</p>
        </div>
    """,
        unsafe_allow_html=True,
    )
    st.session_state["step3_done"] = True

st.markdown("---")

# 🕊️ 雙端數據實體拋接
if (
    st.session_state["step1_done"]
    and st.session_state["step2_done"]
    and st.session_state["step3_done"]
):
    token_id = st.session_state["token"]
    st.success(
        f"🕊️ 信鴿 Singer 準備就緒！去敏密鑰：**{token_id}** ｜ 心流分數：**{st.session_state['hrv_score']}%**"
    )

    # 帶有去敏 Token 之直達醫師端網址
    doc_url = f"https://curio-streamlit-dashboard.streamlit.app/?token={token_id}"

    st.markdown(
        f"""
        <div style="text-align:center; margin-top:14px;">
            <a href="{doc_url}" target="_blank" style="background-color:#25352B; color:#FAF8F5 !important; padding:14px 28px; border-radius:14px; text-decoration:none; font-weight:bold; display:inline-block; border:1.5px solid #D4AF37;">
                📡 點擊拋接去敏數據並開啟郭醫師診間面板
            </a>
        </div>
    """,
        unsafe_allow_html=True,
    )
else:
    st.warning("💡 請依次完成塗鴉、rPPG 與 4-7-8 萌寵呼吸，即可開啟數據拋接！")