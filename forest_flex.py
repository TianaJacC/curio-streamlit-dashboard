import datetime
import random

def get_dynamic_forest_bubbles():
    now_hour = datetime.datetime.now().hour
    # 白天動態波動，夜間休眠
    if now_hour >= 17 or now_hour < 6:
        alishan_crowd = "園區夜間休眠 (人潮 0%)"
        alishan_parking = "夜間停車場尚有餘位"
        alishan_ions = 12450
        neidong_ions = 18900
    else:
        pct = random.randint(28, 65)
        alishan_crowd = f"在園率 {pct}% ({'人潮舒適' if pct < 45 else '人潮適中'})"
        alishan_parking = f"車位剩餘 {random.randint(35, 110)} 格"
        alishan_ions = 12000 + random.randint(100, 800)
        neidong_ions = 18500 + random.randint(100, 900)

    bubbles = [
        {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "🌲 示範步道 ‧ 即時更新", "weight": "bold", "color": "#2C5E43", "size": "xs"},
                    {"type": "text", "text": "阿里山 ‧ 水山療癒步道", "weight": "bold", "size": "md", "margin": "md"},
                    {"type": "text", "text": f"負離子：{alishan_ions:,} ions/cm³", "size": "xs", "color": "#555555", "margin": "sm"},
                    {"type": "text", "text": f"即時人流：{alishan_crowd}", "size": "xs", "color": "#555555"},
                    {"type": "text", "text": f"停車狀況：{alishan_parking}", "size": "xs", "color": "#555555"},
                    {"type": "button", "action": {"type": "uri", "label": "山林悠遊網即時預約", "uri": "https://recreation.forest.gov.tw/"}, "style": "primary", "color": "#2C5E43", "margin": "md"}
                ]
            }
        },
        {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "🌲 負離子冠軍 ‧ 即時更新", "weight": "bold", "color": "#2C5E43", "size": "xs"},
                    {"type": "text", "text": "內洞 ‧ 瀑布觀瀑步道", "weight": "bold", "size": "md", "margin": "md"},
                    {"type": "text", "text": f"負離子：{neidong_ions:,} ions/cm³", "size": "xs", "color": "#555555", "margin": "sm"},
                    {"type": "text", "text": "即時人流：綠燈暢行 (空氣優良)", "size": "xs", "color": "#555555"},
                    {"type": "button", "action": {"type": "uri", "label": "查詢步道動態", "uri": "https://recreation.forest.gov.tw/"}, "style": "primary", "color": "#2C5E43", "margin": "md"}
                ]
            }
        }
    ]
    return bubbles
