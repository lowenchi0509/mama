from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage
from flask import Flask, request, abort
from linebot import WebhookHandler
from linebot.models import *
from linebot.models import TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction


app = Flask(__name__)

import os

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["ChannelAccessToken"]

YOUR_CHANNEL_SECRET = os.environ["ChannelSecret"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)

handler = WebhookHandler(YOUR_CHANNEL_SECRET)
parser  = WebhookParser(YOUR_CHANNEL_SECRET)

#line_bot_api.push_message('Ub8e3cf75739079f25a50f82b2cbd4c63', TextSendMessage(text='你可以開始了'))



def sendText(event):  #傳送文字
    try:
        message = TextSendMessage(  
            text = "我是 Linebot，\n您好！"
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendImage(event):  #傳送圖片
    try:
        message = ImageSendMessage(
            original_content_url = "https://i.imgur.com/4QfKuz1.png",
            preview_image_url = "https://i.imgur.com/4QfKuz1.png"
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendStick(event):  #傳送貼圖
    try:
        message = StickerSendMessage(  #貼圖兩個id需查表
            package_id='1',  
            sticker_id='2'
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendMulti(event):  #多項傳送
    try:
        message = [  #串列
            StickerSendMessage(  #傳送貼圖
                package_id='1',  
                sticker_id='2'
            ),
            TextSendMessage(  #傳送y文字
                text = "這是 Pizza 圖片！"
            ),
            ImageSendMessage(  #傳送圖片
                original_content_url = "https://i.imgur.com/4QfKuz1.png",
                preview_image_url = "https://i.imgur.com/4QfKuz1.png"
            )
        ]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendPosition(event):  #傳送位置
    try:
        message = LocationSendMessage(
            title='101大樓',
            address='台北市信義路五段7號',
            latitude=25.034207,  #緯度
            longitude=121.564590  #經度
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendQuickreply(event):  #快速選單
    try:
        message = TextSendMessage(
            text='請選擇最喜歡的程式語言',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="Python", text="Python")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="Java", text="Java")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="C#", text="C#")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="Basic", text="Basic")
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))




# 監聽所有來自 /callback 的 Post Request

@app.route("/callback", methods=['POST'])

def callback():
    if request.method == 'POST':
    # get X-Line-Signature header value

       signature = request.META['HTTP_X_Line_Signature']
       body = request.body.decode('utf-8')



    # handle webhook body

    try:
        events = parser.parse(body, signature)
           # get request body as text
    except InvalidSignatureError:
        return 'Forbidden'
    except LineBotApiError:
        return 'BadRequest' #handler.handle(body, signature)
        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    if mtext == '@傳送文字':
                        sendText(event)
                    elif mtext == '@傳送圖片':
                        sendImage(event)
                    elif mtext == '@傳送貼圖':
                        sendStick(event)
                    elif mtext == '@多項傳送':
                        sendMulti(event)
                    elif mtext == '@傳送位置':
                        sendPosition(event)
                    if mtext == '@快速選單':
                        sendQuickreply(event)
        return 'HttpResponse'
    

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
