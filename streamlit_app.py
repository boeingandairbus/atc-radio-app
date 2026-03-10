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
