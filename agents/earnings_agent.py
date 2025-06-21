# agents/scraping_agent.py

import yfinance as yf
from typing import Dict

def fetch_earnings_data(tickers: list) -> Dict[str, Dict[str, str]]:
    earnings_data = {}
    for ticker in tickers:
        try:
            # Get stock data using yfinance
            stock = yf.Ticker(ticker)
            earnings = stock.earnings_dates

            # Filter out rows with NaN values for EPS Estimate, Reported EPS, and Surprise(%)
            earnings_filtered = earnings.dropna(subset=["EPS Estimate", "Reported EPS", "Surprise(%)"])

            # Fetch the most recent earnings data (latest entry)
            if not earnings_filtered.empty:
                recent_earnings = earnings_filtered.iloc[0]  # Get the most recent earnings date
                earnings_data[ticker] = {
                    "Earnings Date": recent_earnings.name,
                    "EPS Estimate": recent_earnings["EPS Estimate"],
                    "Reported EPS": recent_earnings["Reported EPS"],
                    "Surprise(%)": recent_earnings["Surprise(%)"]
                }
            else:
                earnings_data[ticker] = {"error": "No valid earnings data found"}
        except Exception as e:
            earnings_data[ticker] = {"error": str(e)}

    return earnings_data


# Get the most recent earnings data for a list of tickers
def get_live_earnings_data(tickers: list) -> Dict[str, Dict[str, str]]:
    return fetch_earnings_data(tickers)
