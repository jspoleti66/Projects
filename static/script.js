let peerConnection;
document.getElementById("start-button").onclick = async () => {
  try {
    const response = await fetch("/api/init", { method: "POST" });
    const data = await response.json();
    
    const streamId = data.streamId;
    const token = data.token;

    if (!streamId || !token) {
      console.error("Faltan streamId o token en la respuesta:", data);
      return;
    }

    console.log("Conectando a:", `wss://api.d-id.com/streams/${streamId}?token=${token}`);
    const encodedToken = encodeURIComponent(token);
    const socket = new WebSocket(`wss://api.d-id.com/streams/${streamId}?token=${encodedToken}`);
    
    socket.onopen = () => {
      console.log("WebSocket conectado.");
    };

    socket.onmessage = async (event) => {
      const msg = JSON.parse(event.data);

      if (msg.type === "offer") {
        console.log("Recibido SDP offer:", msg);

        const config = {
          iceServers: [
            {
              urls: [
                "stun:stun.cloudflare.com:3478",
                "turn:turn.cloudflare.com:3478?transport=udp",
                "turn:turn.cloudflare.com:3478?transport=tcp",
                "turns:turn.cloudflare.com:5349?transport=tcp",
                "turn:turn.cloudflare.com:80?transport=tcp",
                "turns:turn.cloudflare.com:443?transport=tcp"
              ],
              username: "g0442535f9d1e8f0ee98823899be1bcbe84cc966baa34a49bfb77706c71e6c8c",
              credential: "20482627d9bc784e1a56535f5add2d9179e4456a5b5f2fe324b174b4bc758b3c"
            }
          ]
        };

        peerConnection = new RTCPeerConnection(config);

        peerConnection.ontrack = (event) => {
          const remoteVideo = document.getElementById("remoteVideo");
          if (remoteVideo.srcObject !== event.streams[0]) {
            remoteVideo.srcObject = event.streams[0];
            console.log("Video conectado");
          }
        };

        peerConnection.onicecandidate = (event) => {
          if (event.candidate) {
            socket.send(JSON.stringify({ type: "candidate", candidate: event.candidate }));
          }
        };

        await peerConnection.setRemoteDescription(new RTCSessionDescription(msg));
        const answer = await peerConnection.createAnswer();
        await peerConnection.setLocalDescription(answer);
        socket.send(JSON.stringify({ type: "answer", sdp: answer.sdp }));
        console.log("Respuesta enviada");
      }

      if (msg.type === "candidate") {
        try {
          await peerConnection.addIceCandidate(new RTCIceCandidate(msg.candidate));
          console.log("ICE candidate agregado");
        } catch (e) {
          console.error("Error al agregar ICE candidate:", e);
        }
      }
    };

    
    socket.onerror = (err) => {
      console.error("WebSocket error:", err);
    };

    // Video via MediaStream (opcional si D-ID responde con SDP que podés consumir)
    // Podés agregar aquí lógica de WebRTC para reproducir el stream en el <video>
  } catch (error) {
    console.error("Error al iniciar clon:", error);
  }
};
