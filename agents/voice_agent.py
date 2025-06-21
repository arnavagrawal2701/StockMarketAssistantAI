# agents/voice_agent.py

import speech_recognition as sr
import pyttsx3

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    return recognizer.recognize_google(audio)

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
