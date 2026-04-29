import os
import sys
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from linebot.v3.webhook import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent, PostbackEvent
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, 
    ReplyMessageRequest, TextMessage
)
from dotenv import load_dotenv

# Import our modules
import database as db
import ai_service as ai
import stock_service as stock
import flex_builder as fb

load_dotenv()

app = FastAPI()

channel_secret = os.getenv('LINE_CHANNEL_SECRET')
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

if not channel_secret or not channel_access_token:
    print("Error: LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN must be set.")
    sys.exit(1)

configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)

@app.on_event("startup")
async def startup():
    await db.init_db()

@app.post("/callback")
async def callback(request: Request, background_tasks: BackgroundTasks):
    signature = request.headers.get('X-Line-Signature')
    body = await request.body()
    body_decoded = body.decode('utf-8')
    
    try:
        # We handle asynchronously to prevent timeout
        background_tasks.add_task(handler.handle, body_decoded, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    return "OK"

async def reply(reply_token, messages):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(reply_token=reply_token, messages=messages)
        )

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # This runs in background_tasks
    import asyncio
    asyncio.run(process_message(event))

async def process_message(event):
    user_id = event.source.user_id
    user_input = event.message.text
    
    # 紀錄互動紀錄
    await db.log_interaction(user_id, user_input)
    
    intent = await ai.analyze_intent(user_input)
    
    action = intent.get("action")
    symbol = intent.get("symbol")
    user_id = event.source.user_id
    
    if action == "query":
        data = stock.get_stock_data(symbol)
        if data:
            flex = fb.build_stock_flex(data)
            await reply(event.reply_token, [flex])
        else:
            await reply(event.reply_token, [TextMessage(text=f"抱歉，找不到股票代號 {symbol}")])
            
    elif action == "add":
        success = await db.add_to_watchlist(user_id, symbol)
        msg = f"已將 {symbol} 加入自選股！" if success else f"{symbol} 已經在您的清單中囉。"
        await reply(event.reply_token, [TextMessage(text=msg)])
        
    elif action == "remove":
        await db.remove_from_watchlist(user_id, symbol)
        await reply(event.reply_token, [TextMessage(text=f"已將 {symbol} 從自選股移除。")])
        
    elif action == "list":
        symbols = await db.get_watchlist(user_id)
        flex = fb.build_watchlist_flex(symbols)
        if flex:
            await reply(event.reply_token, [flex])
        else:
            await reply(event.reply_token, [TextMessage(text="您的自選股清單目前是空的。")])
            
    elif action == "help":
        help_msg = "您可以輸入：\n- 查詢 2330\n- 加入 2330\n- 刪除 2330\n- 我的清單"
        await reply(event.reply_token, [TextMessage(text=help_msg)])
    else:
        await reply(event.reply_token, [TextMessage(text="抱歉，我不明白您的意思。輸入『幫助』可以查看指令。")])

@handler.add(PostbackEvent)
def handle_postback(event):
    import asyncio
    asyncio.run(process_postback(event))

async def process_postback(event):
    data_str = event.postback.data
    params = dict(item.split("=") for item in data_str.split("&"))
    
    action = params.get("action")
    symbol = params.get("symbol")
    user_id = event.source.user_id
    
    if action == "add":
        success = await db.add_to_watchlist(user_id, symbol)
        msg = f"已將 {symbol} 加入自選股！" if success else f"{symbol} 已經在您的清單中囉。"
        await reply(event.reply_token, [TextMessage(text=msg)])
    elif action == "remove":
        await db.remove_from_watchlist(user_id, symbol)
        await reply(event.reply_token, [TextMessage(text=f"已將 {symbol} 從自選股移除。")])
