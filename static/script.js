import { DID } from "https://cdn.jsdelivr.net/npm/@d-id/talks-sdk@latest/dist/talks.min.js";

async function startStream() {
  const output = document.getElementById('output');
  const videoElement = document.getElementById('talk-video');

  output.innerText = "Iniciando streaming...";

  try {
    const res = await fetch('/start-stream', { method: 'POST' });
    const data = await res.json();

    if (!data.id) {
      output.innerText = "Error al crear el stream: " + JSON.stringify(data);
      return;
    }

    const streamId = data.id;
    const session = await DID.createTalkStream({ streamId, videoElement });

    output.innerText = "Streaming iniciado correctamente.";
  } catch (err) {
    output.innerText = "Error: " + err.message;
  }
}
