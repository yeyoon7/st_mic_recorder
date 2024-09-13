// Streamlit 라이브러리 가져오기
import { Streamlit } from "streamlit-component-lib"

const mic_btn = document.querySelector('#mic');
const playback = document.querySelector('.playback');

mic_btn.addEventListener('click', ToggleMic);

let can_record = false;
let is_recording = false;
let recorder = null;
let chunks = [];

function SetupAudio() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices
            .getUserMedia({
                audio: true
            })
            .then(SetupStream)
            .catch((err) => {
                console.error(err);
            });
    }
}

// 오디오 스트림 설정
function SetupStream(stream) {
    recorder = new MediaRecorder(stream);

    recorder.ondataavailable = e => {
        chunks.push(e.data);
    }

    recorder.onstop = e => {
        const blob = new Blob(chunks, { type: 'audio/wav; codecs=opus' });
        chunks = [];
        const audioURL = window.URL.createObjectURL(blob);
        playback.src = audioURL;

        // 오디오 데이터를 base64로 변환하여 Streamlit에 전송
        const reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onloadend = function() {
            const base64data = reader.result;

            // Streamlit에 오디오 데이터를 전송
            Streamlit.setComponentValue(base64data);
        }

        // 오디오를 재생할 준비가 되었음을 알림
        Streamlit.setFrameHeight();
    }

    can_record = true;
}

// 녹음 시작/정지 기능
function ToggleMic() {
    if (!can_record) return;

    is_recording = !is_recording;

    if (is_recording) {
        recorder.start();
        mic_btn.classList.add('is-recording');
    } else {
        recorder.stop();
        mic_btn.classList.remove('is-recording');
    }
}

// 오디오 설정 초기화
SetupAudio();

// 컴포넌트가 준비되었음을 Streamlit에 알림
Streamlit.setComponentReady();

// 컴포넌트 높이 조정
Streamlit.setFrameHeight();