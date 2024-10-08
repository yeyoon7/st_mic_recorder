import { Streamlit, RenderData } from "streamlit-component-lib";

// Get the UI elements from the pre-defined index.html
const mic_btn = document.querySelector('#mic') as HTMLButtonElement;
const playback = document.querySelector('.playback') as HTMLAudioElement;

let can_record = false;
let is_recording = false;
let recorder: MediaRecorder | null = null;
let chunks: Blob[] = [];

// Set up the audio stream
function SetupAudio() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({
            audio: true
        })
        .then(SetupStream)
        .catch((err) => {
            console.error('Error accessing microphone:', err);
        });
    }
}

// Initialize the media recorder
function SetupStream(stream: MediaStream) {
    // Specify the correct MIME type (ogg or webm for Opus)
    recorder = new MediaRecorder(stream);

    recorder.ondataavailable = (e: BlobEvent) => {
        chunks.push(e.data);
    };

    recorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/ogg' });  // Save in ogg format
        chunks = [];
        const audioURL = window.URL.createObjectURL(blob);
        console.log(audioURL);  // URL을 콘솔에 출력
        playback.src = audioURL;

        // Convert audio blob to byte array (ArrayBuffer) and send to Streamlit
        blob.arrayBuffer().then((arrayBuffer) => {
            // Convert ArrayBuffer to a Uint8Array (byte array)
            const byteArray = new Uint8Array(arrayBuffer);
            const mimeType = blob.type;  // 'audio/ogg; codecs=opus'
            const extension = 'ogg';  // 이미 ogg로 설정되어 있으므로 그대로 사용

            // Send byte array to Streamlit
            Streamlit.setComponentValue({
                byteArray: Array.from(byteArray),
                extension: extension,
                mimeType: mimeType,
                isRecording: false});

            // Notify Streamlit that the component frame height should be updated
            Streamlit.setFrameHeight();
        });
    };

    can_record = true;
}

// Toggle recording on/off
function ToggleMic() {
    if (!can_record) return;

    is_recording = !is_recording;

    if (is_recording) {
        recorder?.start();
        mic_btn.classList.add('is-recording');
        // 녹음이 시작될 때 isRecording을 true로 설정
        Streamlit.setComponentValue({
            isRecording: true  // 녹음 시작
        });
    } else {
        recorder?.stop();
        mic_btn.classList.remove('is-recording');
    }
}

// Add click event listener to the mic button
mic_btn.addEventListener('click', ToggleMic);

// Set up audio when the component is loaded
SetupAudio();

// Handle Streamlit's render events
function onRender(event: Event): void {
    const data = (event as CustomEvent<RenderData>).detail;

    // Optionally adjust styles based on Streamlit's theme
    if (data.theme) {
        const borderStyling = `0px solid ${data.theme.primaryColor}`;
        mic_btn.style.border = borderStyling;
        mic_btn.style.outline = borderStyling;
    }

    // Notify Streamlit of the component's frame height change
    Streamlit.setFrameHeight();
}

// Listen for Streamlit render events
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);

// Notify Streamlit that the component is ready
Streamlit.setComponentReady();

// Set initial frame height
Streamlit.setFrameHeight();
