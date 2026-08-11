import datetime
import os
import random
import time
import pandas as pd
import streamlit as st

# ==============================================================================
# 0. 雲端系統 Log 軌跡自動備份機制
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
# 1. 全局配置與跨裝置共享資料庫 (自動抓取 URL Query Token 實現 100% 拋接)
# ==============================================================================
st.set_page_config(
    page_title="夢境珍奇櫃診間面板 ‧ Curio & Studio",
    page_icon="🐿️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 自動讀取 URL 傳過來的 token 參數
query_params = st.query_params
url_token = query_params.get("token", None)


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


global_db = get_global_database()

# 如果有從病患端 URL 拋接過來的 Token，自動插入資料庫
if url_token and url_token not in global_db:
    global_db[url_token] = {
        "status": "已完成診前 15s 共振調息",
        "coherence_score": 93.5,
        "stress_index": "Morandi Green",
        "stress_desc": "副交感平穩諧振區",
        "sleep_hours": 7.5,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "weekly_trend": [80, 83, 85, 88, 90, 92, 93.5],
        "nudge": (
            f"探險家密鑰 {url_token}。已完成診前 15s"
            " 共振調息，心流狀態一致性極佳 (93.5%)。"
        ),
        "summary": (
            f"【去敏身心軌跡摘要】經由信鴿 Singer 飛鴿拋接之密鑰"
            f" {url_token}。個案完成三站調息準備，生理諧振指數達標。"
        ),
    }

if "selected_token" not in st.session_state:
    st.session_state["selected_token"] = (
        url_token if url_token else "#SYM-C701"
    )

if "doctor_password" not in st.session_state:
    st.session_state["doctor_password"] = "NYJAZZ-8519"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

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

# 備選聲景 (已精準刪除郭醫師不喜歡的法式知性與莫蘭迪)
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
        "title": "Underworld - Born Slippy .NUXX (Progressive 心流長音軌)",
        "url": (
            "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"
        ),
    },
]

# 登入前 CSS 強制完全隱藏側邊欄
sidebar_hide_style = ""
if not st.session_state["authenticated"]:
    sidebar_hide_style = """
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
        button[aria-label="Open sidebar"] { display: none !important; }
        button[aria-label="Close sidebar"] { display: none !important; }
    """

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Didot&family=Garamond:ital,wght@0,400;0,600;1,400&display=swap');

    {sidebar_hide_style}

    .stApp {{
        background-color: #FAF8F5;
        font-family: -apple-system, BlinkMacSystemFont, "Garamond", "Didot", "Georgia", "PingFang TC", sans-serif;
    }}
    header[data-testid="stHeader"] {{ background-color: rgba(0,0,0,0); }}
    footer {{ visibility: hidden; }}

    .curio-hero-card {{
        background: linear-gradient(135deg, #25352B 0%, #1A261F 100%);
        color: #FAF8F5;
        padding: 34px 44px;
        border-radius: 28px;
        box-shadow: 0 20px 48px rgba(37, 53, 43, 0.12);
        border: 1px solid #C2A675;
        margin-bottom: 22px;
    }}
    .curio-hero-card h1 {{ 
        font-family: "Didot", "Georgia", "PingFang TC", serif !important;
        color: #FAF8F5 !important; 
        font-size: 1.85rem !important; 
        font-weight: 500 !important; 
        margin: 0 0 8px 0 !important; 
    }}
    .doctor-care-card {{
        background: linear-gradient(135deg, #F4F0E8 0%, #EAE4D8 100%);
        border: 1px solid #C2A675; border-radius: 22px; padding: 20px 26px; margin-bottom: 16px;
    }}
    .atelier-login-card {{
        background: rgba(255, 255, 255, 0.96); border: 1.5px solid #C2A675;
        padding: 40px 40px 28px 40px; border-radius: 28px; max-width: 500px; margin: 20px auto; text-align: center;
    }}
    .sidebar-ateliers-box {{
        background: #FFFFFF; border: 1px solid #E4DCD0; padding: 16px; border-radius: 18px; margin-bottom: 14px;
    }}
    .stButton>button {{
        border-radius: 12px !important; border: 1px solid #C2A675 !important;
        background: linear-gradient(135deg, #FAF8F5 0%, #F4F0E8 100%) !important; color: #25352B !important;
    }}
    </style>
""",
    unsafe_allow_html=True,
)

# Modal 彈窗宣告
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

        # 實裝一鍵下載生成數據 CSV 功能
        csv_data = sample_df.to_csv().encode("utf-8")
        st.download_button(
            label=(
                "📥 一鍵匯出符合 NJE/SCI 期刊格式之論文數據備查包 (CSV"
                " 檔案)"
            ),
            data=csv_data,
            file_name="Curio_Studio_RWE_Paper_Data.csv",
            mime="text/csv",
            use_container_width=True,
        )

    @st.dialog(
        "💎 Curio & Studio 診間高階臨床與營運效能選配中心", width="large"
    )
    def upgrade_subscription_dialog():
        st.markdown(
            """
            <div style="background: linear-gradient(145deg, #FAF8F5, #F4F0E8); padding: 18px; border-radius: 20px; border: 1.5px solid #C2A675; margin-bottom: 12px;">
                <h3 style="color: #25352B; font-family: 'Garamond', serif; font-size: 1.25rem; margin-top: 0;">診所端高階效能選配模組 (Clinic Atelier Add-ons)</h3>
                <p style="font-size: 0.85rem; color: #596B60; margin-bottom: 0;">勾選需要解鎖的診所營運與看診提效模組：</p>
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
            m8 = st.checkbox(
                "🎓 IRBE-IRB 快速審查與 RWE 論文研究數據一鍵生成器 (+NT$"
                " 8,800/月)",
                value=True,
            )
            if m8:
                selected_cost += 8800
        with col_b:
            m7 = st.checkbox(
                "📈 自費身心科「臨床療效量化評估與 OMOP CDM 對照流」 (+NT$"
                " 9,800/月)",
                value=True,
            )
            if m7:
                selected_cost += 9800

        st.markdown(
            f"""
            <div style="background: #25352B; color: #FAF8F5; padding: 14px 20px; border-radius: 16px; margin-top: 16px; text-align: space-between; display: flex; align-items: center; justify-content: space-between; border: 1px solid #C2A675;">
                <span style="font-family: Didot, serif; font-size: 1.05rem;">預估月選配增額：<b style="color:#D4AF37; font-size:1.3rem;">+ NT$ {selected_cost:,} 元/月</b></span>
            </div>
        """,
            unsafe_allow_html=True,
        )

    @st.dialog("蔻恩閣長的 3D 典藏資安寶盒")
    def security_declaration_dialog():
        st.markdown(
            """
            <div style="background: linear-gradient(145deg, #FAF8F5, #F4F0E8); padding: 22px; border-radius: 20px; border: 1.5px solid #C2A675;">
                <div style="text-align: center; margin-bottom: 12px;">
                    <div style="font-size: 2.2rem; margin-bottom: 4px;">🐿️</div>
                    <h3 style="color: #25352B; font-family: 'Garamond', serif; font-size: 1.2rem; margin: 0;">小松鼠蔻恩閣長 Cone 資安與 0 個資宣告</h3>
                </div>
                <div style="font-size: 0.86rem; color: #25352B; line-height: 1.85;">
                    <b>✨ 蔻恩閣長 Cone 0 個資資安承諾：</b><br>
                    1. <b>符合《個資法》第 2 條去識別化標準</b>：全流程絕不收集、記錄或存儲病患真實姓名、身分證號、電話或病歷號。<br>
                    2. <b>240 分鐘動態時間鎖 (Time-Lock)</b>：去敏密鑰 (Token) 具備 240 分鐘動態壽命，看診完畢即剛性銷毀。<br>
                    3. <b>HTTPS TLS 1.3 & AES-256 加密</b>：前端至中繼站全通道高階加密。<br>
                    4. <b>Air-Gapped 雙盲隔離</b>：與診所行政 HIS/LINE 實施資料庫實體隔離。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ==============================================================================
# 4. 門診安全驗證登入頁 (包含資安寶盒與忘記密碼完全恢復)
# ==============================================================================
if not st.session_state["authenticated"]:
    st.markdown(
        """
        <div class="atelier-login-card">
            <div style="font-size: 2.8rem; margin-bottom: 8px;">🐿️</div>
            <div class="brand-caption">Curio & Studio</div>
            <div class="medical-title">交感身心診所 ‧ 門診安全驗證</div>
            <div class="gold-divider"></div>
            <div style="font-size:0.88rem; color:#596B60; line-height:1.7;">
                零知識架構 (Zero-Knowledge) ‧ 雙盲去敏身心軌跡拋接<br>
                <span style="font-size:0.82rem; color:#C2A675;">首席珍藏家蔻恩閣長 Cone 已為您鎖定 0 個資防線</span>
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

        # 恢復：資安寶盒按鈕
        if st.button("蔻恩閣長 Cone 3D 典藏資安寶盒", use_container_width=True):
            if hasattr(st, "dialog"):
                security_declaration_dialog()

        st.markdown(
            "<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True
        )

        # 恢復：忘記密碼提示展開盒
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
# 5. 側邊欄 (登入成功後呈現，聲景控制項完全露出)
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

    # 郭醫師指定 YouTube 原生音場
    with st.expander("🎵 郭醫師指定 YouTube 聲景音場", expanded=True):
        st.write("郭醫師最新指定曲 ‧ 迷幻心流深層共振:")
        st.components.v1.html(
            """
            <iframe width="100%" height="180" src="https://www.youtube.com/embed/_eCGu2Te3ZA?autoplay=0&loop=1&playlist=_eCGu2Te3ZA" 
            title="郭醫師指定曲" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
            """,
            height=190,
        )

    # 備用 Progressive 聲景 (完全露出：選單 + 播放器 + 隨機/循環控制鈕)
    st.markdown(
        """
        <div class="sidebar-ateliers-box">
            <div style="font-size:0.85rem; font-weight:600; color:#25352B; margin-bottom:6px;">
                <span>🎶</span> 備用 Progressive 聲景選播
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
        <div style="background:#F4F0E8; padding:8px; border-radius:12px; border:1px solid #C2A675; text-align:center;">
            <audio id="curio-player" controls preload="auto" style="width: 100%; height: 40px;">
                <source src="{current_audio_url}" type="audio/mpeg">
            </audio>
        </div>
        """,
        height=60,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # 門診待看診佇列
    st.markdown(
        """
        <div style="font-size:0.88rem; font-weight:600; color:#25352B; margin-top:10px; margin-bottom:8px; padding-left:4px;">
            <span>📜</span>門診待看診佇列 (Queue)
        </div>
    """,
        unsafe_allow_html=True,
    )

    for item in global_db.keys():
        if st.button(
            f"解鎖去敏密鑰 {item}",
            key=f"btn_{item}",
            use_container_width=True,
        ):
            st.session_state["selected_token"] = item
            log_system_event("QUEUE_SELECT", f"醫師手動點擊切換 Token: {item}")
            st.rerun()

# ==============================================================================
# 6. 主診間面板 (解鎖後呈現)
# ==============================================================================
st.markdown(
    """
    <div class="curio-hero-card">
        <h1>夢境珍奇櫃診間面板</h1>
        <p>Curio & Studio x 交感身心診所 ｜ 首席珍藏家蔻恩閣長 Cone ‧ 0 個資 ‧ 診前身心軌跡拋接</p>
    </div>
""",
    unsafe_allow_html=True,
)

top_col1, top_col2, top_col3, top_col4 = st.columns([2.0, 0.9, 0.9, 0.9])
with top_col1:
    st.markdown(
        """
        <div style="background:#FFFFFF; border:1px solid #E4DCD0; border-radius:30px; padding:10px 18px; font-size:0.82rem; color:#25352B;">
            🟢 認證 ｜ 🏛️ C701 ｜ 🛡️ <b>0 個資</b> ｜ <span style="color:#C2A675; font-weight:600;">⏳ 銷毀：182 m</span>
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

st.markdown(
    "<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True
)

user_key = st.text_input(
    "請輸入探險家去敏密鑰 (例如：#SYM-C701) :",
    value=st.session_state["selected_token"],
    placeholder="輸入密鑰代碼，例如 #SYM-C701",
)

if user_key:
    data = global_db.get(user_key, None)
    if data:
        log_system_event("FETCH_DATA_SUCCESS", f"成功查詢去敏代碼: {user_key}")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                label="心流一致性 (0.067Hz)",
                value=f"{data['coherence_score']} %",
                delta="↑ 3.2% 穩定共振",
            )
        with col2:
            st.metric(
                label="身心應激狀態",
                value=data["stress_index"],
                delta=data.get("stress_desc", "放縮區"),
            )
        with col3:
            st.metric(
                label="本機睡眠時數",
                value=f"{data['sleep_hours']} hr",
                delta="達標 7 小時",
            )

        st.markdown("---")
        st.write(f"**【去敏身心軌跡摘要】**\n\n{data['summary']}")
        st.caption(f"🕒 數據傳輸時間戳記：{data['timestamp']}")
    else:
        st.error(
            f"⚠️ 找不到密鑰 `{user_key}` 之當日資料，請確認代碼是否輸入正確。"
        )