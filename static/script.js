const startBtn = document.getElementById("startBtn");
const video = document.getElementById("video");

let pc = null;
let streamId = null;

startBtn.onclick = async () => {
  startBtn.disabled = true;

  // 1) Solicitar stream_id al backend
  const startResp = await fetch("/start-stream", { method: "POST" });
  const startData = await startResp.json();
  if (startData.error) {
    alert("Error al iniciar stream: " + startData.error);
    startBtn.disabled = false;
    return;
  }
  streamId = startData.stream_id;

  // 2) Crear RTCPeerConnection
  pc = new RTCPeerConnection({
    iceServers: [{ urls: "stun:stun.l.google.com:19302" }],
  });

  pc.onicecandidate = async (event) => {
    if (event.candidate === null) {
      // Cuando ya no hay más candidatos, enviar SDP offer al backend
      const offer = pc.localDescription.sdp;
      const resp = await fetch(`/webrtc-offer/${streamId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sdpOffer: offer }),
      });
      const data = await resp.json();
      if (data.error) {
        alert("Error en SDP answer: " + data.error);
        startBtn.disabled = false;
        return;
      }
      // Aplicar SDP answer recibido
      await pc.setRemoteDescription({ type: "answer", sdp: data.sdpAnswer });
    }
  };

  pc.ontrack = (event) => {
    video.srcObject = event.streams[0];
  };

  // 3) Crear oferta SDP y añadir track vacío (no media local)
  pc.addTransceiver("video", { direction: "recvonly" });
  pc.addTransceiver("audio", { direction: "recvonly" });

  const offerDesc = await pc.createOffer();
  await pc.setLocalDescription(offerDesc);
};
