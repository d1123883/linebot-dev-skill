import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create the model
model = genai.GenerativeModel("gemini-2.5-flash")

PROMPT_TEMPLATE = """
你是一個股票機器人的意圖分析專家。請分析使用者的訊息並回傳 JSON 格式。
支援的操作：
- query: 查詢單一股票 (需包含 symbol)
- add: 加入自選股 (需包含 symbol)
- remove: 移除自選股 (需包含 symbol)
- list: 查看自選股清單
- help: 顯示幫助

使用者訊息："{user_input}"

回傳格式規範：
{{
    "action": "query" | "add" | "remove" | "list" | "help" | "unknown",
    "symbol": "股票代號 (台股請帶 .TW，例如 2330.TW)",
    "reason": "簡短理由"
}}

請只回傳 JSON 字串，不要有 Markdown 格式：
"""

async def analyze_intent(user_input: str):
    try:
        response = model.generate_content(PROMPT_TEMPLATE.format(user_input=user_input))
        text = response.text.strip()
        # Remove markdown if present
        if text.startswith("```json"):
            text = text[7:-3]
        elif text.startswith("```"):
            text = text[3:-3]
            
        data = json.loads(text)
        return data
    except Exception as e:
        print(f"AI Analysis error: {e}")
        # Fallback to simple regex-like logic
        if "查" in user_input or any(c.isdigit() for c in user_input):
            # Extract numbers
            digits = "".join(filter(str.isdigit, user_input))
            if digits:
                return {"action": "query", "symbol": f"{digits}.TW"}
        return {"action": "unknown"}
