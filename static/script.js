const startBtn = document.getElementById('startBtn');
const output = document.getElementById('output');
const remoteVideo = document.getElementById('remoteVideo');

let pc;

startBtn.onclick = async () => {
  output.innerText = "Inicializando...";
  const res = await fetch('/start-stream', { method: 'POST' });
  const data = await res.json();

  if (!data.talk_id) {
    output.innerText = "Error al crear stream: " + JSON.stringify(data);
    return;
  }

  const talkId = data.talk_id;
  output.innerText = "Streaming iniciado. Negociando conexión...";

  pc = new RTCPeerConnection();

  pc.ontrack = (event) => {
    remoteVideo.srcObject = event.streams[0];
  };

  pc.onicecandidate = async (event) => {
    if (event.candidate) return;

    const offer = await pc.createOffer();
    await pc.setLocalDescription(offer);

    const res = await fetch(`/webrtc-offer/${talkId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sdp: offer.sdp })
    });

    const data = await res.json();
    if (!data.sdp) {
      output.innerText = "Error: No se recibió SDP answer";
      return;
    }

    await pc.setRemoteDescription({ type: 'answer', sdp: data.sdp });
    output.innerText = "Conexión establecida.";
  };

  pc.addTransceiver('video', { direction: 'recvonly' });
};
