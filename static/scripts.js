window.agenteListo = false;

// Escuchar cuando el agente D-ID esté listo
window.addEventListener("message", (event) => {
  if (event.data?.type === "agent-ready") {
    console.log("🟢 Agente D-ID listo");
    window.agenteListo = true;
  }
});

document.getElementById("formulario").addEventListener("submit", async (e) => {
  e.preventDefault();

  const userInput = document.getElementById("inputTexto").value;
  const respuestaDiv = document.getElementById("respuesta");
  respuestaDiv.textContent = "Pensando...";

  try {
    const response = await fetch("/clon", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mensaje: userInput })
    });

    const data = await response.json();
    const respuestaTexto = data.respuesta;

    respuestaDiv.textContent = respuestaTexto;

    // Enviar la respuesta al agente para que hable
    if (window.agenteListo) {
      window.postMessage({
        type: "agent-action",
        action: "speak",
        text: respuestaTexto
      }, "*");
    } else {
      console.warn("El agente D-ID aún no está listo para hablar.");
    }

  } catch (error) {
    console.error("❌ Error al obtener respuesta del clon:", error);
    respuestaDiv.textContent = "Error al obtener respuesta.";
  }
});
