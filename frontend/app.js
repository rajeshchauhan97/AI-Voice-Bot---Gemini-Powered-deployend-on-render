const backendBase = (function(){
  const url = new URL(window.location.href);
  if (url.hostname === 'localhost' || url.hostname === '127.0.0.1') {
    return 'http://localhost:8000';
  }
  return window.__BACKEND_BASE__ || window.location.origin;
})();

// Personal responses - modify these with YOUR actual responses
const PERSONAL_RESPONSES = {
  "life_story": "I grew up curious about how things work, which led me to technology and problem-solving. My journey has been about continuous learning and adapting to challenges while staying true to my core values. I believe in making meaningful connections and creating positive impact through my work.",
  
  "superpower": "My #1 superpower is connecting seemingly unrelated ideas to create innovative solutions. I can see patterns where others see chaos and translate complex concepts into simple, actionable insights that help teams move forward effectively.",
  
  "growth_areas": "The top 3 areas I'm focused on growing are: 1) Strategic leadership and vision-setting, 2) Advanced technical skills in emerging technologies, and 3) Building deeper empathy and emotional intelligence in my collaborations.",
  
  "misconception": "People often think I'm extremely extroverted because I'm comfortable speaking up, but I'm actually quite introverted and need quiet time to recharge. They also might not realize how much reflection goes into my quick decisions.",
  
  "boundaries": "I consistently push my limits by taking on projects that scare me just enough to be motivating. I seek honest feedback, practice deliberate learning outside my expertise, and regularly step into roles that require skills I haven't fully mastered yet."
};

// Fallback responses for unexpected questions
const FALLBACK_RESPONSES = [
  "That's an interesting question. Based on what I know about myself, I'd probably say...",
  "I haven't thought about that exact question before, but if I were to reflect on it...",
  "That's not something I get asked often. Let me think about how I'd approach that...",
  "I'd need to consider that carefully, but my initial perspective would be..."
];

document.addEventListener('DOMContentLoaded', () => {
  const micBtn = document.getElementById('micBtn');
  const sendBtn = document.getElementById('sendBtn');
  const clearBtn = document.getElementById('clearBtn');
  const input = document.getElementById('textInput');
  const history = document.getElementById('history');

  // Add quick question buttons
  addQuickQuestionButtons();

  let recognition = null;
  let listening = false;

  // Voice recognition setup
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
    recognition.onerror = (e) => console.error('Speech recognition error', e);
    recognition.onend = () => {
      listening = false;
      micBtn.textContent = '🎤 Start Voice';
      micBtn.classList.remove('listening');
    };
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
      micBtn.classList.add('listening');
    } else {
      recognition.stop();
      listening = false;
      micBtn.textContent = '🎤 Start Voice';
      micBtn.classList.remove('listening');
    }
  };

  sendBtn.onclick = () => {
    const t = input.value.trim();
    if (!t) return;
    addBubble('user', t);
    sendText(t);
    input.value = '';
  };

  input.onkeypress = (e) => {
    if (e.key === 'Enter') {
      sendBtn.onclick();
    }
  };

  clearBtn.onclick = () => { 
    history.innerHTML = ''; 
    // Add welcome message back after clearing
    setTimeout(() => {
      addBubble('bot', "Hi! I'm here to share my personal journey and experiences. Ask me about my life story, superpowers, growth areas, or anything else you're curious about!");
    }, 100);
  };

  function addQuickQuestionButtons() {
    const questions = [
      "What should we know about your life story?",
      "What's your #1 superpower?",
      "What are your top 3 growth areas?",
      "What misconception do people have about you?",
      "How do you push your boundaries?"
    ];

    const container = document.createElement('div');
    container.className = 'quick-questions';
    container.innerHTML = '<h3>Quick Questions:</h3>';
    
    questions.forEach(question => {
      const btn = document.createElement('button');
      btn.className = 'question-btn';
      btn.textContent = question;
      btn.onclick = () => {
        input.value = question;
        sendBtn.onclick();
      };
      container.appendChild(btn);
    });

    // Insert after history and before input area
    const inputArea = document.querySelector('.input-area');
    inputArea.parentNode.insertBefore(container, inputArea);
  }

  function addBubble(kind, text) {
    const d = document.createElement('div');
    d.className = 'bubble ' + (kind === 'user' ? 'user' : 'bot');
    d.textContent = text;
    history.appendChild(d);
    history.scrollTop = history.scrollHeight;
  }

  async function sendText(text) {
    try {
      // Show typing indicator
      const typingIndicator = document.createElement('div');
      typingIndicator.className = 'bubble bot typing';
      typingIndicator.textContent = '...';
      history.appendChild(typingIndicator);
      history.scrollTop = history.scrollHeight;

      // First check for predefined personal responses
      const personalResponse = getPersonalResponse(text);
      if (personalResponse) {
        // Remove typing indicator
        typingIndicator.remove();
        addBubble('bot', personalResponse);
        speak(personalResponse);
        return;
      }

      // For other questions, try the backend API
      const res = await fetch(backendBase + '/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          type: "text", 
          message: text,
          context: "Respond as if you're me - be authentic, personal, and speak in first person. Keep responses conversational and natural."
        })
      });
      
      // Remove typing indicator
      typingIndicator.remove();
      
      if (res.ok) {
        const j = await res.json();
        const reply = j.response || (j.error ? 'Error: ' + j.error : getFallbackResponse(text));
        addBubble('bot', reply);
        speak(reply);
      } else {
        throw new Error('API request failed');
      }
    } catch (e) {
      console.error(e);
      // Remove typing indicator if it exists
      document.querySelector('.typing')?.remove();
      const fallbackReply = getPersonalResponse(text) || getFallbackResponse(text);
      addBubble('bot', fallbackReply);
      speak(fallbackReply);
    }
  }

  function getPersonalResponse(text) {
    const lowerText = text.toLowerCase();
    
    if (lowerText.includes('life story') || lowerText.includes('about your life') || lowerText.includes('tell me about yourself')) {
      return PERSONAL_RESPONSES.life_story;
    }
    if (lowerText.includes('superpower') || lowerText.includes('super power') || lowerText.includes('greatest strength')) {
      return PERSONAL_RESPONSES.superpower;
    }
    if (lowerText.includes('grow') || lowerText.includes('growth') || lowerText.includes('improve') || lowerText.includes('development area')) {
      return PERSONAL_RESPONSES.growth_areas;
    }
    if (lowerText.includes('misconception') || lowerText.includes('coworker') || lowerText.includes('people think') || lowerText.includes('wrong about')) {
      return PERSONAL_RESPONSES.misconception;
    }
    if (lowerText.includes('boundary') || lowerText.includes('limit') || lowerText.includes('push') || lowerText.includes('comfort zone')) {
      return PERSONAL_RESPONSES.boundaries;
    }
    
    return null;
  }

  function getFallbackResponse(text) {
    const randomFallback = FALLBACK_RESPONSES[Math.floor(Math.random() * FALLBACK_RESPONSES.length)];
    return `${randomFallback} I believe in being authentic and thoughtful in my responses, so I'd need a moment to give you my genuine perspective on "${text}".`;
  }

  function speak(text) {
    if ('speechSynthesis' in window) {
      const u = new SpeechSynthesisUtterance(text);
      u.lang = 'en-US';
      u.rate = 1.0;
      u.pitch = 1.0;
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(u);
    }
  }

  // Initial welcome message
  setTimeout(() => {
    addBubble('bot', "Hi! I'm here to share my personal journey and experiences. Ask me about my life story, superpowers, growth areas, or anything else you're curious about!");
  }, 500);
});