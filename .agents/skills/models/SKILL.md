# AI Model Selection & Configuration Skill

當使用者需要選擇 AI 模型、調整推理參數或優化 Prompt 效能時，請遵循此指南。

## 指導原則
1. **適材適用**：根據任務複雜度選擇模型（例如：簡單分類用 GPT-4o-mini，複雜推理用 Claude 3.5 Sonnet）。
2. **參數平衡**：明確解釋 Temperature、Top-P 對生成結果多樣性的影響。
3. **Token 意識**：始終考慮上下文長度與 Token 成本，優先考慮縮減 Prompt。
4. **系統提示詞 (System Prompt) 優化**：針對不同模型的特性（如 Role-play 或 Chain-of-Thought）設計 Prompt。

## 主流模型對照表 (2024 中期)

| 模型名稱 | 優勢 | 最佳應用場景 |
| :--- | :--- | :--- |
| **GPT-4o** | 極速、平衡、全能 | 多模態對話、一般助理 |
| **Claude 3.5 Sonnet** | 程式碼能力強、文筆自然 | 軟體開發、長篇寫作 |
| **Gemini 1.5 Pro** | 超長上下文 (2M+) | 大批次文件分析、影片掃描 |
| **GPT-4o-mini** | 極低成本、高效率 | 簡單分類、摘要、Agent 預處理 |
| **Llama 3 (70B+)** | 地端部署、資料隱私 | 內部機敏資料處理 |

## 參數配置清單
- **Temperature**:
    - `0.0 - 0.3`: 結構化資料提取、程式碼生成（追求穩定性）。
    - `0.7 - 1.0`: 創意寫作、腦力激盪（追求創意）。
- **Max Tokens**: 根據預期輸出的長度設定，防止 Token 浪費。
- **Stop Sequences**: 用於 JSON 或特定的格式切斷（例如 `\n\n`）。

## Token 優化技巧
- **Context Pruning**: 移除對話歷史中不相關的部分。
- **Summarization**: 將長對話摘要後再作為 Context。
- **Few-Shot Examples**: 提供的範例應精簡且具有代表性。
