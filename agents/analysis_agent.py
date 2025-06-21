# agents/analysis_agent.py

def analyze(api_data, earnings_data):
    summary = []

    for ticker, values in api_data.items():
        # Check if there's an error in the values for that ticker
        if "error" in values:
            continue

        # Process the stock data (e.g., pct_change) if no error exists
        pct = values.get("pct_change")  # Use .get() to avoid KeyError if pct_change is missing

        if pct is not None:
            direction = "up" if pct > 0 else "down"
            summary.append(f"{ticker} is {direction} {abs(pct)}% from yesterday.")
        else:
            summary.append(f"{ticker} does not have pct_change data.")

    for company, surprise in earnings_data.items():
        summary.append(f"{company} earnings surprise: {surprise}")

    return " ".join(summary)
