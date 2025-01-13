from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, TextSendMessage

app = Flask(__name__)

# LINE Bot的Channel Access Token和Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = 'YOUR_CHANNEL_ACCESS_TOKEN'
LINE_CHANNEL_SECRET = 'YOUR_CHANNEL_SECRET'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # 獲取請求的簽名
    signature = request.headers['X-Line-Signature']

    # 獲取請求的body
    body = request.get_data(as_text=True)

    try:
        # 驗證簽名
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 回應用戶發送的訊息
    reply_token = event.reply_token
    user_message = event.message.text

    # 這裡可以根據用戶的訊息進行不同的回應
    response_message = f"您發送的訊息是: {user_message}"

    # 發送回應訊息
    line_bot_api.reply_message(reply_token, TextSendMessage(text=response_message))

if __name__ == "__main__":
    app.run(port=5000)