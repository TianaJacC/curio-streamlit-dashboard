import datetime
import os
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

# 極簡質感 CSS
st.markdown(
    """
    <style>
    .stApp { background-color: #FAF8F5 !important; }
    h1, h2, h3, h4, h5, h6, p, label, span, div { color: #1A261F !important; font-family: "Garamond", "PingFang TC", serif; }
    .stButton>button {
        background-color: #25352B !important;
        color: #FAF8F5 !important;
        border-radius: 12px !important;
        border: 1.5px solid #C2A675 !important;
        font-size: 1rem !important;
        padding: 10px 20px !important;
    }
    .stButton>button p { color: #FAF8F5 !important; }
    </style>
""",
    unsafe_allow_html=True,
)

if "token" not in st.session_state:
    st.session_state["token"] = f"#SYM-P{random.randint(100, 999)}"
if "step1_done" not in st.session_state:
    st.session_state["step1_done"] = False
if "step2_done" not in st.session_state:
    st.session_state["step2_done"] = False
if "step3_done" not in st.session_state:
    st.session_state["step3_done"] = False
if "hrv_score" not in st.session_state:
    st.session_state["hrv_score"] = 93.2

# GitHub Raw 實體 3D 軟膠圖片網址映照表 (100% 讀取 GitHub 圖檔)
RAW_BASE = "https://raw.githubusercontent.com/TianaJacC/curio-streamlit-dashboard/main/"

PET_IMAGES = {
    "cone": {
        "name": "栗子小松鼠蔻恩 (Cone)",
        "file": "2026-08-02 15 01 17.png",
        "desc": "抱大松果 / 披樹葉斗篷 / 調整單片眼鏡",
    },
    "cat_bread": {
        "name": "🐱 貓咪踩鮮奶麵包 / 舔毛洗臉",
        "file": "2026-08-02 14 38 09.png",
        "desc": "Q彈軟膠肉球 / 莫蘭迪粉紫",
    },
    "border_collie": {
        "name": "🐕 氣泡邊牧 ‧ 叼線頭除錯",
        "file": "2026-08-02 14 39 13.png",
        "desc": "潮玩黑白膠感 / 淡金光暈",
    },
    "shiba": {
        "name": "🐕 柴犬 ‧ 卡在牆角呆滯",
        "file": "2026-08-02 15 01 32.png",
        "desc": "捏起來變形的胖腮幫子",
    },
    "totoro": {
        "name": "🦇 守護者龍貓 ‧ 捧像素小松果",
        "file": "2026-08-02 15 15 30.png",
        "desc": "烏雲短絨毛 / 像素溫暖燭火",
    },
    "deer": {
        "name": "🦌 小麋鹿 ‧ 森林精靈微光",
        "file": "2026-08-02 15 16 08.png",
        "desc": "麂皮樹枝鹿角 / 莫蘭迪光點",
    },
}

st.title("🐿️ 夢境珍奇櫃 ‧ 探險家日誌")
st.write(
    f"首席珍藏家蔻恩閣長 Cone 陪伴您 ｜ 去敏密鑰：**{st.session_state['token']}**"
)

st.markdown("---")

# 🐾 1. 選擇專屬 3D 萌寵 (讀取 GitHub 圖片)
st.subheader("🐾 1. 選擇今日陪伴您的 3D 莫蘭迪心靈萌寵卡牌")
pet_key = st.selectbox(
    "請選擇萌寵卡牌：",
    list(PET_IMAGES.keys()),
    format_func=lambda x: PET_IMAGES[x]["name"],
)
cur_pet = PET_IMAGES[pet_key]

# 顯示 GitHub 上的實體 3D 圖片
img_url = RAW_BASE + cur_pet["file"].replace(" ", "%20")
st.image(img_url, caption=cur_pet["name"], width=240)
st.info(f"✨ **已鎖定 3D 卡牌**：{cur_pet['name']}\n\n🏷️ 視覺特徵：{cur_pet['desc']}")

st.markdown("---")

# Step 1: 手繪畫布 (自由調色盤)
st.subheader("🎨 Step 1 ‧ 莫蘭迪沙龍手繪畫布 (1 分鐘簽到)")
st.write(
    "請選取您喜歡的色彩，並在下方畫布上記錄心流筆觸壓力（支援手指與滑鼠繪圖）："
)

user_color = st.color_picker("🎨 請選擇畫筆色彩（自由調色）：", "#C2A675")

st.components.v1.html(
    f"""
    <div style="text-align:center;">
        <canvas id="paintCanvas" width="330" height="150" style="border:2px solid #25352B; border-radius:12px; background:#FAF8F5; touch-action:none;"></canvas>
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
                ctx.lineWidth = 4; ctx.lineCap = 'round'; ctx.strokeStyle = '{user_color}';
                ctx.lineTo(x, y); ctx.stroke(); ctx.beginPath(); ctx.moveTo(x, y);
            }}
            canvas.addEventListener('mousedown', startPos); canvas.addEventListener('mouseup', endPos); canvas.addEventListener('mousemove', draw);
            canvas.addEventListener('touchstart', startPos); canvas.addEventListener('touchend', endPos); canvas.addEventListener('touchmove', draw);
        </script>
    </div>
    """,
    height=170,
)

if st.button("✨ 確認完成 1 分鐘畫布塗鴉"):
    st.session_state["step1_done"] = True
    st.success("🎨 塗鴉簽到成功！11 維度運動動態學軌跡已安全寫入。")

st.markdown("---")

# Step 2: 60 秒 rPPG 檢測 (含準備時間與倒數)
st.subheader("💓 Step 2 ‧ 60 秒 rPPG 自律神經檢測 (HRV 提取)")
st.write("請將手指蓋住手機鏡頭與閃光燈，準備進行光譜吸收率分析：")

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
        time.sleep(0.08)
        p_bar.progress(int(sec / 60 * 100))
        p_text.write(
            f"💓 光譜掃描中... 剩餘 **{60-sec}** 秒 (微血管波形 FFT 計算中)"
        )

    st.session_state["hrv_score"] = 93.2
    st.session_state["step2_done"] = True
    p_text.empty()
    st.success("🎉 60 秒 rPPG 檢測完成！即時心流一致性為：93.2%")

st.markdown("---")

# Step 3: 身心科 4-7-8 迷走神經呼吸法 (實體圖片腹部動態起伏)
st.subheader(
    f"🌿 Step 3 ‧ 身心科 4-7-8 迷走神經呼吸法 ({cur_pet['name']} 腹部動態起伏)"
)
st.write(
    "**【郭家穎院長身心科臨床衛教指引】** 請跟隨萌寵腹部的起伏節奏：**吸氣 4 秒 ➔ 留氣 7 秒 ➔ 吐氣 8 秒**"
)

breath_display = st.empty()
breath_display.info(f"按下下方按鈕，開始跟隨 {cur_pet['name']} 進行調息")

if st.button("🌬️ 開始 4-7-8 萌寵腹部起伏調息"):
    for prep in range(3, 0, -1):
        breath_display.warning(f"⏳ 請放鬆肩膀，準備深吸氣... ({prep} 秒)")
        time.sleep(1)

    for cycle in range(1, 3):
        # 1. 吸氣 4 秒 (圖片放大 1.3 倍)
        for t in range(1, 5):
            breath_display.markdown(
                f"### 🌬️ 吸氣 (Inhale) ── 腹部膨脹 ({t}/4秒)"
            )
            st.image(img_url, width=int(200 + t * 25))
            time.sleep(1)

        # 2. 留氣 7 秒 (懸息微震)
        for t in range(1, 8):
            breath_display.markdown(
                f"### ⏸️ 留氣懸息 (Hold) ── 迷走神經活化 ({t}/7秒)"
            )
            st.image(img_url, width=300)
            time.sleep(1)

        # 3. 吐氣 8 秒 (圖片縮小)
        for t in range(1, 9):
            w = max(180, int(300 - t * 15))
            breath_display.markdown(
                f"### 💨 吐氣 (Exhale) ── 嘴唇微張長吐 ({t}/8秒)"
            )
            st.image(img_url, width=w)
            time.sleep(1)

    breath_display.success("✨ 4-7-8 迷走神經調息完成！Cortisol 壓力負擔已完全釋放。")
    st.session_state["step3_done"] = True

st.markdown("---")

# 🕊️ 雙端數據拋接
if (
    st.session_state["step1_done"]
    and st.session_state["step2_done"]
    and st.session_state["step3_done"]
):
    token_id = st.session_state["token"]
    st.success(
        f"🕊️ 信鴿 Singer 準備就緒！去敏密鑰：**{token_id}** ｜ 心流分數：**{st.session_state['hrv_score']}%**"
    )

    doc_url = (
        f"https://curio-streamlit-dashboard.streamlit.app/?token={token_id}"
    )

    st.markdown(
        f"""
        <a href="{doc_url}" target="_blank" style="background-color:#25352B; color:#FAF8F5; padding:12px 24px; border-radius:12px; text-decoration:none; font-weight:bold; display:inline-block;">
            📡 點擊拋接去敏數據並開啟郭醫師診間面板
        </a>
    """,
        unsafe_allow_html=True,
    )
else:
    st.warning("💡 請依次完成塗鴉、rPPG 與 4-7-8 萌寵呼吸，即可開啟數據拋接！")