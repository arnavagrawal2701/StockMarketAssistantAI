FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY agents_services/retriever_service/ .

EXPOSE 8003

CMD ["uvicorn", "retriever_service:app", "--host", "0.0.0.0", "--port", "8003", "--reload"]
