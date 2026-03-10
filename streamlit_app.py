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

# 1. Setup & Data
st.set_page_config(page_title="Aeroflot ATC", page_icon="✈️")
airports = airportsdata.load('ICAO')

# 2. Sidebar - Flight Configuration
with st.sidebar:
    st.header("Flight Management")
    callsign = st.text_input("Callsign", "Aeroflot 123")
    dep_icao = st.text_input("Departure Airport", "UUEE").upper()
    arr_icao = st.text_input("Arrival Airport", "URSS").upper()
    phase = st.radio("Current Phase", ["Clearance", "Taxi", "Takeoff", "Enroute", "Landing", "Arrival Taxi"])
    
    # API Key - You can put this in Streamlit Secrets later
    api_key = st.text_input("OpenAI API Key (Optional for now)", type="password")

st.title("🎙️ Virtual ATC Radio")
st.caption(f"Connected to iPad Microphone | Controlling: {callsign}")

# 3. The iPad Microphone Widget
# This is the specific 2026 Streamlit component for iPad/Mobile mic support
audio_value = st.audio_input("Tap to speak to Tower")

if audio_value:
    st.info("Transmission received... analyzing audio.")
    
    # Logic: Get airport names for the AI
    dep_name = airports.get(dep_icao, {}).get('name', dep_icao)
    arr_name = airports.get(arr_icao, {}).get('name', arr_icao)
    current_apt = arr_name if "Arrival" in phase or "Landing" in phase else dep_name

    # Check if we have a key to talk to the 'Brain'
    if api_key:
        client = OpenAI(api_key=api_key)
        
        # A. Transcribe what you said (Ears)
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_value
        )
        pilot_text = transcript.text
        st.chat_message("user").write(pilot_text)

        # B. Get ATC Response (Brain)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are ATC at {current_apt}. Use short aviation phraseology. Know the taxiways for {current_apt}."},
                {"role": "user", "content": pilot_text}
            ]
        )
        atc_reply = response.choices[0].message.content
        st.chat_message("assistant").write(atc_reply)
        
    else:
        # SIMULATION MODE (If no API key yet)
        st.warning("Running in Offline/Simulation mode. Enter API key to hear real AI.")
        if "Taxi" in phase:
            st.success(f"ATC: {callsign}, {current_apt} Ground. Taxi to Runway 24L via Alpha, Bravo. Hold short Runway 20.")
        elif "Landing" in phase:
            st.success(f"ATC: {callsign}, {current_apt} Tower. Wind 240 at 10. Runway 06, cleared to land.")
