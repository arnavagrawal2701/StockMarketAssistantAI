# orchestrator/main.py

import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class BriefRequest(BaseModel):
    query: str

@app.post("/market_brief")
def get_market_brief(req: BriefRequest):
    tickers_res = requests.post("http://localhost:8005/generate_tickers", json={"data_text": req.query})
    tickers = tickers_res.json().get("tickers").split(',')

    api_res = requests.post("http://localhost:8001/get_stock_data", json={"tickers": tickers})
    api_data = api_res.json()

    earnings_res = requests.post("http://localhost:8002/get_earnings_data", json={"tickers": tickers})
    earnings_data = earnings_res.json().get("earnings_data")

    analysis_res = requests.post("http://localhost:8004/analyze", json={
        "api_data": api_data,
        "earnings_data": earnings_data
    })
    analysis_summary = analysis_res.json().get("summary")

    _ = requests.post("http://localhost:8003/build_index", json={"texts": [analysis_summary]})
    retrieval_res = requests.post("http://localhost:8003/retrieve", json={"query": req.query, "k": 2})
    retrieved_chunks = retrieval_res.json().get("chunks", [])

    lang_input = "\n".join(retrieved_chunks) if retrieved_chunks else analysis_summary
    lang_res = requests.post("http://localhost:8005/generate_brief", json={"data_text": lang_input})
    final_brief = lang_res.json().get("brief")

    return {
        "api_data": api_data,
        "earnings_data": earnings_data,
        "summary": analysis_summary,
        "retrieved_chunks": retrieved_chunks,
        "final_brief": final_brief
    }

@app.get("/")
def root():
    return {"message": "Multi-Agent Orchestrator is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("orchestrator.main:app", host="0.0.0.0", port=9000, reload=True)
