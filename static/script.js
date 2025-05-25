let ws;
document.getElementById("connectBtn").onclick = async () => {
  const res = await fetch("/start-stream");
  const { session_id, session_token, stream_url } = await res.json();
  ws = new WebSocket(`wss://api.d-id.com/streams/${session_id}?token=${session_token}`);

  const video = document.getElementById("avatar-video");
  const pc = new RTCPeerConnection();
  pc.ontrack = (event) => {
    [video.srcObject] = event.streams;
  };

  const offer = await pc.createOffer();
  await pc.setLocalDescription(offer);

  ws.onopen = () => {
    ws.send(JSON.stringify({ type: "offer", sdp: offer.sdp }));
  };

  ws.onmessage = async (msg) => {
    const data = JSON.parse(msg.data);
    if (data.type === "answer") {
      await pc.setRemoteDescription(new RTCSessionDescription(data));
    }
  };
};