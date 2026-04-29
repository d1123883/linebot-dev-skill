# Testing & Quality Assurance Skill (FastAPI + HTML)

當使用者需要撰寫測試案例、驗證 API 邏輯或建立品質監控流程時，請遵循此指南。預設使用 **pytest** 與 **httpx**。

## 指導原則
1. **單元化**：每個測試案例僅驗證一個具體功能。
2. **獨立性**：使用 Mock 阻斷外部依賴（如 LLM API），並在測試中使用記憶體內資料庫。
3. **即時性**：測試應能快速運行，以便在開發過程中頻繁調用。
4. **覆蓋率**：確保關鍵路徑（如錯誤處理、極端輸入）都有對應測試。

## 後端測試：pytest + FastAPI

### 基礎配置 (`conftest.py`)
```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from backend.main import app, get_session

# 使用記憶體內 SQLite 進行測試
sqlite_url = "sqlite:///memory"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

@pytest.fixture
def session():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture
def client(session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
```

### API 測試案例 (`test_api.py`)
```python
def test_create_session(client):
    response = client.post("/sessions", json={"title": "Test Chat"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Chat"
```

### 模擬 (Mock) LLM 回覆
```python
from unittest.mock import patch

def test_chat_response(client):
    with patch("backend.orchestrator.call_llm", return_value="Mocked AI Answer"):
        response = client.post("/chat", json={"message": "Hello"})
        assert response.json()["answer"] == "Mocked AI Answer"
```

## 前端測試清單
- **Fetch 驗證**：檢查 API 回傳非 200 時，UI 是否顯示錯誤提示。
- **DOM 操作**：驗證訊息發送後，對話框是否正確渲染。
- **邊界測試**：輸入超長文字或空訊息時的行為。

## AI 評估 (Evals)
- **基礎檢驗**：檢查輸出是否為有效 JSON (如果要求 JSON 格式)。
- **關鍵字檢查**：特定場景下，回覆是否包含必備關鍵字。

## 運行指令
- **全域測試**: `pytest`
- **顯示輸出**: `pytest -s`
- **特定文件**: `pytest tests/test_api.py`
