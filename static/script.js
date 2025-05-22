async function startStream() {
  const output = document.getElementById('output');
  output.innerText = "Solicitando stream...";

  try {
    const res = await fetch('/start-stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });

    const data = await res.json();

    if (!data.id) {
      output.innerText = "Error: no se pudo obtener el ID del stream.";
      console.error("Respuesta inválida del backend:", data);
      return;
    }

    output.innerText = "Conectando al avatar parlante...";

    // Verificamos si el SDK está cargado
    if (!window.DId || !DId.createStream) {
      output.innerText = "Error: SDK de D-ID no cargado.";
      return;
    }

    const canvas = document.getElementById('avatarCanvas');

    const stream = await DId.createStream({
      streamId: data.id,
      container: canvas
    });

    stream.play();

    output.innerText = "Avatar parlante conectado con éxito.";

  } catch (error) {
    output.innerText = "Error al iniciar el stream.";
    console.error("Error en startStream():", error);
  }
}
