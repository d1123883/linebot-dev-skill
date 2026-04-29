from linebot.v3.messaging import FlexMessage, FlexContainer

def build_stock_flex(data: dict):
    """
    Build a premium Flex Message for stock info.
    """
    color = "#ff0000" if data['change'] > 0 else "#00ff00" if data['change'] < 0 else "#888888"
    icon = "▲" if data['change'] > 0 else "▼" if data['change'] < 0 else "-"
    
    bubble_json = {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {"type": "text", "text": data['name'], "weight": "bold", "size": "xl"},
          {"type": "text", "text": data['symbol'], "size": "sm", "color": "#aaaaaa"},
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {"type": "text", "text": str(data['price']), "size": "3xl", "weight": "bold", "flex": 0},
              {"type": "text", "text": data['currency'], "size": "sm", "gravity": "bottom", "margin": "md"}
            ],
            "margin": "lg"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {"type": "text", "text": f"{icon} {abs(data['change'])} ({data['change_pct']}%)", "color": color, "size": "md"}
            ]
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "button",
            "action": {"type": "postback", "label": "加入自選", "data": f"action=add&symbol={data['symbol']}"},
            "style": "primary",
            "color": "#1DB446"
          }
        ]
      }
    }
    return FlexMessage(alt_text=f"{data['name']} 股價: {data['price']}", contents=FlexContainer.from_dict(bubble_json))

def build_watchlist_flex(symbols: list):
    """
    Build a Flex Message for the watchlist.
    """
    if not symbols:
        return None
        
    contents = []
    for s in symbols:
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": s, "flex": 4, "gravity": "center"},
                {
                    "type": "button", 
                    "action": {"type": "postback", "label": "刪除", "data": f"action=remove&symbol={s}"},
                    "style": "link", "color": "#ff0000", "height": "sm"
                }
            ]
        })
        contents.append({"type": "separator"})
    
    if contents:
        contents.pop() # Remove last separator
        
    bubble_json = {
        "type": "bubble",
        "header": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "我的自選股", "weight": "bold", "size": "lg"}]},
        "body": {"type": "box", "layout": "vertical", "contents": contents}
    }
    return FlexMessage(alt_text="我的自選股清單", contents=FlexContainer.from_dict(bubble_json))
