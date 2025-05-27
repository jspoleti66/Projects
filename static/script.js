let ws;
let streamId;

document.getElementById("start-button").onclick = async () => {
  const res = await fetch("/start-stream", { method: "POST" });
  const data = await res.json();
  streamId = data.id;

  const socketUrl = `wss://api.d-id.com/streams/${streamId}`;
  ws = new WebSocket(socketUrl);

  ws.onopen = () => {
    console.log("WebSocket conectado");
    document.getElementById("sendTextBtn").disabled = false;

    const video = document.getElementById("remoteVideo");
    video.src = `https://api.d-id.com/streams/${streamId}/video`;
  };

  ws.onmessage = (event) => {
    console.log("Mensaje recibido:", event.data);
  };
};

document.getElementById("sendTextBtn").onclick = () => {
  const text = document.getElementById("textInput").value;
  if (ws && text) {
    ws.send(JSON.stringify({ type: "text", text }));
  }
};
