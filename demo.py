import streamlit as st
import os
from st_mic import st_mic  # 커스텀 오디오 녹음 컴포넌트 불러오기

st.title("Custom Audio Recorder")

# st_mic 컴포넌트를 호출하여 오디오 데이터를 받음
audio_data = st_mic()

if audio_data:
    st.write("Received audio data:")
    st.audio(audio_data, format="audio/wav")

    # 파일을 .ogg로 저장
    file_path = 'audio.wav'
    with open(file_path, 'wb') as f:
        f.write(audio_data.getvalue())

    # 파일 경로 출력
    st.write("Saved audio file:", os.path.abspath(file_path))
