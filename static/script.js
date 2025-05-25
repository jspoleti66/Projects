let socket;
let streamId = null;
let token = null;

document.getElementById("connectBtn").onclick = async () => {
  const res = await fetch("/api/init", { method: "POST" });
  const data = await res.json();
  streamId = data.streamId;
  token = data.token;

  const videoElement = document.getElementById("videoElement");
  const wsUrl = `wss://api.d-id.com/streams/${streamId}?token=${token}`;
  socket = new WebSocket(wsUrl);
  socket.onmessage = (event) => {
    if (event.data instanceof Blob) {
      videoElement.src = URL.createObjectURL(event.data);
    }
  };
};

document.getElementById("startBtn").onclick = async () => {
  const text = "Hola, soy AlmostMe, un clon parlante.";
  await fetch("/api/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ streamId, text }),
  });
};
