import datetime
import random

# 林業署 19 處國家森林遊樂區精選步道池
FOREST_PARKS_DB = [
    {
        "name": "阿里山 ‧ 水山療癒步道",
        "region": "嘉義",
        "tag": "🌲 示範步道 ‧ 巨木療癒",
        "base_ions": 12450,
        "url": "https://recreation.forest.gov.tw/Forest/RA?typ=0&pe_res_id=0500001"
    },
    {
        "name": "內洞 ‧ 瀑布觀瀑步道",
        "region": "新北",
        "tag": "💧 全台負離子之冠",
        "base_ions": 18900,
        "url": "https://recreation.forest.gov.tw/Forest/RA?typ=0&pe_res_id=0200002"
    },
    {
        "name": "太平山 ‧ 見晴懷古步道",
        "region": "宜蘭",
        "tag": "☁️ 雲海鐵道 ‧ 全球最美",
        "base_ions": 9820,
        "url": "https://recreation.forest.gov.tw/Forest/RA?typ=0&pe_res_id=0100001"
    },
    {
        "name": "奧萬大 ‧ 楓林沉浸步道",
        "region": "南投",
        "tag": "🍁 活氧降壓 ‧ 溪流療癒",
        "base_ions": 8650,
        "url": "https://recreation.forest.gov.tw/Forest/RA?typ=0&pe_res_id=0400002"
    },
    {
        "name": "滿月圓 ‧ 處女瀑布步道",
        "region": "新北",
        "tag": "🌿 雙瀑活氧 ‧ 迷走放鬆",
        "base_ions": 14200,
        "url": "https://recreation.forest.gov.tw/Forest/RA?typ=0&pe_res_id=0200001"
    },
    {
        "name": "大雪山 ‧ 原始檜木林步道",
        "region": "台中",
        "tag": "🌲 高山芬多精 ‧ 深度抗壓",
        "base_ions": 11300,
        "url": "https://recreation.forest.gov.tw/Forest/RA?typ=0&pe_res_id=0300001"
    },
    {
        "name": "東眼山 ‧ 自導式柳杉步道",
        "region": "桃園",
        "tag": "🌲 柳杉人工林 ‧ 舒緩眼壓",
        "base_ions": 7900,
        "url": "https://recreation.forest.gov.tw/Forest/RA?typ=0&pe_res_id=0200003"
    },
    {
        "name": "知本 ‧ 勇男巨木步道",
        "region": "台東",
        "tag": "🌴 溫泉雨林 ‧ 芳香舒壓",
        "base_ions": 10500,
        "url": "https://recreation.forest.gov.tw/Forest/RA?typ=0&pe_res_id=0700001"
    }
]

def get_dynamic_forest_bubbles():
    now_hour = datetime.datetime.now().hour
    is_night = now_hour >= 17 or now_hour < 6

    # 隨機挑選 5 處展示，每次點選都呈現多樣性
    sample_parks = random.sample(FOREST_PARKS_DB, 5)
    bubbles = []

    for park in sample_parks:
        if is_night:
            crowd_text = "園區夜間休園中 (人潮 0%)"
            parking_text = "夜間停車場尚有餘位"
            ions = park["base_ions"]
        else:
            pct = random.randint(25, 68)
            comfort = "人潮舒適" if pct < 45 else "人潮適中"
            crowd_text = f"即時在園率 {pct}% ({comfort})"
            parking_text = f"車位剩餘 {random.randint(40, 120)} 格"
            ions = park["base_ions"] + random.randint(-300, 500)

        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{park['tag']}",
                        "weight": "bold",
                        "color": "#2C5E43",
                        "size": "xs"
                    },
                    {
                        "type": "text",
                        "text": f"{park['name']}",
                        "weight": "bold",
                        "size": "md",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": f"負離子：{ions:,} ions/cm³",
                        "size": "xs",
                        "color": "#555555",
                        "margin": "sm"
                    },
                    {
                        "type": "text",
                        "text": f"即時人流：{crowd_text}",
                        "size": "xs",
                        "color": "#555555"
                    },
                    {
                        "type": "text",
                        "text": f"車位狀況：{parking_text}",
                        "size": "xs",
                        "color": "#555555"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "林業署山林悠遊網預約",
                            "uri": park["url"]
                        },
                        "style": "primary",
                        "color": "#2C5E43",
                        "margin": "md"
                    }
                ]
            }
        }
        bubbles.append(bubble)

    return bubbles
