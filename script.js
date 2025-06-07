const canvas = document.getElementById("faceCanvas");
const ctx = canvas.getContext("2d");
canvas.width = 512;
canvas.height = 768;

const img = new Image();
img.src = "AlmostMe.png";

let isMouthOpen = false;

img.onload = () => {
  drawFace();
};

function drawFace() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

  if (isMouthOpen) {
    // Boca simulada
    ctx.fillStyle = "#222";
    ctx.beginPath();
    ctx.ellipse(256, 520, 30, 18, 0, 0, 2 * Math.PI);
    ctx.fill();
  }
}

function speak() {
  isMouthOpen = true;
  drawFace();
  setTimeout(() => {
    isMouthOpen = false;
    drawFace();
  }, 2000); // Simula duración de "hablar"
}

document.getElementById("textInput").addEventListener("keydown", (e) => {
  if (e.key === "Enter" && e.target.value.trim() !== "") {
    speak();
    e.target.value = "";
  }
});
