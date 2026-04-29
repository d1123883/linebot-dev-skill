# 系統架構文件 (Architecture)

## 1. 系統流程圖 (Request Flow)

```mermaid
sequenceDiagram
    participant User as LINE 使用者
    participant LINE as LINE 平台
    participant App as FastAPI (Webhook)
    participant BG as Background Task
    participant AI as Gemini AI
    participant DB as SQLite
    participant Stock as yfinance API

    User->>LINE: 傳送訊息
    LINE->>App: 轉發 Webhook (POST /callback)
    App->>App: 驗證 Signature
    App-->>LINE: 回傳 200 OK (5秒內)
    App->>BG: 啟動背景任務 (處理邏輯)
    
    BG->>AI: 解析意圖 (NLU)
    AI-->>BG: 回傳 Intent (JSON)
    
    alt 查詢股價
        BG->>Stock: 抓取現價
        BG->>App: 建立 Flex Message
    else 自選股操作
        BG->>DB: 新增/刪除/查詢
        BG->>App: 建立確認訊息
    end
    
    BG->>LINE: 呼叫 Messaging API (Reply Message)
    LINE->>User: 顯示結果 (Flex Message)
```

## 2. 模組職責說明

| 模組 | 職責 |
| :--- | :--- |
| **app.py** | 系統入口、Webhook 接收、簽章驗證、路由配置。 |
| **database.py** | 使用 `aiosqlite` 處理資料庫初始化、自選股 CRUD 操作。 |
| **ai_service.py** | 整合 Google Generative AI SDK，將使用者文字轉化為結構化指令。 |
| **stock_service.py** | 封裝 `yfinance`，提供統一的股價獲取介面與錯誤處理。 |
| **flex_builder.py** | 負責將資料轉化為符合 LINE Flex Message 規格的 JSON。 |

## 3. 資料庫設計 (Database Schema)

### Table: `watchlist`
| 欄位 | 型別 | 說明 |
| :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY (Auto Increment) |
| `user_id` | TEXT | LINE 提供的唯一使用者 ID |
| `symbol` | TEXT | 股票代號 (如 2330.TW) |
| `created_at` | TIMESTAMP | 加入時間 |

## 4. 關鍵技術點 (Technical Highlights)

1.  **異步併發**：所有 I/O 密集型操作 (DB, AI API, Stock API) 均採用 `async/await`，最大化系統吞吐量。
2.  **超時防範**：利用 FastAPI 的 `BackgroundTasks`，在 200ms 內完成驗證並釋放連接，將邏輯運算移至背景執行。
3.  **錯誤彈性**：AI 解析失敗時，系統將自動降級回正則表達式 (Regex) 匹配基本指令。
4.  **Premium UI**：所有股票查詢結果皆以 `FlexMessage` 呈現，優化行動端視覺體驗。
