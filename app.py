import pandas as pd
import streamlit as st

# 1. 全局配置：Mobile-First 響應式
st.set_page_config(
    page_title="交感身心日誌 ‧ 診間去敏拋接面板",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. 注入 Figma 設計規範（Design Tokens）自訂 CSS
st.markdown(
    """
    <style>
    /* 全局背景色：Figma Neutral Slate 50 */
    .stApp {
        background-color: #F8FAFC;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang TC", sans-serif;
    }
    
    header[data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    footer { visibility: hidden; }

    /* Figma 醫師端主視覺 Banner：交感經典深藍漸層 (#1E3A8A -> #2563EB) */
    .figma-hero-card {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
        color: #FFFFFF;
        padding: 24px 28px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.15);
        margin-bottom: 20px;
    }
    .figma-hero-card h1 {
        color: #FFFFFF !important;
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        margin: 0 0 6px 0 !important;
        letter-spacing: 0.3px;
    }
    .figma-hero-card p {
        color: #E0E7FF !important;
        font-size: 0.85rem !important;
        margin: 0 !important;
    }

    /* 診所與防線資訊膠囊 (Figma Pills) */
    .figma-meta-bar {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
        flex-wrap: wrap;
    }
    .figma-pill {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 8px 16px;
        font-size: 0.82rem;
        color: #334155;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }

    /* 指標數據卡片 (Figma Design Token Metric Card) */
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 20px 22px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
        transition: all 0.2s ease-in-out;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.08);
        border-color: #93C5FD;
    }
    div[data-testid="stMetricLabel"] p {
        color: #64748B !important;
        font-size: 0.88rem !important;
        font-weight: 500;
    }
    div[data-testid="stMetricValue"] div {
        color: #0F172A !important;
        font-size: 2rem !important;
        font-weight: 700;
    }

    /* 搜尋輸入欄 (Figma Input Style) */
    .stTextInput input {
        border-radius: 12px !important;
        border: 1.5px solid #CBD5E1 !important;
        background-color: #FFFFFF !important;
        padding: 12px 16px !important;
        font-size: 0.95rem !important;
        color: #0F172A !important;
    }
    .stTextInput input:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
    }

    /* 頁籤 Tab */
    button[data-baseweb="tab"] {
        font-size: 0.95rem;
        color: #64748B;
    }
    button[aria-selected="true"] {
        color: #1E3A8A !important;
        font-weight: 700 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# 3. 數據庫模擬
def fetch_patient_data(user_key):
    mock_db = {
        "#C701": {
            "status": "已完成診前 15s 調息",
            "coherence_score": 92.5,
            "stress_index": "身心平衡 (Sympathetic Calm)",
            "sleep_hours": 7.2,
            "timestamp": "2026-07-29 12:20:15",
            "weekly_trend": [82, 85, 87, 84, 89, 91, 92.5],
            "summary": "【去敏軌跡摘要】個案於看診前 15 秒於候診區完成 0.067 Hz 心流共振調息。連續 7 日數據顯示夜間無應激爆發，心流一致性維持於 90% 以上良好區間。心情結晶呈現交感藍寶石光澤。",
        }
    }
    return mock_db.get(user_key, None)


# --- 頂部 Banner (依 Figma 規範) ---
st.markdown(
    """
    <div class="figma-hero-card">
        <h1>🩺 交感身心日誌 ‧ 診間去敏拋接面板</h1>
        <p>夢境珍奇櫃 x 交感身心診所 ｜ Zero-Knowledge Architecture ‧ 0 個資 ‧ 診前 15 秒身心軌跡拋接</p>
    </div>
""",
    unsafe_allow_html=True,
)

# --- Figma 資訊膠囊 ---
st.markdown(
    """
    <div class="figma-meta-bar">
        <div class="figma-pill"><b>合作機構</b> ｜ 交感身心診所</div>
        <div class="figma-pill"><b>看診醫師</b> ｜ 郭家穎 院長</div>
        <div class="figma-pill" style="border-color:#2563EB; color:#1E3A8A; background:#EFF6FF;"><b>物理隔離防線</b> ｜ A4 保險箱機制 [已死鎖]</div>
    </div>
""",
    unsafe_allow_html=True,
)

# 搜尋欄
user_key = st.text_input(
    "請輸入探險家去敏密鑰 (例如：#C701) :",
    value="#C701",
    placeholder="輸入密鑰代碼，例如 #C701",
)

if user_key:
    data = fetch_patient_data(user_key)

    if data:
        # 連線成功狀態列 (Figma Status Blue Badge)
        st.markdown(
            f"""
            <div style="background-color: #EFF6FF; border-left: 4px solid #2563EB; padding: 12px 18px; border-radius: 12px; margin-bottom: 22px; font-size: 0.9rem; color: #1E3A8A;">
                <b>🔵 成功連線至去敏密鑰 <code>{user_key}</code></b> ｜ 狀態：{data['status']} ｜ 更新時間：{data['timestamp']}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 3 大指標卡片 (對齊 Figma 樣式)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "心流一致性 (0.067Hz)",
                f"{data['coherence_score']} %",
                "↑ 3.2% 穩定共振",
            )
        with col2:
            st.metric("身心應激狀態", data["stress_index"], "交感藍放鬆區")
        with col3:
            st.metric("本機睡眠時數", f"{data['sleep_hours']} hr", "達標 7 小時")

        st.markdown(
            "<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True
        )

        # 分頁 (Figma Tabs)
        tab1, tab2 = st.tabs(
            ["📈 近 7 日心流平穩度曲線", "📄 診前 15 秒去敏摘要"]
        )

        with tab1:
            st.markdown(
                "<h4 style='color:#0F172A; font-size:1.05rem; margin-top:10px;'>近 7 日心流一致性調息曲線 (Coherence Score)</h4>",
                unsafe_allow_html=True,
            )
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

            # 圖表主色改為 Figma 規範藍色 `#2563EB`
            st.line_chart(chart_data, color="#2563EB")

        with tab2:
            st.markdown(
                "<h4 style='color:#0F172A; font-size:1.05rem; margin-top:10px;'>邊緣端 15 秒去敏化身心軌跡</h4>",
                unsafe_allow_html=True,
            )
            st.info(
                "🛡️ 本頁面資料 100% 經邊緣端去敏化處理，絕不含病患姓名、病歷號或私密文字紀錄。"
            )
            st.write(f"**【去敏軌跡摘要】**\n\n{data['summary']}")
            st.caption(f"🕒 數據傳輸時間戳記：{data['timestamp']}")

    else:
        st.error(
            f"⚠️ 找不到密鑰 `{user_key}` 之當日資料，請確認代碼是否輸入正確。"
        )