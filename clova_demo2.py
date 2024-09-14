import streamlit as st
import os
from clova_speech_client import ClovaSpeechClient
from st_mic import st_mic
from audio_utils import convert_to_wav  # 변환 함수가 있는 모듈 import
import tempfile

st.title("CLOVA Speech API를 이용한 음성 텍스트 변환")

# st_mic를 사용하여 오디오 녹음
audio_data = st_mic()

if audio_data:
    st.write("오디오 데이터 수신 완료:")

    # 오디오 데이터의 MIME 타입과 확장자를 고정 값으로 설정
    mime_type = 'audio/ogg'
    extension = 'ogg'

    # 오디오 재생
    st.audio(audio_data.getvalue(), format=mime_type)

    # 오디오 데이터를 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{extension}') as tmp_input_file:
        tmp_input_file.write(audio_data.getvalue())
        tmp_input_file_path = tmp_input_file.name

    # 변환된 WAV 파일을 임시 파일로 생성
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_output_file:
        tmp_output_file_path = tmp_output_file.name

    # 오디오 파일을 WAV로 변환
    success, error_message = convert_to_wav(tmp_input_file_path, tmp_output_file_path)
    if not success:
        st.error("오디오 변환 중 오류가 발생했습니다.")
        st.write(error_message)
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
                if 'text' in result and result['text']:
                    transcription = result['text']
                elif 'segments' in result and len(result['segments']) > 0:
                    transcription = ' '.join([segment['text'] for segment in result['segments']])
                else:
                    transcription = '변환된 텍스트가 없습니다.'

                if transcription and transcription != '변환된 텍스트가 없습니다.':
                    st.success("Transcription Complete!")
                    st.text_area("Transcribed Text", transcription, height=200)
                else:
                    st.warning("변환된 텍스트가 없습니다.")
            else:
                st.error("An error occurred during transcription.")
                st.write(response.text)
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
