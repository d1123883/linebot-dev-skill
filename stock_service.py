import yfinance as yf
import pandas as pd

def get_stock_data(symbol: str):
    """
    Fetch stock data using yfinance. 
    Handles both TW (e.g. 2330.TW) and US stocks.
    """
    try:
        # Standardize symbol for TW stocks if only numbers given
        if symbol.isdigit() and len(symbol) >= 4:
            symbol = f"{symbol}.TW"
            
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        if 'currentPrice' not in info and 'regularMarketPrice' not in info:
            return None
            
        price = info.get('currentPrice') or info.get('regularMarketPrice')
        prev_close = info.get('previousClose')
        change = price - prev_close if price and prev_close else 0
        change_pct = (change / prev_close) * 100 if prev_close else 0
        
        return {
            "symbol": symbol,
            "name": info.get('shortName', symbol),
            "price": round(price, 2),
            "change": round(change, 2),
            "change_pct": round(change_pct, 2),
            "currency": info.get('currency', 'USD')
        }
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None
