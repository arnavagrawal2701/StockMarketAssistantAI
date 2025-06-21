# agents/api_agent.py

import yfinance as yf

def get_stock_data(tickers):
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="2d")
        try:
            close_today = hist['Close'].iloc[-1]
            close_yesterday = hist['Close'].iloc[-2]
            pct_change = round(((close_today - close_yesterday) / close_yesterday) * 100, 2)
            data[ticker] = {
                "close_today": close_today,
                "close_yesterday": close_yesterday,
                "pct_change": pct_change,
            }
        except Exception as e:
            data[ticker] = {"error": str(e)}
    return data
