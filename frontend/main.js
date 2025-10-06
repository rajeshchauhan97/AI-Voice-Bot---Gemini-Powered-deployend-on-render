class VoiceBotApp {
    constructor() {
        this.apiBase = window.location.origin;
        this.chatMessages = document.getElementById('chat-messages');
        this.questionInput = document.getElementById('question-input');
        this.sendButton = document.getElementById('send-button');
        this.statusElement = document.getElementById('status-text');
        this.statusDot = document.querySelector('.status-dot');
        this.suggestionChips = document.querySelectorAll('.chip');
        
        this.init();
    }

    async init() {
        this.initEventListeners();
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
    }

    updateSendButtonState() {
        const hasText = this.questionInput.value.trim().length > 0;
        this.sendButton.disabled = !hasText;
    }

    async checkServerStatus() {
        try {
            const response = await fetch(`${this.apiBase}/health`);
            const data = await response.json();
            
            if (data.status === 'healthy') {
                this.updateStatus('connected', data.ai_enabled ? 'AI Enabled' : 'Fallback Mode');
            } else {
                this.updateStatus('error', 'Service Unhealthy');
            }
        } catch (error) {
            this.updateStatus('error', 'Server Offline');
            console.error('Server status check failed:', error);
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
            
        } catch (error) {
            // Remove typing indicator and show error
            this.removeTypingIndicator(typingIndicator);
            this.addMessage(
                "Sorry, I'm having trouble connecting right now. Please check your connection and try again.",
                'bot'
            );
            console.error('API Error:', error);
        } finally {
            this.sendButton.disabled = false;
            this.questionInput.focus();
        }
    }

    async callChatAPI(question) {
        const response = await fetch(`${this.apiBase}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: question })
        });
        
        if (!response.ok) {
            throw new Error(`API request failed: ${response.status}`);
        }
        
        const data = await response.json();
        return data.response;
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

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
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