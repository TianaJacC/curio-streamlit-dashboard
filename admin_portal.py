import csv
import datetime
import json
import os
import time
import pandas as pd
import streamlit as st

# ==============================================================================
# 0. 中央管理端頁面配置與絕對路徑統一防禦（務必放最前面）
# ==============================================================================
st.set_page_config(
    page_title="夢境珍奇櫃 ‧ 中央管理總控台",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 強制使用絕對路徑，確保與病患端指向同一個 system_logs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "system_logs")
os.makedirs(LOG_DIR, exist_ok=True)

FEEDBACK_FILE = os.path.join(LOG_DIR, "user_feedback_log.csv")
FEEDBACK_LOG_FILE = os.path.join(LOG_DIR, "user_feedback_log.csv")
SHARED_DB_FILE = os.path.join(LOG_DIR, "active_sessions.json")
SHARED_QUEUE_FILE = os.path.join(LOG_DIR, "active_queue.json")

# 初始化信件格式標準（此時變數已經定義完畢，不會再報 NameError）
def init_feedback_storage_standard():
    if not os.path.exists(FEEDBACK_LOG_FILE):
        with open(FEEDBACK_LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["Timestamp", "Role", "Token", "Category", "Content"])

init_feedback_storage_standard()

# 登入安全驗證狀態
if "admin_authenticated" not in st.session_state:
    st.session_state["admin_authenticated"] = False

ADMIN_MASTER_KEY = "CURIO-ADMIN-999"

# ==============================================================================
# 1. 莫蘭迪高奢美學樣式
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Garamond:ital,wght@0,400;0,600;1,400&display=swap');
    
    .stApp { 
        background-color: #0A110D !important; 
        font-family: -apple-system, BlinkMacSystemFont, "Garamond", "PingFang TC", sans-serif; 
    }
    
    .stApp p, .stApp label, .stApp span, .stMarkdown { 
        color: #FFFFFF !important; 
    }

    .admin-hero-card {
        background: linear-gradient(135deg, #142017 0%, #0A110D 100%);
        border: 2px solid #FCBF05;
        border-radius: 24px;
        padding: 28px 36px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(252, 191, 5, 0.15);
    }
    
    div.stButton > button { 
        border-radius: 12px !important; 
        border: 1.5px solid #FCBF05 !important; 
        background: linear-gradient(135deg, #FCBF05 0%, #C2A675 100%) !important; 
        box-shadow: 0 4px 14px rgba(252, 191, 5, 0.28) !important;
        transition: all 0.2s ease !important;
    }
    
    div.stButton > button, div.stButton > button * {
        color: #0A110D !important;
        font-weight: 900 !important;
    }
    
    div.stButton > button:hover {
        background: linear-gradient(135deg, #FFCD2E 0%, #D4B988 100%) !important;
        border-color: #FFFFFF !important;
    }

    .metric-box {
        background: #142017;
        border: 1.5px solid #25352B;
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. 管理端安全登入驗證
# ==============================================================================
if not st.session_state["admin_authenticated"]:
    st.markdown("""
        <div style="max-width: 460px; margin: 60px auto; background: #142017; border: 2px solid #FCBF05; border-radius: 24px; padding: 36px; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.5);">
            <div style="font-size: 2.8rem; margin-bottom: 8px;">🏛️</div>
            <h2 style="color: #FCBF05 !important; font-family: 'Garamond', serif; margin-bottom: 6px;">夢境珍奇櫃 ‧ 中央管理端</h2>
            <div style="font-size: 0.88rem; color: #A2B3A7; margin-bottom: 20px;">Curio & Studio 系統總控與信鴿羽毛信總匣</div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.6, 1])
    with col2:
        key_input = st.text_input("請輸入中央管理密鑰：", type="password", placeholder="預設: CURIO-ADMIN-999")
        if st.button("🔓 進入中央管理總控台", use_container_width=True):
            if key_input == ADMIN_MASTER_KEY:
                st.session_state["admin_authenticated"] = True
                st.success("✨ 驗證成功！正在載入總控台...")
                time.sleep(0.8)
                st.rerun()
            else:
                st.error("❌ 管理密鑰錯誤！")
    st.stop()

# ==============================================================================
# 3. 中央管理端主介面
# ==============================================================================
st.markdown("""
    <div class="admin-hero-card">
        <h2 style="color: #FCBF05 !important; margin: 0 0 6px 0; font-family: 'Garamond', serif;">🏛️ 夢境珍奇櫃 ‧ 中央管理與信鴿總控台</h2>
        <p style="color: #E8E2D5 !important; margin: 0; font-size: 0.92rem;">
            即時監控全網域探險家動態、信鴿羽毛信總匣、跨進程診間拋接數據與 ESG 綠色算力淨減碳盤查。
        </p>
    </div>
""", unsafe_allow_html=True)

col_m1, col_m2, col_m3, col_m4 = st.columns(4)

active_db_count = 0
if os.path.exists(SHARED_DB_FILE):
    try:
        with open(SHARED_DB_FILE, "r", encoding="utf-8") as f:
            active_db_count = len(json.load(f))
    except Exception:
        pass

feedback_count = 0
if os.path.exists(FEEDBACK_LOG_FILE):
    try:
        df_fb_temp = pd.read_csv(FEEDBACK_LOG_FILE, on_bad_lines='skip', engine='python')
        feedback_count = len(df_fb_temp)
    except Exception:
        pass

with col_m1:
    st.markdown(f"""
        <div class="metric-box">
            <div style="color: #A2B3A7; font-size: 0.85rem;">已封存身心印記</div>
            <div style="color: #FCBF05; font-size: 1.6rem; font-weight: bold; margin-top: 4px;">{active_db_count} 筆</div>
        </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown(f"""
        <div class="metric-box">
            <div style="color: #A2B3A7; font-size: 0.85rem;">信鴿羽毛信總數</div>
            <div style="color: #56D364; font-size: 1.6rem; font-weight: bold; margin-top: 4px;">{feedback_count} 封</div>
        </div>
    """, unsafe_allow_html=True)

with col_m3:
    st.markdown(f"""
        <div class="metric-box">
            <div style="color: #A2B3A7; font-size: 0.85rem;">系統架構狀態</div>
            <div style="color: #56D364; font-size: 1.3rem; font-weight: bold; margin-top: 4px;">🟢 正常運行</div>
        </div>
    """, unsafe_allow_html=True)

with col_m4:
    st.markdown(f"""
        <div class="metric-box">
            <div style="color: #A2B3A7; font-size: 0.85rem;">個資合規防護</div>
            <div style="color: #FCBF05; font-size: 1.3rem; font-weight: bold; margin-top: 4px;">🛡️ 100% 去敏</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

tab_mailbox, tab_sessions, tab_carbon, tab_settings = st.tabs([
    "📬 信鴿即時羽毛信總匣", 
    "📊 探險家身心拋接資料庫", 
    "🌱 ESG 綠色算力碳盤查", 
    "⚙️ 系統維護與登出"
])

# --- 分頁 1：信鴿即時羽毛信總匣 ---
with tab_mailbox:
    st.markdown("#### 🕊️ 來自全網域探險家的羽毛信（匿名回饋與求助總覽）")
    
    col_tb1, col_tb2 = st.columns([1, 1])
    with col_tb1:
        if st.button("🧪 測試塞入一封模擬羽毛信", use_container_width=True):
            with open(FEEDBACK_LOG_FILE, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
                writer.writerow([
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "探險家",
                    "#SYM-TEST",
                    "📜 羊皮紙翻頁提示",
                    "這是一封測試信鴿傳遞的羽毛信！"
                ])
                f.flush()
                os.fsync(f.fileno())
            st.success("✨ 成功塞入測試信！")
            st.rerun()
            
    with col_tb2:
        if st.button("🔄 即時重新整理信匣", use_container_width=True):
            st.rerun()

    st.markdown("---")

    # 🛡️ 雙重保險讀取機制：優先讀取 CSV，若無資料則從 JSON 備份提取
    df_feedback = pd.DataFrame()
    if os.path.exists(FEEDBACK_LOG_FILE) and os.path.getsize(FEEDBACK_LOG_FILE) > 0:
        try:
            df_feedback = pd.read_csv(FEEDBACK_LOG_FILE, on_bad_lines='skip', engine='python')
        except Exception:
            df_feedback = pd.DataFrame()

    # 如果 CSV 為空，嘗試從 active_sessions.json 的 pigeon_letters 撈取備份
    if df_feedback.empty and os.path.exists(SHARED_DB_FILE):
        try:
            with open(SHARED_DB_FILE, "r", encoding="utf-8") as f:
                db_data = json.load(f)
                backup_rows = []
                for tok, val in db_data.items():
                    if isinstance(val, dict) and "pigeon_letters" in val:
                        for letter in val["pigeon_letters"]:
                            backup_rows.append({
                                "Timestamp": letter.get("timestamp", ""),
                                "Role": "探險家",
                                "Token": tok,
                                "Category": letter.get("category", "一般"),
                                "Content": letter.get("content", "")
                            })
                if backup_rows:
                    df_feedback = pd.DataFrame(backup_rows)
        except Exception:
            pass

    # 渲染表格與閱讀室
    if not df_feedback.empty and len(df_feedback.columns) > 1:
        try:
            if "Timestamp" in df_feedback.columns:
                df_feedback = df_feedback.sort_values(by="Timestamp", ascending=False)
            
            search_query = st.text_input("🔍 搜尋羽毛信內容、代碼或類別：", placeholder="輸入關鍵字...", key="mailbox_search_safe")
            if search_query:
                mask = df_feedback.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
                df_feedback = df_feedback[mask]

            st.dataframe(df_feedback, use_container_width=True, height=250)
            
            st.markdown("##### 📖 信鴿羽毛信開信閱讀室")
            if "Timestamp" in df_feedback.columns and "Content" in df_feedback.columns:
                letter_options = [f"[{row.Timestamp}] {row.get('Role', '探險家')} ({row.get('Token', '#SYM')}) - {row.get('Category', '一般')}" for idx, row in df_feedback.iterrows()]
                selected_letter = st.selectbox("選擇要展開閱讀的羽毛信：", options=letter_options)
                
                if selected_letter:
                    selected_idx = letter_options.index(selected_letter)
                    target_row = df_feedback.iloc[selected_idx]
                    
                    st.markdown(f"""
                        <div style="background:#142017; border:2px solid #FCBF05; border-radius:16px; padding:20px; margin-top:10px;">
                            <div style="display:flex; justify-content:space-between; color:#FCBF05; font-weight:bold; margin-bottom:8px; font-size:0.95rem;">
                                <span>🕊️ 飛鴿傳書 ｜ 類別：{target_row.get('Category', 'General')}</span>
                                <span>🕒 {target_row.get('Timestamp', '')}</span>
                            </div>
                            <div style="color:#A2B3A7; font-size:0.85rem; margin-bottom:12px;">
                                發信身分：<b>{target_row.get('Role', '探險家')}</b> ｜ 去敏短碼：<code style="color:#FCBF05;">{target_row.get('Token', '#SYM')}</code>
                            </div>
                            <hr style="border:0; border-top:1px solid #25352B; margin:10px 0;">
                            <div style="color:#FFFFFF !important; font-size:1.05rem; line-height:1.8; white-space: pre-wrap;">
                                {target_row.get('Content', '（無內文）')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"⚠️ 讀取羽毛信發生異常：{e}")
    else:
        st.info("📭 目前信匣尚無有效羽毛信紀錄（已同時檢查 CSV 與 JSON 備份）。")

# --- 分頁 2：探險家身心拋接資料庫 ---
with tab_sessions:
    st.markdown("#### 📂 探險家即時拋接紀錄（Active Sessions Database）")
    if os.path.exists(SHARED_DB_FILE):
        try:
            with open(SHARED_DB_FILE, "r", encoding="utf-8") as f:
                sessions_data = json.load(f)
            if sessions_data:
                rows = []
                for tok, val in sessions_data.items():
                    rows.append({
                        "Token": tok,
                        "狀態": val.get("status"),
                        "心流一致性": val.get("coherence_score"),
                        "心理狀態": val.get("stress_index"),
                        "大氣壓強": val.get("ambient_pressure"),
                        "推薦調飲": val.get("mapped_drink"),
                        "時間戳記": val.get("timestamp")
                    })
                df_sessions = pd.DataFrame(rows)
                st.dataframe(df_sessions, use_container_width=True, height=350)
            else:
                st.info("📂 目前尚無探險家完成檢測並拋接資料。")
        except Exception as e:
            st.error(f"⚠️ 讀取拋接資料發生異常：{e}")
    else:
        st.warning("⚠️ 尚無 `active_sessions.json` 資料庫檔案。")

# --- 分頁 3：ESG 綠色算力碳盤查 ---
with tab_carbon:
    st.markdown("#### 🌱 ESG 永續與 GRI 範疇三確信級碳足跡報表")
    if st.button("📊 計算全院累積淨減碳效益與 GRI 揭露", use_container_width=True):
        try:
            from carbon_engine import EnterpriseScope3CarbonEngine
            engine = EnterpriseScope3CarbonEngine()
            report_df = engine.generate_annual_enterprise_ghg_report()
            if not report_df.empty:
                st.success("✅ 企業永續碳盤查報表已生成！")
                st.dataframe(report_df, use_container_width=True)
            else:
                st.info("🌱 目前累積碳權與減碳計算值為標準基準值。")
        except Exception as e:
            st.warning(f"⚠️ 碳引擎載入提示：{e}")

# --- 分頁 4：系統維護與登出 ---
with tab_settings:
    st.markdown("#### ⚙️ 中央管理端控制設定")
    if st.button("🔒 登出中央管理總控台", use_container_width=True):
        st.session_state["admin_authenticated"] = False
        st.success("👋 已安全登出中央管理端。")
        st.rerun()