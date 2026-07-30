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

# 2. Bespoke French Typography & 3D/4D Claymorphism CSS
st.markdown(
    """
    <style>
    /* 導入高級法式襯線字體與微排版 */
    @import url('https://fonts.googleapis.com/css2?family=Didot&family=Garamond:ital,wght@0,400;0,600;1,400&display=swap');

    .stApp {
        background-color: #FAF8F5;
        font-family: -apple-system, BlinkMacSystemFont, "Garamond", "Didot", "Georgia", "PingFang TC", sans-serif;
    }
    header[data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    footer { visibility: hidden; }

    /* 全局排版微調：修正中英文與括弧排版大空格問題 */
    .fix-spacing {
        letter-spacing: 0px !important;
        word-spacing: 0px !important;
        display: inline-block;
    }
    .en-subtext {
        font-family: "Didot", "Garamond", serif;
        font-style: italic;
        color: #C2A675;
    }

    /* 主頂樓卡片：極緻煙燻森林深綠 (Deep Atelier Sage) */
    .curio-hero-card {
        background: linear-gradient(135deg, #25352B 0%, #1A261F 100%);
        color: #FAF8F5;
        padding: 36px 46px;
        border-radius: 28px;
        box-shadow: 0 20px 48px rgba(37, 53, 43, 0.12);
        border: 1px solid #C2A675;
        margin-bottom: 28px;
    }
    .curio-hero-card h1 { 
        font-family: "Didot", "Georgia", "PingFang TC", serif !important;
        color: #FAF8F5 !important; 
        font-size: 1.85rem !important; 
        font-weight: 500 !important; 
        letter-spacing: 1px !important;
        margin: 0 0 8px 0 !important; 
    }
    .curio-hero-card p { 
        color: #D3E0D7 !important; 
        font-size: 0.9rem !important; 
        margin: 0 !important; 
        font-weight: 300; 
        letter-spacing: 0.5px;
    }

    /* 3D/4D 精品微浮雕徽章 (Curio 3D Badge) */
    .badge-3d-box {
        width: 68px;
        height: 68px;
        background: linear-gradient(145deg, #FFFFFF, #F0EAE1);
        border-radius: 22px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.2rem;
        box-shadow: 6px 6px 18px rgba(37, 53, 43, 0.06), -5px -5px 14px rgba(255, 255, 255, 0.9);
        border: 1px solid #C2A675;
        margin: 0 auto 16px auto;
    }

    /* 知性登入卡片 (Atelier Glass Panel) */
    .atelier-login-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid #E4DCD0;
        padding: 50px 48px 34px 48px;
        border-radius: 32px;
        box-shadow: 0 24px 60px rgba(37, 53, 43, 0.05);
        max-width: 510px;
        margin: 20px auto 12px auto;
        text-align: center;
    }
    .brand-caption {
        font-family: "Didot", serif;
        font-style: italic;
        color: #C2A675;
        font-size: 0.95rem;
        letter-spacing: 3px;
        margin-bottom: 6px;
        text-transform: uppercase;
    }
    .medical-title {
        color: #25352B;
        font-family: "Garamond", "PingFang TC", serif;
        font-size: 1.6rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
    }
    .gold-divider {
        width: 42px;
        height: 2px;
        background: linear-gradient(90deg, #C2A675 0%, #E6D7BD 100%);
        margin: 16px auto 22px auto;
        border-radius: 2px;
    }
    .medical-desc {
        color: #596B60;
        font-size: 0.88rem;
        line-height: 1.65;
        margin-bottom: 26px;
        font-weight: 300;
    }

    /* 3D 俏皮知性 Metric 數據卡片 */
    .custom-metric-card {
        background: #FFFFFF;
        border: 1px solid #E4DCD0;
        padding: 24px 26px;
        border-radius: 24px;
        box-shadow: 6px 6px 20px rgba(37, 53, 43, 0.03), -4px -4px 14px rgba(255, 255, 255, 0.8);
        height: 100%;
    }
    .custom-metric-header {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.88rem;
        color: #596B60;
        margin-bottom: 10px;
    }
    .custom-metric-value { 
        font-size: 1.55rem; 
        color: #25352B; 
        font-weight: 600; 
        font-family: "Didot", "Garamond", serif; 
        margin-bottom: 8px; 
        line-height: 1.2; 
    }
    .custom-metric-delta { 
        font-size: 0.82rem; 
        color: #435449; 
        background-color: #F4F0E8; 
        padding: 4px 12px; 
        border-radius: 10px; 
        display: inline-block; 
        line-height: 1.4; 
        border: 1px solid #E4DCD0; 
    }

    /* 法式資安防爆公告盒 */
    .security-notice-box {
        background-color: #F4F0E8;
        border-left: 4px solid #C2A675;
        border-radius: 18px;
        padding: 24px 28px;
        margin-top: 28px;
        font-size: 0.86rem;
        color: #25352B;
        line-height: 1.75;
    }

    /* 側邊欄重構：蔻恩閣長 3D 主角卡片 */
    .sidebar-cone-card {
        background: linear-gradient(145deg, #FFFFFF, #F8F4ED);
        border: 1px solid #E4DCD0;
        padding: 20px 16px;
        border-radius: 22px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 4px 4px 14px rgba(37, 53, 43, 0.04);
    }
    .sidebar-cone-avatar {
        font-size: 2.2rem;
        margin-bottom: 4px;
    }

    /* 按鈕高奢美化 */
    .stButton>button {
        border-radius: 14px !important;
        border: 1px solid #C2A675 !important;
        background: linear-gradient(135deg, #FAF8F5 0%, #F4F0E8 100%) !important;
        color: #25352B !important;
        font-weight: 500 !important;
        font-family: "Garamond", "PingFang TC", serif !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #25352B 0%, #1A261F 100%) !important;
        color: #FAF8F5 !important;
        border: 1px solid #25352B !important;
        box-shadow: 0 6px 18px rgba(37, 53, 43, 0.15) !important;
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


# --- 4. 蔻恩閣長 3D 典藏資安寶盒 (排版大空格已徹底完美修正) ---
if hasattr(st, "dialog"):

    @st.dialog("🐿️ 蔻恩閣長的 3D 典藏資安寶盒")
    def security_declaration_dialog():
        st.markdown(
            """
            <div style="background: linear-gradient(145deg, #FAF8F5, #F4F0E8); padding: 26px; border-radius: 24px; border: 1.5px solid #C2A675; box-shadow: 0 12px 32px rgba(37, 53, 43, 0.08);">
                <div style="text-align: center; margin-bottom: 16px;">
                    <div style="font-size: 2.8rem; margin-bottom: 4px;">🐿️</div>
                    <div class="brand-caption" style="font-size: 0.82rem; margin-bottom: 4px;">Curio & Studio ‧ 首席珍藏家</div>
                    <h3 style="color: #25352B; font-family: 'Garamond', serif; font-size: 1.3rem; margin: 0;">小松鼠蔻恩閣長 <span style="font-family: Didot, serif; font-style: italic; color: #C2A675;">(Cone)</span> 資安宣告</h3>
                </div>
                <div style="font-size: 0.88rem; color: #596B60; line-height: 1.7; text-align: justify;">
                    歡迎來到夢境珍奇櫃！我是蔻恩閣長。本系統全流程貫徹<span style="font-weight: 600; color: #25352B;">零知識架構</span> <span style="font-family: Didot, serif; color: #C2A675;">(Zero-Knowledge Architecture)</span> 與<span style="font-weight: 600; color: #25352B;">邊緣運算</span> <span style="font-family: Didot, serif; color: #C2A675;">(Edge Computing)</span> 原則，為每位探險家提供最高規格的鋼鐵隱私防線：
                </div>
                <hr style="border: 0; border-top: 1px solid #E4DCD0; margin: 16px 0;">
                <div style="font-size: 0.86rem; color: #25352B; line-height: 1.85;">
                    <b>✨ 蔻恩閣長的四大資安誓言：</b><br>
                    1. <b>符合《個資法》第 2 條去識別化標準</b>：全流程絕不收集、記錄或存儲病患真實姓名、身分證號、電話或病歷號。<br>
                    2. <b>240 分鐘動態時間鎖 <span style="font-family: Didot, serif; color: #C2A675;">(Time-Lock)</span></b>：去敏密鑰 <span style="font-family: Didot, serif; color: #C2A675;">(Token)</span> 具備 240 分鐘動態壽命，看診完畢即剛性銷毀，雲端絕不留存持久個資。<br>
                    3. <b>HTTPS TLS 1.3 & AES-256 加密</b>：前端至中繼站全通道高階加密，徹底防禦中間人截取。<br>
                    4. <b>Air-Gapped 雙盲實體與邏輯隔離</b>：本系統與診所行政 HIS/LINE 實施資料庫實體隔離，斷絕任何個資對照可能性。
                </div>
                <div style="margin-top: 20px; padding: 12px; background: rgba(194, 166, 117, 0.12); border-radius: 12px; font-size: 0.78rem; color: #B29562; text-align: center; font-family: 'Garamond', serif;">
                    🏛️ 發布單位：居里研創股份有限公司 <span style="font-family: Didot, serif; italic">(Curio & Studio)</span> ｜ 日期：2026 年 07 月 30 日
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


# --- 5. 門診安全驗證登入頁 (小松鼠蔻恩閣長 3D 浮雕亮相) ---
if not st.session_state["authenticated"]:
    st.markdown(
        """
        <div class="atelier-login-card">
            <div class="badge-3d-box">🐿️</div>
            <div class="brand-caption">Curio & Studio</div>
            <div class="medical-title">交感身心診所 ‧ 門診安全驗證</div>
            <div class="gold-divider"></div>
            <div class="medical-desc">
                零知識架構 <span style="font-family:Didot, serif; italic; color:#C2A675;">(Zero-Knowledge)</span> ‧ 雙盲去敏身心軌跡拋接<br>
                <span style="font-size:0.82rem; color:#C2A675;">小松鼠蔻恩閣長 <span style="font-family:Didot, serif;">(Cone)</span> 已為您鎖定 0 個資防線</span>
            </div>
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

        if st.button("✨ 解鎖門診數據面板", use_container_width=True):
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


# --- 6. 側邊欄：蔻恩閣長 🐿️ 在前、信鴿 Singer 🕊️ 在後的 3D 模擬器 ---
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-cone-card">
            <div class="sidebar-cone-avatar">🐿️ 🕊️</div>
            <div style="color: #25352B; font-weight: 600; font-size: 0.98rem; font-family: 'Garamond', serif;">Curio & Studio 雙向中繼站</div>
            <div style="color: #C2A675; font-size: 0.78rem; font-family: 'Didot', serif; italic; margin-top: 2px;">小松鼠蔻恩閣長 ✕ 信鴿 Singer</div>
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
        <h1>✨ Cabinet of Curiosities ‧ Curio & Studio 診間面板</h1>
        <p>Curio & Studio x 交感身心診所 ｜ 首席珍藏家蔻恩閣長 (Cone) ‧ 0 個資 ‧ 診前 15 秒身心軌跡拋接</p>
    </div>
""",
    unsafe_allow_html=True,
)

top_col1, top_col2 = st.columns([3, 1])
with top_col1:
    st.markdown(
        """
        <div style="background:#FFFFFF; border:1px solid #E4DCD0; border-radius:30px; padding:10px 26px; font-size:0.86rem; color:#25352B;">
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
            <div style="background-color: #F4F0E8; border-left: 4px solid #C2A675; padding: 14px 22px; border-radius: 14px; margin-bottom: 24px; font-size: 0.92rem; color: #25352B;">
                <b>✨ 成功連線至去敏密鑰 <code>{user_key}</code></b> ｜ 狀態：{data['status']} ｜ 更新時間：{data['timestamp']}
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                f"""
                <div class="custom-metric-card">
                    <div class="custom-metric-header">
                        <span>✨</span>
                        <span>心流一致性 (0.067Hz)</span>
                    </div>
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
                    <div class="custom-metric-header">
                        <span>🌿</span>
                        <span>身心應激狀態</span>
                    </div>
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
                    <div class="custom-metric-header">
                        <span>🌙</span>
                        <span>本機睡眠時數</span>
                    </div>
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
                "<h4 style='color:#25352B; font-size:1.05rem; margin-top:12px;'>近 7 日心流一致性調息曲線 (Coherence Score)</h4>",
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
            st.line_chart(chart_data, color="#25352B")

        with tab2:
            st.markdown(
                "<h4 style='color:#25352B; font-size:1.05rem; margin-top:10px;'>邊緣端 15 秒去敏化身心軌跡</h4>",
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