import streamlit as st
import datetime
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="郭醫師診間 ‧ 莫蘭迪身心數據脈衝後台",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 莫蘭迪調色盤與診間高奢質感 CSS
st.markdown("""
<style>
    .main-panel {
        background-color: #F7F5F0;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #DCD6CD;
        color: #3E3E3E;
    }
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 16px;
        border: 1px solid #E5DFD7;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
        text-align: center;
    }
    .tea-card {
        background-color: #EFECE6;
        border-left: 5px solid #8C6D62;
        border-radius: 8px;
        padding: 18px;
        margin-top: 15px;
    }
    .tag-badge {
        display: inline-block;
        background-color: #C2C9D1;
        color: #2C3E50;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 模擬後台安全資料庫 (雙盲 Redis TTL 快取)
if "clinic_db" not in st.session_state:
    st.session_state.clinic_db = {
        "#SYM-A810": {
            "token": "#SYM-A810",
            "name_alias": "探險家 A",
            "coherence": 0.88,
            "stress": "平穩平衡 (心流共振)",
            "sleep": 7.2,
            "color_hex": "#4A707A",
            "animal": ["石虎（警覺放鬆共存）"],
            "created_at": "08:30:00",
            "ttl": "240 分鐘"
        },
        "#SYM-P439": {
            "token": "#SYM-P439",
            "name_alias": "探險家 B",
            "coherence": 0.54,
            "stress": "交感亢進 (急性應激)",
            "sleep": 4.5,
            "color_hex": "#C89595",
            "animal": ["草鴞（夜間深層安定）", "長鬃山羊（平衡與專注）"],
            "created_at": "14:15:00",
            "ttl": "180 分鐘"
        }
    }

if "doctor_key" not in st.session_state:
    st.session_state.doctor_key = "CLINIC-KEY-2026-AIRGAP-SECURE"

# 時間感知問候邏輯
now = datetime.datetime.now()
current_hour = now.hour
if 5 <= current_hour < 12:
    time_greeting = "早安"
elif 12 <= current_hour < 18:
    time_greeting = "午安"
else:
    time_greeting = "晚安"

# 三款專屬研發茶飲與香氛精準邏輯
def evaluate_tea_prescription(hour, stress_state, coherence_score):
    # 規則一：未超過晚上 22:00（晚上10點前），暮夜靜謐茶嚴禁上線
    if hour >= 22 or hour < 5:
        return {
            "name": "暮夜靜謐・香草琥珀晚安茶",
            "category": "助眠安神 ✕ 深層修復",
            "desc": "收斂自律神經心流，引導大腦進入慢波深睡期。嚴禁白天或未達 22:00 飲用。",
            "aroma": "澳洲檀香 ✕ 煙燻雪松香氛",
            "lock_note": "🌙 夜間專屬解鎖（22:00-05:00 限定）"
        }
    # 規則二：急性應激、交感偏高、或下午水腫緊繃
    elif "亢進" in stress_state or "應激" in stress_state or (13 <= hour < 18):
        return {
            "name": "朝露白桃・玫瑰舒妍茶",
            "category": "疏肝解鬱 ✕ 調和氣血消水腫",
            "desc": "舒緩因高壓導致之經絡緊繃與水分代謝滯留，撫平浮躁情緒。",
            "aroma": "大馬士革玫瑰 ✕ 甜白桃薄霧香氛",
            "lock_note": "🌸 日間解鬱舒緩推薦"
        }
    # 規則三：早晨或心流不足時提神
    else:
        return {
            "name": "破霧清醒・薄荷焙香玄米茶",
            "category": "提神醒腦 ✕ 激發清陽",
            "desc": "活化副交感與交感協調，增強認知專注度，提升 0.067Hz 心流一致性。",
            "aroma": "綠薄荷 ✕ 焙煎玄米原木香氛",
            "lock_note": "🍵 晨光專注甦醒推薦"
        }

# ======================= 醫師儀表板 UI =======================
st.title("🩺 郭醫師診間 ‧ 身心脈衝臨床面板")
st.markdown(f"**{time_greeting}，郭醫師。** 今日排定預約看診 **{len(st.session_state.clinic_db)}** 位探險家 ｜ 系統時間：`{now.strftime('%Y-%m-%d %H:%M:%S')}`")

# 升級選配與醫師金鑰修改區
with st.expander("🔑 診間安全金鑰與升級選配管理", expanded=False):
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        new_key = st.text_input("修改診所機構驗證簽章 (Clinic Session Token)：", value=st.session_state.doctor_key, type="password")
        if st.button("確認更新金鑰"):
            st.session_state.doctor_key = new_key
            st.success("診間機構密鑰已更新。")
    with col_k2:
        st.write("⚙️ **診間進階升級選配**：")
        st.checkbox("啟用雙盲 Redis TTL 動態時間鎖自動銷毀", value=True)
        st.checkbox("啟用莫蘭迪診間氣氛與沉香精油聯動模組", value=True)
        st.checkbox("實體 Air-Gap 保險箱紙本知情死鎖對照", value=True)

st.write("---")

# 病患代碼輸入與解鎖
col_search, col_btn = st.columns([3, 1])
with col_search:
    target_token = st.text_input("請輸入探險家拋接短碼（例如：#SYM-P439 或 #SYM-A810）：", value="#SYM-P439")
with col_btn:
    st.write("")
    st.write("")
    unlock_action = st.button("🔓 瞬間比對解鎖")

if target_token:
    if target_token in st.session_state.clinic_db:
        p = st.session_state.clinic_db[target_token]
        st.markdown(f"""
        <div class="main-panel">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h3>🛡️ 探險家去敏身心特徵面板：{p['token']}</h3>
                <span class="tag-badge">實體隔離防線：Air-Gap 100% (No-PII)</span>
            </div>
            <p style="color:#7A7A7A; font-size:0.9rem;">拋接時間：{p['created_at']} ｜ 雙盲時間鎖存活倒數：{p['ttl']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 4 大動態生理指標
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"<div class='metric-card'><h4>心流一致性 (0.067Hz)</h4><h2 style='color:#4A707A;'>{p['coherence']*100:.0f}%</h2><p>共振諧波指標</p></div>", unsafe_allow_html=True)
        with m2:
            st.markdown(f"<div class='metric-card'><h4>身心應激狀態</h4><h3 style='color:#8C6D62;'>{p['stress']}</h3><p>rPPG 邊緣運算</p></div>", unsafe_allow_html=True)
        with m3:
            st.markdown(f"<div class='metric-card'><h4>本機睡眠時數</h4><h2 style='color:#3D5A80;'>{p['sleep']} hrs</h2><p>昨夜睡眠深度</p></div>", unsafe_allow_html=True)
        with m4:
            st.markdown(f"<div class='metric-card'><h4>原石共鳴色</h4><div style='background:{p['color_hex']}; width:40px; height:40px; border-radius:50%; margin:auto;'></div><p>{p['color_hex']}</p></div>", unsafe_allow_html=True)
        
        # 專屬研發茶飲推薦 (依時間與生理數據精準匹配)
        tea_info = evaluate_tea_prescription(current_hour, p['stress'], p['coherence'])
        st.markdown(f"""
        <div class="tea-card">
            <h3>🍵 診間莫蘭迪茶飲 / 沉香精油處方：</h3>
            <div style="font-size:1.25rem; font-weight:bold; color:#5D4037; margin:8px 0;">{tea_info['name']} <span class="tag-badge">{tea_info['category']}</span></div>
            <p><b>處方功效</b>：{tea_info['desc']}</p>
            <p><b>診間建議搭配香氛</b>：{tea_info['aroma']}</p>
            <p style="color:#8C6D62; font-size:0.85rem; margin-top:5px;"><b>調配規範</b>：{tea_info['lock_note']}</p>
            <hr style="border:0.5px solid #DCD6CD; margin:10px 0;">
            <p>🐾 <b>個案調息選擇之自然夥伴（友善動物福利）</b>：{', '.join(p['animal'])}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error(f"❌ 查無代碼 `{target_token}`。可能已超過 TTL 時間自動銷毀，或個案尚未完成邊緣拋接。")