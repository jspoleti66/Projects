document.getElementById("animateBtn").addEventListener("click", async () => {
  const input = document.getElementById("inputText");
  const text = input.value.trim();
  const avatar = document.getElementById("avatarFrame");

  if (!text) {
    alert("Escribí algo para animar.");
    return;
  }

  // Limpiar estado previo
  input.disabled = true;
  avatar.src = "";
  avatar.alt = "Procesando animación...";
  document.getElementById("animateBtn").disabled = true;

  try {
    const res = await fetch("/animate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });

    const data = await res.json();
    if (data.status !== "ok") throw new Error(data.details);

    const session = data.session;
    let frame = 0;
    const fps = 15;
    const maxFrames = 100; // Corte de seguridad

    const updateFrame = async () => {
      const frameUrl = `/live_frames/${session}/${frame}.jpg?t=${Date.now()}`;
      try {
        const r = await fetch(frameUrl);
        if (!r.ok || frame >= maxFrames) {
          console.log("🎬 Animación completa");
          input.disabled = false;
          document.getElementById("animateBtn").disabled = false;
          return;
        }
        avatar.src = frameUrl;
        frame++;
        setTimeout(updateFrame, 1000 / fps);
      } catch (e) {
        console.warn("Error cargando frame:", e);
      }
    };

    updateFrame();
  } catch (err) {
    console.error("❌ Error al animar:", err);
    alert("Error al animar: " + err.message);
    input.disabled = false;
    document.getElementById("animateBtn").disabled = false;
  }
});
