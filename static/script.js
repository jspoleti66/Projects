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

    // Puedes guardar session si querés luego controlarlo (detener, mutear, etc.)
  } catch (err) {
    output.innerText = "Error: " + err.message;
  }
}
