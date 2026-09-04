import os
import requests
import datetime

# 板橋 / 新北市中心經緯度
LAT = 25.0118
LON = 121.4658

# LINE Messaging API 設定 (從 LINE Developers Console 取得)
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "YOUR_ACCESS_TOKEN")

def check_weather_and_nudge():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=surface_pressure,temperature_2m&timezone=Asia%2FTaipei"
    resp = requests.get(url).json()
    
    hourly = resp.get("hourly", {})
    pressures = hourly.get("surface_pressure", [])
    temps = hourly.get("temperature_2m", [])
    
    # 取得當前小時 (約 20:00) 與未來 24 小時數據
    current_p = pressures[20]
    next_24h_p = pressures[20:44]
    min_future_p = min(next_24h_p)
    delta_p = min_future_p - current_p  # 氣壓變化量
    
    # 溫差計算 (明日最高溫與最低溫之差)
    tomorrow_temps = temps[24:48]
    temp_diff = max(tomorrow_temps) - min(tomorrow_temps)
    
    # 觸發條件判定
    condition_1 = delta_p <= -4.0  # 氣壓驟降 >= 4.0 hPa
    condition_2 = temp_diff >= 7.0  # 明日溫差 >= 7度
    
    if condition_1 or condition_2:
        reason = "氣壓驟降" if condition_1 else "溫差劇烈變化"
        send_silent_nudge(delta_p, temp_diff, reason)

def send_silent_nudge(delta_p, temp_diff, reason):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    
    message_text = (
        "🐿️【蔻恩閣長 ‧ 氣象身心預警關懷】\n\n"
        f"觀測到明晨環境大氣有顯著波動（{reason}），氣壓變化約 {delta_p:.1f} hPa、明日溫差達 {temp_diff:.1f}°C。\n\n"
        "體內的自律神經與內耳氣壓感受器若隱約感到微悶或肩頸緊繃，這是身體對大自然的自然保護機制。\n\n"
        "今夜請泡一杯溫熱草本茶，提早 20 分鐘就寢。長明燈始終為您點亮。"
    )
    
    # notificationDisabled: True 代表無聲靜音推播，絕不打擾病患
    payload = {
        "messages": [{"type": "text", "text": message_text}],
        "notificationDisabled": True
    }
    
    # 對所有好友廣播 (Broadcast API)
    broadcast_url = "https://api.line.me/v2/bot/message/broadcast"
    requests.post(broadcast_url, headers=headers, json=payload)
    print(f"[{datetime.datetime.now()}] 劇烈天氣警報已發送！原因: {reason}")

if __name__ == "__main__":
    check_weather_and_nudge()
