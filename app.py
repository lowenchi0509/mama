#載入LineBot所需要的套件
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage
from module import func
from flask import Flask, request, abort
from linebot import WebhookHandler
from linebot.models import *
from linebot.models import TextSendMessage

app = Flask(__name__)
import os
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["ChannelAccessToken"]
YOUR_CHANNEL_SECRET = os.environ["ChannelSecret"]
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
parser  = WebhookParser(YOUR_CHANNEL_SECRET)
#line_bot_api.push_message('Ub8e3cf75739079f25a50f82b2cbd4c63', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
          events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
    for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    if mtext == '@傳送文字':
                        func.sendText(event)
    
                    elif mtext == '@傳送圖片':
                        func.sendImage(event)
    
                    elif mtext == '@傳送貼圖':
                        func.sendStick(event)
    
                    elif mtext == '@多項傳送':
                        func.sendMulti(event)
    
                    elif mtext == '@傳送位置':
                        func.sendPosition(event)
    
                    if mtext == '@快速選單':
                        func.sendQuickreply(event)
    return HttpResponse()

#訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
