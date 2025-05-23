const videoElement = document.getElementById("talking-video");

async function startStream() {
  const peerConnection = new RTCPeerConnection({
    iceServers: [{ urls: "stun:stun.l.google.com:19302" }]
  });

  let streamId = null;

  peerConnection.ontrack = (event) => {
    videoElement.srcObject = event.streams[0];
  };

  peerConnection.onicecandidate = async (event) => {
    if (event.candidate && streamId) {
      await fetch("/send_ice_candidate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: "Hola, soy tu clon AlmostMe"
        }),
      });
    }
  };

  const offer = await peerConnection.createOffer();
  await peerConnection.setLocalDescription(offer);

  const response = await fetch("/create_stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      sdpOffer: peerConnection.localDescription
    }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    alert("Error al iniciar el stream: " + JSON.stringify(errorData));
    return;
  }

  const data = await response.json();
  streamId = data.streamId;

  await peerConnection.setRemoteDescription(new RTCSessionDescription(data.sdp));
}
