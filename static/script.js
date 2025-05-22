document.getElementById("startBtn").onclick = async () => {
  const output = document.getElementById("output");
  try {
    const response = await fetch("/start-stream", { method: "POST" });
    const data = await response.json();

    if (!data.stream_url) {
      output.innerText = "Error: " + JSON.stringify(data);
      return;
    }

    output.innerText = "Clon parlante iniciado.";
    const iframe = document.getElementById("streamFrame");
    iframe.src = data.stream_url;
    iframe.style.display = "block";
  } catch (err) {
    output.innerText = "Error: " + err.message;
  }
};
