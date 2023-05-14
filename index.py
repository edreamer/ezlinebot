from flask import Flask, request, abort
import openai, os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

openai.api_key = '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'

app = Flask(__name__)

line_bot_api = LineBotApi('srFTsHK62OAvxrtPQxwkyYdXrS0ICYgrSgKarEpd5ayHlSMPY2TEP1KNbDMUm5bx4cDb7610wTfayRUG+ZXOkPrPt6zwIP5VrmGLJnqSvioWwxVL7m4g9Vr9OqNcr1ucsS2fxqWFCsajmWxfN32mTgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3422ef0232368541bcf7867e2f7f8443')

def askchatgpt(q):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=q,
        temperature=0.5,
        max_tokens=1024
    )
    return response['choices'][0]['text'].strip()

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler1.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler1.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=askchatgpt(event.message.text)))
    
if __name__ == "__main__":
    app.run()
