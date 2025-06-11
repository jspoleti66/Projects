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
    }, 100); // 10 fps
  } else {
    alert("Error: " + data.details);
  }
}
