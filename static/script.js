const videoElement = document.getElementById("talking-video");

async function startStream() {
  const response = await fetch("/create_stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: "Hola, soy tu clon interactivo AlmostMe" }),
  });

  if (!response.ok) {
    alert("Error al iniciar el stream");
    return;
  }

  const data = await response.json();
  const { sdp, streamId, iceServers } = data;

  const peerConnection = new RTCPeerConnection({ iceServers });

  peerConnection.ontrack = (event) => {
    videoElement.srcObject = event.streams[0];
  };

  peerConnection.onicecandidate = async (event) => {
    if (event.candidate) {
      await fetch(`/send_ice_candidate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          streamId: streamId,
          candidate: event.candidate,
        }),
      });
    }
  };

  await peerConnection.setRemoteDescription(sdp);
  const answer = await peerConnection.createAnswer();
  await peerConnection.setLocalDescription(answer);

  await fetch(`/send_sdp_answer`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      streamId: streamId,
      answer: peerConnection.localDescription,
    }),
  });
}

