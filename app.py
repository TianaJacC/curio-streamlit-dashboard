import pandas as pd
import streamlit as st

# 1. 全局配置：預設展開、自動適應手機
st.set_page_config(
    page_title="夢境珍奇櫃 ‧ 診間拋接後台",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. 手機與電腦強效 RWD 莫蘭迪 CSS
st.markdown(
    """
    <style>
    /* 莫蘭迪平靜燕麥色背景 */
    .stApp {
        background-color: #F6F7F5;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* 頂部標頭卡片 */
    .header-card {
        background: #3D4A41;
        color: #F6F7F5;
        padding: 16px 20px;
        border-radius: 14px;
        margin-bottom: 16px;
    }
    .header-card h2 {
        color: #FFFFFF !important;
        font-size: 1.25rem !important;
        margin: 0 0 4px 0 !important;
        font-weight: 600;
    }
    .header-card p {
        color: #C2CBC5 !important;
        font-size: 0.8rem !important;
        margin: 0 !important;
    }

    /* 醫師與診所資訊膠囊標籤 */
    .info-pill {
        background: #FFFFFF;
        border: 1px solid #E1E6E1;
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        color: #4A584F;
    }

    /* 數據卡片（自動適應手機寬度） */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E1E6E1;
        padding: 16px;
        border-radius: 14px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.02);
        margin-bottom: 10px;
    }
    div[data-testid="stMetricLabel"] p {
        color: #7A8A80 !important;
        font-size: 0.85rem !important;
    }
    div[data-testid="stMetricValue"] div {
        color: #2C3631 !important;
        font-size: 1.8rem !important;
        font-weight: 700;
    }

    /* 輸入框適應手機手指點擊 */
    .stTextInput input {
        border-radius: 10px;
        border: 1px solid #D1D8D2;
        padding: 10px 14px;
        font-size: 0.95rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# 3. 資料庫模擬
def fetch_patient_data(user_key):
    mock_db = {
        "#C701": {
            "status": "已完成診前 15s 調息",
            "coherence_score": 92.5,
            "stress_index": "Morandi Sage",
            "sleep_hours": 7.2,
            "timestamp": "2026-07-29 12:20",
            "weekly_trend": [82, 85, 87, 84, 89, 91, 92.5],
            "summary": "【去敏軌跡】看診前 15 秒於候診區完成 0.067 Hz 心流調息。近 7 日夜間無應激爆發，心流一致性保持高水準平穩。",
        }
    }
    return mock_db.get(user_key, None)


# --- 頂部黑森林綠標頭 ---
st.markdown(
    """
    <div class="header-card">
        <h2>🏛️ 夢境珍奇櫃 ‧ 診間拋接面板</h2>
        <p>SaMD 0 個資 ‧ 診前 15 秒身心軌跡拋接</p>
    </div>
""",
    unsafe_allow_html=True,
)

# --- 診所資訊條 ---
st.markdown(
    """
    <div class="info-pill">
        <span><b>診所</b>: 交感身心診所</span>
        <span><b>醫師</b>: 郭家穎 院長</span>
        <span style="color:#2A7A4C;"><b>防線</b>: 物理隔離死鎖</span>
    </div>
""",
    unsafe_allow_html=True,
)

# 搜尋輸入框
user_key = st.text_input("輸入探險家去敏密鑰 :", value="#C701")

if user_key:
    data = fetch_patient_data(user_key)

    if data:
        st.caption(
            f"🟢 密鑰 `{user_key}` ｜ 狀態：{data['status']} ｜ 更新：{data['timestamp']}"
        )

        # 自動適應手機與電腦的卡片排版
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.metric("心流一致性 (0.067Hz)", f"{data['coherence_score']} %", "↑ 3.2%")
        with col2:
            st.metric("身心應激狀態", data["stress_index"], "放鬆區")
        with col3:
            st.metric("本機睡眠時數", f"{data['sleep_hours']} hr", "達標")

        st.markdown("---")

        # 頁籤
        tab1, tab2 = st.tabs(["📈 7日心流曲線", "📄 15s 摘要"])

        with tab1:
            chart_data = pd.DataFrame(
                {
                    "日": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                    "分數": data["weekly_trend"],
                }
            ).set_index("日")
            st.line_chart(chart_data, color="#3D4A41")

        with tab2:
            st.info("🛡️ 數據 100% 經邊緣端去敏化，絕無個人個資。")
            st.write(data["summary"])
    else:
        st.error(f"⚠️ 找不到代碼 `{user_key}` 之資料。")