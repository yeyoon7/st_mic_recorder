import streamlit as st
import os
from clova_speech_client import ClovaSpeechClient
from st_mic import st_mic
import tempfile
import subprocess 


st.title("CLOVA Speech API를 이용한 음성 텍스트 변환")

audio_data = st_mic()

if audio_data:
    st.write("오디오 데이터 수신 완료:")
    
    mime_type = "audio/ogg"
    extension = "ogg"

    st.audio(audio_data.getvalue(), format=mime_type)

    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{extension}') as tmp_input_file:
        tmp_input_file.write(audio_data.getvalue())
        tmp_input_file_path = tmp_input_file.name
        
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_output_file:
        tmp_output_file_path = tmp_output_file.name
        
    # ffmpeg 명령어 구성
    command = [
    'ffmpeg',
    '-y',  # 기존 파일 덮어쓰기
    '-i', tmp_input_file_path,  # 입력 파일
    '-ac', '1',                 # 모노 채널
    '-ar', '16000',             # 샘플링 레이트 16kHz
    '-sample_fmt', 's16',       # 16비트 샘플 포맷
    tmp_output_file_path        # 출력 파일
]

    #ffmpeg 실행
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        st.error("오디오 변환 중 오류가 발생했습니다.")
        st.write(result.stderr.decode())
        # 임시 파일 삭제
        os.remove(tmp_input_file_path)
        os.remove(tmp_output_file_path)
    else:
        # 변환된 파일을 API에 전달
        client = ClovaSpeechClient()
        st.info("Transcribing...")
        try:
            response = client.req_upload(tmp_output_file_path, completion='sync')
            # 임시 파일 삭제
            os.remove(tmp_input_file_path)
            os.remove(tmp_output_file_path)

            # API 응답 처리
            if response.status_code == 200:
                result = response.json()
                # 변환된 텍스트 추출
                transcription = result.get('text', '')
                if transcription:
                    st.success("Transcription Complete!")
                    st.text_area("Transcribed Text", transcription, height=200)
                else:
                    st.warning("변환된 텍스트가 없습니다.")
            else:
                st.error("An error occurred during transcription.")
                st.write(response.text)
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")