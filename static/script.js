async function startStream() {
  const output = document.getElementById('output');
  const iframe = document.getElementById('streamFrame');
  output.textContent = 'Generando...';
  iframe.style.display = 'none';

  try {
    const res = await fetch('/start-stream', { method: 'POST' });
    const data = await res.json();

    if (res.ok && data.stream_url) {
      output.textContent = 'Avatar parlante cargado correctamente.';
      iframe.src = data.stream_url;
      iframe.style.display = 'block';
    } else {
      output.textContent = `Error: ${JSON.stringify(data)}`;
    }
  } catch (err) {
    output.textContent = `Error: ${err.message}`;
  }
}
