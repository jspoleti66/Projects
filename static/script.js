import DID from "https://cdn.jsdelivr.net/npm/@d-id/web-sdk@latest/dist/index.min.js";

const startBtn = document.getElementById("start-btn");
const output = document.getElementById("output");
const video = document.getElementById("talk-video");

let client;

startBtn.onclick = async () => {
  output.innerText = "Iniciando talk...";

  try {
    const res = await fetch('/start-talk', { method: 'POST' });
    const data = await res.json();

    if (data.error) {
      output.innerText = "Error: " + data.error;
      return;
    }

    const talkId = data.talk_id;
    output.innerText = "Talk creado: " + talkId;

    // Crear cliente D-ID WebRTC
    client = new DID.WebRTCClient();

    client.on('play', () => {
      output.innerText = "Streaming en vivo...";
    });

    client.on('error', (err) => {
      output.innerText = "Error streaming: " + err.message;
    });

    // Conectar y reproducir stream
    await client.connect(talkId);

    // Poner el stream en el video tag
    video.srcObject = client.getMediaStream();

  } catch (err) {
    output.innerText = "Error: " + err.message;
  }
};
