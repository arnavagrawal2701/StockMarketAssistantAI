FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY agents_services/voice_service/ .

EXPOSE 8006

CMD ["uvicorn", "voice_service:app", "--host", "0.0.0.0", "--port", "8006", "--reload"]
