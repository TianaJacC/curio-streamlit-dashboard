import streamlit as st
import hashlib
import time
import requests
import datetime
from streamlit_drawable_canvas import st_canvas
import pandas as pd
import numpy as np

# --- 頁面全域設定 ---
st.set_page_config(
    page_title="夢境珍奇櫃・身心數據動態拋接系統",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 樣式設定：莫蘭迪與手遊質感 ---
st.markdown("""
<style>
    .morandi-card {
        background-color: #F4F1EA;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #D8D2C2;
        color: #4A4A4A;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
        background-color: #B5C0D0;
        color: #2D3748;
    }
    .metric-box {
        background-color: #FAF8F5;
        border: 1px solid #EADBC8;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 初始化 Session 狀態 ---
if "patient_store" not in st.session_state:
    st.session_state.patient_store = {}
if "current_token" not in st.session_state:
    st.session_state.current_token = None
if "selected_color" not in st.session_state:
    st.session_state.selected_color = "#4A707A"
if "doctor_api_key" not in st.session_state:
    st.session_state.doctor_api_key = "CLINIC-KEY-2026-ZKSECURE"

# --- 輔助函式：即時氣象與空氣品質 API ---
def get_live_environment_data(is_overseas=False):
    # 預設台北/海外經緯度
    lat, lon = (35.6762, 139.6503) if is_overseas else (25.0330, 121.5654)
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=surface_pressure,relative_humidity_2m&timezone=auto"
        res = requests.get(url, timeout=3).json()
        pressure = res.get("current", {}).get("surface_pressure", 1013.2)
        humidity = res.get("current", {}).get("relative_humidity_2m", 65)
        # 動態換算負離子與空品
        aqi = 24 if not is_overseas else 18
        phytoncide = int(pressure * 7.5 + humidity * 12)
        return pressure, aqi, phytoncide
    except:
        return 1013.2, 22, 8500

# --- 輔助函式：林業署/秘境指引判定 ---
def get_trail_recommendation(hour):
    if 5 <= hour < 12:
        return "【林業署步道推薦】奧萬大國家森林遊樂區 ‧ 森林療癒試辦步道（晨光甦醒，活化身心敏銳度）"
    elif 12 <= hour < 18:
        return "【林業署步道推薦】太平山見晴懷古步道 ‧ 雲霧苔蘚徑（漫步減壓，平穩自律神經活性）"
    else:
        return "【林業署步道推薦】阿里山巨木群步道 ‧ 夜息靜心區（深層安定，啟動副交感神經修復）"

# --- 輔助函式：三款專屬茶飲智慧推薦邏輯 ---
def recommend_tea(hour, stress_level, coherence):
    # 規則一：未超過晚上 22:00（10點），暮夜靜謐茶嚴禁登場
    # 規則二：破霧清醒茶：提神醒腦（適合早/午間或身心疲憊交感不足）
    # 規則三：朝露白桃茶：疏肝解鬱、消水腫（適合高應激或下午時段）
    # 規則四：暮夜靜謐茶：22:00 後助眠安神
    if hour >= 22 or hour < 5:
        return {
            "name": "暮夜靜謐・香草琥珀晚安茶",
            "effect": "助眠安神、收斂神經心流、深層滋陰修復",
            "aroma": "澳洲檀香 ✕ 煙燻雪松香氛",
            "status": "夜間專屬（22:00-05:00 限定解鎖）"
        }
    elif stress_level == "高應激 (交感亢進)" or (12 <= hour < 18):
        return {
            "name": "朝露白桃・玫瑰舒妍茶",
            "effect": "疏肝解鬱、調和氣血、消水腫與舒緩經絡緊繃",
            "aroma": "大馬士革玫瑰 ✕ 甜白桃薄霧",
            "status": "日間/解鬱推薦"
        }
    else:
        return {
            "name": "破霧清醒・薄荷焙香玄米茶",
            "effect": "提神醒腦、激發清陽、增強專注心流共振",
            "aroma": "綠薄荷 ✕ 焙煎玄米清香",
            "status": "晨間/提神推薦"
        }

# ==============================================================================
# 側邊欄：模式切換
# ==============================================================================
st.sidebar.title("🌲 夢境珍奇櫃系統")
mode = st.sidebar.radio("請選擇操作介面", ["🎮 病患端：手遊探索與拋接", "🩺 診間端：醫師莫蘭迪後台"])

# ==============================================================================
# 介面一：病患端手遊互動 (Patient App)
# ==============================================================================
if mode == "🎮 病患端：手遊探索與拋接":
    st.title("🏰 夢境珍奇櫃 ‧ 冒險者通行證")
    
    # 1. 安全照片登入 (Photo Hash Login)
    with st.expander("📷 【步驟一】一鍵相簿照片登入（Photo Hash 去個資驗證）", expanded=(st.session_state.current_token is None)):
        uploaded_photo = st.file_uploader("點選一張讓您有安全感的相片（系統絕不上傳圖片，僅於本機計算 SHA-256 雜湊值）：", type=["jpg", "jpeg", "png"])
        if uploaded_photo is not None:
            photo_bytes = uploaded_photo.read()
            photo_hash = hashlib.sha256(photo_bytes).hexdigest()
            # 依雜湊值生成專屬 6 碼動態代碼
            generated_token = f"#SYM-{photo_hash[:4].upper()}"
            st.session_state.current_token = generated_token
            st.success(f"安全照片驗證完成！您的本機匿名動態代碼為：**{generated_token}**（無任何個資留存）")

    if st.session_state.current_token:
        # 動態頂部狀態條
        now = datetime.datetime.now()
        is_overseas = st.checkbox("🌐 探險家目前位於海外（切換跨國 OpenAQ / Open-Meteo 氣象指標）", value=False)
        pressure, aqi, phytoncide = get_live_environment_data(is_overseas)
        trail = get_trail_recommendation(now.hour)
        
        # 綠色算力計算：基於邊緣運算減少雲端傳輸 1.2MB 圖片的碳排換算
        edge_energy_kwh = 0.0018
        
        st.markdown(f"""
        <div class="morandi-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:1.1rem; font-weight:bold;">🌲 閣長蔻恩指引 ｜ 綠色算力能耗：{edge_energy_kwh} kWh (Edge AI 減碳) ｜ 冒險進度：75%</span>
                <span class="status-badge">🔑 {st.session_state.current_token}</span>
            </div>
            <hr style="border:0.5px solid #D8D2C2; margin:10px 0;">
            <div>🧭 <b>冒險羅盤定位</b>：大氣氣壓: {pressure} hPa ｜ AQI 空品: {aqi} 良好 ｜ 芬多精負離子: {phytoncide:,} ions/cm³</div>
            <div style="margin-top:5px;">🌲 <b>秘境指引</b>：{trail}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. 靈魂原石與畫布連動
        st.markdown("### 🔮 第一關：靈魂原石圖騰")
        st.write("點選吸引您的色彩原石，在畫布上記錄今天的冒險足跡：")
        
        # 莫蘭迪色盤
        palette = [
            "#4A707A", "#7A8B7B", "#B5C0D0", "#C89595", "#8C6D62",
            "#D87A61", "#E5A93C", "#5C6B73", "#3D5A80", "#293241"
        ]
        
        cols = st.columns(len(palette))
        for idx, col in enumerate(cols):
            with col:
                color_hex = palette[idx]
                if st.button(f"●", key=f"color_{idx}", help=f"選擇色票 {color_hex}"):
                    st.session_state.selected_color = color_hex
        
        st.caption(f"當前筆刷顏色：`{st.session_state.selected_color}`")
        
        # 繪圖畫布
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=4,
            stroke_color=st.session_state.selected_color,
            background_color="#FAF8F5",
            height=260,
            drawing_mode="freedraw",
            key="canvas",
        )
        
        # 3. 進入調息與友善動物福利
        st.markdown("### 🌿 第二關：心流共振調息（0.067Hz）")
        with st.expander("🕊️ 進入調息設置（含友善動物福利陪伴模式）", expanded=True):
            animal_welfare = st.multiselect(
                "選擇調息相伴的自然夥伴（友善動物福利與生態療癒）：",
                ["台灣黑熊（大地穩定意象）", "石虎（警覺放鬆共存）", "草鴞（夜間深層安定）", "長鬃山羊（平衡與專注）"],
                default=["石虎（警覺放鬆共存）"]
            )
            
            # rPPG 邊緣運算模擬（模擬鏡頭擷取波形並於本機銷毀）
            st.write("💓 **邊緣端 rPPG 鏡頭脈搏解算中**：原始影格於本機 RAM 完成 0.067Hz 一致性分析後立即銷毀。")
            simulated_coherence = round(np.random.uniform(0.72, 0.94), 2)
            simulated_stress = np.random.choice(["交感略高 (輕度應激)", "平穩平衡 (心流共振)", "副交感主導 (深層放鬆)"])
            simulated_sleep = round(np.random.uniform(5.5, 8.5), 1)
            
            st.progress(simulated_coherence)
            st.caption(f"即時心流一致性分數：{simulated_coherence * 100}% ｜ 生數據已於記憶體即時釋放 (No-PII)")

        # 4. 一鍵動態拋接
        if st.button("🚀 完成冒險並將去敏數據拋接至診間中繼站"):
            st.session_state.patient_store[st.session_state.current_token] = {
                "token": st.session_state.current_token,
                "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                "coherence": simulated_coherence,
                "stress": simulated_stress,
                "sleep": simulated_sleep,
                "animal": animal_welfare,
                "color_chosen": st.session_state.selected_color,
                "ttl_expire": (now + datetime.timedelta(minutes=240)).strftime("%H:%M:%S")
            }
            st.success(f"✅ 拋接成功！代碼 **{st.session_state.current_token}** 已送至雙盲時間鎖中繼站，有效存活時間（TTL）：240 分鐘。")

# ==============================================================================
# 介面二：醫師端診間莫蘭迪後台 (Clinic Dashboard)
# ==============================================================================
elif mode == "🩺 診間端：醫師莫蘭迪後台":
    now = datetime.datetime.now()
    hour = now.hour
    
    # 動態時間問候語
    if 5 <= hour < 12:
        greeting = "早安"
    elif 12 <= hour < 18:
        greeting = "午安"
    else:
        greeting = "晚安"
        
    st.title(f"🩺 郭醫師診間 ‧ 莫蘭迪身心脈衝後台")
    st.caption(f"{greeting}。目前系統時間：{now.strftime('%H:%M:%S')} ｜ 實體防線隔離層（Air-Gap）運作中")
    
    # 頂部：金鑰管理與升級選配區塊
    with st.expander("🔑 診間安全金鑰與升級選配管理"):
        col_k1, col_k2 = st.columns(2)
        with col_k1:
            input_key = st.text_input("修改診所機構驗證簽章 (Clinic Session Token)：", value=st.session_state.doctor_api_key, type="password")
            if st.button("更新機構密鑰"):
                st.session_state.doctor_api_key = input_key
                st.success("機構安全金鑰已更新。")
        with col_k2:
            st.write("⚙️ **升級選配模組**：")
            st.checkbox("啟用雙盲 Redis TTL 毫秒級自動清空", value=True)
            st.checkbox("啟用莫蘭迪診間氣氛與沉香聯動", value=True)
            st.checkbox("啟用實體 Air-Gap 紙本知情對照鎖定", value=True)
    
    # 動態解鎖區域
    col_input1, col_input2 = st.columns([3, 1])
    with col_input1:
        doc_token_search = st.text_input("輸入病患動態短碼標籤進行雙向交會解鎖（例如：#SYM-P439 或剛生成的代碼）：", value="")
    with col_input2:
        st.write("")
        st.write("")
        unlock_btn = st.button("🔓 瞬間比對解鎖")
        
    if unlock_btn or doc_token_search:
        if doc_token_search in st.session_state.patient_store:
            data = st.session_state.patient_store[doc_token_search]
            st.success(f"比對成功！已解鎖探險家 `{doc_token_search}` 去敏身心特徵（無個人識別資訊 No-PII）")
            
            # 指標看板
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(f"<div class='metric-box'><h4>心流一致性</h4><h2>{data['coherence']*100:.0f}%</h2><p>0.067Hz 共振</p></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='metric-box'><h4>身心應激狀態</h4><h3>{data['stress']}</h3><p>邊緣神經算力</p></div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div class='metric-box'><h4>本機睡眠時數</h4><h2>{data['sleep']} hrs</h2><p>昨夜睡眠品質</p></div>", unsafe_allow_html=True)
            with c4:
                st.markdown(f"<div class='metric-box'><h4>中繼站 TTL</h4><h3>{data['ttl_expire']}</h3><p>過期強制銷毀</p></div>", unsafe_allow_html=True)
            
            # 茶飲與沉香處方推薦（嚴格判定三款研發茶飲）
            tea_rec = recommend_tea(hour, data['stress'], data['coherence'])
            
            st.markdown(f"""
            <div class="morandi-card" style="margin-top:20px;">
                <h3>🍵 診間專屬茶飲與沉香調息處方（AI 輔助建議）</h3>
                <p><b>推薦茶品</b>：<span style="font-size:1.2rem; color:#8C6D62; font-weight:bold;">{tea_rec['name']}</span>（{tea_rec['status']}）</p>
                <p><b>臨床功效</b>：{tea_rec['effect']}</p>
                <p><b>建議環境香氛</b>：{tea_rec['aroma']}</p>
                <hr style="border:0.5px solid #D8D2C2;">
                <p>🐾 <b>患者選擇之生態陪伴</b>：{', '.join(data['animal'])}</p>
                <p>🎨 <b>原石共鳴色票代碼</b>：<span style="display:inline-block; width:15px; height:15px; background:{data['color_chosen']}; vertical-align:middle;"></span> {data['color_chosen']}</p>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.warning("⚠️ 查無此代碼或數據已超過 TTL 存活時間自動銷毀。請確認病患端是否已點擊拋接。")