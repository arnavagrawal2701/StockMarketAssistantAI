FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY agents_services/earnings_service/ .

EXPOSE 8002

CMD ["uvicorn", "earnings_service:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]
