async function startStream() {
  if (typeof DID === 'undefined') {
    document.getElementById('output').innerText = "Error: SDK de D-ID no cargado.";
    return;
  }

  try {
    const response = await fetch('/start-stream', {
      method: 'POST',
    });

    const data = await response.json();
    const streamUrl = data.stream_url;

    if (!streamUrl) {
      document.getElementById('output').innerText = "Error: " + JSON.stringify(data);
      return;
    }

    document.getElementById('output').innerText = "Avatar parlante cargado correctamente.";
    const iframe = document.getElementById('streamFrame');
    iframe.style.display = "block";
    iframe.src = streamUrl;

  } catch (err) {
    document.getElementById('output').innerText = "Error: " + err.message;
  }
}
