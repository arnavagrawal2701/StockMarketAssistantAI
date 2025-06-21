# microservices/api_service.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from agents.api_agent import get_stock_data

app = FastAPI()

class TickerRequest(BaseModel):
    tickers: list[str]

@app.post("/get_stock_data")
def fetch_data(req: TickerRequest):
    return get_stock_data(req.tickers)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

