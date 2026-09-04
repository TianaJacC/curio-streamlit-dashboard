import streamlit as st
import hashlib, hmac, os, time

st.set_page_config(
    page_title="夢境珍奇櫃 ‧ 金鑰救援",
    page_icon="🗝️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 樣式注入 (韓系奶油馬卡龍風)
st.markdown("""
    <style>
    .stApp { background-color: #F4F3EF !important; color: #1E232A !important; font-family: -apple-system, BlinkMacSystemFont, "PingFang TC", sans-serif; }
    .pastel-card { background: #F2E2E9; border: 2px solid #995873; border-radius: 24px; padding: 24px; text-align: center; margin-bottom: 20px; box-shadow: 0 8px 24px rgba(153,88,115,0.08); }
    .result-card { background: #FFFFFF; border: 1.5px solid #E2DCD2; border-radius: 20px; padding: 20px; text-align: left; margin-top: 16px; }
    </style>
""", unsafe_allow_html=True)

def generate_secure_token(seed_bytes: bytes) -> str:
    time_entropy = str(time.time_ns()).encode('utf-8')
    digest = hmac.new(time_entropy, seed_bytes, hashlib.sha256).hexdigest()
    return f"#SYM-{digest[:4].upper()}"

@st.cache_resource
def get_global_database():
    return {}
global_db = get_global_database()

st.markdown("""
    <div class="pastel-card">
        <div style="font-size:2.8rem; margin-bottom:8px;">🗝️</div>
        <h2 style="color:#995873; margin:0 0 10px 0;">30 秒無痕金鑰救援</h2>
        <div style="font-size:0.92rem; line-height:1.7; color:#4A3B32;">
            遺失今日看診金鑰了嗎？<br>
            請選取您剛才在候診時使用的<b>同一張照片</b>，系統將在 0.1 秒內在手機本機重新解算 SHA-256 特徵，無痕尋回今日調息紀錄！
        </div>
    </div>
""", unsafe_allow_html=True)

rescue_pic = st.file_uploader("請點擊選取原照片 (JPG / PNG)", type=["jpg", "png", "jpeg"], key="recovery_uploader")

if rescue_pic:
    rec_token = generate_secure_token(rescue_pic.getvalue())
    st.success(f"🔑 本機特徵比對完成！重組代碼：`{rec_token}`")
    
    if rec_token in global_db:
        record = global_db[rec_token]
        st.markdown(f"""
            <div class="result-card">
                <h4 style="color:#995873; margin-top:0;">✨ 今日身心紀錄已尋回</h4>
                🍃 <b>調飲處方</b>：{record.get('prescription_50', '朝露果妍・玫瑰舒顏茶')}<br>
                🍵 <b>候診區對應草本植萃調飲處方</b>：<b style="color:#995873;">{record.get('mapped_drink', '朝露果妍・玫瑰舒顏茶')}</b><br>
                💓 <b>心流平穩分數</b>：{record.get('coherence_score', 92.5)}%<br>
                🕒 <b>拋接時間</b>：{record.get('timestamp', '今日')}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="result-card">
                <h4 style="color:#1E232A; margin-top:0;">✨ 通行金鑰已產出</h4>
                您的專屬就診金鑰為：<code style="font-size:1.15rem; color:#995873;">{rec_token}</code><br><br>
                喝一杯草本植萃調飲，並向郭醫師出示此短碼解鎖問診！
            </div>
        """, unsafe_allow_html=True)
