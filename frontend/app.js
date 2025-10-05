const backendBase = (function(){
  // Auto-detect backend base: assume same host with port 8000 if served statically.
  const url = new URL(window.location.href);
  // If served from a static host, set your backend URL here or rely on config.
  // For local dev with docker-compose: http://localhost:8000
  if (url.hostname === 'localhost' || url.hostname === '127.0.0.1') {
    return 'http://localhost:8000';
  }
  // Default: call backend at same origin (if backend serves frontend)
  return window.__BACKEND_BASE__ || (window.location.origin);
})();

document.addEventListener('DOMContentLoaded', () => {
  const micBtn = document.getElementById('micBtn');
  const sendBtn = document.getElementById('sendBtn');
  const clearBtn = document.getElementById('clearBtn');
  const input = document.getElementById('textInput');
  const history = document.getElementById('history');

  let recognition = null;
  let listening = false;
  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SR();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.onresult = (e) => {
      const t = e.results[0][0].transcript;
      input.value = t;
      addBubble('user', t);
      sendText(t);
    };
    recognition.onerror = (e) => console.error('rec err', e);
    recognition.onend = () => { listening = false; micBtn.textContent = '🎤 Start Voice'; }
  } else {
    micBtn.disabled = true;
    micBtn.textContent = 'Voice not supported';
  }

  micBtn.onclick = () => {
    if (!recognition) return;
    if (!listening) {
      listening = true;
      recognition.start();
      micBtn.textContent = '⏹️ Stop';
    } else {
      recognition.stop();
      listening = false;
      micBtn.textContent = '🎤 Start Voice';
    }
  };

  sendBtn.onclick = () => {
    const t = input.value.trim();
    if (!t) return;
    addBubble('user', t);
    sendText(t);
    input.value = '';
  };

  clearBtn.onclick = () => { history.innerHTML = ''; };

  function addBubble(kind, text) {
    const d = document.createElement('div');
    d.className = 'bubble ' + (kind === 'user' ? 'user' : 'bot');
    d.textContent = text;
    history.appendChild(d);
    history.scrollTop = history.scrollHeight;
  }

  async function sendText(text) {
    try {
      const res = await fetch(backendBase + '/chat', {
        method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({text})
      });
      const j = await res.json();
      const reply = j.text || (j.error ? 'Error: '+j.error : 'No reply');
      addBubble('bot', reply);
      speak(reply);
    } catch (e) {
      console.error(e);
      addBubble('bot', 'Network error — make sure the backend is running.');
    }
  }

  function speak(text) {
    if ('speechSynthesis' in window) {
      const u = new SpeechSynthesisUtterance(text);
      u.lang = 'en-US';
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(u);
    }
  }
});
