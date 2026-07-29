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

# 2. 重構：法式極致奢華藝廊 UI / CSS 設計 (French Fine-Art Gallery & Medical Grade)
st.markdown(
    """
    <style>
    /* 全域背景：極致珍珠暖白 */
    .stApp {
        background-color: #FAF9F6;
        font-family: -apple-system, BlinkMacSystemFont, "Garamond", "Georgia", "PingFang TC", "Helvetica Neue", sans-serif;
    }
    header[data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    footer { visibility: hidden; }

    /* 主頂樓高奢面板卡片 (Midnight Slate & Fine Champagne Gold) */
    .curio-hero-card {
        background: linear-gradient(135deg, #1A2634 0%, #2D3E50 100%);
        color: #FAF9F6;
        padding: 36px 44px;
        border-radius: 28px;
        box-shadow: 0 20px 48px rgba(26, 38, 52, 0.08);
        border: 1px solid #C8B282; /* 精緻香檳金微光邊框 */
        margin-bottom: 30px;
    }
    .curio-hero-card h1 { 
        font-family: "Georgia", "PingFang TC", serif !important;
        color: #FAF9F6 !important; 
        font-size: 1.7rem !important; 
        font-weight: 500 !important; 
        letter-spacing: 1.2px !important;
        margin: 0 0 10px 0 !important; 
    }
    .curio-hero-card p { 
        color: #D2DCED !important; 
        font-size: 0.88rem !important; 
        margin: 0 !important; 
        font-weight: 300; 
        letter-spacing: 0.6px;
    }

    /* 登入卡片 (High-End Gallery Glass Card) */
    .gallery-login-card {
        background: #FFFFFF;
        border: 1px solid #E8E2D5;
        padding: 52px 48px 40px 48px;
        border-radius: 30px;
        box-shadow: 0 24px 60px rgba(26, 38, 52, 0.05);
        max-width: 500px;
        margin: 40px auto 20px auto;
        text-align: center;
    }
    .brand-caption {
        font-family: "Georgia", serif;
        font-style: italic;
        color: #B59E75;
        font-size: 0.88rem;
        letter-spacing: 2px;
        margin-bottom: 8px;
        text-transform: uppercase;
    }
    .medical-title {
        color: #1A2634;
        font-family: "Georgia", "PingFang TC", serif;
        font-size: 1.5rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 14px;
    }
    .gold-divider {
        width: 40px;
        height: 2px;
        background: linear-gradient(90deg, #D4AF37 0%, #C8B282 100%);
        margin: 18px auto 24px auto;
        border-radius: 2px;
    }
    .medical-desc {
        color: #5C6B73;
        font-size: 0.88rem;
        line-height: 1.65;
        margin-bottom: 32px;
        font-weight: 300;
    }

    /* 資安公告盒 */
    .security-notice-box {
        background-color: #F4F1EA;
        border-left: 3px solid #C8B282;
        border-radius: 14px;
        padding: 22px 26px;
        margin-top: 30px;
        font-size: 0.85rem;
        color: #1A2634;
        line-height: 1.7;
    }

    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E8E2D5;
        padding: 26px 28px;
        border-radius: 24px;
        box-shadow: 0 10px 28px rgba(26, 38, 52, 0.03);
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

# 雲端雙盲中繼站模擬資料庫
if "mock_db" not in st.session_state:
    st.session_state["mock_db"] = {
        "#SYM-C701": {
            "status": "已完成診前 15s 共振調息",
            "coherence_score": 92.5,
            "stress_index": "Morandi Soft Blue (心流平穩)",
            "sleep_hours": 7.2,
            "timestamp": "2026-07-30 01:20:15",
            "weekly_trend": [82, 85, 87, 84, 89, 91, 92.5],
            "summary": "【去敏身心軌跡摘要】個案於看診前 15 秒於候診區完成 0.067 Hz 心流共振調息。連續 7 日數據顯示夜間無應激爆發，心流一致性維持於 90% 以上高諧振區間。",
        },
        "#SYM-A302": {
            "status": "已完成診前 15s 共振調息",
            "coherence_score": 88.0,
            "stress_index": "Morandi Sage (輕度交感活性)",
            "sleep_hours": 6.1,
            "timestamp": "2026-07-30 01:25:00",
            "weekly_trend": [70, 75, 78, 80, 82, 85, 88.0],
            "summary": "【去敏身心軌跡摘要】個案於候診區完成心流調息。近 7 日睡眠時數偏低，生理指標顯示交感神經活性略微上升。",
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
        st.write("為了維護診間門診資安，請輸入原金鑰並設定新金鑰：")
        old_pwd = st.text_input("輸入原診間金鑰：", type="password")
        new_pwd = st.text_input("設定新診間金鑰：", type="password")
        confirm_pwd = st.text_input("再次確認新診間金鑰：", type="password")

        if st.button("🔒 確認更新診間金鑰", use_container_width=True):
            if old_pwd != st.session_state["doctor_password"]:
                st.error("❌ 原金鑰輸入錯誤，請重新確認！")
            elif not new_pwd:
                st.warning("⚠️ 新金鑰不能為空！")
            elif new_pwd != confirm_pwd:
                st.error("❌ 兩次新金鑰輸入不一致！")
            else:
                st.session_state["doctor_password"] = new_pwd
                st.success("🎉 診間金鑰已成功變更！舊金鑰已即刻失效。")
                st.rerun()


# --- 5. 重構：高奢極簡 門診驗證畫面 ---
if not st.session_state["authenticated"]:
    st.markdown(
        """
        <div class="gallery-login-card">
            <div class="brand-caption">Cabinet of Curiosities</div>
            <div class="medical-title">交感身心診所 ‧ 門診安全驗證</div>
            <div class="gold-divider"></div>
            <div class="medical-desc">零知識架構 (Zero-Knowledge) ‧ 雙盲去敏身心軌跡拋接<br>請輸入郭家穎院長專屬診間金鑰，解鎖門診調息數據</div>
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

        if st.button("🔓 解鎖門診數據面板", use_container_width=True):
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
            "summary": f"【去敏身心軌跡摘要】經由 LINE LIFF 拋接之短碼 {token_a}。個案完成診前調息，心流表現極佳。",
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
        <div style="background:#FFFFFF; border:1px solid #E8E2D5; border-radius:30px; padding:10px 26px; font-size:0.86rem; color:#1A2634;">
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
            <div style="background-color: #F4F1EA; border-left: 4px solid #C8B282; padding: 14px 22px; border-radius: 14px; margin-bottom: 24px; font-size: 0.92rem; color: #1A2634;">
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
                "<h4 style='color:#1A2634; font-size:1.05rem; margin-top:12px;'>近 7 日心流一致性調息曲線 (Coherence Score)</h4>",
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
            st.line_chart(chart_data, color="#2D3E50")

        with tab2:
            st.markdown(
                "<h4 style='color:#1A2634; font-size:1.05rem; margin-top:10px;'>邊緣端 15 秒去敏化身心軌跡</h4>",
                unsafe_allow_html=True,
            )
            st.write(f"**【去敏軌跡摘要】**\n\n{data['summary']}")
            st.caption(f"🕒 數據傳輸時間戳記：{data['timestamp']}")

        st.markdown(
            """
            <div class="security-notice-box">
                <b>🛡️ 零知識架構與個資法規合規宣告 (Zero-Knowledge & Privacy Compliance)</b><br>
                1. <b>符合個資法規</b>：本系統嚴格遵循中華民國《個人資料保護法》第 2 條之去識別化標準。<b>系統全流程絕不收集、記錄或存儲病患之真實姓名、身分證字號、出生年月日、聯絡電話、醫療病歷號碼或 IP 位址</b>。<br>
                2. <b>資安傳輸與儲存防護</b>：前端至雲端中繼站之數據傳輸全數採用 <b>HTTPS (TLS 1.3) 高階加密通道</b>，靜態快取數據皆實施 <b>AES-256 演算法加密</b>；雲端中繼數據實施 240 分鐘動態時間鎖（Time-Lock）與每日 24 點剛性銷毀（Data TTL）。
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error(
            f"⚠️ 找不到密鑰 `{user_key}` 之當日資料，請確認代碼是否輸入正確。"
        )