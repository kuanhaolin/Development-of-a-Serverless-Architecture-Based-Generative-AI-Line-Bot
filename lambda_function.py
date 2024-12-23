import json, os
import openai
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

#init
line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINE_CHANNEL_SECRET'])
openai.api_key = os.environ['OPENAI_API_KEY']

#trigger.         #http info, lamda env info
def lambda_handler(event, context):
    #textmsg trigger
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        #input
        user_message = event.message.text

        #apply gpt model
        response = openai.ChatCompletion.create(
            model="gpt-4o", 
            messages=[{"role": "user", "content": user_message}]
        )

        #reply to chatroom
        reply = response.choices[0].message.content
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)  # 回傳格式化的 JSON
        )

    # get X-Line-Signature header value
    signature = event['headers']['x-line-signature']

    # get request body as text
    body = event['body']

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return {
            'statusCode': 502,
            'body': json.dumps("Invalid signature. Please check your channel access token/channel secret.")
            }
    return {
        'statusCode': 200,
        'body': json.dumps("OK")
        }