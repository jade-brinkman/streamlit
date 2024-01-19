import streamlit as st
from audio_recorder_streamlit import audio_recorder

audio_bytes = audio_recorder(text="Cliquez pour enregistrer",
    recording_color="#21B8BB",
    neutral_color="#33FBFF",
    icon_name="microphone",
    icon_size="6x",)
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")