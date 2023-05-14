from flask import Flask, request, abort

from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi('Wg7R/Gpo7g7TLAZXhNgHu7mw+ADzNTBk4DYc3/Qnr53ahMBl4WR9IzaW+2w8Tk8TcRbHF0y+9SahfLTUxjj55QugXurAip/5ExuIERSc5fb2qz03PCVLKPuTNTmu7W/ENZ310wepUZZihjrmi9c2LQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0f91a5c0a4c8b3f02693b5d35fa17877')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    app.run()
