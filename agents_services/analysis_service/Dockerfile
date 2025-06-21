FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY agents_services/analysis_service/ .

EXPOSE 8004

CMD ["uvicorn", "analysis_service:app", "--host", "0.0.0.0", "--port", "8004", "--reload"]
