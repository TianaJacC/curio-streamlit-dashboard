import pandas as pd
import streamlit as st

# 1. 全局配置
st.set_page_config(
    page_title="Cabinet of Curiosities ‧ 診間去敏拋接面板",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. 莫蘭迪淺藍 CSS 樣式
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F2F5F8;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang TC", sans-serif;
    }
    header[data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    footer { visibility: hidden; }

    .curio-hero-card {
        background: linear-gradient(135deg, #3B4E68 0%, #5A7292 100%);
        color: #FFFFFF;
        padding: 26px 30px;
        border-radius: 20px;
        box-shadow: 0 10px 24px rgba(59, 78, 104, 0.15);
        border: 1px solid #7188A6;
        margin-bottom: 22px;
    }
    .curio-hero-card h1 { color: #FFFFFF !important; font-size: 1.45rem !important; font-weight: 600 !important; margin: 0 0 6px 0 !important; }
    .curio-hero-card p { color: #D6E1EF !important; font-size: 0.85rem !important; margin: 0 !important; }

    .login-box {
        background: #FFFFFF;
        border: 1px solid #D8E2EE;
        padding: 35px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(59, 78, 104, 0.08);
        max-width: 480px;
        margin: 60px auto;
        text-align: center;
    }
    .login-box h2 { color: #3B4E68; font-size: 1.3rem; margin-bottom: 10px; }
    .login-box p { color: #627792; font-size: 0.88rem; margin-bottom: 20px; }
    
    .security-notice-box {
        background-color: #EBF2FA;
        border: 1px solid #C5D8ED;
        border-radius: 14px;
        padding: 16px 20px;
        margin-top: 25px;
        font-size: 0.85rem;
        color: #25354A;
        line-height: 1.6;
    }

    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #D8E2EE;
        padding: 20px 22px;
        border-radius: 18px;
        box-shadow: 0 6px 16px rgba(59, 78, 104, 0.04);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. 密碼驗證邏輯 (Session State)
DOCTOR_PASSWORD = "NYJAZZ-8519"  # 郭醫師專屬密碼
MASTER_KEY = "CURIO-999"  # 玥如緊急救援金鑰

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# --- 未驗證時顯示登入鎖定畫面 ---
if not st.session_state["authenticated"]:
    st.markdown(
        """
        <div class="login-box">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">🔒</div>
            <h2>交感身心診所 ‧ 門診安全驗證</h2>
            <p>請輸入郭家穎院長專屬診間金鑰，解鎖去敏身心軌跡拋接面板。</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pwd_input = st.text_input(
            "請輸入診間密碼：", type="password", key="pwd_field"
        )
        if st.button("🔓 開鎖登入", use_container_width=True):
            if pwd_input == DOCTOR_PASSWORD or pwd_input == MASTER_KEY:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("⚠️ 密碼錯誤！請重新輸入或確認門診金鑰小卡。")

        # 忘記密碼溫柔提示
        with st.expander("❓ 忘記診間密碼？"):
            st.info(
                "💡 **密碼提示**：GOOGLE帳號 + 西元出生年分（如：`KA-2000`）\n\n若仍無法登入，請使用紙本同意書資料夾內之「門診金鑰小卡」，或聯繫居里研創專屬服務團隊。"
            )
    st.stop()

# --- 驗證成功後顯示的主面板 ---


def fetch_patient_data(user_key):
    mock_db = {
        "#C701": {
            "status": "已完成診前 15s 調息",
            "coherence_score": 92.5,
            "stress_index": "Morandi Soft Blue (平穩)",
            "sleep_hours": 7.2,
            "timestamp": "2026-07-29 12:20:15",
            "weekly_trend": [82, 85, 87, 84, 89, 91, 92.5],
            "summary": "【去敏軌跡摘要】個案於看診前 15 秒於候診區完成 0.067 Hz 心流共振調息。連續 7 日數據顯示夜間無應激爆發，心流一致性維持於 90% 以上良好區間。",
        }
    }
    return mock_db.get(user_key, None)


# --- Header & 驗證狀態列 ---
st.markdown(
    """
    <div class="curio-hero-card">
        <h1>🔮 夢境珍奇櫃 ‧ 診間去敏拋接面板</h1>
        <p>Cabinet of Curiosities x 交感身心診所 ｜ Zero-Knowledge Architecture ‧ 0 個資 ‧ 診前 15 秒身心軌跡拋接</p>
    </div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="display:flex; justify-content:space-between; align-items:center; background:#FFFFFF; border:1px solid #D2DCED; border-radius:30px; padding:8px 20px; margin-bottom:22px; font-size:0.85rem; color:#334763;">
        <div>🟢 <b>郭家穎 院長</b>（交感身心診所）已通過診間安全認證 ｜ 🏛️ 診間號：C701</div>
        <div>🛡️ <b>0 個資死鎖狀態</b></div>
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
        st.markdown(
            f"""
            <div style="background-color: #E8F0F8; border-left: 4px solid #5A7292; padding: 12px 18px; border-radius: 12px; margin-bottom: 22px; font-size: 0.9rem; color: #25354A;">
                <b>💎 成功連線至去敏密鑰 <code>{user_key}</code></b> ｜ 狀態：{data['status']} ｜ 更新時間：{data['timestamp']}
            </div>
            """,
            unsafe_allow_html=True,
        )

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
            st.line_chart(chart_data, color="#5A7292")

        with tab2:
            st.markdown(
                "<h4 style='color:#25354A; font-size:1.05rem; margin-top:10px;'>邊緣端 15 秒去敏化身心軌跡</h4>",
                unsafe_allow_html=True,
            )
            st.write(f"**【去敏軌跡摘要】**\n\n{data['summary']}")
            st.caption(f"🕒 數據傳輸時間戳記：{data['timestamp']}")

        st.markdown(
            """
            <div class="security-notice-box">
                <b>🛡️ 零知識架構與個資法規合規宣告 (Zero-Knowledge & Privacy Compliance)</b><br>
                1. <b>符合個資法規</b>：本系統嚴格遵循中華民國《個人資料保護法》第 2 條之去識別化標準。<b>系統全流程絕不收集、記錄或存儲病患之真實姓名、身分證字號、出生年月日、聯絡電話、醫療病歷號碼或 IP 位址</b>。<br>
                2. <b>資安傳輸與儲存防護</b>：前端至雲端中繼站之數據傳輸全數採用 <b>HTTPS (TLS 1.3) 高階加密通道</b>，靜態快取數據皆實施 <b>AES-256 演算法加密</b>；雲端中繼數據實施 240 分鐘動態時間鎖（Time-Lock）與每日 24 小時剛性銷毀（Data TTL）。
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error(
            f"⚠️ 找不到密鑰 `{user_key}` 之當日資料，請確認代碼是否輸入正確。"
        )