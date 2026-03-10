import streamlit as st

st.set_page_config(page_title="ATC Radio", page_icon="✈️")

st.title("🎙️ Aeroflot Virtual ATC")
st.write("Use your iPad microphone to talk to the tower.")

# Flight Info Sidebar
with st.sidebar:
    st.header("Flight Plan")
    callsign = st.text_input("Callsign", "Aeroflot 123")
    location = st.selectbox("Current Phase", ["Gate", "Taxi", "Takeoff", "Enroute", "Landing"])

# The iPad Microphone Button
audio_input = st.audio_input("Tap to speak to ATC")

if audio_input:
    st.info(f"Receiving transmission from {callsign}...")
    # This is where the AI response will eventually appear
    st.success("ATC: [Simulated Response] Aeroflot 123, cleared for taxi to runway 24L via Alpha.")
    # Add an ICAO search box
icao_code = st.sidebar.text_input("Enter Airport ICAO (e.g., UUEE or KLAX)", "UUEE")

# This is the "Knowledge Base" you send to the AI
if icao_code == "UUEE":
    airport_context = "Taxiways: A, B, C, M, P. Runway 24L is active. Main Terminal is South."
elif icao_code == "KLAX":
    airport_context = "Taxiways: Alpha, Bravo, Charlie, Tango. Runway 25R is active."
else:
    airport_context = "Standard airport procedures apply."

# Update the AI Prompt
system_prompt = f"You are ATC at {icao_code}. {airport_context} Give taxi instructions using these taxiways."
import streamlit as st
from openai import OpenAI
import airportsdata

st.set_page_config(page_title="ATC Radio", page_icon="✈️", layout="wide")
airports = airportsdata.load('ICAO')

# UI Header
st.title("🎙️ iPad ATC Terminal")
st.write("Ensuring 'HTTPS' is active for microphone access.")

# 1. SIDEBAR CONFIG
with st.sidebar:
    st.header("Flight Settings")
    callsign = st.text_input("Callsign", "Aeroflot 123")
    icao = st.text_input("Airport ICAO", "UUEE").upper()
    api_key = st.text_input("OpenAI Key", type="password")

# 2. THE AUDIO WIDGET (iPad Specific Fix)
# We use a key to ensure the widget resets properly after each use
audio_data = st.audio_input("Hold to speak to Tower", key="ipad_mic")

if audio_data is not None:
    # DEBUG: Check if data actually arrived from the iPad
    st.toast("Audio captured successfully!")
    
    if api_key:
        client = OpenAI(api_key=api_key)
        
        # EAR: Transcribe using Whisper
        # Note: We send the 'audio_data' directly as a file-like object
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_data
        )
        pilot_text = transcript.text
        
        with st.chat_message("user"):
            st.write(f"**{callsign}:** {pilot_text}")

        # BRAIN: Generate ATC response
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are ATC at {icao}. Use strict aviation phraseology. Keep it short."},
                {"role": "user", "content": pilot_text}
            ]
        )
        atc_reply = response.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.write(f"**Tower:** {atc_reply}")
            
            # VOICE: iOS Playback Fix
            # Safari requires specific formatting to play back audio reliably
            audio_response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=atc_reply
            )
            # This allows the iPad to play the sound immediately
            st.audio(audio_response.content, format="audio/mpeg")
    else:
        st.warning("Please enter your OpenAI API Key in the sidebar to process audio.")
