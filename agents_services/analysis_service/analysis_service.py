# microservices/analysis_service.py

from fastapi import FastAPI
from pydantic import BaseModel
from agents.analysis_agent import analyze

app = FastAPI()

class AnalysisInput(BaseModel):
    api_data: dict
    earnings_data: dict

@app.post("/analyze")
def analyze_data(req: AnalysisInput):
    summary = analyze(req.api_data, req.earnings_data)
    return {"summary": summary}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
