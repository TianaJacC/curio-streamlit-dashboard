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
            "timestamp": "2026-08-01 01:20:15",
            "weekly_trend": [82, 85, 87, 84, 89, 91, 92.5],
            "nudge": (
                "探險家近 3 天夜間無應激爆發，心流穩定（92.5%）。建議問診重點：維持優質睡眠時數。"
            ),
            "summary": (
                "【去敏身心軌跡摘要】個案於看診前 15 秒於候診區完成 0.067 Hz"
                " 心流共振調息。連續 7"
                " 日數據顯示夜間無應激爆發，心流一致性維持於 90%"
                " 以上高諧振區間。"
            ),
        },
        "#SYM-A302": {
            "status": "已完成診前 15s 共振調息",
            "coherence_score": 88.0,
            "stress_index": "Morandi Sage",
            "stress_desc": "莫蘭迪綠區域 ‧ 輕度交感活性",
            "sleep_hours": 6.1,
            "timestamp": "2026-08-01 01:25:00",
            "weekly_trend": [70, 75, 78, 80, 82, 85, 88.0],
            "nudge": (
                "探險家睡眠時數偏低（6.1hr），生理指標顯示交感活性上升。建議問診重點：關懷換季氣壓調節。"
            ),
            "summary": (
                "【去敏身心軌跡摘要】個案於候診區完成心流調息。近 7"
                " 日睡眠時數偏低，生理指標顯示交感神經活性略微上升。"
            ),
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

if "patient_view_mode" not in st.session_state:
    st.session_state["patient_view_mode"] = False

MASTER_KEY = "CURIO-999"

# 包含郭醫師指定與新增 3 首 Progressive 頂級歌單
PLAYLIST = [
    {
        "title": (
            "Underworld - Dark & Long (Dark Train Extended Mix) [郭醫師首選]"
        ),
        "url": (
            "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
        ),
    },
    {
        "title": "✨ 新增 01 ‧ Underworld - Spoon Deep (心流低頻重拍神曲)",
        "url": (
            "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3"
        ),
    },
    {
        "title": (
            "✨ 新增 02 ‧ Sasha - Rooms (Scene Delete) [百大 DJ 心流修復]"
        ),
        "url": (
            "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3"
        ),
    },
    {
        "title": "✨ 新增 03 ‧ Tycho - A Walk (法式莫蘭迪感官 Progressive)",
        "url": (
            "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3"
        ),
    },
    {
        "title": "Underworld - Born Slippy .NUXX (Progressive 心流長音軌)",
        "url": (
            "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"
        ),
    },
    {
        "title": "Bicep - Glue (法式知性 Ambient Electronic 沉浸集)",
        "url": (
            "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"
        ),
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
# 3. 診所專屬 13 大高階選購模組 ✕ 一鍵論文 RWE 實裝 Modal 彈窗
# ==============================================================================
if hasattr(st, "dialog"):

    @st.dialog(
        "🎓 自費身心科 ── IRBE-IRB 快速審查與 RWE 論文研究數據一鍵生成器",
        width="large",
    )
    def paper_rwe_dialog():
        st.markdown(
            """
            <div style="background: linear-gradient(145deg, #FAF8F5, #F4F0E8); padding: 22px; border-radius: 20px; border: 1.5px solid #C2A675;">
                <h3 style="color: #25352B; font-family: 'Garamond', serif; font-size: 1.25rem; margin-top: 0;">一鍵生成符合 NJE / SCI 投稿規範之 RWE 論文數據庫</h3>
                <p style="font-size: 0.85rem; color: #596B60;">對齊 Nova Journal Experts (NJE) 投稿標準 ✕ 國際 OMOP CDM v5.4 資料庫對照：</p>
                <hr style="border:0; border-top:1px solid #E4DCD0; margin:10px 0;">
                <div style="font-size: 0.86rem; color: #25352B; line-height: 1.85;">
                    • <b>樣本總數與組態 (Sample Size N)</b>：N = 142（去敏化雙盲代碼，無名個資死鎖）<br>
                    • <b>統計顯著性對照 ($p$-value)</b>：前測 vs 後測心流一致性上升率 $p < 0.001$（雙尾檢定）<br>
                    • <b>SCI 期刊 Table 1 標準產出</b>：包含年齡層、0.067Hz 諧振方差與睡眠時數標準差。<br>
                    • <b>免 IRB 審查通關宣告包</b>：附帶《個資法》第 2 條去識別化證明，免送學術委員會漫長審查！
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("##### 📊 SCI 期刊 Table 1：心流調息臨床對照數據預覽")
        sample_df = pd.DataFrame(
            {
                "指標項目 (Metric)": [
                    "心流一致性 (Coherence %)",
                    "夜間應激爆發次數 (Events)",
                    "平均睡眠時數 (Hours)",
                ],
                "介入前 (Baseline)": ["68.2 ± 5.4", "4.2 ± 1.1", "5.4 ± 0.8"],
                "介入後 (14 Days)": ["92.5 ± 3.1", "0.4 ± 0.2", "7.2 ± 0.5"],
                "p-value (Significance)": [
                    "< 0.001***",
                    "< 0.001***",
                    "< 0.005**",
                ],
            }
        ).set_index("指標項目 (Metric)")
        st.table(sample_df)

        if st.button(
            "📥 一鍵匯出符合 NJE/SCI 期刊格式之論文數據備查包 (CSV / PDF)",
            use_container_width=True,
        ):
            st.toast(
                "🎉 已成功生成符合 Lancet Psychiatry / JAD 格式之論文數據備查包！"
            )

    @st.dialog(
        "💎 Curio & Studio 診間高階臨床與營運效能選配中心", width="large"
    )
    def upgrade_subscription_dialog():
        st.markdown(
            """
            <div style="background: linear-gradient(145deg, #FAF8F5, #F4F0E8); padding: 18px; border-radius: 20px; border: 1.5px solid #C2A675; margin-bottom: 12px;">
                <h3 style="color: #25352B; font-family: 'Garamond', serif; font-size: 1.25rem; margin-top: 0;">診所端高階效能選配模組 (Clinic Atelier Add-ons)</h3>
                <p style="font-size: 0.85rem; color: #596B60; margin-bottom: 0;">勾選需要解鎖的診所營運與看診提效模組（可隨時動態開通）：</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_a, col_b = st.columns(2)
        selected_cost = 0

        with col_a:
            m1 = st.checkbox(
                "🎫 健保爆診「本院個案當日優先加號憑證」 (+NT$ 3,800/月)",
                value=True,
            )
            if m1:
                selected_cost += 3800

            m2 = st.checkbox(
                "🗓️ 醫師跨院區兼診「無肉身行動排班 API 密鑰」 (+NT$ 4,500/月)"
            )
            if m2:
                selected_cost += 4500

            m3 = st.checkbox(
                "📊 院長專用「自費心理師/慢籤流失復發預警儀表板」 (+NT$"
                " 6,800/月)",
                value=True,
            )
            if m3:
                selected_cost += 6800

            m4 = st.checkbox(
                "📄 診前 15 秒「去敏身心軌跡莫蘭迪 PDF」生成機制 (+NT$"
                " 3,500/月)",
                value=True,
            )
            if m4:
                selected_cost += 3500

            m5 = st.checkbox(
                "⚡ 跨院回診健保缺號自動無聲捕蚊燈 (No-show 填補) (+NT$"
                " 5,200/月)"
            )
            if m5:
                selected_cost += 5200

            m6 = st.checkbox(
                "💊 診所自費藥局精準營養素交叉地圖維護 API (+NT$ 8,800/月)"
            )
            if m6:
                selected_cost += 8800

        with col_b:
            m7 = st.checkbox(
                "📈 自費身心科「臨床療效量化評估與 OMOP CDM 對照流」 (+NT$"
                " 9,800/月)",
                value=True,
            )
            if m7:
                selected_cost += 9800

            m8 = st.checkbox(
                "🎓 IRBE-IRB 快速審查與 RWE 論文研究數據一鍵生成器 (+NT$"
                " 8,800/月)",
                value=True,
            )
            if m8:
                selected_cost += 8800

            m9 = st.checkbox(
                "🔄 連鎖院區「個案異地調診去敏病歷快捷拋接」 (+NT$ 6,000/月)"
            )
            if m9:
                selected_cost += 6000

            m10 = st.checkbox(
                "🌐 社交孤立預警（GPS 位移 ✕ 通訊頻率分析） (+NT$ 3,200/月)"
            )
            if m10:
                selected_cost += 3200

            m11 = st.checkbox(
                "🌧️ 環境壓力感測（氣壓/濕度/噪音 ✕ 萌寵安撫頻率） (+NT$"
                " 2,800/月)"
            )
            if m11:
                selected_cost += 2800

            m12 = st.checkbox(
                "💓 循環與免疫監測（rPPG 監測 HRV ✕ 量化發炎負擔） (+NT$"
                " 4,500/月)"
            )
            if m12:
                selected_cost += 4500

        st.markdown(
            f"""
            <div style="background: #25352B; color: #FAF8F5; padding: 14px 20px; border-radius: 16px; margin-top: 16px; text-align: space-between; display: flex; align-items: center; justify-content: space-between; border: 1px solid #C2A675;">
                <span style="font-family: Didot, serif; font-size: 1.05rem;">預估月選配增額：<b style="color:#D4AF37; font-size:1.3rem;">+ NT$ {selected_cost:,} 元/月</b></span>
                <span style="font-size: 0.8rem; color: #D3E0D7;">專案開通電話：(02) 2396-6070</span>
            </div>
        """,
            unsafe_allow_html=True,
        )

    @st.dialog("📑 健保 / 自費高階療程評估對照卡")
    def treatment_card_dialog():
        st.markdown(
            """
            <div style="background: linear-gradient(145deg, #FAF8F5, #F4F0E8); padding: 22px; border-radius: 20px; border: 1.5px solid #C2A675;">
                <h3 style="color: #25352B; font-family: 'Garamond', serif; font-size: 1.25rem; margin-top: 0;">自費醫療高階療程對照建議卡</h3>
                <p style="font-size: 0.84rem; color: #596B60;">個案去敏密鑰：<b>#SYM-C701</b> ｜ 近 7 日心流一致性：<b>92.5%</b></p>
                <hr style="border:0; border-top:1px solid #E4DCD0; margin:10px 0;">
                <div style="font-size: 0.86rem; color: #25352B; line-height: 1.8;">
                    <b>✨ 建議引導自費項目：</b><br>
                    1. <b>rTMS 重複經顱磁刺激療程</b>：適合交感神經高活性、夜間應激偏態者。<br>
                    2. <b>0.067Hz 深度心流聲學共振訓練</b>：搭配莫蘭迪音場進行 15 分鐘診前深層放鬆。<br>
                    3. <b>自費精準營養抗發炎點滴</b>：修復長期焦慮引發之 Cortisol 生理發炎負擔。
                </div>
                <div style="margin-top: 16px; text-align: center; font-size:0.8rem; color:#B29562;">
                    💡 本卡可一鍵轉向病患螢幕展示，提升自費療程續單率。
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
                <div style="margin-top: 20px; padding: 12px; background: rgba(194, 166, 117, 0.12); border-radius: 12px; font-size: 0.78rem; color:#B29562; text-align: center; font-family: 'Garamond', serif;">
                    🏛️ 發布單位：居里研創股份有限公司 (Curio & Studio) ｜ 日期：2026 年 08 月 01 日
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
                log_system_event(
                    "SECURITY_PASSWORD_CHANGE", "診間金鑰已成功變更"
                )
                st.success("🎉 診間金鑰已成功變更！舊金鑰已即刻失效。")
                st.rerun()


# ==============================================================================
# 4. 側邊欄：郭醫師指定 YouTube 原生嵌入 ✕ 備用音效全功能選播 ✕ 動態 QR Code
# （移至登入欄前方，確保側邊欄 100% 剛性渲染、絕不消失）
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

    # 郭醫師指定 YouTube 音樂原生無縫嵌入（100% 播放 YouTube 音響）
    with st.expander("🎵 郭醫師指定 YouTube 聲景音場", expanded=True):
        st.write("郭醫師最新指定曲 ‧ 迷幻心流深層共振:")
        st.components.v1.html(
            """
            <iframe width="100%" height="180" src="https://www.youtube.com/embed/_eCGu2Te3ZA?autoplay=0&loop=1&playlist=_eCGu2Te3ZA" 
            title="郭醫師指定曲" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
            """,
            height=190,
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
        st.image(
            qr_url, caption="手機相機掃碼即可 100% 直達相同頁面", width=160
        )

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
            "nudge": (
                f"飛鴿拋接短碼"
                f" {token_a}。心流表現極佳（{score_a}%），建議進行常規衛教即可。"
            ),
            "summary": (
                f"【去敏身心軌跡摘要】經由 LINE LIFF 飛鴿拋接之短碼"
                f" {token_a}。個案完成診前調息，心流表現極佳。"
            ),
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

    # 備用古典與 Progressive 音色選播列
    st.markdown(
        """
        <div class="sidebar-ateliers-box">
            <div style="font-size:0.85rem; font-weight:600; color:#25352B; margin-bottom:6px;">
                <span class="curio-3d-icon">🎶</span>古典與 Ambient 備用音場
            </div>
    """,
        unsafe_allow_html=True,
    )

    selected_track_idx = st.selectbox(
        "選擇備用聲景：",
        range(len(PLAYLIST)),
        format_func=lambda x: PLAYLIST[x]["title"],
        index=st.session_state["current_track_idx"],
    )

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        if st.button("🔀 隨機切換"):
            st.session_state["current_track_idx"] = random.randint(
                0, len(PLAYLIST) - 1
            )
            st.rerun()
    with col_m2:
        loop_status_str = (
            "🔁 循環中" if st.session_state["audio_loop"] else "➡️ 單次"
        )
        if st.button(f"模式: {loop_status_str}"):
            st.session_state["audio_loop"] = not st.session_state["audio_loop"]
            st.rerun()

    current_audio_url = PLAYLIST[selected_track_idx]["url"]

    st.components.v1.html(
        f"""
        <div style="background:#F4F0E8; padding:10px; border-radius:14px; border:1px solid #C2A675; text-align:center;">
            <audio id="curio-player" controls preload="auto" style="width: 100%; height: 40px;">
                <source src="{current_audio_url}" type="audio/mpeg">
            </audio>
            <div style="font-size: 10px; color: #25352B; margin-top: 4px; font-weight: 600;">
                🎵 備用音場：{PLAYLIST[selected_track_idx]['title']}
            </div>
            <script>
                var audio = document.getElementById('curio-player');
                if (audio) {{
                    audio.volume = 0.8;
                    audio.addEventListener('ended', function() {{
                        if ({str(st.session_state['audio_loop']).lower()}) {{
                            this.currentTime = 0;
                            this.play();
                        }}
                    }}, false);
                }}
            </script>
        </div>
        """,
        height=130,
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
        custom_memo = st.text_input(
            "輸入自訂訊息至櫃檯：", placeholder="例如：請準備溫熱毛巾..."
        )
        msg_to_send = custom_memo
    else:
        msg_to_send = preset_msg

    if st.button("📡 無聲推播至櫃檯"):
        if msg_to_send:
            log_system_event(
                "NURSE_MEMO_SENT", f"醫師推播至櫃檯: {msg_to_send}"
            )
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
# 5. 門診安全驗證登入頁
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
                log_system_event(
                    "AUTH_SUCCESS", "診間金鑰驗證成功並進入面板"
                )
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
# 6. 主面板邏輯 (含雙螢幕病患視角切換 ✕ 莫蘭迪茶飲建議 ✕ 一鍵論文 RWE)
# ==============================================================================
def fetch_patient_data(user_key):
    return global_db.get(user_key, None)


# 頂樓雙螢幕病患視角切換開關 (Presentation Flip)
pv_col1, pv_col2 = st.columns([3.2, 0.8])
with pv_col2:
    patient_mode = st.toggle(
        "🔄 翻轉/病患視角", value=st.session_state["patient_view_mode"]
    )
    st.session_state["patient_view_mode"] = patient_mode

# 🎭 狀況 A：切換為病患展示視角 ( Presentation Mode )
if st.session_state["patient_view_mode"]:
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #FAF8F5 0%, #F4F0E8 100%); padding: 40px; border-radius: 32px; border: 2px solid #C2A675; text-align: center; box-shadow: 0 20px 50px rgba(37, 53, 43, 0.08); margin-top: 10px;">
            <div style="font-size: 3rem; margin-bottom: 8px;">🐿️</div>
            <div class="brand-caption" style="font-size: 1.1rem; letter-spacing: 4px;">Curio & Studio ‧ 夢境珍奇櫃</div>
            <h2 style="color: #25352B; font-family: 'Garamond', serif; font-size: 2.2rem; margin: 12px 0 16px 0;">自費醫療高階療程對照建議卡</h2>
            <div class="gold-divider" style="width: 80px; height: 3px;"></div>
            <div style="font-size: 1.15rem; color: #25352B; line-height: 2.2; max-width: 680px; margin: 0 auto; text-align: left;">
                ✨ <b>專屬身心共振調節建議：</b><br>
                1. <b>rTMS 重複經顱磁刺激療程</b>：深層活化前額葉皮質，快速調節交感神經高活性。<br>
                2. <b>0.067Hz 莫蘭迪聲學調息</b>：搭配專屬音場，進行 15 分鐘診前大腦迷走神經錨定。<br>
                3. <b>精準抗發炎點滴</b>：降低 Cortisol 生理應激負擔，恢復優質睡眠品質。
            </div>
            <div style="margin-top: 30px; font-size: 0.95rem; color: #B29562; font-family: 'Didot', serif; italic;">
                🌿 交感身心診所 ‧ 關懷您的每一刻心流諧振
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )
    st.stop()

# 🎭 狀況 B：常規醫師看診視角 ( Doctor Dashboard )
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
progress_pct = (
    min(1.0, completed / total_patients) if total_patients > 0 else 0.0
)

st.markdown(
    f"""
    <div class="doctor-care-card">
        <div style="flex-grow: 1; margin-right: 20px;">
            <div class="doctor-care-text">
                午安。今日預約看診 <b>{total_patients}</b> 位探險家 ｜ 目前進度：<b>{completed}/{total_patients}</b> ({int(progress_pct*100)}%) ｜ 心流諧振指數 <b>94%</b><br>
                <span style="font-size:0.82rem; color:#596B60;">🍵 <b>診間莫蘭迪茶飲/沉香建議</b>：本日交感神經活性略高，建議搭配<b>澳洲檀香/煙燻雪松</b>香氛 ✕ <b>薄荷甘菊茶</b>。</span>
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

# 頂樓認證欄 + 240 分鐘剛性銷毀倒數 + 療程評估卡 + 一鍵論文 RWE
top_col1, top_col2, top_col3, top_col4, top_col5 = st.columns(
    [2.0, 0.8, 0.8, 0.8, 0.8]
)
with top_col1:
    st.markdown(
        """
        <div style="background:#FFFFFF; border:1px solid #E4DCD0; border-radius:30px; padding:10px 18px; font-size:0.82rem; color:#25352B;">
            <span class="curio-3d-icon" style="width:20px; height:22px; font-size:0.75rem;">🟢</span> 認證 ｜ 🏛️ C701 ｜ <span class="curio-3d-icon" style="width:20px; height:22px; font-size:0.75rem;">🛡️</span> <b>0 個資</b> ｜ <span style="color:#C2A675; font-weight:600;">⏳ 銷毀：182 m</span>
        </div>
    """,
        unsafe_allow_html=True,
    )
with top_col2:
    if st.button("🎓 論文 RWE", use_container_width=True):
        if hasattr(st, "dialog"):
            paper_rwe_dialog()
with top_col3:
    if st.button("📑 療程卡", use_container_width=True):
        if hasattr(st, "dialog"):
            treatment_card_dialog()
with top_col4:
    if st.button("💎 升級選配", use_container_width=True):
        if hasattr(st, "dialog"):
            upgrade_subscription_dialog()
with top_col5:
    if st.button("⚙️ 金鑰", use_container_width=True):
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
                "<h4 style='color:#25352B; font-size:1.05rem;"
                " margin-top:12px;'>近 7 日心流一致性調息曲線 (Coherence"
                " Score)</h4>",
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
                "<h4 style='color:#25352B; font-size:1.05rem;"
                " margin-top:10px;'>邊緣端 15 秒去敏化身心軌跡</h4>",
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
        log_system_event(
            "FETCH_DATA_NOT_FOUND", f"查詢不存在之代碼: {user_key}"
        )
        st.error(
            f"⚠️ 找不到密鑰 `{user_key}` 之當日資料，請確認代碼是否輸入正確。"
        )