import pandas as pd
import streamlit as st

# 1. 全局配置：Mobile-First 響應式，隱藏側欄
st.set_page_config(
    page_title="Cabinet of Curiosities ‧ 診間去敏拋接面板",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. 注入夢境珍奇櫃 ‧ 莫蘭迪淺藍 (Morandi Soft Blue) CSS
st.markdown(
    """
    <style>
    /* 全局背景：柔和莫蘭迪霧藍微灰 */
    .stApp {
        background-color: #F2F5F8;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang TC", sans-serif;
    }
    
    header[data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    footer { visibility: hidden; }

    /* 夢境珍奇櫃 典藏霧藍 Banner (Morandi Slate Blue) */
    .curio-hero-card {
        background: linear-gradient(135deg, #3B4E68 0%, #5A7292 100%);
        color: #FFFFFF;
        padding: 26px 30px;
        border-radius: 20px;
        box-shadow: 0 10px 24px rgba(59, 78, 104, 0.15);
        border: 1px solid #7188A6;
        margin-bottom: 22px;
    }
    .curio-hero-card h1 {
        color: #FFFFFF !important;
        font-size: 1.45rem !important;
        font-weight: 600 !important;
        margin: 0 0 6px 0 !important;
        letter-spacing: 0.8px;
    }
    .curio-hero-card p {
        color: #D6E1EF !important;
        font-size: 0.85rem !important;
        margin: 0 !important;
    }

    /* 夢境珍奇櫃 圖騰膠囊標籤 */
    .curio-meta-bar {
        display: flex;
        gap: 12px;
        margin-bottom: 22px;
        flex-wrap: wrap;
    }
    .curio-pill {
        background: #FFFFFF;
        border: 1px solid #D2DCED;
        border-radius: 30px;
        padding: 8px 18px;
        font-size: 0.83rem;
        color: #334763;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }

    /* 指標數據卡片 (莫蘭迪淺藍柔和浮雕) */
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #D8E2EE;
        padding: 20px 22px;
        border-radius: 18px;
        box-shadow: 0 6px 16px rgba(59, 78, 104, 0.04);
        transition: all 0.25s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 24px rgba(59, 78, 104, 0.09);
        border-color: #8BA0BD;
    }
    div[data-testid="stMetricLabel"] p {
        color: #627792 !important;
        font-size: 0.88rem !important;
        font-weight: 500;
    }
    div[data-testid="stMetricValue"] div {
        color: #25354A !important;
        font-size: 2.1rem !important;
        font-weight: 700;
    }

    /* 搜尋輸入欄 (莫蘭迪淺藍焦點邊框) */
    .stTextInput input {
        border-radius: 14px !important;
        border: 1.5px solid #C8D6E5 !important;
        background-color: #FFFFFF !important;
        padding: 12px 18px !important;
        font-size: 0.95rem !important;
        color: #25354A !important;
    }
    .stTextInput input:focus {
        border-color: #5A7292 !important;
        box-shadow: 0 0 0 3px rgba(90, 114, 146, 0.18) !important;
    }

    /* 頁籤 Tab */
    button[data-baseweb="tab"] {
        font-size: 0.95rem;
        color: #627792;
    }
    button[aria-selected="true"] {
        color: #25354A !important;
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
            "stress_index": "Morandi Soft Blue (平穩)",
            "sleep_hours": 7.2,
            "timestamp": "2026-07-29 12:20:15",
            "weekly_trend": [82, 85, 87, 84, 89, 91, 92.5],
            "summary": "【去敏軌跡摘要】個案於看診前 15 秒於候診區完成 0.067 Hz 心流共振調息。連續 7 日數據顯示夜間無應激爆發，心流一致性維持於 90% 以上良好區間。心情結晶呈 Morandi Sky 莫蘭迪天青藍微光。",
        }
    }
    return mock_db.get(user_key, None)


# --- 夢境珍奇櫃 典藏 Header ---
st.markdown(
    """
    <div class="curio-hero-card">
        <h1>🔮 夢境珍奇櫃 ‧ 診間去敏拋接面板</h1>
        <p>Cabinet of Curiosities x 交感身心診所 ｜ Zero-Knowledge Architecture ‧ 0 個資 ‧ 診前 15 秒身心軌跡拋接</p>
    </div>
""",
    unsafe_allow_html=True,
)

# --- 夢境珍奇櫃 典藏膠囊標籤 ---
st.markdown(
    """
    <div class="curio-meta-bar">
        <div class="curio-pill"><b>🏛️ 合作機構</b> ｜ 交感身心診所</div>
        <div class="curio-pill"><b>🩺 看診醫師</b> ｜ 郭家穎 院長</div>
        <div class="curio-pill" style="border-color:#5A7292; color:#25354A; background:#EBF2FA;"><b>🛡️ 物理隔離防線</b> ｜ A4 保險箱機制 [已死鎖]</div>
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
        # 連線成功狀態列 (莫蘭迪淺藍徽章)
        st.markdown(
            f"""
            <div style="background-color: #E8F0F8; border-left: 4px solid #5A7292; padding: 12px 18px; border-radius: 12px; margin-bottom: 22px; font-size: 0.9rem; color: #25354A;">
                <b>💎 成功連線至去敏密鑰 <code>{user_key}</code></b> ｜ 狀態：{data['status']} ｜ 更新時間：{data['timestamp']}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 3 大指標卡片 (夢境珍奇櫃 圖騰風)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "🌌 心流一致性 (0.067Hz)",
                f"{data['coherence_score']} %",
                "↑ 3.2% 穩定共振",
            )
        with col2:
            st.metric("🌿 身心應激狀態", data["stress_index"], "莫蘭迪淺藍放鬆區")
        with col3:
            st.metric("🌙 本機睡眠時數", f"{data['sleep_hours']} hr", "達標 7 小時")

        st.markdown(
            "<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True
        )

        # 分頁
        tab1, tab2 = st.tabs(
            ["📈 近 7 日心流平穩度曲線", "📄 診前 15 秒去敏摘要"]
        )

        with tab1:
            st.markdown(
                "<h4 style='color:#25354A; font-size:1.05rem; margin-top:10px;'>近 7 日心流一致性調息曲線 (Coherence Score)</h4>",
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

            # 折線圖採用莫蘭迪藍主色 `#5A7292`
            st.line_chart(chart_data, color="#5A7292")

        with tab2:
            st.markdown(
                "<h4 style='color:#25354A; font-size:1.05rem; margin-top:10px;'>邊緣端 15 秒去敏化身心軌跡</h4>",
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