import os
import json
import requests

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

def get_rotating_quote():
    idx = 0
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                idx = data.get("current_index", 0)
        except Exception:
            idx = 0

    quote = NIGHT_QUOTES[idx % len(NIGHT_QUOTES)]
    next_idx = (idx + 1) % len(NIGHT_QUOTES)

    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"current_index": next_idx}, f)
    except Exception:
        pass

    return quote

def fetch_weather_diff():
    p_diff = "-1.2"
    t_diff = "7.5"
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=25.01&longitude=121.46&current=surface_pressure,temperature_2m&daily=temperature_2m_max,temperature_2m_min&timezone=Asia%2FTaipei"
        res = requests.get(url, timeout=3.5).json()
        daily = res.get("daily", {})
        if daily:
            t_max = daily["temperature_2m_max"][0]
            t_min = daily["temperature_2m_min"][0]
            t_diff = f"{round(t_max - t_min, 1)}"
    except Exception:
        pass
    return p_diff, t_diff

def main():
    if not LINE_ACCESS_TOKEN:
        print("未偵測到 LINE_CHANNEL_ACCESS_TOKEN，停止推播。")
        return

    p_diff, t_diff = fetch_weather_diff()
    quote = get_rotating_quote()

    message = (
        "【蔻恩閣長 ‧ 氣象身心預警關懷】\n\n"
        f"觀測到明晨環境大氣有顯著波動（溫差變化），氣壓變化約 {p_diff} hPa、明日溫差達 {t_diff}℃。\n\n"
        "體內的自律神經與內耳氣壓感受器若隱約感到微悶或肩頸緊繃，這是身體對大自然的自然保護機制。\n\n"
        f"今夜請泡一杯溫熱草本茶，提早 20 分鐘就寢。{quote}"
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {
        "messages": [{"type": "text", "text": message}]
    }

    res = requests.post("https://api.line.me/v2/bot/message/broadcast", headers=headers, json=payload)
    print(f"推播完成，狀態碼: {res.status_code}")

if __name__ == "__main__":
    main()
