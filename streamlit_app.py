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
