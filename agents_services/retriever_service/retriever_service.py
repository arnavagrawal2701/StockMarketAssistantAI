# microservices/retriever_service.py

from fastapi import FastAPI
from pydantic import BaseModel
from agents.retriever_agent import build_pinecone_index, retrieve_chunks_from_pinecone
from dotenv import load_dotenv
import uvicorn

load_dotenv()
app = FastAPI()

class IndexRequest(BaseModel):
    texts: list[str]

class QueryRequest(BaseModel):
    query: str
    k: int = 3

@app.post("/build_index")
def build_index(req: IndexRequest):
    try:
        build_pinecone_index(req.texts)
        return {"status": "index_built", "num_docs": len(req.texts)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/retrieve")
def retrieve(req: QueryRequest):
    try:
        chunks = retrieve_chunks_from_pinecone(req.query, k=req.k)
        return {"chunks": [doc.page_content for doc in chunks]}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
