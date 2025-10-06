class VoiceBotApp {
    constructor() {
        this.apiBase = window.location.origin;
        this.chatMessages = document.getElementById('chat-messages');
        this.questionInput = document.getElementById('question-input');
        this.sendButton = document.getElementById('send-button');
        this.voiceBtn = document.getElementById('voice-btn');
        this.voiceStatus = document.getElementById('voice-status');
        this.audioWave = document.getElementById('audio-wave');
        this.statusElement = document.getElementById('status-text');
        this.statusDot = document.querySelector('.status-dot');
        this.suggestionChips = document.querySelectorAll('.chip');
        
        this.recognition = null;
        this.isListening = false;
        this.speechSynth = window.speechSynthesis;
        
        this.init();
    }

    async init() {
        this.initEventListeners();
        this.initSpeechRecognition();
        await this.checkServerStatus();
    }

    initEventListeners() {
        // Send button click
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        // Enter key press
        this.questionInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Suggestion chips
        this.suggestionChips.forEach(chip => {
            chip.addEventListener('click', () => {
                const question = chip.getAttribute('data-question');
                this.questionInput.value = question;
                this.sendMessage();
            });
        });
        
        // Input validation
        this.questionInput.addEventListener('input', () => {
            this.updateSendButtonState();
        });
        
        // Voice button
        this.voiceBtn.addEventListener('click', () => this.toggleVoiceRecognition());
    }

    initSpeechRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            
            this.recognition.continuous = false;
            this.recognition.interimResults = true;
            this.recognition.lang = 'en-US';
            
            this.recognition.onstart = () => {
                this.isListening = true;
                this.updateVoiceUI('listening', 'Listening... Speak now');
                this.audioWave.classList.add('listening');
            };
            
            this.recognition.onresult = (event) => {
                let transcript = '';
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    if (event.results[i].isFinal) {
                        transcript += event.results[i][0].transcript;
                    }
                }
                
                if (transcript) {
                    this.questionInput.value = transcript;
                    this.updateVoiceUI('processing', 'Processing your speech...');
                }
            };
            
            this.recognition.onend = () => {
                this.isListening = false;
                this.updateVoiceUI('ready', 'Ready to listen');
                this.audioWave.classList.remove('listening');
                
                // Auto-send if we have text
                if (this.questionInput.value.trim()) {
                    setTimeout(() => this.sendMessage(), 500);
                }
            };
            
            this.recognition.onerror = (event) => {
                this.isListening = false;
                this.updateVoiceUI('error', 'Error: ' + event.error);
                this.audioWave.classList.remove('listening');
            };
        } else {
            this.voiceBtn.style.display = 'none';
            this.voiceStatus.textContent = 'Speech recognition not supported';
        }
    }

    toggleVoiceRecognition() {
        if (!this.recognition) return;
        
        if (this.isListening) {
            this.recognition.stop();
        } else {
            this.recognition.start();
        }
    }

    updateVoiceUI(state, message) {
        this.voiceStatus.textContent = message;
        this.voiceBtn.className = 'voice-btn';
        
        if (state === 'listening') {
            this.voiceBtn.classList.add('listening');
            this.voiceBtn.querySelector('.voice-text').textContent = 'Stop Listening';
        } else if (state === 'processing') {
            this.voiceBtn.classList.add('processing');
            this.voiceBtn.querySelector('.voice-text').textContent = 'Processing...';
        } else {
            this.voiceBtn.querySelector('.voice-text').textContent = 'Click to Speak';
        }
    }

    async checkServerStatus() {
        try {
            const response = await fetch(`${this.apiBase}/health`);
            const data = await response.json();
            
            if (data.status === 'healthy') {
                this.updateStatus('connected', 'Ready to chat');
            } else {
                this.updateStatus('error', 'Service Unhealthy');
            }
        } catch (error) {
            this.updateStatus('error', 'Server Offline');
        }
    }

    updateStatus(status, message) {
        this.statusElement.textContent = message;
        this.statusDot.className = 'status-dot';
        
        if (status === 'connected') {
            this.statusDot.classList.add('connected');
        } else if (status === 'error') {
            this.statusDot.classList.add('error');
        }
    }

    async sendMessage() {
        const question = this.questionInput.value.trim();
        
        if (!question) return;
        
        // Add user message to chat
        this.addMessage(question, 'user');
        
        // Clear input and disable button
        this.questionInput.value = '';
        this.updateSendButtonState();
        this.sendButton.disabled = true;
        
        // Show typing indicator
        const typingIndicator = this.showTypingIndicator();
        
        try {
            const response = await this.callChatAPI(question);
            
            // Remove typing indicator and add actual response
            this.removeTypingIndicator(typingIndicator);
            this.addMessage(response, 'bot');
            
            // Auto-speak the response
            this.speakText(response);
            
        } catch (error) {
            // Remove typing indicator and show error
            this.removeTypingIndicator(typingIndicator);
            this.addMessage(
                "I'm having trouble connecting right now. Please try again in a moment.",
                'bot'
            );
        } finally {
            this.sendButton.disabled = false;
        }
    }

    async callChatAPI(question) {
        const response = await fetch(`${this.apiBase}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question })
        });
        
        if (!response.ok) {
            throw new Error(`API request failed: ${response.status}`);
        }
        
        const data = await response.json();
        return data.answer;
    }

    addMessage(content, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = type === 'user' ? '👤' : '🤖';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = `<p>${this.escapeHtml(content)}</p>`;
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(contentDiv);
        this.chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        this.scrollToBottom();
        
        return messageDiv;
    }

    showTypingIndicator() {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        messageDiv.id = 'typing-indicator';
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = '🤖';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        
        contentDiv.appendChild(typingDiv);
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(contentDiv);
        this.chatMessages.appendChild(messageDiv);
        
        this.scrollToBottom();
        return messageDiv;
    }

    removeTypingIndicator(typingElement) {
        if (typingElement && typingElement.parentNode) {
            typingElement.parentNode.removeChild(typingElement);
        }
    }

    speakText(text) {
        if (this.speechSynth.speaking) {
            this.speechSynth.cancel();
        }

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        utterance.volume = 0.8;
        this.speechSynth.speak(utterance);
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    updateSendButtonState() {
        const hasText = this.questionInput.value.trim().length > 0;
        this.sendButton.disabled = !hasText;
    }

    escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;")
            .replace(/\n/g, '<br>');
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new VoiceBotApp();
});