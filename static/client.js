document.getElementById("animateBtn").addEventListener("click", async () => {
  const text = document.getElementById("inputText").value.trim();
  if (!text) return alert("Escribí algo para animar.");

  const avatar = document.getElementById("avatarFrame");
  avatar.src = "";

  const res = await fetch("/animate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  const data = await res.json();
  if (data.status !== "ok") {
    alert("Error al animar: " + data.details);
    return;
  }

  const session = data.session;
  let frame = 0;
  const totalFrames = 64; // SadTalker genera típicamente hasta ~64 frames

  const updateFrame = () => {
    const frameName = `${frame}.jpg`;
    const frameUrl = `/live_frames/${session}/${frameName}?t=${Date.now()}`;
    fetch(frameUrl)
      .then((r) => {
        if (r.ok) {
          avatar.src = frameUrl;
          frame++;
          setTimeout(updateFrame, 1000 / 15); // 15 FPS
        } else {
          // Terminó la animación
        }
      })
      .catch(() => {});
  };

  updateFrame();
});
