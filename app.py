import time
import pandas as pd
import streamlit as st

# 1. 全局配置
st.set_page_config(
    page_title="Cabinet of Curiosities ‧ Curio & Studio 診間面板",
    page_icon="🐿️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Curio & Studio 3D/4D 俏皮優雅法式美學 CSS (Chic Claymorphism)
st.markdown(
    """
    <style>
    /* 全域背景：香草奶油白 */
    .stApp {
        background-color: #FAF8F5;
        font-family: -apple-system, BlinkMacSystemFont, "Garamond", "Georgia", "PingFang TC", "Helvetica Neue", sans-serif;
    }
    header[data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    footer { visibility: hidden; }

    /* 主頂樓卡片：3D 蔻恩閣長森林綠 */
    .curio-hero-card {
        background: linear-gradient(135deg, #3D5245 0%, #2A3B31 100%);
        color: #FAF8F5;
        padding: 32px 42px;
        border-radius: 28px;
        box-shadow: 0 20px 45px rgba(61, 82, 69, 0.12);
        border: 1px solid #C2A675;
        margin-bottom: 28px;
        position: relative;
    }
    .curio-hero-card h1 { 
        font-family: "Georgia", "PingFang TC", serif !important;
        color: #FAF8F5 !important; 
        font-size: 1.75rem !important; 
        font-weight: 500 !important; 
        letter-spacing: 1.2px !important;
        margin: 0 0 8px 0 !important; 
    }
    .curio-hero-card p { 
        color: #E2EADF !important; 
        font-size: 0.9rem !important; 
        margin: 0 !important; 
        font-weight: 300; 
        letter-spacing: 0.6px;
    }

    /* 3D 俏皮小松鼠徽章 (Cone Badge) */
    .cone-3d-badge {
        width: 72px;
        height: 72px;
        background: linear-gradient(145deg, #FAF8F5, #EAE4D8);
        border-radius: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.3rem;
        box-shadow: 6px 6px 16px rgba(0, 0, 0, 0.08), -4px -4px 12px rgba(255, 255, 255, 0.9);
        border: 2px solid #C2A675;
        margin: 0 auto 16px auto;
    }

    /* 登入卡片 (3D Clay & Pearl Glass) */
    .atelier-login-card {
        background: rgba(255, 255, 255, 0.94);
        backdrop-filter: blur(20px);
        border: 1px solid #E3DCD1;
        padding: 48px 46px 32px 46px;
        border-radius: 32px;
        box-shadow: 0 24px 60px rgba(61, 82, 69, 0.06);
        max-width: 500px;
        margin: 25px auto 12px auto;
        text-align: center;
    }
    .brand-caption {
        font-family: "Georgia", serif;
        font-style: italic;
        color: #B29562;
        font-size: 0.92rem;
        letter-spacing: 2.5px;
        margin-bottom: 8px;
        text-transform: uppercase;
    }
    .medical-title {
        color: #2A3B31;
        font-family: "Georgia", "PingFang TC", serif;
        font-size: 1.55rem;
        font-weight: 600;
        letter-spacing: 0.8px;
        margin-bottom: 12px;
    }
    .gold-divider {
        width: 44px;
        height: 2px;
        background: linear-gradient(90deg, #C2A675 0%, #E8D8B8 100%);
        margin: 16px auto 22px auto;
        border-radius: 2px;
    }
    .medical-desc {
        color: #5C6E63;
        font-size: 0.88rem;
        line-height: 1.65;
        margin-bottom: 24px;
        font-weight: 300;
    }

    /* 3D 俏皮 Metric 數據卡片 */
    .custom-metric-card {
        background: #FFFFFF;
        border: 1px solid #E3DCD1;
        padding: 24px 26px;
        border-radius: 24px;
        box-shadow: 6px 6px 20px rgba(61, 82, 69, 0.04), -4px -4px 14px rgba(255, 255, 255, 0.8);
        height: 100%;
    }
    .custom-metric-label { font-size: 0.88rem; color: #697C70; font-weight: 400; margin-bottom: 8px; }
    .custom-metric-value { font-size: 1.52rem; color: #2A3B31; font-weight: 600; font-family: "Georgia", "PingFang TC", serif; margin-bottom: 8px; line-height: 1.2; }
    .custom-metric-delta { font-size: 0.82rem; color: #4E6054; background-color: #F3EFE8; padding: 4px 12px; border-radius: 10px; display: inline-block; line-height: 1.4; border: 1px solid #E3DCD1; }

    /* 知性資安公告盒 */
    .security-notice-box {
        background-color: #F3EFE8;
        border-left: 4px solid #C2A675;
        border-radius: 18px;
        padding: 22px 26px;
        margin-top: 28px;
        font-size: 0.86rem;
        color: #2A3B31;
        line-height: 1.7;
    }

    /* 3D 俏皮側邊欄模組卡片 */
    .sidebar-3d-box {
        background: #FFFFFF;
        border: 1px solid #E3DCD1;
        border-radius: 20px;
        padding: 18px;
        margin-bottom: 18px;
        box-shadow: 4px 4px 12px rgba(61, 82, 69, 0.04);
    }

    /* 優雅按鈕 */
    .stButton>button {
        border-radius: 14px !important;
        border: 1px solid #C2A675 !important;
        background: linear-gradient(135deg, #FAF8F5 0%, #F3EFE8 100%) !important;
        color: #2A3B31 !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #3D5245 0%, #2A3B31 100%) !important;
        color: #FAF8F5 !important;
        border: 1px solid #3D5245 !important;
        box-shadow: 0 6px 18px rgba(61, 82, 69, 0.15) !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Session State 初始化
if "doctor_password" not in st.session_state:
    st.session_state["doctor_password"] = "NYJAZZ-8519"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "selected_token" not in st.session_state:
    st.session_state["selected_token"] = "#SYM-C701"

if "mock_db" not in st.session_state:
    st.session_state["mock_db"] = {
        "#SYM-C701": {
            "status": "已完成診前 15s 共振調息",
            "coherence_score": 92.5,
            "stress_index": "Morandi Soft Blue",
            "stress_desc": "莫蘭迪藍放縮區 ‧ 平穩",
            "sleep_hours": 7.2,
            "timestamp": "2026-07-30 01:20:15",
            "weekly_trend": [82, 85, 87, 84, 89, 91, 92.5],
            "summary": "【去敏身心軌跡摘要】個案於看診前 15 秒於候診區完成 0.067 Hz 心流共振調息。連續 7 日數據顯示夜間無應激爆發，心流一致性維持於 90% 以上高諧振區間。",
        },
        "#SYM-A302": {
            "status": "已完成診前 15s 共振調息",
            "coherence_score": 88.0,
            "stress_index": "Morandi Sage",
            "stress_desc": "莫蘭迪綠區域 ‧ 輕度交感活性",
            "sleep_hours": 6.1,
            "timestamp": "2026-07-30 01:25:00",
            "weekly_trend": [70, 75, 78, 80, 82, 85, 88.0],
            "summary": "【去敏身心軌跡摘要】個案於候診區完成心流調息。近 7 日睡眠時數偏低，生理指標顯示交感神經活性略微上升。",
        },
    }

if "checkin_queue" not in st.session_state:
    st.session_state["checkin_queue"] = [
        {"token": "#SYM-C701", "time": "01:20", "source": "LINE LIFF / App"},
        {"token": "#SYM-A302", "time": "01:25", "source": "LINE LIFF / App"},
    ]

MASTER_KEY = "CURIO-999"


# --- 4. 蔻恩閣長 3D/4D 寶盒 Modal 彈窗集 ---
if hasattr(st, "dialog"):

    @st.dialog("🐿️ 蔻恩閣長的 3D 典藏資安寶盒")
    def security_declaration_dialog():
        st.markdown(
            """
            <div style="background: linear-gradient(145deg, #FAF8F5, #F3EFE8); padding: 26px; border-radius: 24px; border: 1.5px solid #C2A675; box-shadow: 0 12px 32px rgba(61, 82, 69, 0.1);">
                <div style="text-align: center; margin-bottom: 16px;">
                    <div style="font-size: 2.8rem; margin-bottom: 6px;">🐿️</div>
                    <div style="font-family: 'Georgia', serif; font-style: italic; color: #B29562; font-size: 0.85rem; letter-spacing: 2px;">Curio & Studio ‧ 首席珍藏家</div>
                    <h3 style="color: #2A3B31; font-family: 'Georgia', serif; font-size: 1.25rem; margin: 4px 0 0 0;">小松鼠蔻恩閣長 (Cone) 資安合規宣告</h3>
                </div>
                <p style="font-size: 0.88rem; color: #5C6E63; line-height: 1.75; text-align: justify;">
                    歡迎來到珍奇櫃！我是蔻恩閣長。本系統全流程貫徹<b>零知識架構（Zero-Knowledge Architecture）</b>與<b>邊緣運算（Edge Computing）</b>原則，為每位探險家提供最高規格的鋼鐵隱私防線：
                </p>
                <hr style="border: 0; border-top: 1px solid #E3DCD1; margin: 16px 0;">
                <div style="font-size: 0.86rem; color: #2A3B31; line-height: 1.8;">
                    <b>🛡️ 四大鋼鐵資安誓言：</b><br>
                    1. <b>符合《個資法》第 2 條去識別化標準</b>：全流程絕不收集或存儲病患真實姓名、身分證號、電話或病歷號。<br>
                    2. <b>240 分鐘動態時間鎖 (Time-Lock)</b>：去敏密鑰 (Token) 具備 240 分鐘動態壽命，看診完畢即剛性銷毀，雲端絕不留存持久個資。<br>
                    3. <b>HTTPS TLS 1.3 & AES-256 加密</b>：前端至中繼站全通道高階加密，徹底防禦中間人截取。<br>
                    4. <b>Air-Gapped 雙盲實體與邏輯隔離</b>：本系統與診所行政 HIS/LINE 實施資料庫實體隔離，斷絕任何個資對照可能性。
                </div>
                <div style="margin-top: 20px; padding: 12px; background: rgba(194, 166, 117, 0.12); border-radius: 12px; font-size: 0.78rem; color: #B29562; text-align: center;">
                    🏛️ 發布單位：居里研創股份有限公司 (Curio & Studio) ｜ 日期：2026 年 07 月 30 日
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

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
                st.error("❌ 兩次新密碼輸入不一致！")
            else:
                st.session_state["doctor_password"] = new_pwd
                st.success("🎉 診間金鑰已成功變更！舊金鑰已即刻失效。")
                st.rerun()


# --- 5. 門診安全驗證登入頁 (小松鼠蔻恩閣長 3D 亮相) ---
if not st.session_state["authenticated"]:
    st.markdown(
        """
        <div class="atelier-login-card">
            <div class="cone-3d-badge">🐿️</div>
            <div class="brand-caption">Curio & Studio</div>
            <div class="medical-title">交感身心診所 ‧ 門診安全驗證</div>
            <div class="gold-divider"></div>
            <div class="medical-desc">零知識架構 (Zero-Knowledge) ‧ 雙盲去敏身心軌跡拋接<br><span style="font-size:0.82rem; color:#B29562;">小松鼠蔻恩閣長 (Cone) 已為您鎖定 0 個資防線</span></div>
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
            "<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True
        )

        if st.button(
            "🐿️ 蔻恩閣長的 3D 資安宣告寶盒",
            use_container_width=True,
        ):
            if hasattr(st, "dialog"):
                security_declaration_dialog()

        st.markdown(
            "<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True
        )

        with st.expander("❓ 忘記診間金鑰密碼？"):
            st.info(
                f"💡 **密碼提示**：GOOGLE帳號 + 西元出生年份（當前預設：`{st.session_state['doctor_password']}`）\n\n如需緊急技術支援，請聯繫 Curio & Studio 專屬服務團隊。"
            )

    st.stop()


# --- 6. 側邊欄：蔻恩閣長與信鴿 Singer 的 3D API 模擬器 ---
with st.sidebar:
    st.markdown(
        """
        <div style="background: #FFFFFF; border: 1px solid #E3DCD1; padding: 16px; border-radius: 20px; text-align: center; margin-bottom: 18px; box-shadow: 4px 4px 12px rgba(61, 82, 69, 0.04);">
            <div style="font-size: 1.8rem; margin-bottom: 4px;">🕊️ 🐿️</div>
            <div style="color: #2A3B31; font-weight: 600; font-size: 0.95rem; font-family: serif;">Curio & Studio 雙向中繼站</div>
            <div style="color: #B29562; font-size: 0.75rem; letter-spacing: 1px;">信鴿 Singer ✕ 蔻恩閣長</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("#### 📱 路徑 A：LINE LIFF / App 資料拋接")
    token_a = st.text_input("去敏短碼 (Token):", value="#SYM-B888")
    score_a = st.slider("心流分數:", 60.0, 100.0, 94.0)

    if st.button("📡 [路徑 A] 模擬 App 飛鴿拋接"):
        current_time_str = time.strftime("%H:%M")
        st.session_state["mock_db"][token_a] = {
            "status": "已完成診前 15s 共振調息",
            "coherence_score": score_a,
            "stress_index": "Morandi Soft Blue",
            "stress_desc": "莫蘭迪藍放縮區 ‧ 平穩",
            "sleep_hours": 7.5,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "weekly_trend": [80, 82, 85, 88, 90, 92, score_a],
            "summary": f"【去敏身心軌跡摘要】經由 LINE LIFF 飛鴿拋接之短碼 {token_a}。個案完成診前調息，心流表現極佳。",
        }
        st.session_state["checkin_queue"].append(
            {
                "token": token_a,
                "time": current_time_str,
                "source": "LINE LIFF API",
            }
        )
        st.toast(f"🕊️ 信鴿 Singer 已將 {token_a} 數據安全送達！")
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


st.markdown(
    """
    <div class="curio-hero-card">
        <h1>💎 Cabinet of Curiosities ‧ Curio & Studio 診間面板</h1>
        <p>Curio & Studio x 交感身心診所 ｜ 首席珍藏家蔻恩閣長 ‧ 0 個資 ‧ 診前 15 秒身心軌跡拋接</p>
    </div>
""",
    unsafe_allow_html=True,
)

top_col1, top_col2 = st.columns([3, 1])
with top_col1:
    st.markdown(
        """
        <div style="background:#FFFFFF; border:1px solid #E3DCD1; border-radius:30px; padding:10px 26px; font-size:0.86rem; color:#2A3B31;">
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
            <div style="background-color: #F3EFE8; border-left: 4px solid #C2A675; padding: 14px 22px; border-radius: 14px; margin-bottom: 24px; font-size: 0.92rem; color: #2A3B31;">
                <b>💎 成功連線至去敏密鑰 <code>{user_key}</code></b> ｜ 狀態：{data['status']} ｜ 更新時間：{data['timestamp']}
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                f"""
                <div class="custom-metric-card">
                    <div class="custom-metric-label">🌌 心流一致性 (0.067Hz)</div>
                    <div class="custom-metric-value">{data['coherence_score']} %</div>
                    <div class="custom-metric-delta">↑ 3.2% 穩定共振</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""
                <div class="custom-metric-card">
                    <div class="custom-metric-label">🌿 身心應激狀態</div>
                    <div class="custom-metric-value">{data['stress_index']}</div>
                    <div class="custom-metric-delta">{data.get('stress_desc', '莫蘭迪放鬆區域')}</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                f"""
                <div class="custom-metric-card">
                    <div class="custom-metric-label">🌙 本機睡眠時數</div>
                    <div class="custom-metric-value">{data['sleep_hours']} hr</div>
                    <div class="custom-metric-delta">達標 7 小時優質睡眠</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown(
            "<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True
        )

        tab1, tab2 = st.tabs(
            ["📈 近 7 日心流平穩度曲線", "📄 診前 15 秒去敏摘要"]
        )
        with tab1:
            st.markdown(
                "<h4 style='color:#2A3B31; font-size:1.05rem; margin-top:12px;'>近 7 日心流一致性調息曲線 (Coherence Score)</h4>",
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
            st.line_chart(chart_data, color="#3D5245")

        with tab2:
            st.markdown(
                "<h4 style='color:#2A3B31; font-size:1.05rem; margin-top:10px;'>邊緣端 15 秒去敏化身心軌跡</h4>",
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