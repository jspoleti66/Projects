async function startStream() {
  const output = document.getElementById('output');
  output.textContent = 'Cargando...';

  try {
    const res = await fetch('/start-stream', {
      method: 'POST'
    });

    const data = await res.json();

    if (res.ok) {
      output.textContent = JSON.stringify(data, null, 2);
    } else {
      output.textContent = `Error: ${JSON.stringify(data)}`;
    }
  } catch (err) {
    output.textContent = `Error: ${err.message}`;
  }
}
