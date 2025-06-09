
function sendText() {
    const text = document.getElementById("textInput").value;
    fetch("/animate", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({text})
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("response").innerText = JSON.stringify(data, null, 2);
    });
}
