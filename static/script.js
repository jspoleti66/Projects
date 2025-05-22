async function startStream() {
    const response = await fetch("/start-stream", { method: "POST" });
    const data = await response.json();
    const streamId = data.stream_id;

    if (!streamId) {
        console.error("Error al iniciar el stream:", data);
        return;
    }

    const socket = new WebSocket(`wss://api.d-id.com/streams/${streamId}`);

    const pc = new RTCPeerConnection();

    pc.ontrack = (event) => {
        const video = document.getElementById("talk-video");
        video.srcObject = event.streams[0];
    };

    const offer = await pc.createOffer();
    await pc.setLocalDescription(offer);

    socket.onopen = () => {
        socket.send(JSON.stringify({ type: "offer", sdp: offer.sdp }));
    };

    socket.onmessage = async (event) => {
        const message = JSON.parse(event.data);

        if (message.type === "answer") {
            const remoteDesc = new RTCSessionDescription({ type: "answer", sdp: message.sdp });
            await pc.setRemoteDescription(remoteDesc);
        }

        if (message.candidate) {
            try {
                await pc.addIceCandidate(message);
            } catch (e) {
                console.error("Error al agregar candidato ICE", e);
            }
        }
    };

    pc.onicecandidate = (event) => {
        if (event.candidate) {
            socket.send(JSON.stringify({ type: "candidate", candidate: event.candidate }));
        }
    };
}
