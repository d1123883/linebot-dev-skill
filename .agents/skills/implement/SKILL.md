# Full-Stack Implementation Skill (HTML + FastAPI + SQLite)

當使用者需要實作具體的程式碼、建立專案結構或串接前後端時，請遵循此指南。此技能預設使用 **HTML/CSS/JS (Vanilla)** 與 **FastAPI + SQLModel (SQLite)**。

## 指導原則
1. **結構清晰**：區分 `frontend/` (靜態檔案) 與 `backend/` (API 服務)。
2. **非同步 (Async)**：FastAPI 應使用 `async def` 處理 I/O 密集型任務。
3. **類型安全**：使用 Pydantic/SQLModel 定義資料模型。
4. **原生前端**：優先使用 Vanilla JS 與 Fetch API，減少外部依賴。

## 專案結構建議
```text
my_ai_app/
├── backend/
│   ├── main.py          # FastAPI 進入點
│   ├── models.py        # SQLModel 定義
│   ├── database.py      # SQLite 連線設定
│   └── .env             # 環境變數 (API Key)
├── frontend/
│   ├── index.html       # 主頁面
│   ├── style.css        # 樣式
│   └── app.js           # 前端邏輯 (Fetch/SSE)
└── requirements.txt
```

## 後端：FastAPI + SQLModel (SQLite)

### 資料庫連線 (`database.py`)
```python
from sqlmodel import SQLModel, create_engine, Session

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

### 串流 API 範例 (`main.py`)
```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/chat/stream")
async def chat_stream(message: str):
    async def event_generator():
        # 模擬 AI 串流輸出
        for word in ["Hello", " this", " is", " a", " stream."]:
            yield f"data: {word}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

## 前端：Vanilla HTML/JS

### Fetch API 範例 (`app.js`)
```javascript
async function sendMessage(text) {
    const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
    });
    const data = await response.json();
    console.log(data);
}
```

### SSE 串流接收範例
```javascript
function startStream(message) {
    const eventSource = new EventSource(`/chat/stream?message=${message}`);
    eventSource.onmessage = (event) => {
        const content = event.data;
        document.getElementById('chat-box').innerHTML += content;
    };
    eventSource.onerror = () => eventSource.close();
}
```

## 開發工具指令
- **安裝依賴**: `pip install fastapi uvicorn sqlmodel`
- **運行後端**: `uvicorn backend.main:app --reload`
