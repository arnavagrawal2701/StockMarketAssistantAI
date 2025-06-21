# microservices/lang_service.py

from fastapi import FastAPI
from pydantic import BaseModel
from agents.lang_agent import generate_brief, generate_tickers

app = FastAPI()

class LangInput(BaseModel):
    data_text: str

@app.post("/generate_tickers")
def generate(req: LangInput):
    result = generate_tickers(req.data_text)
    return {"tickers": result}

@app.post("/generate_brief")
def generate(req: LangInput):
    result = generate_brief(req.data_text)
    return {"brief": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
