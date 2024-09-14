import subprocess
import os

def convert_to_wav(input_file_path, output_file_path):
    """
    주어진 오디오 파일을 WAV 포맷으로 변환합니다.

    Parameters:
    - input_file_path (str): 변환할 원본 오디오 파일의 경로
    - output_file_path (str): 변환된 WAV 파일을 저장할 경로

    Returns:
    - bool: 변환 성공 여부
    - str: 오류 발생 시 오류 메시지
    """
    command = [
        'ffmpeg',
        '-y',  # 기존 파일 덮어쓰기
        '-i', input_file_path,  # 입력 파일
        '-ac', '1',             # 모노 채널
        '-ar', '16000',         # 샘플링 레이트 16kHz
        '-sample_fmt', 's16',   # 16비트 샘플 포맷
        output_file_path        # 출력 파일
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        error_message = result.stderr.decode()
        return False, error_message
    return True, ""
