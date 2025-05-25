let ws;
let streamId;

document.getElementById("connectBtn").onclick = async () => {
  const res = await fetch("/start-stream", { method: "POST" });
  const data = await res.json();
  streamId = data.id;

  ws = new WebSocket(`wss://api.d-id.com/streams/${streamId}`);
  ws.onopen = () => {
    document.getElementById("startBtn").disabled = false;
    document.getElementById("sendTextBtn").disabled = false;
    console.log("WebSocket connected");
  };
  ws.onmessage = (event) => {
    console.log("Message:", event.data);
  };
};

document.getElementById("startBtn").onclick = () => {
  const video = document.getElementById("videoElement");
  video.src = `https://api.d-id.com/streams/${streamId}/video`;
};

document.getElementById("sendTextBtn").onclick = () => {
  const text = document.getElementById("textInput").value;
  if (ws && text) {
    ws.send(JSON.stringify({ type: "text", text }));
  }
};