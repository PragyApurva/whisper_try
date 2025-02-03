// script.js
const recordButton = document.getElementById('recordButton');
const stopButton = document.getElementById('stopButton');
const responseText = document.getElementById('responseText');

let mediaRecorder;
let audioChunks = [];
let socket;

// Initialize WebSocket connection
function initWebSocket() {
    socket = new WebSocket('ws://localhost:8000/transcribe');

    socket.onopen = () => {
        console.log('WebSocket connection established');
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        responseText.innerText = data.response;
    };

    socket.onclose = () => {
        console.log('WebSocket connection closed');
    };
}

// Start recording audio
recordButton.addEventListener('click', async () => {
    audioChunks = [];
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
        // Specify WAV format explicitly
        const audioBlob = new Blob(audioChunks, { 
            type: 'audio/wav; codecs=MS_PCM'
        });
        const reader = new FileReader();
        reader.readAsDataURL(audioBlob);
        reader.onloadend = () => {
            const base64Audio = reader.result.split(',')[1];
            socket.send(JSON.stringify({ audio: base64Audio }));
        };
    };

    mediaRecorder.start();
    recordButton.disabled = true;
    stopButton.disabled = false;
});

// Stop recording audio
stopButton.addEventListener('click', () => {
    mediaRecorder.stop();
    recordButton.disabled = false;
    stopButton.disabled = true;
});

// Initialize WebSocket on page load
window.onload = initWebSocket;