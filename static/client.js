document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("inputText");
  const button = document.getElementById("animateBtn");
  const avatar = document.getElementById("avatarFrame");
  const status = document.getElementById("statusText");
  const spinner = document.getElementById("spinner");

  button.addEventListener("click", async () => {
    const text = input.value.trim();
    if (!text) return alert("Escribí algo para animar.");

    avatar.src = "";
    status.textContent = "Generando animación...";
    button.disabled = true;
    spinner.style.display = "inline-block";

    try {
      const res = await fetch("/animate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      const data = await res.json();
      if (data.status !== "ok") {
        status.textContent = "Error: " + data.details;
        button.disabled = false;
        spinner.style.display = "none";
        return;
      }

      const session = data.session;
      let frame = 0;

      const updateFrame = async () => {
        const frameUrl = `/live_frames/${session}/${frame}.jpg?t=${Date.now()}`;
        try {
          const r = await fetch(frameUrl);
          if (r.ok) {
            avatar.src = frameUrl;
            frame++;
            setTimeout(updateFrame, 1000 / 15); // 15 fps
          } else {
            status.textContent = "✅ Animación completa.";
            button.disabled = false;
            spinner.style.display = "none";
          }
        } catch {
          status.textContent = "❌ Error cargando frame.";
          button.disabled = false;
          spinner.style.display = "none";
        }
      };

      updateFrame();
    } catch (err) {
      status.textContent = "❌ Error inesperado: " + err.message;
      button.disabled = false;
      spinner.style.display = "none";
    }
  });
});
