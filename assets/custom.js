let mediaRecorder;
let audioChunks = [];

async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        audioChunks = [];
        const formData = new FormData();
        formData.append("audio_file", audioBlob, "audio.webm");

        const response = await fetch('http://localhost:8000/handle_audio_chunk', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        Reflex.callEvent("set_transcribed_text", result.transcribed_text);
    };

    mediaRecorder.start();
}

function stopRecording() {
    mediaRecorder.stop();
}
