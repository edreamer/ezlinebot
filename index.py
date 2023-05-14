from flask import Flask, request, abort
import os
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

def askchatgpt(q):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=q,
        temperature=0.5,
        max_tokens=1024
    )
    return response['choices'][0]['text'].strip()

line_bot_api = LineBotApi(os.getenv('LINE_ACCESS_TOKEN'))
handler1 = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler1.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

@handler1.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=askchatgpt(event.message.text)))

if __name__ == "__main__":
    app.run()
