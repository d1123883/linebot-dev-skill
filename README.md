# Stock LINE Bot 開發專案 (linebot-dev-skill)

本專案示範如何結合多個 AI Agent Skills，從零開始開發一個具備 SQLite 持久化功能的 **股票 LINE Bot**。

## 🚀 開發工作流 (Workflow)

為了確保開發過程清晰且具備完整的版本歷史，請遵循以下步驟：

1.  **需求定義 (`/prd`)**
    *   確認股票 LINE Bot 的核心功能（如：查詢股價、到價提醒）。
    *   產出文件：`docs/PRD.md`。
2.  **階段性提交 (`/commit`)**
3.  **架構設計 (`/architecture`)**
    *   確認技術堆疊：`FastAPI` + `line-bot-sdk v3` + `SQLite`。
    *   產出架構設計文件。
4.  **階段性提交 (`/commit`)**
5.  **程式碼實作 (`/linebot-dev`)**
    *   使用專屬 Skill 生成標準化的程式碼。
    *   產出檔案：`app.py`, `requirements.txt`, `.env.example`。
6.  **手動測試**
    *   於本機執行並使用 ngrok 進行測試。
7.  **最終提交 (`/commit`)**

---

## 🛠️ 專案結構
- `.agents/skills/`: 存放 AI 指引文件（包含 `linebot-dev/SKILL.md`）。
- `docs/`: 存放 PRD 與架構文件。
- `app.py`: LINE Bot 主程式。
- `requirements.txt`: 依賴套件清單。
- `.env.example`: 環境變數範本。
