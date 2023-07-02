from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import requests, os
url = "https://api.openai.com/v1/completions"
api_key = os.getenv('OPENAI_API_KEY')
headers = {"Authorization":"Bearer " + api_key}

def askchatgpt(q):
    data = {
    "model": "text-davinci-003",
    "prompt": q,
    "temperature": 1,
    "max_tokens": 1024,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0
    }
    r = requests.post(url, json=data, headers=headers)
    datas = r.json()
    return datas['choices'][0]['text'].strip()

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('LINE_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=askchatgpt(event.message.text)))


if __name__ == "__main__":
    app.run()
