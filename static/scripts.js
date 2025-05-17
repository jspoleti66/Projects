document.getElementById('chat-form').addEventListener('submit', async function (e) {
  e.preventDefault();
  const input = document.getElementById('user-input');
  const chatBox = document.getElementById('chat-box');

  const userText = input.value.trim();
  if (!userText) return;

  // Mostrar mensaje del usuario
  const userBubble = document.createElement('div');
  userBubble.className = 'bg-blue-600 p-2 rounded self-end';
  userBubble.textContent = userText;
  chatBox.appendChild(userBubble);

  input.value = '';
  chatBox.scrollTop = chatBox.scrollHeight;

  // Enviar al servidor
  const res = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: userText })
  });

  const data = await res.json();

  // Mostrar respuesta del clon
  const botBubble = document.createElement('div');
  botBubble.className = 'bg-gray-700 p-2 rounded self-start';
  botBubble.textContent = data.response;
  chatBox.appendChild(botBubble);

  chatBox.scrollTop = chatBox.scrollHeight;

  // Reproducir voz si disponible
  const utterance = new SpeechSynthesisUtterance(data.response);
  speechSynthesis.speak(utterance);
});
