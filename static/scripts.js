async function startStream() {
  const apiKey = "WTJWallYSnlhWHB2WjBCbmJXRnBiQzVqYjIwOml6bTZaaEIzd29rQy1xUHBaVFlXSg=="; // Tu API key en Base64

  const response = await fetch("https://api.d-id.com/talks/streams", {
    method: "POST",
    headers: {
      "Authorization": `Basic ${apiKey}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      source_url: "https://raw.githubusercontent.com/jspoleti66/Projects/main/static/AlmostMe.png",
      driver_url: "bank://lively"
    })
  });

  const result = await response.json();
  console.log(result);

  document.getElementById("result").innerText = response.ok
    ? `Stream ID: ${result.id}`
    : `Error: ${result.error}`;
}
