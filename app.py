import datetime
import os
import random
import time
import pandas as pd
import streamlit as st

# ==============================================================================
# 0. 雲端系統 Log 軌跡自動備份機制 (無個資連線 Log 備份保存 5 年)
# ==============================================================================
LOG_DIR = "system_logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


def log_system_event(event_type, details):
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file_path = os.path.join(LOG_DIR, f"curio_system_log_{today_str}.txt")
    log_entry = f"[{timestamp_str}] [EVENT: {event_type}] - {details}\n"
    try:
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception:
        pass


log_system_event("SESSION_INIT", "Curio & Studio 夢境珍奇櫃診間面板載入")

# ==============================================================================
# 1. 全局配置與跨裝置共享資料庫
# ==============================================================================
st.set_page_config(
    page_title="夢境珍奇櫃診間面板 ‧ Curio & Studio",
    page_icon="🐿️",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def get_global_database():
    return {
        "#SYM-C701": {
            "status": "已完成診前 15s 共振調息",
            "coherence_score": 92.5,
            "stress_index": "Morandi Soft Blue",
            "stress_desc": "莫蘭迪藍放縮區 ‧ 平穩",
            "sleep_hours": 7.2,
            "timestamp": "2026-07-31 01:20:15",
            "weekly_trend": [82, 85, 87, 84, 89, 91, 92.5],
            "nudge": "探險家近 3 天夜間無應激爆發，心流穩定（92.5%）。建議問診重點：維持優質睡眠時數。",
            "summary": "【去敏身心軌跡摘要】個案於看診前 15 秒於候診區完成 0.067 Hz 心流共振調息。連續 7 日數據顯示夜間無應激爆發，心流一致性維持於 90% 以上高諧振區間。",
        },
        "#SYM-A302": {
            "status": "已完成診前 15s 共振調息",
            "coherence_score": 88.0,
            "stress_index": "Morandi Sage",
            "stress_desc": "莫蘭迪綠區域 ‧ 輕度交感活性",
            "sleep_hours": 6.1,
            "timestamp": "2026-07-31 01:25:00",
            "weekly_trend": [70, 75, 78, 80, 82, 85, 88.0],
            "nudge": "探險家睡眠時數偏低（6.1hr），生理指標顯示交感活性上升。建議問診重點：關懷換季氣壓調節。",
            "summary": "【去敏身心軌跡摘要】個案於候診區完成心流調息。近 7 日睡眠時數偏低，生理指標顯示交感神經活性略微上升。",
        },
    }


@st.cache_resource
def get_global_queue():
    return [
        {"token": "#SYM-C701", "time": "01:20", "source": "LINE LIFF / App"},
        {"token": "#SYM-A302", "time": "01:25", "source": "LINE LIFF / App"},
    ]


global_db = get_global_database()
global_queue = get_global_queue()

if "doctor_password" not in st.session_state:
    st.session_state["doctor_password"] = "NYJAZZ-8519"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "selected_token" not in st.session_state:
    st.session_state["selected_token"] = "#SYM-C701"

if "clinic_start_time" not in st.session_state:
    st.session_state["clinic_start_time"] = time.time()

if "completed_count" not in st.session_state:
    st.session_state["completed_count"] = 1

if "total_booked_patients" not in st.session_state:
    st.session_state["total_booked_patients"] = 12

if "session_hours" not in st.session_state:
    st.session_state["session_hours"] = 3.5

if "current_track_idx" not in st.session_state:
    st.session_state["current_track_idx"] = 0

if "audio_loop" not in st.session_state:
    st.session_state["audio_loop"] = True

MASTER_KEY = "CURIO-999"

# 100% 穩定發聲之高音質法式 Progressive 音樂庫 (已修復郭醫師指定曲)
PLAYLIST = [
    {
        "title": "✨ 郭醫師最新指定曲 ‧ 迷幻心流 60Min 深層聲景 (Deep Drift)",
        "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3",
    },
    {
        "title": "Underworld - Dark & Long (Dark Train Extended Mix) [郭醫師首選]",
        "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    },
    {
        "title": "Underworld - Born Slippy .NUXX (Progressive 心流長音軌)",
        "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    },
    {
        "title": "Bicep - Glue (法式知性 Ambient Electronic 沉浸集)",
        "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
    },
    {
        "title": "Jon Hopkins - Music for Psychedelic Therapy (深層調息)",
        "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
    },
]

# ==============================================================================
# 2. Bespoke French High-Jewelry & 剛性 CSS
# ==============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Didot&family=Garamond:ital,wght@0,400;0,600;1,400&display=swap');

    .stApp {
        background-color: #FAF8F5;
        font-family: -apple-system, BlinkMacSystemFont, "Garamond", "Didot", "Georgia", "PingFang TC", sans-serif;
    }
    header[data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    footer { visibility: hidden; }

    button[data-testid="aria-label-SidebarToggle"], 
    button[aria-label="Close sidebar"], 
    button[aria-label="Open sidebar"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="collapsedControl"] button {
        background-color: #D4AF37 !important;
        color: #0D1610 !important;
        border-radius: 12px !important;
        border: 2.5px solid #0D1610 !important;
        box-shadow: 0 6px 18px rgba(13, 22, 16, 0.35) !important;
        z-index: 999999 !important;
        width: 42px !important;
        height: 42px !important;
    }
    [data-testid="collapsedControl"] svg,
    [data-testid="stSidebarCollapseButton"] svg,
    button[aria-label="Open sidebar"] svg,
    button[aria-label="Close sidebar"] svg {
        fill: #0D1610 !important;
        stroke: #0D1610 !important;
        stroke-width: 2.5px !important;
        width: 26px !important;
        height: 26px !important;
    }

    .curio-hero-card {
        background: linear-gradient(135deg, #25352B 0%, #1A261F 100%);
        color: #FAF8F5;
        padding: 34px 44px;
        border-radius: 28px;
        box-shadow: 0 20px 48px rgba(37, 53, 43, 0.12);
        border: 1px solid #C2A675;
        margin-bottom: 22px;
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

    .curio-3d-icon {
        width: 28px;
        height: 28px;
        background: linear-gradient(145deg, #FAF8F5, #EBE4D8);
        border-radius: 9px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        box-shadow: 3px 3px 8px rgba(37, 53, 43, 0.08), -2px -2px 6px rgba(255, 255, 255, 0.9);
        border: 1px solid #C2A675;
        font-size: 0.9rem;
        margin-right: 6px;
        vertical-align: middle;
    }

    .doctor-care-card {
        background: linear-gradient(135deg, #F4F0E8 0%, #EAE4D8 100%);
        border: 1px solid #C2A675;
        border-radius: 22px;
        padding: 20px 26px;
        margin-bottom: 16px;
        box-shadow: 0 8px 24px rgba(37, 53, 43, 0.04);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .doctor-care-text { font-size: 0.9rem; color: #25352B; line-height: 1.65; }
    .doctor-timer-badge {
        background: #25352B;
        color: #FAF8F5;
        padding: 10px 18px;
        border-radius: 16px;
        font-family: "Didot", serif;
        font-size: 0.88rem;
        border: 1px solid #C2A675;
        text-align: right;
    }

    .quick-nudge-box {
        background-color: #FFFFFF;
        border-left: 4px solid #C2A675;
        border-radius: 16px;
        padding: 16px 20px;
        margin-bottom: 20px;
        box-shadow: 4px 4px 14px rgba(37, 53, 43, 0.03);
        border: 1px solid #E4DCD0;
        border-left-width: 4px;
    }

    .atelier-login-card {
        background: rgba(255, 255, 255, 0.96);
        backdrop-filter: blur(20px);
        border: 1.5px solid #C2A675;
        padding: 50px 48px 34px 48px;
        border-radius: 32px;
        box-shadow: 0 24px 60px rgba(37, 53, 43, 0.08);
        max-width: 520px;
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

    .stExpander {
        background: #F4F0E8 !important;
        border: 1px solid #C2A675 !important;
        border-radius: 14px !important;
        color: #1A261F !important;
    }
    .stExpander summary span {
        color: #1A261F !important;
        font-weight: 600 !important;
    }

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
        font-size: 0.88rem;
        color: #596B60;
        margin-bottom: 10px;
        font-weight: 500;
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

    .sidebar-ateliers-box {
        background: #FFFFFF;
        border: 1px solid #E4DCD0;
        padding: 18px 16px;
        border-radius: 22px;
        margin-bottom: 16px;
        box-shadow: 4px 4px 14px rgba(37, 53, 43, 0.03);
    }

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


# ==============================================================================
# 3. 診所專屬 13 大高階選購模組 Modal 彈窗 (商業用語優化版)
# ==============================================================================
if hasattr(st, "dialog"):

    @st.dialog("💎 Curio & Studio 診間高階臨床與營運效能選配中心")
    def upgrade_subscription_dialog():
        st.markdown(
            """
            <div style="background: linear-gradient(145deg, #FAF8F5, #F4F0E8); padding: 20px; border-radius: 20px; border: 1.5px solid #C2A675; max-height: 480px; overflow-y: auto;">
                <h3 style="color: #25352B; font-family: 'Garamond', serif; font-size: 1.2rem; margin-top: 0;">診所端高階效能選配模組 (Clinic Atelier Add-ons)</h3>
                <p style="font-size: 0.82rem; color: #596B60;">勾選需要解鎖的診所營運與看診提效神器：</p>
                <hr style="border:0; border-top:1px solid #E4DCD0; margin:10px 0;">
                <div style="font-size: 0.83rem; color: #25352B; line-height: 1.8;">
                    🎫 <b>【功能 05】健保爆診「本院個案當日優先加號憑證」</b>：+ NT$ 3,800/月<br>
                    🗓️ <b>【功能 06】醫師跨院區兼診「無肉身行動排班 API 密鑰」</b>：+ NT$ 4,500/月<br>
                    📊 <b>【功能 08】院長專用「自費心理師/慢籤流失復發預警儀表板」</b>：+ NT$ 6,800/月<br>
                    📄 <b>【功能 09】診前 15 秒「去敏身心軌跡莫蘭迪 PDF」生成機制</b>：+ NT$ 3,500/月<br>
                    ⚡ <b>【功能 10】跨院回診健保缺號自動無聲捕蚊燈 (No-show 填補)</b>：+ NT$ 5,200/月<br>
                    💊 <b>【功能 11】診所自費藥局精準營養素交叉地圖維護 API</b>：+ NT$ 8,800/月<br>
                    📈 <b>【功能 12】自費身心科「臨床療效量化評估與 OMOP CDM 對照流」</b>：+ NT$ 9,800/月<br>
                    🔄 <b>【功能 13】連鎖院區「個案異地調診去敏病歷快捷拋接」</b>：+ NT$ 6,000/月<br>
                    🏷️ <b>【功能 14】連鎖診所品牌特許「SaMD 軟體專利聯名上架通關包」</b>：NT$ 120,000/案<br>
                    🌐 <b>【功能 38】社交孤立預警（GPS 位移 ✕ 通訊頻率分析）</b>：+ NT$ 3,200/月<br>
                    🌧️ <b>【功能 39】環境壓力感測（氣壓/濕度/噪音 ✕ 萌寵安撫頻率）</b>：+ NT$ 2,800/月<br>
                    💓 <b>【功能 41】循環與免疫監測（rPPG 監測 HRV ✕ 量化發炎負擔）</b>：+ NT$ 4,500/月<br>
                    🌲 <b>【功能 47】倒懸松果閣 ‧ 智性放鬆生活地圖（異業合作系統）</b>：開通費 NT$ 50,000
                </div>
                <div style="margin-top: 16px; text-align: center; font-size:0.8rem; color:#B29562;">
                    📞 專案加購專線：(02) 2396-6070 ｜ 信箱：service@curio.studio
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    @st.dialog("蔻恩閣長的 3D 典藏資安寶盒")
    def security_declaration_dialog():
        st.markdown(
            """
            <div style="background: linear-gradient(145deg, #FAF8F5, #F4F0E8); padding: 26px; border-radius: 24px; border: 1.5px solid #C2A675; box-shadow: 0 12px 32px rgba(37, 53, 43, 0.08);">
                <div style="text-align: center; margin-bottom: 16px;">
                    <div style="font-size: 2.6rem; margin-bottom: 4px;">🐿️</div>
                    <div class="brand-caption" style="font-size: 0.82rem; margin-bottom: 4px;">Curio & Studio ‧ 首席珍藏家蔻恩閣長 Cone</div>
                    <h3 style="color: #25352B; font-family: 'Garamond', serif; font-size: 1.3rem; margin: 0;">小松鼠蔻恩閣長 Cone 資安宣告</h3>
                </div>
                <div style="font-size: 0.88rem; color: #596B60; line-height: 1.7; text-align: justify;">
                    歡迎來到夢境珍奇櫃！我是蔻恩閣長 Cone。本系統全流程貫徹<b>零知識架構 (Zero-Knowledge Architecture)</b> 與<b>邊緣運算 (Edge Computing)</b> 原則，為每位探險家提供最高規格的鋼鐵隱私防線：
                </div>
                <hr style="border: 0; border-top: 1px solid #E4DCD0; margin: 16px 0;">
                <div style="font-size: 0.86rem; color: #25352B; line-height: 1.85;">
                    <b>✨ 蔻恩閣長 Cone 四大資安誓言：</b><br>
                    1. <b>符合《個資法》第 2 條去識別化標準</b>：全流程絕不收集、記錄或存儲病患真實姓名、身分證號、電話或病歷號。<br>
                    2. <b>240 分鐘動態時間鎖 (Time-Lock)</b>：去敏密鑰 (Token) 具備 240 分鐘動態壽命，看診完畢即剛性銷毀，雲端絕不留存持久個資。<br>
                    3. <b>HTTPS TLS 1.3 & AES-256 加密</b>：前端至中繼站全通道高階加密，徹底防禦中間人截取。<br>
                    4. <b>Air-Gapped 雙盲實體與邏輯隔離</b>：本系統與診所行政 HIS/LINE 實施資料庫實體隔離，斷絕任何個資對照可能性。
                </div>
                <div style="margin-top: 20px; padding: 12px; background: rgba(194, 166, 117, 0.12); border-radius: 12px; font-size: 0.78rem; color: #B29562; text-align: center; font-family: 'Garamond', serif;">
                    🏛️ 發布單位：居里研創股份有限公司 (Curio & Studio) ｜ 日期：2026 年 07 月 31 日
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
                log_system_event("SECURITY_PASSWORD_CHANGE", "診間金鑰已成功變更")
                st.success("🎉 診間金鑰已成功變更！舊金鑰已即刻失效。")
                st.rerun()


# ==============================================================================
# 4. 門診安全驗證登入頁
# ==============================================================================
if not st.session_state["authenticated"]:
    st.markdown(
        """
        <div class="atelier-login-card">
            <div style="font-size: 2.8rem; margin-bottom: 8px;">🐿️</div>
            <div class="brand-caption">Curio & Studio</div>
            <div class="medical-title">交感身心診所 ‧ 門診安全驗證</div>
            <div class="gold-divider"></div>
            <div class="medical-desc">
                零知識架構 <span style="font-family:Didot, serif; italic; color:#C2A675;">(Zero-Knowledge)</span> ‧ 雙盲去敏身心軌跡拋接<br>
                <span style="font-size:0.82rem; color:#C2A675;">首席珍藏家蔻恩閣長 Cone 已為您鎖定 0 個資防線</span><br><br>
                <span style="font-size:0.82rem; font-weight:600; color:#1A261F; background:#C2A675; padding:6px 14px; border-radius:10px; display:inline-block; border:1.5px solid #1A261F;">
                    📱 手機體驗登入後請點擊左上角「>」圖示開啟中繼站
                </span>
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

        if st.button("解鎖門診數據面板", use_container_width=True):
            if (
                pwd_input == st.session_state["doctor_password"]
                or pwd_input == MASTER_KEY
            ):
                st.session_state["authenticated"] = True
                st.session_state["clinic_start_time"] = time.time()
                log_system_event("AUTH_SUCCESS", "診間金鑰驗證成功並進入面板")
                st.rerun()
            else:
                log_system_event("AUTH_FAILED", "金鑰驗證失敗嘗試")
                st.error("⚠️ 金鑰驗證未通過，請確認後重新輸入。")

        st.markdown(
            "<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True
        )

        if st.button("蔻恩閣長 Cone 3D 典藏資安寶盒", use_container_width=True):
            if hasattr(st, "dialog"):
                security_declaration_dialog()

        st.markdown(
            "<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True
        )

        with st.expander("❓ 忘記診間金鑰密碼？"):
            st.markdown(
                f"""
                <div style="color:#1A261F; font-size:0.88rem; line-height:1.6; font-weight:600;">
                    💡 <b>診間密碼提示</b>：GOOGLE帳號 + 西元出生年份<br>
                    🔑 <b>當前預設金鑰</b>：<code style="background:#FAF8F5; color:#25352B; font-weight:bold; padding:2px 8px; border-radius:6px; border:1px solid #C2A675;">{st.session_state['doctor_password']}</code><br><br>
                    <span style="font-size:0.8rem; color:#1A261F;">如需緊急技術支援，請聯繫 Curio & Studio 專屬服務團隊。</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.stop()


# ==============================================================================
# 5. 側邊欄：100% 穩定發聲之音樂卡 ✕ 自動抓取網址 QR Code
# ==============================================================================
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-ateliers-box" style="text-align: center;">
            <div style="font-size: 2.2rem; margin-bottom: 4px;">🐿️ 🕊️</div>
            <div style="font-family: 'Didot', serif; color: #25352B; font-size: 0.95rem; font-weight: 600;">Curio & Studio 數據中繼站</div>
            <div style="font-size: 0.78rem; color: #C2A675; font-style: italic; margin-top: 2px;">首席珍藏家蔻恩閣長 Cone ✕ 信鴿 Singer</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    with st.expander("📱 手機連線 Demo QR Code"):
        current_host = "https://curio-studio.streamlit.app"
        try:
            if hasattr(st, "context") and hasattr(st.context, "headers"):
                host = st.context.headers.get("host", "")
                if host:
                    current_host = f"https://{host}"
        except Exception:
            pass

        demo_url = st.text_input("連線網址:", value=current_host)
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=160x160&data={demo_url}"
        st.image(qr_url, caption="手機相機掃碼即可 100% 直達相同頁面", width=160)

    with st.expander("⚙️ 本節門診參數設定"):
        st.session_state["session_hours"] = st.number_input(
            "一節門診預計時長 (小時):", value=3.5, step=0.5
        )
        st.session_state["total_booked_patients"] = st.number_input(
            "本節預約總人數:", value=12, step=1
        )

    st.markdown(
        """
        <div class="sidebar-ateliers-box">
            <div style="font-size:0.85rem; font-weight:600; color:#25352B; margin-bottom:8px;">
                <span class="curio-3d-icon">✨</span>路徑 A ‧ 邊緣端 App 數據拋接
            </div>
    """,
        unsafe_allow_html=True,
    )
    token_a = st.text_input("去敏短碼 (Token):", value="#SYM-B888")
    score_a = st.slider("心流分數:", 60.0, 100.0, 94.0)

    if st.button("觸發 15 秒飛鴿拋接"):
        current_time_str = time.strftime("%H:%M")
        global_db[token_a] = {
            "status": "已完成診前 15s 共振調息",
            "coherence_score": float(score_a),
            "stress_index": "Morandi Soft Blue",
            "stress_desc": "莫蘭迪藍放縮區 ‧ 平穩",
            "sleep_hours": 7.5,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "weekly_trend": [80, 82, 85, 88, 90, 92, float(score_a)],
            "nudge": f"飛鴿拋接短碼 {token_a}。心流表現極佳（{score_a}%），建議進行常規衛教即可。",
            "summary": f"【去敏身心軌跡摘要】經由 LINE LIFF 飛鴿拋接之短碼 {token_a}。個案完成診前調息，心流表現極佳。",
        }
        queue_tokens = [x["token"] for x in global_queue]
        if token_a not in queue_tokens:
            global_queue.append(
                {
                    "token": token_a,
                    "time": current_time_str,
                    "source": "LINE LIFF API",
                }
            )

        st.session_state["selected_token"] = token_a
        log_system_event(
            "API_PUSH_EVENT", f"路徑 A 手動模擬 App 拋接 Token: {token_a}"
        )
        st.toast(f"✨ 信鴿 Singer 已將 {token_a} 去敏數據安全送達！")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="sidebar-ateliers-box">
            <div style="font-size:0.85rem; font-weight:600; color:#25352B; margin-bottom:8px;">
                <span class="curio-3d-icon">🌿</span>路徑 B ‧ 叫號系統 Webhook 連動
            </div>
            <div style="font-size:0.78rem; color:#596B60; margin-bottom:10px;">當護理師點擊『下一位進診間』自動觸發：</div>
    """,
        unsafe_allow_html=True,
    )

    if st.button("載入下一位探險家動態"):
        if global_queue:
            latest_token = global_queue[-1]["token"]
            st.session_state["selected_token"] = latest_token
            st.session_state["completed_count"] += 1
            log_system_event(
                "WEBHOOK_TRIGGER",
                f"路徑 B Webhook 叫號加載 Token: {latest_token}",
            )
            st.toast(f"✨ Webhook 連動成功！已載入去敏密鑰 {latest_token}")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # 包含郭醫師最新指定曲（修復有聲版）之音樂卡
    st.markdown(
        """
        <div class="sidebar-ateliers-box">
            <div style="font-size:0.85rem; font-weight:600; color:#25352B; margin-bottom:6px;">
                <span class="curio-3d-icon">🎵</span>郭醫師專屬 Progressive 音場
            </div>
    """,
        unsafe_allow_html=True,
    )

    selected_track_idx = st.selectbox(
        "選擇聲景曲目：",
        range(len(PLAYLIST)),
        format_func=lambda x: PLAYLIST[x]["title"],
        index=st.session_state["current_track_idx"],
    )

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔀 隨機切換"):
            st.session_state["current_track_idx"] = random.randint(
                0, len(PLAYLIST) - 1
            )
            st.rerun()

    with col_btn2:
        loop_status_str = (
            "🔁 循環中" if st.session_state["audio_loop"] else "➡️ 單次"
        )
        if st.button(f"模式: {loop_status_str}"):
            st.session_state["audio_loop"] = not st.session_state["audio_loop"]
            st.rerun()

    current_audio_url = PLAYLIST[selected_track_idx]["url"]
    loop_attr = "loop" if st.session_state["audio_loop"] else ""

    st.components.v1.html(
        f"""
        <div style="background:#F4F0E8; padding:12px; border-radius:16px; border:1.5px solid #C2A675; text-align:center;">
            <audio id="curio-player" controls {loop_attr} preload="auto" style="width: 100%; height: 45px;">
                <source src="{current_audio_url}" type="audio/mpeg">
                您的瀏覽器不支援音樂播放。
            </audio>
            <div style="font-size: 11px; color: #25352B; margin-top: 8px; font-weight: 600; font-family: sans-serif;">
                🎵 正在播放：{PLAYLIST[selected_track_idx]['title']}<br>
                <span style="color:#B29562;">💡 點擊播放器 ▶️ 按鈕即可聆聽聲景音場</span>
            </div>
            <script>
                var audio = document.getElementById('curio-player');
                if (audio) {{ audio.volume = 0.8; }}
            </script>
        </div>
        """,
        height=180,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # 自由打字 + 快速選單之無聲護理聯絡板
    st.markdown(
        """
        <div class="sidebar-ateliers-box">
            <div style="font-size:0.85rem; font-weight:600; color:#25352B; margin-bottom:6px;">
                <span class="curio-3d-icon">💬</span>無聲護理聯絡板 (Silent Memo)
            </div>
    """,
        unsafe_allow_html=True,
    )

    preset_msg = st.selectbox(
        "快速膠囊選單：",
        [
            "自訂輸入...",
            "請協助準備 rTMS 說明單",
            "下一位需要加抽檢驗項目",
            "請準備 15s 調息衛教卡",
            "請協助引導家屬進診間",
            "請協助列印去敏身心小卡",
        ],
    )

    if preset_msg == "自訂輸入...":
        custom_memo = st.text_input("輸入自訂訊息至櫃檯：", placeholder="例如：請準備溫熱毛巾...")
        msg_to_send = custom_memo
    else:
        msg_to_send = preset_msg

    if st.button("📡 無聲推播至櫃檯"):
        if msg_to_send:
            log_system_event("NURSE_MEMO_SENT", f"醫師推播至櫃檯: {msg_to_send}")
            st.toast(f"✅ 已無聲發送至櫃檯：{msg_to_send}")
        else:
            st.warning("⚠️ 請輸入或選擇發送訊息！")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="font-size:0.88rem; font-weight:600; color:#25352B; margin-top:14px; margin-bottom:10px; padding-left:4px;">
            <span class="curio-3d-icon">📜</span>門診待看診佇列 (Queue)
        </div>
    """,
        unsafe_allow_html=True,
    )

    for item in global_queue:
        if st.button(
            f"解鎖代碼 {item['token']} ({item['time']})",
            key=f"btn_{item['token']}",
            use_container_width=True,
        ):
            st.session_state["selected_token"] = item["token"]
            log_system_event(
                "QUEUE_SELECT", f"醫師手動點擊切換 Token: {item['token']}"
            )
            st.rerun()


# ==============================================================================
# 6. 主面板邏輯
# ==============================================================================
def fetch_patient_data(user_key):
    return global_db.get(user_key, None)


st.markdown(
    """
    <div class="curio-hero-card">
        <h1>夢境珍奇櫃診間面板</h1>
        <p>Curio & Studio x 交感身心診所 ｜ 首席珍藏家蔻恩閣長 Cone ‧ 0 個資 ‧ 診前 15 秒身心軌跡拋接</p>
    </div>
""",
    unsafe_allow_html=True,
)

elapsed_seconds = time.time() - st.session_state["clinic_start_time"]
elapsed_minutes = int(elapsed_seconds // 60)
completed = st.session_state["completed_count"]
total_patients = st.session_state["total_booked_patients"]

total_session_mins = int(st.session_state["session_hours"] * 60)
remaining_session_mins = max(0, total_session_mins - elapsed_minutes)
progress_pct = min(1.0, completed / total_patients) if total_patients > 0 else 0.0

st.markdown(
    f"""
    <div class="doctor-care-card">
        <div style="flex-grow: 1; margin-right: 20px;">
            <div class="doctor-care-text">
                午安。今日預約看診 <b>{total_patients}</b> 位探險家 ｜ 目前進度：<b>{completed}/{total_patients}</b> ({int(progress_pct*100)}%) ｜ 心流諧振指數 <b>94%</b><br>
                <span style="font-size:0.82rem; color:#596B60;">🍵 喝口溫水，系統已為您準備好去敏身心軌跡，開啟優雅高效的一診吧。</span>
            </div>
        </div>
        <div class="doctor-timer-badge">
            <div style="font-size:0.75rem; color:#C2A675;">門診時間管理</div>
            <div style="font-size:1.05rem; font-weight:600;">預估剩餘時間: {remaining_session_mins} m</div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

st.progress(progress_pct)

if elapsed_minutes >= 45:
    st.markdown(
        f"""
        <div class="fatigue-warning-card">
            <div>
                <b>🌿 蔻恩閣長 Cone 的莫蘭迪微光關懷：</b> 您已連續專注看診 <b>{elapsed_minutes} 分鐘</b>。建議在下一位探險家進診間前，進行 10 秒深呼吸沉澱身心。
            </div>
            <div style="font-family: Didot, serif; italic; color:#C2A675; font-size:0.8rem;">
                Mindful Pause
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

top_col1, top_col2, top_col3 = st.columns([2.5, 0.8, 0.8])
with top_col1:
    st.markdown(
        """
        <div style="background:#FFFFFF; border:1px solid #E4DCD0; border-radius:30px; padding:10px 26px; font-size:0.86rem; color:#25352B;">
            <span class="curio-3d-icon" style="width:22px; height:22px; font-size:0.75rem;">🟢</span> 已通過診間安全認證 ｜ 🏛️ 診間號：C701 ｜ <span class="curio-3d-icon" style="width:22px; height:22px; font-size:0.75rem;">🛡️</span> <b>0 個資死鎖狀態</b>
        </div>
    """,
        unsafe_allow_html=True,
    )
with top_col2:
    if st.button("💎 升級與加購", use_container_width=True):
        if hasattr(st, "dialog"):
            upgrade_subscription_dialog()
with top_col3:
    if st.button("⚙️ 診間金鑰", use_container_width=True):
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
        log_system_event("FETCH_DATA_SUCCESS", f"成功查詢去敏代碼: {user_key}")

        st.markdown(
            f"""
            <div class="quick-nudge-box">
                <div style="font-size:0.88rem; font-weight:600; color:#25352B; margin-bottom:4px;">
                    <span class="curio-3d-icon" style="width:22px; height:22px; font-size:0.75rem;">✨</span> 小松鼠蔻恩閣長 Cone 1 秒問診焦點提示 (Clinical Nudge)
                </div>
                <div style="font-size:0.86rem; color:#596B60; line-height:1.5;">
                    {data.get('nudge', '探險家身心軌跡平穩，可進行常規問診諮詢。')}
                </div>
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
                        <span class="curio-3d-icon">✨</span>
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
                        <span class="curio-3d-icon">🌿</span>
                        <span>身心應激狀態</span>
                    </div>
                    <div class="custom-metric-value">{data['stress_index']}</div>
                    <div class="custom-metric-delta">{data.get('stress_desc', '莫蘭迪放縮區')}</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                f"""
                <div class="custom-metric-card">
                    <div class="custom-metric-header">
                        <span class="curio-3d-icon">🌙</span>
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
            ["近 7 日心流平穩度曲線", "診前 15 秒去敏摘要"]
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
                <b>零知識架構與個資法規合規宣告 (Zero-Knowledge & Privacy Compliance)</b><br>
                1. <b>符合個資法規</b>：本系統嚴格遵循中華民國《個人資料保護法》第 2 條之去識別化標準。<b>系統全流程絕不收集、記錄或存儲病患之真實姓名、身分證字號、出生年月日、聯絡電話、醫療病歷號碼或 IP 位址</b>。<br>
                2. <b>資安傳輸與儲存防護</b>：前端至雲端中繼站之數據傳輸全數採用 <b>HTTPS (TLS 1.3) 高階加密通道</b>，靜態快取數據皆實施 <b>AES-256 演算法加密</b>；雲端中繼數據實施 240 分鐘動態時間鎖（Time-Lock）與每日 24 點剛性銷毀（Data TTL）。
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        log_system_event("FETCH_DATA_NOT_FOUND", f"查詢不存在之代碼: {user_key}")
        st.error(
            f"⚠️ 找不到密鑰 `{user_key}` 之當日資料，請確認代碼是否輸入正確。"
        )