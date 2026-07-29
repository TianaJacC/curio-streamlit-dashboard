import pandas as pd
import streamlit as st

# 1. 全局配置：Mobile-First 響應式
st.set_page_config(
    page_title="Cabinet of Curiosities ‧ 門診去敏拋接系統",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. 注入莫蘭迪高奢藝廊級 CSS
st.markdown(
    """
    <style>
    /* 全局燕麥奶霜背景 */
    .stApp {
        background-color: #F5F6F4;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang TC", sans-serif;
    }
    
    /* 隱藏上方預設紅條與 Header */
    header[data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    footer { visibility: hidden; }

    /* 頂級藝廊黑森林綠 Banner */
    .hero-card {
        background: linear-gradient(135deg, #2E3B33 0%, #435248 100%);
        color: #F5F6F4;
        padding: 24px 28px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(46, 59, 51, 0.12);
        margin-bottom: 20px;
    }
    .hero-card h1 {
        color: #FFFFFF !important;
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        margin: 0 0 6px 0 !important;
        letter-spacing: 0.5px;
    }
    .hero-card p {
        color: #C3CDC6 !important;
        font-size: 0.85rem !important;
        margin: 0 !important;
    }

    /* 頂級資訊膠囊列 */
    .meta-pills {
        display: flex;
        gap: 10px;
        margin-bottom: 22px;
        flex-wrap: wrap;
    }
    .pill {
        background: #FFFFFF;
        border: 1px solid #E3E8E3;
        border-radius: 30px;
        padding: 8px 16px;
        font-size: 0.82rem;
        color: #4A584F;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }

    /* 指標數據卡片 (微懸浮奢華效果) */
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E3E8E3;
        padding: 20px 22px;
        border-radius: 18px;
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.03);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 28px rgba(46, 59, 51, 0.08);
        border-color: #A3B1A0;
    }
    div[data-testid="stMetricLabel"] p {
        color: #7A8A80 !important;
        font-size: 0.88rem !important;
        font-weight: 500;
    }
    div[data-testid="stMetricValue"] div {
        color: #2E3B33 !important;
        font-size: 2rem !important;
        font-weight: 700;
    }

    /* 搜尋輸入欄美化 */
    .stTextInput input {
        border-radius: 14px !important;
        border: 1.5px solid #D5DDD5 !important;
        background-color: #FFFFFF !important;
        padding: 12px 18px !important;
        font-size: 1rem !important;
        color: #2E3B33 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
    }
    .stTextInput input:focus {
        border-color: #6B7C6E !important;
        box-shadow: 0 0 0 3px rgba(107, 124, 110, 0.15) !important;
    }

    /* 頁籤 Tab */
    button[data-baseweb="tab"] {
        font-size: 0.95rem;
        color: #7A8A80;
    }
    button[aria-selected="true"] {
        color: #2E3B33 !important;
        font-weight: 700 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# 3. 數據庫
def fetch_patient_data(user_key):
    mock_db = {
        "#C701": {
            "status": "已完成診前 15s 調息",
            "coherence_score": 92.5,
            "stress_index": "Morandi Sage (平穩)",
            "sleep_hours": 7.2,
            "timestamp": "2026-07-29 12:20:15",
            "weekly_trend": [82, 85, 87, 84, 89, 91, 92.5],
            "summary": "個案於看診前 15 秒於候診區完成 0.067 Hz 心流共振調息。連續 7 日數據顯示夜間無應激爆發，心流一致性維持於 90% 以上良好區間。心情結晶呈 Morandi Jade 莫蘭迪玉色。",
        }
    }
    return mock_db.get(user_key, None)


# --- 頁面頭部 Banner ---
st.markdown(
    """
    <div class="hero-card">
        <h1>🏛️ 夢境珍奇櫃 ‧ 診間去敏拋接面板</h1>
        <p>Curio & Studio ｜ Zero-Knowledge Architecture ‧ 0 個資 ‧ 診前 15 秒身心軌跡拋接</p>
    </div>
""",
    unsafe_allow_html=True,
)

# --- 資訊膠囊 ---
st.markdown(
    """
    <div class="meta-pills">
        <div class="pill"><b>合作機構</b> ｜ 交感身心診所</div>
        <div class="pill"><b>看診醫師</b> ｜ 郭家穎 院長</div>
        <div class="pill" style="border-color:#A3B1A0; color:#2E3B33;"><b>物理隔離防線</b> ｜ A4 保險箱機制 [已死鎖]</div>
    </div>
""",
    unsafe_allow_html=True,
)

# 搜尋欄
user_key = st.text_input(
    "請輸入探險家去敏密鑰 (例如：#C701) :",
    value="#C701",
    placeholder="輸入代碼，例如 #C701",
)

if user_key:
    data = fetch_patient_data(user_key)

    if data:
        st.markdown(
            f"""
            <div style="background-color: #EBF0EC; border-left: 4px solid #6B7C6E; padding: 12px 18px; border-radius: 12px; margin-bottom: 22px; font-size: 0.9rem; color: #2E3B33;">
                <b>🟢 成功連線至去敏密鑰 <code>{user_key}</code></b> ｜ 狀態：{data['status']} ｜ 更新時間：{data['timestamp']}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 3 大指標卡片 (手機電腦 RWD 自動適應)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "心流一致性 (0.067Hz)",
                f"{data['coherence_score']} %",
                "↑ 3.2% 穩定",
            )
        with col2:
            st.metric("身心應激狀態", data["stress_index"], "莫蘭迪綠放鬆區")
        with col3:
            st.metric("本機睡眠時數", f"{data['sleep_hours']} hr", "達標 7 小時")

        st.markdown(
            "<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True
        )

        # 分頁
        tab1, tab2 = st.tabs(
            ["📈 近 7 日心流平穩度曲線", "📄 診前 15 秒去敏摘要"]
        )

        with tab1:
            st.markdown(
                "<h4 style='color:#2E3B33; font-size:1.05rem; margin-top:10px;'>近 7 日心流一致性調息曲線 (Coherence Score)</h4>",
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
            st.line_chart(chart_data, color="#6B7C6E")

        with tab2:
            st.markdown(
                "<h4 style='color:#2E3B33; font-size:1.05rem; margin-top:10px;'>邊緣端 15 秒去敏化身心軌跡</h4>",
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