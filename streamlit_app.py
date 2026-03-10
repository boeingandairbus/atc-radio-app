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
system_prompt = f"You are ATC at {icao_code}. {airport_context} Give taxi instructions using these taxiways."import streamlit as st
import streamlit as st
from openai import OpenAI
import airportsdata

# Load airport database (Free & Offline)
airports = airportsdata.load('ICAO')

st.set_page_config(page_title="Aeroflot ATC Radio", page_icon="✈️")
st.title("🎙️ Aeroflot ATC: Departure & Arrival")

# Sidebar: Flight Management
with st.sidebar:
    st.header("Flight Plan")
    callsign = st.text_input("Callsign", "Aeroflot 123")
    dep_icao = st.text_input("Departure Airport (ICAO)", "UUEE")
    arr_icao = st.text_input("Arrival Airport (ICAO)", "URSS")
    
    # Critical for logic: Are we leaving or arriving?
    phase = st.radio("Flight Phase", ["Departure", "Enroute", "Arrival/Landing"])

# Get airport names for better AI context
dep_name = airports.get(dep_icao, {}).get('name', 'Departure Airport')
arr_name = airports.get(arr_icao, {}).get('name', 'Arrival Airport')

# The iPad Microphone Input
audio_data = st.audio_input("Tap to talk to ATC")

if audio_data:
    st.info(f"Talking to {arr_name if phase == 'Arrival/Landing' else dep_name}...")
    
    # SYSTEM PROMPT: This is the "Brain" of the ATC
    atc_role = f"""
    You are an expert Air Traffic Controller. 
    Current Airport: {arr_name if phase == 'Arrival/Landing' else dep_name} ({arr_icao if phase == 'Arrival/Landing' else dep_icao}).
    Pilot Callsign: {callsign}.
    Flight Phase: {phase}.
    
    INSTRUCTIONS:
    1. If phase is 'Departure', give taxi instructions to the runway via taxiways (e.g., A, B, M).
    2. If phase is 'Arrival/Landing', give landing clearance or taxi-to-gate instructions after landing.
    3. Use professional, short aviation phraseology.
    """
    
    # (Optional) Here you would call your AI API to process audio_data
    # For now, we show a sample response on the iPad:
    st.success(f"ATC: {callsign}, welcome to {arr_name}. Taxi to Gate 12 via Taxiway Charlie and Bravo. Hold short of Runway 06.")
