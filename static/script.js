async function startStream() {
  try {
    const res = await fetch("/start-stream", {
      method: "POST",
    });
    const data = await res.json();
    if (data.stream_url) {
      const video = document.getElementById("avatar");
      video.src = data.stream_url;
      video.play();
    } else {
      console.error("Error al obtener stream_url:", data);
      alert("Error iniciando el clon parlante.");
    }
  } catch (err) {
    console.error("Error en startStream:", err);
    alert("Error al conectar con el backend.");
  }
}
