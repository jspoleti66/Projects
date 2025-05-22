async function startTalk() {
  document.getElementById('output').innerText = "Solicitando video...";
  document.getElementById('video-container').innerHTML = "";

  try {
    const response = await fetch('/start-talk', {
      method: 'POST',
    });

    const data = await response.json();
    if (!data.id) {
      document.getElementById('output').innerText = "Error: " + JSON.stringify(data);
      return;
    }

    const talkId = data.id;

    const interval = setInterval(async () => {
      const statusResponse = await fetch(`/check-status/${talkId}`);
      const statusData = await statusResponse.json();

      if (statusData.status === 'done') {
        clearInterval(interval);
        document.getElementById('output').innerText = "Video listo.";

        const video = document.createElement("video");
        video.src = statusData.result_url;
        video.controls = true;
        video.autoplay = true;
        video.style.maxWidth = "100%";

        const container = document.getElementById("video-container");
        container.innerHTML = "";
        container.appendChild(video);
      } else if (statusData.status === 'error') {
        clearInterval(interval);
        document.getElementById('output').innerText = "Error al generar el video.";
      } else {
        document.getElementById('output').innerText = "Procesando...";
      }
    }, 2000);

  } catch (err) {
    document.getElementById('output').innerText = "Error: " + err.message;
  }
}
