import streamlit as st
import requests
import tempfile
from audiorecorder import audiorecorder
import re

# --- Function to fetch market brief ---
def get_market_brief(query):
    url = st.secrets.get("ORCHESTRATOR_URL", "http://localhost:9000/market_brief")
    payload = {"query": query}
    try:
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        return resp.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)

# --- Function to transcribe audio via voice_service ---
def transcribe_audio_via_api(audio_blob):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        audio_blob.export(tmpfile.name, format="wav")
        with open(tmpfile.name, "rb") as f:
            files = {"file": f}
            resp = requests.post("http://localhost:8006/transcribe", files=files)
            if resp.ok:
                return resp.json().get("transcription", "")
            else:
                return f"Error: {resp.text}"


# --- Function to call voice speak ---
def call_voice_speak(text):
    try:
        response = requests.post("http://localhost:8006/speak", json={"text": text})
        if response.ok:
            return True
    except Exception as e:
        st.error(f"Voice error: {e}")
    return False


# --- Streamlit App UI ---
st.set_page_config(page_title="Multi-Agent Finance Assistant", layout="wide")
st.title("🎙️ Voice-enabled Stock Market Assistant")

# 🎤 Voice recorder
st.subheader("Record your voice query")
audio = audiorecorder("Click to record", "Recording...")

if len(audio) > 0:
    st.audio(audio.export().read(), format="audio/wav")
    if st.button("Transcribe Recording"):
        with st.spinner("Transcribing..."):
            transcription = transcribe_audio_via_api(audio)
            if transcription:
                st.success("Transcription complete!")
                st.write("📝 Transcribed Text:", transcription)
                st.session_state["query_input"] = transcription

# --- Input form ---
st.subheader("Manual Query Input")
with st.form(key="brief_form"):
    query_input = st.text_input("Enter query", value=st.session_state.get("query_input", "Asia tech stock exposure and earnings surprises"))
    submitted = st.form_submit_button("Get Market Brief")

if submitted:
    with st.spinner("Fetching market brief..."):
        result, error = get_market_brief(query_input)
    if error:
        st.error(f"Error fetching data: {error}")
    else:
        st.subheader("API Data")
        st.json(result.get("api_data", {}))

        st.subheader("Earnings Data")
        st.json(result.get("earnings_data", {}))

        st.subheader("Analysis Summary")
        st.write(result.get("summary", ""))

        st.subheader("Retrieved Chunks")
        for chunk in result.get("retrieved_chunks", []):
            st.write(f"- {chunk}")

        st.subheader("Final Brief")
        st.write(result.get("final_brief", ""))

        if (result.get("final_brief", "")):
            st.info("Speaking summary...")
            call_voice_speak(result.get("final_brief", ""))

# Footer
st.markdown("---")
st.write("Powered by Streamlit, FastAPI & Agentic Voice Intelligence")
