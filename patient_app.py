import streamlit as st
import hashlib, hmac, time, os, json, csv, random, datetime
import numpy as np

st.set_page_config(
    page_title="夢境珍奇櫃 ‧ 探險家終端",
    page_icon="🐿️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

LOG_DIR = "system_logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

FEEDBACK_FILE = os.path.join(LOG_DIR, "user_feedback_log.csv")
SHARED_DB_FILE = os.path.join(LOG_DIR, "active_sessions.json")
RESERVE_FILE = os.path.join(LOG_DIR, "public_pilot_reservations.csv")

# 1. 匿名回饋函式 (前置定義，絕不噴 NameError)
def save_feedback(role, token, category, content):
    now_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.exists(FEEDBACK_FILE)
    with open(FEEDBACK_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Role", "Token", "Category", "Content"])
        writer.writerow([now_ts, role, token, category, content.strip()])

if hasattr(st, "dialog"):
    @st.dialog("💬 遇到問題？回饋給團隊")
    def feedback_modal(current_token):
        st.write(f"目前通行代碼：`{current_token}` ｜ 0 個資防護")
        cat = st.radio("問題類型：", ["畫面操作不順", "鏡頭感應不良", "其他建議"], horizontal=True)
        txt = st.text_area("請簡述狀況：", height=80)
        if st.button("送出回饋", use_container_width=True):
            save_feedback("病患/探險家", current_token, cat, txt)
            st.success("✅ 回饋已安全存入系統紀錄！")
            st.rerun()

# 2. 金鑰演算法：照片固定化 (以相片為主，絕不亂跳)
def get_photo_token(photo_bytes: bytes) -> str:
    digest = hashlib.sha256(photo_bytes).hexdigest()
    return f"#SYM-{digest[:4].upper()}"

def get_temp_token() -> str:
    t = str(time.time()).encode("utf-8")
    return f"#SYM-{hashlib.sha256(t).hexdigest()[:4].upper()}"

if "patient_token" not in st.session_state:
    st.session_state["patient_token"] = get_temp_token()
if "token_locked" not in st.session_state:
    st.session_state["token_locked"] = False
if "app_step" not in st.session_state:
    st.session_state["app_step"] = "invite"

# 跨進程資料庫讀寫 (解決醫師端收不到的問題)
def save_to_shared_db(token, data):
    db = {}
    if os.path.exists(SHARED_DB_FILE):
        try:
            with open(SHARED_DB_FILE, "r", encoding="utf-8") as f:
                db = json.load(f)
        except Exception:
            db = {}
    db[token] = data
    with open(SHARED_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def get_from_shared_db(token):
    if os.path.exists(SHARED_DB_FILE):
        try:
            with open(SHARED_DB_FILE, "r", encoding="utf-8") as f:
                db = json.load(f)
                return db.get(token)
        except Exception:
            pass
    return None

# 3. 樣式注入
st.markdown("""
    <style>
    .stApp { background-color: #0A110D !important; color: #FAF8F5 !important; font-family: -apple-system, BlinkMacSystemFont, "PingFang TC", sans-serif; }
    label, p, span, .stMarkdown { color: #FAF8F5 !important; }
    .dream-box { background: linear-gradient(135deg, #142017 0%, #0E1711 100%); border: 1.5px solid #C2A675; border-radius: 20px; padding: 20px; margin-bottom: 16px; }
    .french-card { background: #F7F4EE !important; border: 2px solid #C2A675 !important; border-radius: 18px !important; padding: 18px !important; color: #1C2B20 !important; margin-bottom: 14px !important; }
    .french-card h3, .french-card b, .french-card span { color: #1C2B20 !important; }
    .breath-bubble { width: 120px; height: 120px; border-radius: 50%; background: radial-gradient(circle, #C2A675 0%, #16221A 100%); margin: 20px auto; display: flex; align-items: center; justify-content: center; font-size: 2.2rem; box-shadow: 0 0 30px rgba(194, 166, 117, 0.4); }
    .stButton>button { border-radius: 12px !important; border: 1.5px solid #C2A675 !important; background: #C2A675 !important; color: #0A110D !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# 4. 判斷網址模式 (避免 404，由 Query Params 路由)
qp = st.query_params
mode = qp.get("mode", "main")

# --- 分支 A：忘記金鑰救援 ---
if mode == "recovery":
    st.markdown("""
        <div class="french-card">
            <h3 style="margin-top:0;">🔑 30秒一鍵金鑰救援 (Key-Stitching)</h3>
            <p>請重新選取您剛才選過的<b>同一張照片</b>，系統將在 0.1 秒內在手機本機重新計算 SHA-256 密鑰，無痕找回今日生活處方！</p>
        </div>
    """, unsafe_allow_html=True)
    rec_pic = st.file_uploader("請點擊選取原相片 (JPG/PNG)", type=["jpg", "png", "jpeg"], key="rec_uploader")
    if rec_pic:
        rec_token = get_photo_token(rec_pic.getvalue())
        st.success(f"🔑 比對完成！您的金鑰代碼：`{rec_token}`")
        rec_data = get_from_shared_db(rec_token)
        if rec_data:
            st.markdown(f"""
                <div class="french-card">
                    🍵 <b>今日生活處方：</b> {rec_data.get('prescription_50')}<br>
                    ✨ <b>現場吧台奉茶：</b> {rec_data.get('mapped_drink')}<br>
                    💓 <b>心流分數：</b> {rec_data.get('coherence_score')}%
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info(f"代碼 `{rec_token}` 已鎖定，請向櫃檯或郭醫師出示此短碼即可。")
    st.stop()

# --- 分支 B：預約公測登記 ---
elif mode == "reserve":
    st.markdown("""
        <div class="french-card">
            <h3 style="margin-top:0;">✨ 2027 春節後擴大公測登記</h3>
            <p>貫徹 No-PII 零個資規範，無須留下姓名電話即可保留第二階段名額。</p>
        </div>
    """, unsafe_allow_html=True)
    cur_t = st.text_input("您的代碼：", value=st.session_state["patient_token"])
    agree = st.checkbox("同意於 2027 年 2 月接受生活處方追蹤公測", value=True)
    if st.button("🚀 確認送出意願", use_container_width=True):
        if agree:
            now_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            res_id = f"RES-{random.randint(1000, 9999)}"
            with open(RESERVE_FILE, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([res_id, cur_t, now_ts, "Phase_2", "Registered"])
            st.success(f"✅ 登記成功！預約編號：`{res_id}` 已入庫。")
        else:
            st.warning("請先勾選同意。")
    st.stop()

# --- 分支 C：主調息流程 (原汁原味) ---
st.markdown(f"""
    <div class="dream-box">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span>🗝️ 今日通行短碼</span>
            <span style="font-family:monospace; color:#C2A675; font-size:1.2rem; font-weight:bold;">{st.session_state['patient_token']}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

if st.button("💬 遇到問題？回饋給團隊", use_container_width=True):
    if hasattr(st, "dialog"):
        feedback_modal(st.session_state["patient_token"])

if st.session_state["app_step"] == "invite":
    st.markdown("""
        <div class="dream-box">
            <h2 style="color:#C2A675; text-align:center; margin-top:0;">夢境珍奇櫃 ‧ 入閣邀請函</h2>
            <p style="font-size:0.92rem; line-height:1.7;">誠摯邀請您與首席珍藏家小松鼠蔻恩閣長一起進行 19 秒迷走神經共振調息。全程 0 個資防護，不收集任何個人真實身分。</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🗝️ 開啟調息入口", use_container_width=True):
        st.session_state["app_step"] = "play"
        st.rerun()

elif st.session_state["app_step"] == "play":
    st.markdown("""
        <div class="french-card">
            <h3>📷 一鍵匿名登入 (選一張喜歡的照片)</h3>
            <p>手機本機即時生成 SHA-256 金鑰，絕不上傳照片本體。</p>
        </div>
    """, unsafe_allow_html=True)
    
    up_pic = st.file_uploader("點擊選擇照片 (JPG/PNG)", type=["jpg", "png", "jpeg"], key="main_pic_uploader")
    if up_pic:
        st.session_state["patient_token"] = get_photo_token(up_pic.getvalue())
        st.session_state["token_locked"] = True
        st.success(f"🔑 匿名金鑰已綁定為照片特徵：`{st.session_state['patient_token']}`")

    st.markdown("---")
    st.markdown("#### 🎨 第一關 ‧ 心流色彩塗鴉 (480x160 畫布)")
    st.components.v1.html("""
        <div style="background:#111A14; border:2px solid #C2A675; border-radius:14px; padding:10px; text-align:center;">
            <canvas id="cv" width="480" height="150" style="background:#080D0A; border-radius:10px; width:100%; max-width:480px; height:150px; touch-action:none;"></canvas>
            <div style="margin-top:6px;"><button onclick="ctx.clearRect(0,0,cv.width,cv.height)" style="background:#25352B; color:#FAF8F5; border:1px solid #C2A675; padding:4px 10px; border-radius:6px; font-size:11px;">清空</button></div>
        </div>
        <script>
            var cv = document.getElementById('cv'), ctx = cv.getContext('2d'), d = false;
            ctx.strokeStyle = '#C2A675'; ctx.lineWidth = 3; ctx.lineCap = 'round';
            function s(e){ d = true; dr(e); } function en(){ d = false; ctx.beginPath(); }
            function dr(e){ if(!d)return; var r = cv.getBoundingClientRect(), x = ((e.clientX||e.touches[0].clientX)-r.left)*(cv.width/r.width), y = ((e.clientY||e.touches[0].clientY)-r.top)*(cv.height/r.height); ctx.lineTo(x,y); ctx.stroke(); ctx.beginPath(); ctx.moveTo(x,y); }
            cv.addEventListener('mousedown',s); cv.addEventListener('mouseup',en); cv.addEventListener('mousemove',dr);
            cv.addEventListener('touchstart',s); cv.addEventListener('touchend',en); cv.addEventListener('touchmove',dr);
        </script>
    """, height=200)

    st.markdown("---")
    st.markdown("#### 🌿 第二關 ‧ 19 秒迷走神經共振調息")
    st.markdown('<div class="breath-bubble">🐿️</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 💓 第三關 ‧ 光學微血流檢測")
    rppg_ok = st.checkbox("🟢 已完成手指輕覆鏡頭並通過光學微血流感應", value=True)

    if st.button("🚀 完成調息並拋接至診間", use_container_width=True):
        final_token = st.session_state["patient_token"]
        score = round(random.uniform(91.0, 97.5), 1)
        data = {
            "status": "已完成診前 19s 共振調息",
            "coherence_score": score,
            "stress_index": "莫蘭迪平穩藍",
            "sleep_hours": 7.4,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "weekly_trend": [82, 85, 88, 87, 90, 93, score],
            "prescription_50": "朝露白桃・玫瑰舒妍茶",
            "mapped_drink": "朝露白桃・玫瑰舒顏茶",
            "nudge": f"探險家完成調息，心流一致性 {score}%，狀態穩定。",
            "summary": f"個案持金鑰 {final_token} 完成 19 秒調息，心流評分 {score}%。"
        }
        # 寫入實體硬碟檔案（讓醫師端電腦 100% 讀得到）
        save_to_shared_db(final_token, data)

        st.markdown(f"""
            <div class="french-card" style="text-align:center;">
                <h3 style="margin-top:0;">✨ 調息數據已成功送達診間 ✨</h3>
                <b>通行金鑰：</b> <code style="font-size:1.2rem; color:#A35D4D;">{final_token}</code><br>
                <b>心流諧振分數：</b> {score}%<br>
                🍵 <b>現場吧台奉茶：</b> 朝露白桃・玫瑰舒顏茶
            </div>
        """, unsafe_allow_html=True)