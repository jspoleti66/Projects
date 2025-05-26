document.getElementById("start-button").onclick = async () => {
  try {
    const response = await fetch("/api/init", { method: "POST" });
    const data = await response.json();
    
    const streamId = data.streamId;
    const token = data.token;

    if (!streamId || !token) {
      console.error("Faltan streamId o token en la respuesta:", data);
      return;
    }

    console.log("Conectando a:", `wss://api.d-id.com/streams/${streamId}?token=${token}`);
    const socket = new WebSocket(`wss://api.d-id.com/streams/${streamId}?token=${token}`);

    socket.onopen = () => {
      console.log("WebSocket conectado.");
    };

    socket.onerror = (err) => {
      console.error("WebSocket error:", err);
    };

    // Video via MediaStream (opcional si D-ID responde con SDP que podés consumir)
    // Podés agregar aquí lógica de WebRTC para reproducir el stream en el <video>
  } catch (error) {
    console.error("Error al iniciar clon:", error);
  }
};
