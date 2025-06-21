# microservices/api_service.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from agents.earnings_agent import get_live_earnings_data  # Assuming the earnings function is in earnings_agent.py

app = FastAPI()


class TickerRequest(BaseModel):
    tickers: list[str]


@app.post("/get_earnings_data")
def fetch_stock_data(req: TickerRequest):
    earnings_data = get_live_earnings_data(req.tickers)

    return {
        "earnings_data": earnings_data
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
