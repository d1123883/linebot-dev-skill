# LINE Bot 開發專家 (linebot-dev)

本 Skill 指導 AI 如何正確使用 `line-bot-sdk-python` v3 進行開發，並遵循最佳實踐。

> [!IMPORTANT]
> **核心開發原則：**
> 1. **強制使用 v3**：除非使用者明確要求 v2，否則一律使用 `linebot.v3` 及其子模組。
> 2. **Webhook 必須回傳 HTTP 200**：無論處理成功與否，Webhook Endpoint 必須儘速回傳 `200 OK` 給 LINE 平台。
> 3. **Reply Token 唯一性**：一個 `reply_token` 只能使用一次，呼叫後立即失效。

## 1. SDK 版本差異 (v2 vs v3)

`line-bot-sdk-python` v3 是一個重大的架構更新，不回溯相容。

| 特性 | Version 2 (Legacy) | Version 3 (Modern) |
| :--- | :--- | :--- |
| **主要包路徑** | `linebot` | `linebot.v3`, `linebot.v3.messaging`, `linebot.v3.webhooks` |
| **Client 初始化** | `LineBotApi(token)` | `ApiClient` + `Configuration` + `MessagingApi` |
| **訊息類別** | `TextSendMessage(text=...)` | `TextMessage(text=...)` |
| **回覆 API** | `reply_message(token, messages)` | `reply_message(ReplyMessageRequest(reply_token, messages))` |

---

## 2. 環境變數配置 (.env)

開發 LINE Bot 時，必須在 `.env` 中準備以下 Key：

```bash
LINE_CHANNEL_SECRET="你的 Channel Secret"
LINE_CHANNEL_ACCESS_TOKEN="你的 Channel Access Token"
```

> [!TIP]
> 如果需要處理 Flex Message 或 Rich Menu，建議也將其定義在環境變數或獨立的 JSON 檔中。

---

## 3. 標準 Webhook + Handler 寫法 (FastAPI)

```python
import os
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks, Response
from linebot.v3.webhook import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage

app = FastAPI()

# 從環境變數讀取
channel_secret = os.getenv('LINE_CHANNEL_SECRET')
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)

@app.post("/callback")
async def callback(request: Request):
    signature = request.headers.get('X-Line-Signature')
    body = await request.body()
    
    try:
        handler.handle(body.decode('utf-8'), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    return Response(content="OK", status_code=200) # 強制回傳 200

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )
```

---

## 4. 常見地雷與最佳實踐

### ⚠️ Reply Token 限制
- **一次性使用**：每個 `reply_token` 只能呼叫一次 API。若要傳送多個訊息，請在 `messages` 列表中放入多個物件 (最多 5 個)。
- **時效性**：必須在收到 Webhook 後的 **30-60 秒內** 使用，過期失效。

### ⚠️ Webhook 5 秒超時 (HTTP 200)
- LINE 平台要求 Webhook 必須在 5 秒內回應。若處理邏輯過長（例如調用 AI API），必須使用背景作業。
- **解決方案**：
  ```python
  @app.post("/callback")
  async def callback(request: Request, background_tasks: BackgroundTasks):
      # ... 驗證 signature ...
      # 將邏輯丟入背景，立即回傳 200
      background_tasks.add_task(handler.handle, body, signature)
      return Response(status_code=200)
  ```

### ⚠️ AI 模型選擇 (Gemini)
- **推薦模型**：優先使用 `gemini-2.5-flash`，以避免某些區域 v1beta 版本找不到 `1.5-flash` 的問題。
- **解析格式**：要求 LLM 只回傳純 JSON 字串，並在程式端處理可能的 Markdown 標籤（如 ```json ... ```）。

### ⚠️ Flex Message 常見錯誤
- **dict vs json**：在 v3 SDK 中，`FlexContainer.from_dict()` 接收 Python 字典 (dict)，而 `FlexContainer.from_json()` 接收 JSON 字串。開發時請確保型別正確。

---

## 5. 事件類型與訊息類型列表

### 事件類型 (Events)
- `MessageEvent`: 收到訊息
- `FollowEvent`: 使用者加好友/解除封鎖
- `UnfollowEvent`: 使用者封鎖
- `JoinEvent`: Bot 加入群組/聊天室
- `LeaveEvent`: Bot 離開群組
- `PostbackEvent`: 使用者點擊按鈕 (Rich Menu 或 Template)
- `BeaconEvent`: LINE Beacon 事件

### 訊息類型 (Message Content - 接收)
- `TextMessageContent`, `ImageMessageContent`, `VideoMessageContent`, `AudioMessageContent`, `LocationMessageContent`, `StickerMessageContent`, `FileMessageContent`

---

## 6. 開發前 Checklist

1. [ ] **LINE Developers Console**: 是否已建立 Messaging API Channel？
2. [ ] **.env 準備**: `LINE_CHANNEL_SECRET` 與 `LINE_CHANNEL_ACCESS_TOKEN` 是否已填妥？
3. [ ] **Webhook URL**: 是否已設定 HTTPS (ngrok) 並在 Console 測試通過？
4. [ ] **Auto-response**: 是否已在 LINE Official Account Manager 關閉「自動回應訊息」？
5. [ ] **SDK Version**: 確認安裝命令為 `pip install line-bot-sdk>=3.0.0`？
