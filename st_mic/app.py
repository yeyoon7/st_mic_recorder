import streamlit as st
from st_mic import st_mic  # 커스텀 오디오 녹음 컴포넌트 불러오기

st.title("Custom Audio Recorder")

# st_mic 컴포넌트를 호출하여 오디오 데이터를 받음
audio_data = st_mic()

if audio_data:
    st.write("Received audio data:")
    st.audio(audio_data, format="audio/wav")
