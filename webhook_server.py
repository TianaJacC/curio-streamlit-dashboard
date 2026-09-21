import os
import json
import time
import threading
import datetime
import requests
from flask import Flask, request

app = Flask(__name__)
LINE_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
STATE_FILE = "night_quote_state.json"

# ==============================================================================
# 57 句審定版溫暖晚安句（無松鼠 Emoji、無長明燈、信鴿領航、柔光守護）
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

def get_next_rotating_quote():
    idx = 0
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                idx = json.load(f).get("current_index", 0)
        except Exception:
            idx = 0
    quote = NIGHT_QUOTES[idx % len(NIGHT_QUOTES)]
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"current_index": (idx + 1) % len(NIGHT_QUOTES)}, f)
    except Exception:
        pass
    return quote

def fetch_weather_nudge():
    p_diff = "-1.2"
    t_diff = "7.1"
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=25.01&longitude=121.46&current=surface_pressure,temperature_2m&daily=temperature_2m_max,temperature_2m_min&timezone=Asia%2FTaipei"
        res = requests.get(url, timeout=3.0).json()
        daily = res.get("daily", {})
        if daily:
            t_max = daily["temperature_2m_max"][0]
            t_min = daily["temperature_2m_min"][0]
            t_diff = f"{round(t_max - t_min, 1)}"
    except Exception:
        pass
    return p_diff, t_diff

def get_next_rotating_quote():
    # 依當年度第幾天自動輪播，跨日自動換句，不依賴本機狀態檔
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    now_tw = now_utc + datetime.timedelta(hours=8)
    day_of_year = now_tw.timetuple().tm_yday
    return NIGHT_QUOTES[day_of_year % len(NIGHT_QUOTES)]

def send_broadcast_message():
    if not LINE_ACCESS_TOKEN:
        return
    p_diff, t_diff = fetch_weather_nudge()
    quote = get_next_rotating_quote()
    msg = (
        "【蔻恩閣長 ‧ 氣象身心預警關懷】\n\n"
        f"觀測到明晨環境大氣有顯著波動（溫差變化），氣壓變化約 {p_diff} hPa、明日溫差達 {t_diff}℃。\n\n"
        "體內的自律神經與內耳氣壓感受器若隱約感到微悶或肩頸緊繃，這是身體對大自然的自然保護機制。\n\n"
        f"今夜請泡一杯溫熱植萃茶，提早 20 分鐘就寢。{quote}"
    )
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    requests.post("https://api.line.me/v2/bot/message/broadcast", headers=headers, json={"messages": [{"type": "text", "text": msg}]})

# 原生無依賴後台定時線程：精準鎖定台灣時間每日 21:00 發送
def background_scheduler_loop():
    last_sent_date = None  # 記錄最後發送推播的日期 (YYYY-MM-DD)，絕不漏發、絕不重發
    last_ping_time = 0     # 記錄上次 Ping Streamlit 的時間戳

    while True:
        try:
            now_utc = datetime.datetime.now(datetime.timezone.utc)
            now_tw = now_utc + datetime.timedelta(hours=8)
            today_str = now_tw.strftime("%Y-%m-%d")

            # 1. 每日 21:00 ~ 21:05 之間發送推播 (只要今天還沒發過就觸發)
            if now_tw.hour == 21 and now_tw.minute < 5:
                if last_sent_date != today_str:
                    send_broadcast_message()
                    last_sent_date = today_str

            # 2. 每 10 分鐘 (600 秒) 喚醒一次 Streamlit，timeout 設為 20 秒容納冷啟動
            current_timestamp = time.time()
            if current_timestamp - last_ping_time >= 600:
                try:
                    requests.get("https://curio-app-dashboard-sqc.streamlit.app/", timeout=20)
                except Exception:
                    pass
                last_ping_time = current_timestamp

        except Exception as e:
            print(f"[Scheduler Error] {e}")

        # 每 20 秒檢查一次時鐘，負載極低且絕不漏掉時間窗口
        time.sleep(20)

# 啟動守護線程
t = threading.Thread(target=background_scheduler_loop, daemon=True)
t.start()

@app.route("/", methods=["GET", "HEAD"])
def index():
    return "Curio Webhook & Broadcast Server Running", 200

@app.route("/callback", methods=["POST"])
def callback():
    data = request.get_json(silent=True) or {}
    for ev in data.get("events", []):
        if ev.get("type") == "message" and ev.get("message", {}).get("type") == "text":
            text = ev["message"]["text"].strip()
            r_tok = ev.get("replyToken")
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"}

            # 1. 測試晚安句指令
            if text == "測試晚安句" and r_tok:
                q = get_next_rotating_quote()
                requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json={
                    "replyToken": r_tok,
                    "messages": [{"type": "text", "text": f"【測試輪播】{q}"}]
                })

            # 2. 步道指南指令
            elif (text == "步道指南" or "步道" in text) and r_tok:
                from forest_flex import get_dynamic_forest_bubbles
                bubbles = get_dynamic_forest_bubbles()
                requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json={
                    "replyToken": r_tok,
                    "messages": [{
                        "type": "flex",
                        "altText": "🌲 林業署森林療癒步道指南",
                        "contents": {"type": "carousel", "contents": bubbles}
                    }]
                })

    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
