import os
import streamlit.components.v1 as components
import streamlit as st
from io import BytesIO

# 개발 중인지 배포 중인지 여부를 나타내는 변수
_RELEASE = True

# Streamlit 컴포넌트 선언
if not _RELEASE:
    _component_func = components.declare_component(
        "st_mic",  # 컴포넌트 이름
        url="http://localhost:3001",  # 개발 중일 때는 npm 서버의 URL 사용
    )
else:
    # 배포 시 컴포넌트 빌드 경로 설정
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_mic", path=build_dir)

# 텍스트 중앙 정렬을 위한 CSS 추가
def apply_centered_text_css():
    st.markdown(
        """
        <style>
        .stAlert p {
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# 오디오 녹음 컴포넌트를 위한 래퍼 함수
def st_mic(key=None):
    """Create a new instance of the audio recorder component.

    Parameters
    ----------
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    BytesIO
        The recorded audio data as a byte stream.
    """
    # 컴포넌트를 호출하고 데이터 받아오기
    component_value = _component_func(key=key)
    
    apply_centered_text_css()
    
    if component_value is None:
        st.error("마이크 버튼을 누르면 녹음이 시작됩니다.")
        return None

    
    # 딕셔너리에서 byteArray 추출
    if isinstance(component_value, dict):
        byte_array = component_value.get("byteArray")
        is_recording = component_value.get("isRecording", False)
        
        # 상태 확인을 위한 디버깅
        #st.write(f"Is recording: {is_recording}, Byte array: {byte_array}")
        
        if byte_array:

            if isinstance(byte_array, list):
                # byteArray가 list일 경우 이를 bytes로 변환
                byte_array = bytes(byte_array)

            if isinstance(byte_array, (bytes, bytearray)):
                # 바이트 데이터를 BytesIO로 변환
                audio_data = BytesIO(byte_array)
                st.success("녹음이 완료되었습니다.")
                return audio_data
            else:
                st.error("Invalid byteArray or missing data.")

        if is_recording: # 녹음 중일 때
            st.info("녹음이 끝나면 마이크를 한 번 더 눌러주세요.")
        else: # 녹음 전일 때
            st.error("마이크 버튼을 누르면 녹음이 시작됩니다.")
            
    return None