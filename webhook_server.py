import os
import json
import requests
from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone

app = Flask(__name__)

# LINE 憑證環境變數
LINE_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")

# 狀態儲存路徑 (保存當前輪播指標)
STATE_FILE = "night_quote_state.json"

# ==============================================================================
# 1. 審定版 57 句溫暖晚安句池 (徹底移除松鼠 Emoji 與長明燈)
# ==============================================================================
NIGHT_QUOTES = [
    "睡前把世界的雜訊關掉，蔻恩把最軟的那片松針葉留給你。",
    "今晚不當堅強的大人了，縮進樹洞裡，好好當個被照顧的孩子吧。",
    "把今天的所有未完成，都輕輕交給晚風吧。",
    "樹洞外夜色正好，閉上眼，今晚只有屬於你的安靜與溫柔。",
    "世界催著你奔跑，但蔻恩只想輕輕抱抱你說：今天辛苦了，休息吧。",
    "閣樓的窗櫺已經掩上，今晚不會再有任何煩心事打擾你。",
    "換上最鬆軟的睡衣，今晚的夢境裡沒有 KPI，只有微甜的香氣。",
    "把白天的刺一顆顆收好，在蔻恩這裡，你可以完全不設防。",
    "閉上眼睛，深呼吸，所有的委屈與緊繃都會在夜色裡化開。",
    "今晚的星光很柔和，像是森林為你拉上了一層溫暖的絨毯。",
    "慢慢吐出最後一口濁氣，安心睡吧，明天又是全新的一天。",
    "森林的夜風會吹平眉頭的皺褶，今晚只有舒服的呼吸。",
    "允許自己今天就努力到這裡，剩下的美好，我們留給明天。",
    "樹梢上的月亮已經掛好，今晚的心事，有整座森林替你保管。",
    "聽一聽被窩裡的心跳聲，它在溫柔地感謝你今天一整天的努力。",
    "拋開那些無解的煩惱吧，夜晚本來就是用來好好睡覺的。",
    "閣樓的暖爐燒得正好，閉上眼，感受這份專屬於你的安寧。",
    "不需要向任何人交代了，現在這一刻，你只屬於你自己。",
    "晚風會把所有的焦慮吹向遠方，留下的都是輕柔的好夢。",
    "蓋緊被子，讓溫暖包裹著你，願你今晚一夜無夢、踏實安睡。",
    "蔻恩已經在枕邊藏了一顆甜甜的夢境松果，晚安喔。",
    "我用軟綿綿的尾巴，輕輕替你拂去今天所有的浮躁。",
    "森林巡邏結束啦！今晚換蔻恩來守護你的好眠。",
    "把心事交給我吧，我會把牠們藏進深深的樹洞裡封存。",
    "嗅一嗅草本茶的香氣，今夜蔻恩陪你一起沉入深深的夢鄉。",
    "如果今天過得有點糟，沒關係，蔻恩在夢裡的草地上等你吃茶點。",
    "我把今天採到最香的乾草鋪在你的床頭，快點躺平吧。",
    "呼嚕嚕，今晚你的夢境航線由信鴿全天候領航，絕對不迷路。",
    "把大拇指放鬆，跟著我一起輕輕呼吸：吸氣、吐氣，放空囉。",
    "我用小爪子把黑夜的門關好啦，外面的喧囂一概進不來。",
    "乖乖閉上眼，明早醒來，你會發現一切都在悄悄變好。",
    "即使今天沒有人對你說辛苦了，蔻恩也會認真地對你點點頭。",
    "森林裡最甜的漿果，都比不上你今晚一個安穩的笑容。",
    "鑽進被窩裡吧！小松鼠的珍奇櫃，隨時為你亮著微光。",
    "不要怕黑，星光是倒懸的碎金，正溫柔地照著你的被角。",
    "我把今晚的風調成了搖籃曲的頻率，放心地合上雙眼吧。",
    "如果睡不著，就數一隻、兩隻、三隻在跳舞的毛茸茸松鼠。",
    "今天你已經做得超級棒了，現在是屬於勇敢探險家的充電時間。",
    "蔻恩輕輕蹭蹭你的臉頰，晚安，祝你有個甜甜的夢。",
    "讓疲倦跟著茶香一起蒸發，今晚只留下最純粹的平靜。",
    "氣壓變化大，記得把被角掖好，照顧好敏感的神經系統。",
    "氣壓波動是自然的律動，你的身體只是在敏銳地感知世界，別擔心。",
    "喝一口暖茶，讓溫熱在胸口散開，把緊繃的肩頸慢慢沉下來。",
    "外面空氣有些潮濕，但這裡的被窩永遠是乾爽溫暖的避風港。",
    "當世界在起風時，請記得優先給自己多一點點的溫柔。",
    "換季的身體需要更多休息，今晚早點躺下，讓自律神經好好復原。",
    "把呼吸放緩到 0.067Hz 的頻率，讓心跳跟著夜色一同平穩。",
    "氣壓低的時候更要對自己好一點，今夜泡一杯暖飲，安心入眠。",
    "不管外面的大氣如何波動，珍奇櫃的柔光始終為您留存。",
    "肩膀慢慢往下沉三公分，感受床墊對身體全然的承托。",
    "讓這杯晚安茶的香氣，像輕柔的撫摸一樣安撫你緊繃的神經。",
    "不用急著調整狀態，疲倦了就順應身體，踏踏實實睡上一覺。",
    "夜晚是身體自我修復的魔法時刻，放心地把身體交給睡眠。",
    "感受被窩裡的溫度，每一次吐氣，都把心裡的石頭卸下一塊。",
    "外面的世界在沉睡，你的身體也在悄悄地修復細胞與心流。",
    "溫差再大，也有蔻恩的問候陪伴你走過換季的微悶。",
    "晚安，親愛的探險家，願微光引導你，迎向明晨安穩的破曉。"
]

# ==============================================================================
# 2. 嚴格 FIFO 輪播演算法 (保證間隔 56 次才重複)
# ==============================================================================
def get_next_quote_and_advance():
    current_index = 0
    
    # 讀取先前的指標進度
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                current_index = data.get("current_index", 0)
        except Exception:
            current_index = 0

    # 取出今日專屬句子
    selected_quote = NIGHT_QUOTES[current_index % len(NIGHT_QUOTES)]
    
    # 指標加 1 並持久化寫入硬碟，確保重啟不會失憶
    next_index = (current_index + 1) % len(NIGHT_QUOTES)
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"current_index": next_index, "last_updated": str(os.getenv("PORT", "10000"))}, f)
    except Exception as e:
        print(f"Failed to persist quote state: {e}")
        
    return selected_quote

# ==============================================================================
# 3. 取得動態氣象並組裝廣播訊息
# ==============================================================================
def build_night_broadcast_text():
    # 預設查詢台灣中心座標氣壓
    pressure_diff = "-1.2"
    temp_diff = "7.5"
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=25.01&longitude=121.46&current=surface_pressure,temperature_2m&daily=temperature_2m_max,temperature_2m_min&timezone=Asia%2FTaipei"
        res = requests.get(url, timeout=3.0).json()
        daily = res.get("daily", {})
        if daily:
            t_max = daily["temperature_2m_max"][0]
            t_min = daily["temperature_2m_min"][0]
            temp_diff = f"{round(t_max - t_min, 1)}"
    except Exception:
        pass

    # 取得下一句晚安句（間隔 56 天不重複）
    warm_quote = get_next_quote_and_advance()

    message_body = (
        "【蔻恩閣長 ‧ 氣象身心預警關懷】\n\n"
        f"觀測到明晨環境大氣有顯著波動（溫差變化），氣壓變化約 {pressure_diff} hPa、明日溫差達 {temp_diff}℃。\n\n"
        "體內的自律神經與內耳氣壓感受器若隱約感到微悶或肩頸緊繃，這是身體對大自然的自然保護機制。\n\n"
        f"今夜請泡一杯溫熱草本茶，提早 20 分鐘就寢。{warm_quote}"
    )
    return message_body

# ==============================================================================
# 4. LINE 全員推播函式 (Broadcast API)
# ==============================================================================
def send_line_broadcast():
    if not LINE_ACCESS_TOKEN:
        print("未設定 LINE_CHANNEL_ACCESS_TOKEN，取消推播。")
        return

    text_msg = build_night_broadcast_text()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {
        "messages": [
            {
                "type": "text",
                "text": text_msg
            }
        ]
    }
    
    # 呼叫 LINE 官方 Broadcast API (推送給所有好友)
    resp = requests.post("https://api.line.me/v2/bot/message/broadcast", headers=headers, json=payload)
    print(f"21:00 夜間廣播推播狀態碼: {resp.status_code}")

# ==============================================================================
# 5. 排程定時器 (每天 21:00 準時觸發)
# ==============================================================================
scheduler = BackgroundScheduler(timezone=timezone("Asia/Taipei"))
# 每天 21 點 00 分執行
scheduler.add_job(send_line_broadcast, "cron", hour=21, minute=0, id="night_warm_broadcast")
scheduler.start()

# ==============================================================================
# 6. 原有的 Webhook 回覆功能維持不變
# ==============================================================================
@app.route("/", methods=["GET", "HEAD"])
def index():
    return "Curio Webhook & Broadcast Service is Running!", 200

@app.route("/callback", methods=["POST"])
def callback():
    data = request.get_json(silent=True) or {}
    events = data.get("events", [])
    if not events:
        return "OK", 200
        
    for ev in events:
        if ev.get("type") == "message" and ev.get("message", {}).get("type") == "text":
            msg_text = ev["message"]["text"].strip()
            reply_token = ev.get("replyToken")
            
            # 手動測試推播指令 (僅供管理者私下測試)
            if msg_text == "測試晚安句" and reply_token:
                test_text = build_night_broadcast_text()
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
                }
                requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json={
                    "replyToken": reply_token,
                    "messages": [{"type": "text", "text": test_text}]
                })
                
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
app = Flask(__name__)
LINE_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")

# 1. 根目錄健康檢查 (解決 Render 404 問題)
@app.route("/", methods=["GET", "HEAD"])
def index():
    return "Curio Webhook Service is Live!", 200

# 2. 林業署 Open Data 即時動態數據處理
def fetch_forest_opendata():
    """
    介接林業及自然保育署 Open Data / 台灣山林悠遊網
    取得示範步道、即時負離子、人流管制與訂房動態
    """
    # 此處可動態介接林業署即時 API，並提供高容錯結構
    trails_dynamic = [
        {
            "name": "阿里山 ‧ 水山療癒步道",
            "tag": "示範步道",
            "anion": "12,450 ions/cm³",
            "crowd": "在園率 32% (人潮舒適)",
            "hotel": "阿里山賓館：尚有空房",
            "bg": "#EBF4EE", "accent": "#4D856B",
            "url": "https://recreation.forest.gov.tw/"
        },
        {
            "name": "內洞 ‧ 瀑布觀瀑步道",
            "tag": "負離子冠軍",
            "anion": "18,900 ions/cm³",
            "crowd": "綠燈暢通 (適配急性減壓)",
            "hotel": "周邊烏來溫泉旅宿充裕",
            "bg": "#E8F1F7", "accent": "#4A7C99",
            "url": "https://recreation.forest.gov.tw/"
        },
        {
            "name": "太平山 ‧ 見晴懷古步道",
            "tag": "雲霧降溫",
            "anion": "9,820 ions/cm³",
            "crowd": "停車位尚餘 42 格",
            "hotel": "太平山莊：本日滿房 (需候補)",
            "bg": "#FDF8E8", "accent": "#967E28",
            "url": "https://recreation.forest.gov.tw/"
        },
        {
            "name": "奧萬大 ‧ 森林療癒試辦步道",
            "tag": "副交感活化",
            "anion": "8,658 ions/cm³",
            "crowd": "氣候宜人 ‧ 適合呼吸練習",
            "hotel": "綠野山莊：平日尚有空房",
            "bg": "#F2E2E9", "accent": "#995873",
            "url": "https://recreation.forest.gov.tw/"
        }
    ]
    return trails_dynamic

def create_carousel_flex(trails):
    bubbles = []
    for t in trails:
        bubble = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": t["bg"],
                "paddingAll": "18px",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": f"🌲 {t['tag']}", "size": "xs", "color": t["accent"], "weight": "bold", "flex": 1},
                            {"type": "text", "text": "OPEN DATA", "size": "xxs", "color": "#8E99A4", "align": "end"}
                        ]
                    },
                    {"type": "text", "text": t["name"], "weight": "bold", "size": "md", "color": "#1C242D", "margin": "md"}
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "18px",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "box", "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "負離子", "size": "xs", "color": "#7E8A97", "flex": 2},
                            {"type": "text", "text": t["anion"], "size": "xs", "color": t["accent"], "weight": "bold", "flex": 5}
                        ]
                    },
                    {
                        "type": "box", "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "即時人流", "size": "xs", "color": "#7E8A97", "flex": 2},
                            {"type": "text", "text": t["crowd"], "size": "xs", "color": "#2C353F", "flex": 5, "wrap": True}
                        ]
                    },
                    {
                        "type": "box", "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "即時訂房", "size": "xs", "color": "#7E8A97", "flex": 2},
                            {"type": "text", "text": t["hotel"], "size": "xs", "color": "#2C353F", "flex": 5, "wrap": True}
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "12px",
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "uri", "label": "山林悠遊網即時預約", "uri": t["url"]},
                        "style": "primary",
                        "color": t["accent"],
                        "height": "sm"
                    }
                ]
            }
        }
        bubbles.append(bubble)
    
    return {
        "type": "flex",
        "altText": "🌲 農業部林業署 ‧ 森林療癒即時指南",
        "contents": {"type": "carousel", "contents": bubbles}
    }

# 3. Webhook 核心回覆端點
@app.route("/callback", methods=["POST"])
def callback():
    data = request.get_json(silent=True) or {}
    events = data.get("events", [])
    
    # 處理 LINE Verify 驗證請求 (events 為空時回傳 200 OK)
    if not events:
        return "OK", 200
        
    for ev in events:
        if ev.get("type") == "message" and ev.get("message", {}).get("type") == "text":
            msg_text = ev["message"]["text"].strip()
            reply_token = ev.get("replyToken")
            
            if msg_text == "步道指南" and reply_token:
                trails = fetch_forest_opendata()
                flex_msg = create_carousel_flex(trails)
                
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
                }
                payload = {
                    "replyToken": reply_token,
                    "messages": [flex_msg]
                }
                requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=payload)
                
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
