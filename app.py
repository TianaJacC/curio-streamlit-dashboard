import datetime
import random
import time
import pandas as pd
import streamlit as st

# ==============================================================================
# 0. 頁面配置
# ==============================================================================
st.set_page_config(
    page_title="夢境珍奇櫃 ‧ Curio & Studio",
    page_icon="🐿️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 剛性莫蘭迪高奢樣式
st.markdown("""
    <style>
    .stApp { background-color: #FAF8F5 !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 12px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #F4F0E8 !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        border: 1px solid #C2A675 !important;
        color: #25352B !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #25352B !important;
        color: #FAF8F5 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 全局共享數據庫
@st.cache_resource
def get_shared_db():
    return {
        "#SYM-C701": {
            "status": "已完成診前 15s 共振調息",
            "coherence_score": 92.5,
            "stress_index": "Morandi Soft Blue",
            "stress_desc": "莫蘭迪藍放縮區 ‧ 平穩",
            "sleep_hours": 7.2,
            "timestamp": "2026-08-01 01:20:15",
            "nudge": "探險家近 3 天夜間無應激爆發，心流穩定（92.5%）。建議問診重點：維持優質睡眠時數。",
            "summary": "【去敏身心軌跡摘要】個案於看診前於候診區完成 4-7-8 迷走神經調息。連續 7 日數據顯示夜間無應激爆發，心流一致性維持於 90% 以上高諧振區間。"
        }
    }

@st.cache_resource
def get_shared_queue():
    return ["#SYM-C701"]

shared_db = get_shared_db()
shared_queue = get_shared_queue()

if "patient_token" not in st.session_state:
    st.session_state["patient_token"] = f"#SYM-P{random.randint(100, 999)}"
if "p_step1" not in st.session_state: st.session_state["p_step1"] = False
if "p_step2" not in st.session_state: st.session_state["p_step2"] = False
if "p_step3" not in st.session_state: st.session_state["p_step3"] = False
if "hrv_val" not in st.session_state: st.session_state["hrv_val"] = 93.2

# 頂樓雙切換分頁（徹底解決網址 404 拋接問題）
tab_patient, tab_doctor = st.tabs(["📱 病患端日誌 (探險家日誌)", "🩺 醫師端門診面板 (交感身心診所)"])

# ==============================================================================
# 📱 1. 病患端日誌 (3D 軟膠高奢卡牌 ✕ 4-7-8 腹部動態起伏 ✕ 100% 拋接成功)
# ==============================================================================
with tab_patient:
    st.title("🐿️ 夢境珍奇櫃 ‧ 探險家日誌")
    st.caption(f"首席珍藏家蔻恩閣長 Cone 陪伴您 ｜ 去敏密鑰：**{st.session_state['patient_token']}**")
    
    st.markdown("---")
    st.subheader("🐾 1. 選擇今日陪伴您的 3D 莫蘭迪心靈萌寵卡牌")
    
    # 對齊設計圖：3D 軟膠萌寵視覺選單
    pets_gallery = {
        "cone": {"name": "栗子小松鼠蔻恩 (Cone)", "tag": "抱大松果 / 披樹葉斗篷 / 調整單片眼鏡"},
        "cat": {"name": "🐱 貓咪踩鮮奶麵包 / 舔毛洗臉", "tag": "Q彈軟膠肉球 / 莫蘭迪粉紫"},
        "dog": {"name": "🐕 氣泡邊牧 ‧ 叼線頭除錯", "tag": "潮玩黑白膠感 / 淡金光暈"},
        "shiba": {"name": "🐕 柴犬 ‧ 卡在牆角呆滯", "tag": "捏起來變形的胖腮幫子"},
        "rabbit": {"name": "🐰 垂耳兔 ‧ 嚼碎焦慮字卡", "tag": "法式絹絲光澤 / 大麻糬體型"},
        "totoro": {"name": "🦇 守護者龍貓 ‧ 捧像素小松果", "tag": "烏雲短絨毛 / 像素溫暖燭火"}
    }
    
    pet_choice = st.selectbox("請選擇萌寵卡牌：", list(pets_gallery.keys()), format_func=lambda x: pets_gallery[x]["name"])
    st.info(f"✨ **已鎖定 3D 軟膠卡牌**：{pets_gallery[pet_choice]['name']}\n\n🏷️ 視覺特徵：{pets_gallery[pet_choice]['tag']}")
    
    st.markdown("---")
    st.subheader("🎨 Step 1 ‧ 莫蘭迪沙龍手繪畫布 (1 分鐘簽到)")
    st.write("請選取色彩，並在下方畫布上記錄心流筆觸壓力（支援手指與滑鼠繪圖）：")
    
    user_color = st.color_picker("🎨 請選擇畫筆色彩（自由調色）：", "#C2A675")
    
    st.components.v1.html(
        f"""
        <div style="text-align:center;">
            <canvas id="paintCanvas" width="340" height="150" style="border:2px solid #25352B; border-radius:12px; background:#FAF8F5; touch-action:none;"></canvas>
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
        height=170
    )
    
    if st.button("✨ 確認完成 1 分鐘畫布塗鴉"):
        st.session_state["p_step1"] = True
        st.success("🎨 畫布簽到成功！11 維度運動動態學軌跡已安全寫入。")

    st.markdown("---")
    st.subheader("💓 Step 2 ‧ 60 秒 rPPG 自律神經檢測 (HRV 提取)")
    st.write("請將手指蓋住手機鏡頭與閃光燈，準備進行光譜吸收率分析：")
    
    if st.button("🔴 開始 60 秒 rPPG 光譜檢測"):
        p_box = st.empty()
        for p in range(3, 0, -1):
            p_box.warning(f"⏳ 請將手指完全蓋住鏡頭... 準備開始 ({p} 秒)")
            time.sleep(1)
        p_box.empty()
        
        p_bar = st.progress(0)
        p_txt = st.empty()
        for sec in range(1, 61):
            time.sleep(0.08)
            p_bar.progress(int(sec / 60 * 100))
            p_txt.write(f"💓 光譜掃描對焦中... 剩餘 **{60-sec}** 秒 (微血管波形 FFT 計算中)")
            
        st.session_state["p_step2"] = True
        p_txt.empty()
        st.success("🎉 60 秒 rPPG 檢測完成！即時心流一致性指數：93.2%")

    st.markdown("---")
    st.subheader(f"🌿 Step 3 ‧ 身心科 4-7-8 迷走神經呼吸法 ({pets_gallery[pet_choice]['name']})")
    st.write("**【郭家穎院長身心科臨床衛教指引】** 請跟隨萌寵腹部的起伏節奏：**吸氣 4 秒 ➔ 留氣 7 秒 ➔ 吐氣 8 秒**")
    
    b_display = st.empty()
    b_display.info("按下下方按鈕，開始跟隨萌寵腹部動態起伏進行調息")
    
    if st.button("🌬️ 開始 4-7-8 萌寵腹部起伏調息"):
        for prep in range(3, 0, -1):
            b_display.warning(f"⏳ 請放鬆肩膀，準備深吸氣... ({prep} 秒)")
            time.sleep(1)
            
        for cycle in range(1, 3):
            # 吸氣 4 秒 (肚子膨脹)
            for t in range(1, 5):
                b_display.markdown(f"### 🌬️ 吸氣 (Inhale) ── 腹部膨脹 ({t}/4秒)\n# 🐿️ " + "🎈" * t)
                time.sleep(1)
            # 留氣 7 秒 (懸息微震)
            for t in range(1, 8):
                b_display.markdown(f"### ⏸️ 留氣懸息 (Hold) ── 迷走神經活化 ({t}/7秒)\n# 🐿️ 🎈🎈🎈🎈")
                time.sleep(1)
            # 吐氣 8 秒 (肚子收縮)
            for t in range(1, 9):
                rem = max(1, 4 - int(t/2))
                b_display.markdown(f"### 💨 吐氣 (Exhale) ── 嘴唇微張長吐 ({t}/8秒)\n# 🐿️ " + "🎈" * rem)
                time.sleep(1)
                
        b_display.success("✨ 4-7-8 迷走神經調息完成！Cortisol 壓力負擔已完全釋放。")
        st.session_state["p_step3"] = True

    st.markdown("---")
    # 鋼鐵拋接機制：寫入共享記憶體，100% 拋接成功
    if st.session_state["p_step1"] and st.session_state["p_step2"] and st.session_state["p_step3"]:
        token_code = st.session_state["patient_token"]
        st.success(f"🕊️ 信鴿 Singer 準備就緒！去敏密鑰：**{token_code}** ｜ 心流分數：**{st.session_state['hrv_val']}%**")
        
        if st.button("📡 一鍵飛鴿拋接去敏數據至郭醫師診間面板"):
            shared_db[token_code] = {
                "status": "已完成診前 15s 共振調息",
                "coherence_score": float(st.session_state["hrv_val"]),
                "stress_index": "Morandi Soft Blue",
                "stress_desc": "莫蘭迪藍放縮區 ‧ 平穩",
                "sleep_hours": 7.4,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "nudge": f"探險家 {token_code} 已完成 4-7-8 迷走神經調息，心流一致性高達 {st.session_state['hrv_val']}%，狀態平穩，建議常規衛教。",
                "summary": f"【去敏身心軌跡摘要】經由探險家 App 邊緣端飛鴿拋接之代碼 {token_code}。個案完成 4-7-8 迷走神經調息，心流一致性維持於 {st.session_state['hrv_val']}% 高諧振區間。"
            }
            if token_code not in shared_queue:
                shared_queue.append(token_code)
                
            st.toast(f"🎉 數據已成功拋接至郭醫師門診佇列！請點擊上方分頁切換至『醫師端門診面板』查看！")
    else:
        st.warning("💡 請依次完成塗鴉、rPPG 與 4-7-8 萌寵呼吸，即可開啟數據拋接！")

# ==============================================================================
# 🩺 2. 醫師端門診面板 (1 秒即時接收拋接數據)
# ==============================================================================
with tab_doctor:
    st.title("夢境珍奇櫃診間面板")
    st.caption("Curio & Studio x 交感身心診所 ｜ 首席珍藏家蔻恩閣長 Cone ‧ 0 個資身心軌跡拋接")
    
    st.info("午安。今日預約看診 12 位探險家 ｜ 心流諧振指數 94% ｜ 🍵 建議搭配澳洲檀香/煙燻雪松香氛 ✕ 薄荷甘菊茶。")
    
    # 門診待看診佇列選擇
    selected_doc_token = st.selectbox("請選擇門診佇列或輸入探險家密鑰：", shared_queue, index=len(shared_queue)-1)
    
    data_doc = shared_db.get(selected_doc_token, None)
    
    if data_doc:
        st.success(f"✨ **1 秒問診焦點提示 (Clinical Nudge)**：{data_doc.get('nudge')}")
        
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("心流一致性 (0.067Hz)", f"{data_doc['coherence_score']} %")
        with col2: st.metric("身心應激狀態", data_doc['stress_index'])
        with col3: st.metric("本機睡眠時數", f"{data_doc['sleep_hours']} hr")
        
        st.write(f"**【去敏軌跡摘要】**\n\n{data_doc['summary']}\n\n🕒 時間戳記：{data_doc['timestamp']}")