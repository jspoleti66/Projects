const video = document.getElementById("videoElement");

document.getElementById("connectBtn").onclick = async () => {
  const res = await fetch("/start-stream", { method: "POST" });
  const data = await res.json();
  console.log("Respuesta completa de /start-stream:", data);

  const streamId = data.id;
  const offer = data.offer;
  const iceServers = data.ice_servers;

  const pc = new RTCPeerConnection({ iceServers });
  pc.ontrack = (event) => {
    video.srcObject = event.streams[0];
  };

  await pc.setRemoteDescription(offer);
  const answer = await pc.createAnswer();
  await pc.setLocalDescription(answer);

  await fetch(`https://api.d-id.com/streams/${streamId}/sdp`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ answer }),
  });

  const ws = new WebSocket(`wss://api.d-id.com/streams/${streamId}`);
  ws.onopen = () => {
    document.getElementById("sendTextBtn").disabled = false;
    console.log("WebSocket conectado");
  };
  ws.onmessage = (event) => {
    console.log("Mensaje:", event.data);
  };

  document.getElementById("sendTextBtn").onclick = () => {
    const text = document.getElementById("textInput").value;
    if (text) {
      ws.send(JSON.stringify({ type: "text", text }));
    }
  };
};
