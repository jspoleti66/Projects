const startBtn = document.getElementById("start-btn");
const output = document.getElementById("output");
const video = document.getElementById("talk-video");

let peerConnection;

startBtn.onclick = async () => {
  output.innerText = "Creando talk y negociando WebRTC...";

  try {
    // 1. Crear talk en backend y obtener talkId
    const resTalk = await fetch('/start-talk', { method: 'POST' });
    const dataTalk = await resTalk.json();

    if (dataTalk.error) {
      output.innerText = "Error: " + dataTalk.error;
      return;
    }

    const talkId = dataTalk.talk_id;
    output.innerText = `Talk creado con ID: ${talkId}`;

    // 2. Pedir SDP offer para WebRTC
    const resOffer = await fetch(`/webrtc-offer/${talkId}`);
    const offerData = await resOffer.json();

    if (!offerData.sdp) {
      output.innerText = "Error: no se recibió SDP offer";
      return;
    }

    // 3. Crear RTCPeerConnection
    peerConnection = new RTCPeerConnection();

    // Cuando recibimos el stream remoto, asignamos al video
    peerConnection.ontrack = (event) => {
      video.srcObject = event.streams[0];
    };

    // Establecemos la oferta SDP recibida
    await peerConnection.setRemoteDescription(new RTCSessionDescription({type: "offer", sdp: offerData.sdp}));

    // Creamos la respuesta SDP (answer)
    const answer = await peerConnection.createAnswer();
    await peerConnection.setLocalDescription(answer);

    // 4. Enviamos la respuesta SDP al backend para completar la negociación
    const resAnswer = await fetch(`/webrtc-answer/${talkId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sdp: peerConnection.localDescription.sdp }),
    });

    const answerResult = await resAnswer.json();
    if (answerResult.error) {
      output.innerText = "Error al enviar respuesta SDP: " + answerResult.error;
      return;
    }

    output.innerText = "Streaming en vivo iniciado.";

    // 5. Manejar candidatos ICE
    peerConnection.onicecandidate = async (event) => {
      if (event.candidate) {
        await fetch(`/webrtc-candidate/${talkId}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ candidate: event.candidate }),
        });
      }
    };

  } catch (error) {
    output.innerText = "Error: " + error.message;
  }
};
