def build_forest_carousel_message(trails_data):
    """
    將林業署步道資料轉換為 LINE 韓系粉彩 Flex Message (Carousel 輪播)
    """
    bubbles = []
    
    # 輪播卡片的配色循環 (Powdered Pastels)
    colors = [
        {"bg": "#EBF4EE", "accent": "#4D856B", "tag": "示範場域"},  # 薄荷粉綠
        {"bg": "#E8F1F7", "accent": "#4A7C99", "tag": "負離子王"},  # 冰融澄藍
        {"bg": "#FDF8E8", "accent": "#967E28", "tag": "景觀雲霧"},  # 柔檸檬黃
    ]

    for idx, t in enumerate(trails_data):
        c = colors[idx % len(colors)]
        bubble = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["bg"],
                "paddingAll": "18px",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"🌲 {c['tag']}",
                                "size": "xs",
                                "color": c["accent"],
                                "weight": "bold",
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": "OPEN DATA",
                                "size": "xxs",
                                "color": "#8E99A4",
                                "align": "end"
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "text": t["name"],
                        "weight": "bold",
                        "size": "md",
                        "color": "#1C242D",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": t["type"],
                        "size": "xs",
                        "color": "#606B77",
                        "margin": "xs"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "18px",
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "負離子", "size": "xs", "color": "#7E8A97", "flex": 2},
                            {"type": "text", "text": t["anion"], "size": "xs", "color": c["accent"], "weight": "bold", "flex": 5}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "人潮路況", "size": "xs", "color": "#7E8A97", "flex": 2},
                            {"type": "text", "text": t["status"], "size": "xs", "color": "#2C353F", "flex": 5, "wrap": True}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "訂房現況", "size": "xs", "color": "#7E8A97", "flex": 2},
                            {"type": "text", "text": t["hotel"], "size": "xs", "color": "#2C353F", "flex": 5, "wrap": True}
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "14px",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "查看山林悠遊網即時路況",
                            "uri": t["link"]
                        },
                        "style": "primary",
                        "color": c["accent"],
                        "height": "sm"
                    }
                ]
            }
        }
        bubbles.append(bubble)

    flex_message = {
        "type": "flex",
        "altText": "🌲 農業部林業署 ‧ 森林療癒即時指南",
        "contents": {
            "type": "carousel",
            "contents": bubbles
        }
    }
    return flex_message
