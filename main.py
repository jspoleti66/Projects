<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Clon Parlante - AlmostMe</title>
  <script src="https://unpkg.com/@d-id/web-sdk"></script>
</head>
<body>
  <h1>Clon Parlante</h1>
  <input type="text" id="mensaje" placeholder="Escribí algo">
  <button onclick="enviar()">Enviar</button>

  <div id="talking-head" style="width: 400px; height: 400px;"></div>

  <script>
    const player = new DID.Player({
      element: document.getElementById('talking-head'),
      apiKey: "Y2VjYXJyaXpvZ0BnbWFpbC5jb20:KRphQ-Ulqibq5EpN8xj3f"
    });

    async function enviar() {
      const mensaje = document.getElementById('mensaje').value;

      const respuesta = await fetch("/clon", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mensaje })
      });
      const data = await respuesta.json();

      console.log("Respuesta:", data.respuesta);

      if (typeof player.play === "function") {
        player.play({
          script: {
            type: "text",
            input: data.respuesta,
            provider: {
              type: "microsoft",
              voice_id: "es-ES-AlvaroNeural"
            }
          },
          avatar: {
            type: "url",
            url: "https://create-images-results.d-id.com/DefaultPresentationFace_v2.png"
          }
        });
      } else {
        console.error("El player no tiene función .play()");
      }
    }
  </script>
</body>
</html>
