import pandas as pd
import streamlit as st

# 1. 頁面配置與主題
st.set_page_config(
    page_title="居里研創 ‧ 機構端去敏管理面板",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. 注入高奢莫蘭迪 CSS 樣式
st.markdown(
    """
    <style>
    /* 全局背景色：燕麥莫蘭迪溫柔白 */
    .stApp {
        background-color: #F8F9F8;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* 高奢卡片邊框 */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8E2;
        padding: 18px 22px;
        border-radius: 16px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.03);
    }
    
    /* 標題與內文顏色 */
    h1 {
        color: #2D3732 !important;
        font-weight: 600;
    }
    
    /* 側邊欄樣式 */
    section[data-testid="stSidebar"] {
        background-color: #EEF1EE;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# 3. 去敏模擬資料庫
def fetch_patient_data(user_key):
    mock_db = {
        "#C701": {
            "status": "🟢 已完成診前 15s 心流調息",
            "coherence_score": 92.5,
            "stress_index": "莫蘭迪綠 (穩定放鬆)",
            "sleep_hours": 7.2,
            "timestamp": "2026-07-29 12:20:15",
            "weekly_trend": [82, 84, 88, 79, 89, 91, 92.5],
            "note_summary": "個案近 3 日於 App 端完成 0.067 Hz 共振調息，夜間無應激爆發。心情結晶呈 Morandi Jade 莫蘭迪玉色。",
        }
    }
    return mock_db.get(user_key, None)


# --- 側邊欄：機構與醫師資訊 ---
with st.sidebar:
    st.markdown("### 🏛️ 居里研創 Curio & Studio")
    st.caption("SaMD 臨床去敏拋接系統 v2.4")
    st.markdown("---")
    st.markdown("**合作診所**：交感身心診所")
    st.markdown("**看診醫師**：郭家穎醫師")
    st.markdown("**物理隔離防線**：`A4 保險箱機制 [已死鎖]`")
    st.markdown("---")
    st.info("💡 **提示**：輸入個案 A4 知情同意書右上角之探險家密鑰（如 `#C701`）即可載入 15 秒去敏身心軌跡。")

# --- 主介面 ---
st.title("🏛️ 夢境珍奇櫃 ‧ 機構端去敏管理面板")
st.caption(
    "Zero-Knowledge Architecture ｜ 0 個資 ‧ 零知識證明 ‧ 診前 15 秒去敏軌跡自動拋接"
)

st.markdown("---")

# 搜尋列
col_search, col_btn = st.columns([4, 1])
with col_search:
    user_key = st.text_input(
        "請輸入探險家去敏密鑰 :",
        value="#C701",
        placeholder="例如：#C701",
    )

if user_key:
    data = fetch_patient_data(user_key)

    if data:
        st.success(
            f"連線成功 ｜ 去敏標籤：`{user_key}` ｜ 狀態：{data['status']}"
        )

        # 3 大指標卡片
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(
                label="心流一致性評分 (0.067Hz)",
                value=f"{data['coherence_score']} %",
                delta="↑ 3.2% (穩定)",
            )
        with c2:
            st.metric(
                label="身心應激狀態",
                value=data["stress_index"],
                delta="Morandi Green",
            )
        with c3:
            st.metric(
                label="本機睡眠時數",
                value=f"{data['sleep_hours']} hr",
                delta="達標",
            )

        st.markdown("###")

        # 兩大核心功能展示區
        tab1, tab2 = st.tabs(
            ["📈 近 7 日身心軌跡趨勢", "📄 診前 15 秒去敏 PDF 摘要觀看"]
        )

        with tab1:
            st.subheader("近 7 日心流調息穩定度 (Coherence Trend)")
            chart_data = pd.DataFrame(
                {
                    "日期": [
                        "Mon",
                        "Tue",
                        "Wed",
                        "Thu",
                        "Fri",
                        "Sat",
                        "Sun",
                    ],
                    "心流分數": data["weekly_trend"],
                }
            ).set_index("日期")
            st.line_chart(chart_data, color="#8A9A86")

        with tab2:
            st.subheader("診前 15 秒去敏身心軌跡 (PDF 摘要模擬)")
            st.warning(
                "🛡️ 本頁面資料 100% 經邊緣端去敏化，不含任何個資、姓名或私密日誌筆跡。"
            )
            st.text_area(
                "邊緣端特徵解算摘要",
                value=data["note_summary"],
                height=100,
            )
            st.caption(f"🕒 數據傳輸時間戳記：{data['timestamp']}")

    else:
        st.error(
            f"⚠️ 找不到密鑰 `{user_key}` 之當日資料，請確認代碼是否輸入正確。"
        )