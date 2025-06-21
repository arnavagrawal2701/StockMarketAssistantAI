# microservices/voice_service.py

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from agents.voice_agent import transcribe_audio, speak_text
import tempfile

app = FastAPI()

class SpeakRequest(BaseModel):
    text: str

@app.post("/speak")
def speak(req: SpeakRequest):
    speak_text(req.text)
    return {"status": "spoken"}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        transcription = transcribe_audio(tmp_path)
        return {"transcription": transcription}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)
