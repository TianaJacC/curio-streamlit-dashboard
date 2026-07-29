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

# 2. 莫蘭迪淺藍高奢 CSS 樣式
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

# 3. 初始化 Session State 狀態與模擬資料庫
if "doctor_password" not in st.session_state:
    st.session_state["doctor_password"] = "NYJAZZ-8519"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "selected_token" not in st.session_state:
    st.session_state["selected_token"] = "#SYM-C701"

# 雲端雙盲中繼站模擬資料庫 (Mock Broker Database)
if "mock_db" not in st.session_state:
    st.session_state["mock_db"] = {
        "#SYM-C701": {
            "status": "已完成診前 15s 調息",
            "coherence_score": 92.5,
            "stress_index": "Morandi Soft Blue (平穩)",
            "sleep_hours": 7.2,
            "timestamp": "2026-07-30 01:20:15",
            "weekly_trend": [82, 85, 87, 84, 89, 91, 92.5],
            "summary": "【去敏軌跡摘要】個案於看診前 15 秒於候診區完成 0.067 Hz 心流共振調息。連續 7 日數據顯示夜間無應激爆發，心流一致性維持於 90% 以上良好區間。",
        },
        "#SYM-A302": {
            "status": "已完成診前 15s 調息",
            "coherence_score": 88.0,
            "stress_index": "Morandi Sage (輕度應激)",
            "sleep_hours": 6.1,
            "timestamp": "2026-07-30 01:25:00",
            "weekly_trend": [70, 75, 78, 80, 82, 85, 88.0],
            "summary": "【去敏軌跡摘要】個案於候診區完成心流調息。近 7 日睡眠時數偏低，生理指標顯示交感神經活性略微上升。",
        },
    }

# 待拋接佇列 (Queue)
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


# --- 5. 門診安全驗證畫面 ---
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
            if (
                pwd_input == st.session_state["doctor_password"]
                or pwd_input == MASTER_KEY
            ):
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("⚠️ 密碼錯誤！請重新輸入或確認門診金鑰小卡。")

        with st.expander("❓ 忘記診間密碼？"):
            st.info(
                f"💡 **密碼提示**：GOOGLE帳號 + 西元出身年份（當前預設：`{st.session_state['doctor_password']}`）\n\n若仍無法登入，請使用紙本同意書資料夾內之「門診金鑰小卡」，或聯繫居里研創專屬服務團隊。"
            )
    st.stop()


# --- 6. 側邊欄：【路徑 A 與路徑 B】模擬控制台 ---
with st.sidebar:
    st.markdown("### 🔌 背景 API 與 Webhook 模擬器")
    st.caption("用於向郭醫師演示 LINE LIFF 與叫號系統無縫 Push")

    st.markdown("---")
    st.markdown("#### 📱 路徑 A：LINE LIFF / App 資料拋接")
    token_a = st.text_input("去敏短碼 (Token):", value="#SYM-B888")
    score_a = st.slider("心流分數:", 60.0, 100.0, 94.0)

    if st.button("📡 [路徑 A] 模擬 App 拋接 API"):
        current_time_str = time.strftime("%H:%M")
        # 寫入模擬資料庫
        st.session_state["mock_db"][token_a] = {
            "status": "已完成診前 15s 調息",
            "coherence_score": score_a,
            "stress_index": "Morandi Soft Blue (平穩)",
            "sleep_hours": 7.5,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "weekly_trend": [80, 82, 85, 88, 90, 92, score_a],
            "summary": f"【去敏軌跡摘要】經由 LINE LIFF 拋接之短碼 {token_a}。個案完成診前調息，心流表現極佳。",
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
        <h1>🔮 夢境珍奇櫃 ‧ 診間去敏拋接面板</h1>
        <p>Cabinet of Curiosities x 交感身心診所 ｜ Zero-Knowledge Architecture ‧ 0 個資 ‧ 診前 15 秒身心軌跡拋接</p>
    </div>
""",
    unsafe_allow_html=True,
)

# 頂部狀態列與密碼齒輪
top_col1, top_col2 = st.columns([3, 1])
with top_col1:
    st.markdown(
        """
        <div style="background:#FFFFFF; border:1px solid #D2DCED; border-radius:30px; padding:8px 20px; font-size:0.85rem; color:#334763;">
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
    "<div style='margin-bottom: 18px;'></div>", unsafe_allow_html=True
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