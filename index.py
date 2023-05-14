from flask import Flask, request, abort

from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi('srFTsHK62OAvxrtPQxwkyYdXrS0ICYgrSgKarEpd5ayHlSMPY2TEP1KNbDMUm5bx4cDb7610wTfayRUG+ZXOkPrPt6zwIP5VrmGLJnqSvioWwxVL7m4g9Vr9OqNcr1ucsS2fxqWFCsajmWxfN32mTgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3422ef0232368541bcf7867e2f7f8443')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
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
