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
  const { streamId, offer, iceServers, sessionId } = data;

  const peerConnection = new RTCPeerConnection({ iceServers });

  peerConnection.ontrack = (event) => {
    videoElement.srcObject = event.streams[0];
  };

  peerConnection.onicecandidate = async (event) => {
    if (event.candidate) {
      await fetch(`https://api.d-id.com/streams/${streamId}/ice`, {
        method: "POST",
        headers: {
          Authorization: "Bearer WTJWallYSnlhWHB2WjBCbmJXRnBiQzVqYjIwOml6bTZaaEIzd29rQy1xUHBaVFlXSg==",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ candidate: event.candidate }),
      });
    }
  };

  await peerConnection.setRemoteDescription(offer);
  const answer = await peerConnection.createAnswer();
  await peerConnection.setLocalDescription(answer);

  await fetch(`https://api.d-id.com/streams/${streamId}/sdp`, {
    method: "POST",
    headers: {
      Authorization: "Bearer <YOUR_DID_API_KEY>",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ answer }),
  });
}
