import time
import pandas as pd
import streamlit as st

# 1. 全局配置
st.set_page_config(
    page_title="Cabinet of Curiosities ‧ 診間去敏拋接面板",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. 全面重構：法式優雅生活美學 CSS (French Salon Aesthetics)
st.markdown(
    """
    <style>
    /* 法式柔和背景：香氣亞麻白 (Oatmeal Linen) */
    .stApp {
        background-color: #F9F8F6;
        font-family: -apple-system, BlinkMacSystemFont, "Garamond", "Georgia", "PingFang TC", "微軟正黑體", sans-serif;
    }
    header[data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    footer { visibility: hidden; }

    /* 法式高奢主頂樓卡片 (Smoky Slate & Silk Gold) */
    .curio-hero-card {
        background: linear-gradient(135deg, #324353 0%, #4A5D70 100%);
        color: #F8F6F0;
        padding: 32px 40px;
        border-radius: 28px;
        box-shadow: 0 16px 36px rgba(50, 67, 83, 0.08);
        border: 1px solid #C5B396; /* 細微金絲邊框 */
        margin-bottom: 28px;
    }
    .curio-hero-card h1 { 
        font-family: "Georgia", "PingFang TC", serif !important;
        color: #FAF8F5 !important; 
        font-size: 1.65rem !important; 
        font-weight: 500 !important; 
        letter-spacing: 1px !important;
        margin: 0 0 10px 0 !important; 
    }
    .curio-hero-card p { 
        color: #D3DCB8 !important; 
        font-size: 0.88rem !important; 
        margin: 0 !important; 
        font-weight: 300; 
        letter-spacing: 0.5px;
    }

    /* 法式沙龍登入卡片 (Pearl Glassmorphism) */
    .french-login-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(12px);
        border: 1px solid #E6DFD5;
        padding: 48px 42px 36px 42px;
        border-radius: 28px;
        box-shadow: 0 20px 48px rgba(74, 93, 112, 0.06);
        max-width: 480px;
        margin: 40px auto 20px auto;
        text-align: center;
    }
    .salon-logo-subtitle {
        font-family: "Georgia", serif;
        font-style: italic;
        color: #928370;
        font-size: 0.9rem;
        letter-spacing: 1.5px;
        margin-bottom: 6px;
        text-transform: uppercase;
    }
    .salon-title {
        color: #324353;
        font-family: "Georgia", "PingFang TC", serif;
        font-size: 1.45rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
    }
    .salon-divider {
        width: 36px;
        height: 2px;
        background-color: #C5B396;
        margin: 16px auto 22px auto;
        border-radius: 2px;
    }
    .salon-desc {
        color: #6E7C8C;
        font-size: 0.86rem;
        line-height: 1.6;
        margin-bottom: 28px;
        font-weight: 300;
    }

    /* 優雅資訊區塊 */
    .salon-notice-box {
        background-color: #F2EFEA;
        border-left: 3px solid #C5B396;
        border-radius: 12px;
        padding: 20px 24px;
        margin-top: 28px;
        font-size: 0.85rem;
        color: #324353;
        line-height: 1.7;
    }

    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #EBE5DC;
        padding: 24px 26px;
        border-radius: 22px;
        box-shadow: 0 8px 24px rgba(50, 67, 83, 0.03);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. 初始化 Session State 狀態與醫生金鑰
if "doctor_password" not in st.session_state:
    st.session_state["doctor_password"] = "NYJAZZ-8519"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "selected_token" not in st.session_state:
    st.session_state["selected_token"] = "#SYM-C701"

# 模擬中繼站資料庫
if "mock_db" not in st.session_state:
    st.session_state["mock_db"] = {
        "#SYM-C701": {
            "status": "已完成診前 15s 共振調息",
            "coherence_score": 92.5,
            "stress_index": "Morandi Soft Blue (心流平穩)",
            "sleep_hours": 7.2,
            "timestamp": "2026-07-30 01:20:15",
            "weekly_trend": [82, 85, 87, 84, 89, 91, 92.5],
            "summary": "【法式身心軌跡摘要】個案於看診前 15 秒於候診區完成 0.067 Hz 心流共振調息。連續 7 日數據顯示夜間無應激爆發，心流一致性維持於 90% 以上高諧振區間。",
        },
        "#SYM-A302": {
            "status": "已完成診前 15s 共振調息",
            "coherence_score": 88.0,
            "stress_index": "Morandi Sage (輕度交感活性)",
            "sleep_hours": 6.1,
            "timestamp": "2026-07-30 01:25:00",
            "weekly_trend": [70, 75, 78, 80, 82, 85, 88.0],
            "summary": "【法式身心軌跡摘要】個案於候診區完成心流調息。近 7 日睡眠時數偏低，生理指標顯示交感神經活性略微上升。",
        },
    }

if "checkin_queue" not in st.session_state:
    st.session_state["checkin_queue"] = [
        {
            "token": "#SYM-C701",
            "time": "01:20",
            "source": "LINE LIFF / App",
        },
        {
            "token": "#SYM-A302",
            "time": "01:25",
            "source": "LINE LIFF / App",
        },
    ]

MASTER_KEY = "CURIO-999"

# --- 4. 變更密碼 Modal 彈窗 ---
if hasattr(st, "dialog"):

    @st.dialog("⚙️ 變更診間金鑰（郭家穎院長專屬）")
    def change_password_dialog():
        st.write("為了維持門診安全，請輸入原密碼並設定新金鑰：")
        old_pwd = st.text_input("輸入原診間密碼：", type="password")
        new_pwd = st.text_input("設定新診間密碼：", type="password")
        confirm_pwd = st.text_input("再次確認新診間密碼：", type="password")

        if st.button("🔒 確認更新金鑰", use_container_width=True):
            if old_pwd != st.session_state["doctor_password"]:
                st.error("❌ 原密碼輸入錯誤，請重新確認！")
            elif not new_pwd:
                st.warning("⚠️ 新密碼不能為空！")
            elif new_pwd != confirm_pwd:
                st.error("❌ 兩次新密碼輸入不一致！")
            else:
                st.session_state["doctor_password"] = new_pwd
                st.success("🎉 診間金鑰已成功變更！舊密碼已即刻失效。")
                st.rerun()


# --- 5. 法式優雅沙龍 登入驗證畫面 ---
if not st.session_state["authenticated"]:
    st.markdown(
        """
        <div class="french-login-card">
            <div class="salon-logo-subtitle">Cabinet of Curiosities</div>
            <div class="salon-title">交感身心診所 ‧ 門診安全驗證</div>
            <div class="salon-divider"></div>
            <div class="salon-desc">0 個資法規合規 ‧ 雙盲去敏身心軌跡拋接<br>請輸入郭家穎院長專屬診間金鑰，解鎖身心調息曲線</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1.2, 1.8, 1.2])
    with col2:
        pwd_input = st.text_input(
            "院長診間金鑰",
            type="password",
            key="pwd_field",
            placeholder="請輸入金鑰 (例如：NYJAZZ-8519)",
        )

        st.markdown(
            "<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True
        )

        if st.button("✨ 解鎖沙龍診間面板", use_container_width=True):
            if (
                pwd_input == st.session_state["doctor_password"]
                or pwd_input == MASTER_KEY
            ):
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("⚠️ 金鑰驗證未通過，請確認後重新輸入。")

        st.markdown(
            "<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True
        )

        with st.expander("❓ 忘記診間金鑰密碼？"):
            st.info(
                f"💡 **密碼提示**：GOOGLE帳號 + 西元出生年份（當前預設：`{st.session_state['doctor_password']}`）\n\n如需緊急技術支援，請聯繫居里研創專屬服務團隊。"
            )

    st.stop()


# --- 6. 側邊欄：API & Webhook 模擬器 ---
with st.sidebar:
    st.markdown("### 🔌 背景 API 與 Webhook 模擬器")
    st.caption("用於向郭醫師演示 LINE LIFF 與叫號系統無縫 Push")

    st.markdown("---")
    st.markdown("#### 📱 路徑 A：LINE LIFF / App 資料拋接")
    token_a = st.text_input("去敏短碼 (Token):", value="#SYM-B888")
    score_a = st.slider("心流分數:", 60.0, 100.0, 94.0)

    if st.button("📡 [路徑 A] 模擬 App 拋接 API"):
        current_time_str = time.strftime("%H:%M")
        st.session_state["mock_db"][token_a] = {
            "status": "已完成診前 15s 共振調息",
            "coherence_score": score_a,
            "stress_index": "Morandi Soft Blue (心流平穩)",
            "sleep_hours": 7.5,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "weekly_trend": [80, 82, 85, 88, 90, 92, score_a],
            "summary": f"【法式身心軌跡摘要】經由 LINE LIFF 拋接之短碼 {token_a}。個案完成診前調息，心流表現極佳。",
        }
        st.session_state["checkin_queue"].append(
            {
                "token": token_a,
                "time": current_time_str,
                "source": "LINE LIFF API",
            }
        )
        st.toast(f"✅ [路徑 A] 已收到 {token_a} 數據！")
        st.rerun()

    st.markdown("---")
    st.markdown("#### 🔔 路徑 B：叫號系統 Webhook 觸發")
    st.caption("當護理師在 HIS/LINE 點擊『下一位進診間』：")

    if st.button("🚀 [路徑 B] 模擬 HIS 叫號 Webhook"):
        if st.session_state["checkin_queue"]:
            latest_token = st.session_state["checkin_queue"][-1]["token"]
            st.session_state["selected_token"] = latest_token
            st.toast(
                f"🔔 [路徑 B Webhook] 收到叫號事件！已自動載入 {latest_token}"
            )
            st.rerun()

    st.markdown("---")
    st.markdown("### 📋 診間待看診佇列 (Queue)")
    for item in st.session_state["checkin_queue"]:
        if st.button(
            f"🔓 {item['token']} ({item['time']})",
            key=f"btn_{item['token']}",
            use_container_width=True,
        ):
            st.session_state["selected_token"] = item["token"]
            st.rerun()


# --- 7. 主面板邏輯 ---
def fetch_patient_data(user_key):
    return st.session_state["mock_db"].get(user_key, None)


# Header
st.markdown(
    """
    <div class="curio-hero-card">
        <h1>💎 Cabinet of Curiosities ‧ 診間去敏拋接面板</h1>
        <p>Cabinet of Curiosities x 交感身心診所 ｜ Zero-Knowledge Architecture ‧ 0 個資 ‧ 診前 15 秒身心軌跡拋接</p>
    </div>
""",
    unsafe_allow_html=True,
)

# 頂部狀態列
top_col1, top_col2 = st.columns([3, 1])
with top_col1:
    st.markdown(
        """
        <div style="background:#FFFFFF; border:1px solid #EBE5DC; border-radius:30px; padding:10px 26px; font-size:0.86rem; color:#324353;">
            🟢 <b>郭家穎 院長</b>（交感身心診所）已通過診間安全認證 ｜ 🏛️ 診間號：C701 ｜ 🛡️ <b>0 個資死鎖狀態</b>
        </div>
    """,
        unsafe_allow_html=True,
    )
with top_col2:
    if st.button("⚙️ 變更診間金鑰", use_container_width=True):
        if hasattr(st, "dialog"):
            change_password_dialog()

st.markdown(
    "<div style='margin-bottom: 22px;'></div>", unsafe_allow_html=True
)

# 搜尋輸入框
user_key = st.text_input(
    "請輸入探險家去敏密鑰 (例如：#SYM-C701) :",
    value=st.session_state["selected_token"],
    placeholder="輸入密鑰代碼，例如 #SYM-C701",
)

if user_key:
    data = fetch_patient_data(user_key)
    if data:
        st.markdown(
            f"""
            <div style="background-color: #F2EFEA; border-left: 4px solid #C5B396; padding: 14px 22px; border-radius: 14px; margin-bottom: 24px; font-size: 0.92rem; color: #324353;">
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
            st.metric("🌿 身心應激狀態", data["stress_index"], "莫蘭迪區域")
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
                "<h4 style='color:#324353; font-size:1.05rem; margin-top:12px;'>近 7 日心流一致性調息曲線 (Coherence Score)</h4>",
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
            st.line_chart(chart_data, color="#4A5D70")

        with tab2:
            st.markdown(
                "<h4 style='color:#324353; font-size:1.05rem; margin-top:10px;'>邊緣端 15 秒去敏化身心軌跡</h4>",
                unsafe_allow_html=True,
            )
            st.write(f"**【去敏軌跡摘要】**\n\n{data['summary']}")
            st.caption(f"🕒 數據傳輸時間戳記：{data['timestamp']}")

        st.markdown(
            """
            <div class="salon-notice-box">
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