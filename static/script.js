let ws;
let streamId;
let pc;

document.getElementById("connectBtn").onclick = async () => {
  try {
    const res = await fetch("/start-stream", { method: "POST" });
    const data = await res.json();
    console.log("✅ Respuesta de /start-stream:", data);

    if (!data.id || !data.ice_servers || !data.offer) {
      console.error("❌ Datos incompletos o error:", data);
      return;
    }

    streamId = data.id;

    pc = new RTCPeerConnection({
      iceServers: data.ice_servers,
    });

    const video = document.getElementById("videoElement");
    pc.ontrack = (event) => {
      if (video.srcObject !== event.streams[0]) {
        console.log("🎥 Recibiendo video track");
        video.srcObject = event.streams[0];
      }
    };

    const offer = await pc.createOffer();
    await pc.setLocalDescription(offer);
    console.log("📡 Enviando offer:", offer.sdp);

    const offerRes = await fetch("/send-offer", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        stream_id: streamId,
        offer: offer.sdp
      })
    });

    const answerData = await offerRes.json();
    console.log("📨 Respuesta SDP:", answerData);

    await pc.setRemoteDescription({
      type: "answer",
      sdp: answerData.sdp
    });

    document.getElementById("sendTextBtn").disabled = false;

    ws = new WebSocket(`wss://api.d-id.com/streams/${streamId}`);
    ws.onopen = () => {
      console.log("🔗 WebSocket conectado");
    };
    ws.onmessage = (event) => {
      console.log("📥 Mensaje WebSocket:", event.data);
    };

  } catch (err) {
    console.error("❗ Error al iniciar conexión:", err);
  }
};

document.getElementById("sendTextBtn").onclick = () => {
  const text = document.getElementById("textInput").value;
  if (ws && text) {
    console.log("✉️ Enviando texto:", text);
    ws.send(JSON.stringify({ type: "text", text }));
  }
};
