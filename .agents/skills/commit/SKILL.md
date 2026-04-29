# Git Commit & Version Control Skill

當使用者需要進行版本備份、設定 Git 身分或撰寫 Commit 訊息時，請遵循此指南。

## 身分設定
如需設定 Git 使用者，請使用以下預設值：
- **User Name**: `Antigravity`
- **User Email**: `antigravity@ai.com` (預設範例)

執行指令：
```powershell
git config --local user.name "Antigravity"
git config --local user.email "antigravity@ai.com"
```

## Commit 訊息規範 (Conventional Commits)
請採用以下格式：`<type>: <description>`

### 常用類型 (Types)
- **feat**: 加入新功能 (New feature)
- **fix**: 修復錯誤 (Bug fix)
- **docs**: 僅修改文件 (Documentation only)
- **style**: 不影響程式邏輯的代碼格式修改 (Formatting, missing semi colons, etc)
- **refactor**: 重構程式碼（既非新功能也非修復錯誤）
- **test**: 新增或修改測試案例
- **chore**: 建置流程或輔助工具的變動

### 範例
- `feat: add streaming support to chat api`
- `fix: resolve sqlite connection timeout issue`

## 標準工作流程
1. **確認狀態**: `git status`
2. **暫存更改**: `git add .` (或特定檔案)
3. **建立提交**: `git commit -m "feat: your message"`
4. **檢查歷史**: `git log --oneline -n 5`

## 指導原則
1. **原子性**: 每次 Commit 應只包含一個邏輯變動。
2. **描述清晰**: 訊息應簡潔明瞭，讓人一眼看出改了什麼。
3. **先 Add 後 Commit**: 在執行 Commit 前，務必確認所有相關檔案都已加入暫存。
