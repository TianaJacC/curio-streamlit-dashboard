import os
import requests
from flask import Flask, request, abort

app = Flask(__name__)
LINE_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

@app.route("/callback", methods=["POST"])
def callback():
    body = request.get_json()
    events = body.get("events", [])
    
    for event in events:
        # 當病患傳送文字訊息
        if event.get("type") == "message" and event["message"].get("type") == "text":
            user_text = event["message"]["text"].strip()
            reply_token = event["replyToken"]
            
            # 觸發詞判定：病患點擊圖文選單第 4 格「步道指南」
            if user_text == "步道指南":
                data = get_forest_live_data() # 調用林業署資料函式
                flex_payload = build_forest_carousel_message(data)
                
                # 發送回覆
                reply_url = "https://api.line.me/v2/bot/message/reply"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
                }
                payload = {
                    "replyToken": reply_token,
                    "messages": [flex_payload]
                }
                requests.post(reply_url, headers=headers, json=payload)
                
    return "OK", 200

if __name__ == "__main__":
    app.run(port=8000)
