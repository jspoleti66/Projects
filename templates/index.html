<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>AlmostMe - Demo</title>
  <style>
    body { font-family: sans-serif; padding: 2em; }
    #animation { max-width: 512px; margin-top: 20px; }
  </style>
</head>
<body>
  <h1>AlmostMe</h1>
  <input type="text" id="text" placeholder="Escribí algo..." value="Hola, soy tu clon" />
  <button onclick="animate()">Animar</button>

  <div id="animation"></div>

  <script>
    async function animate() {
      const text = document.getElementById("text").value;
      const response = await fetch("/animate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });
      const data = await response.json();

      if (data.status === "ok") {
        const session = data.session;
        const container = document.getElementById("animation");
        container.innerHTML = "";

        let index = 0;
        const maxFrames = 50; // ajustá según cuántos frames genere SadTalker
        const img = document.createElement("img");
        img.width = 512;
        container.appendChild(img);

        setInterval(() => {
          img.src = `/live_frames/${session}/${String(index).padStart(5, "0")}.jpg`;
          index = (index + 1) % maxFrames;
        }, 100); // 100 ms por frame (10 fps)
      } else {
        alert("Error: " + data.details);
      }
    }
  </script>
</body>
</html>
