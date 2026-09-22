import streamlit as st
import hashlib
import json
import os

st.set_page_config(page_title="金鑰救援 ‧ 夢境珍奇櫃", page_icon="🗝️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0A110D !important; font-family: -apple-system, sans-serif; }
    p, label, span, h2, h3 { color: #FFFFFF !important; }
    div[data-testid="stFileUploader"] {
        background-color: #FFFFFF !important;
        border: 2px dashed #FCBF05 !important;
        border-radius: 16px !important;
        padding: 16px !important;
    }
    div[data-testid="stFileUploader"] * { color: #000000 !important; font-weight: bold !important; }
    .stButton>button { 
        background: linear-gradient(135deg, #FCBF05 0%, #C2A675 100%) !important; 
        color: #000000 !important; 
        font-weight: 900 !important; 
        border-radius: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="background:#142017; border:2px solid #FCBF05; border-radius:18px; padding:22px; text-align:center; margin-bottom:16px;">
        <div style="font-size:2.6rem; margin-bottom:6px;">🗝️</div>
        <h3 style="color:#FCBF05 !important; font-size:1.3rem; margin-top:0; font-weight:bold;">30 秒無痕金鑰救援 (Key-Stitching)</h3>
        <p style="color:#FFFFFF !important; font-size:0.92rem; line-height:1.6;">
            遺失今日通行短碼了嗎？請選取您剛才在候診時上傳的<b>同一張相片</b>，系統將在手機本機重新解算特徵，尋回今日生活處方！
        </p>
    </div>
""", unsafe_allow_html=True)

SHARED_DB_FILE = os.path.join("system_logs", "active_sessions.json")

def read_token(token):
    if os.path.exists(SHARED_DB_FILE):
        try:
            with open(SHARED_DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get(token)
        except Exception:
            pass
    return None

rescue_file = st.file_uploader("選取剛才使用的相片 (JPG / PNG)", type=["jpg", "png", "jpeg"], key="rec_up")
if rescue_file:
    recovered_tok = f"#SYM-{hashlib.sha256(rescue_file.getvalue()).hexdigest()[:4].upper()}"
    st.success(f"🔑 比對完成！您的通行代碼：`{recovered_tok}`")
    saved = read_token(recovered_tok)
    if saved:
        st.markdown(f"""
            <div style="background:#0B120E; border:1.5px solid #FCBF05; border-radius:14px; padding:16px; color:#FFFFFF !important; line-height:1.8;">
                🍃 <b>生活處方：</b> <span style="color:#FCBF05 !important;">{saved.get('prescription_50')}</span><br>
                🍵 <b>現場備有調飲：</b> <span style="color:#FFB085 !important; font-weight:bold;">{saved.get('mapped_drink')}</span><br>
                💓 <b>心流一致性：</b> {saved.get('coherence_score')}%<br>
                🕒 <b>拋接時間：</b> {saved.get('timestamp')}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info(f"代碼 `{recovered_tok}` 已解算。請出示此代碼至現場候診區領取調飲！")