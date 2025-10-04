class VoiceBot {
    constructor() {
        this.isRecording = false;
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.initializeEventListeners();
        this.checkMicrophonePermission();
    }

    async checkMicrophonePermission() {
        try {
            await navigator.mediaDevices.getUserMedia({ audio: true });
            console.log('Microphone access granted');
        } catch (error) {
            console.warn('Microphone access not granted:', error);
        }
    }

    initializeEventListeners() {
        // Record button
        const recordBtn = document.getElementById('recordBtn');
        recordBtn.addEventListener('click', () => this.toggleRecording());

        // Text input
        const textInput = document.getElementById('textInput');
        const sendTextBtn = document.getElementById('sendTextBtn');
        
        sendTextBtn.addEventListener('click', () => this.sendTextQuestion());
        textInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendTextQuestion();
            }
        });

        // Suggested questions
        document.querySelectorAll('.question-chip').forEach(chip => {
            chip.addEventListener('click', (e) => {
                const question = e.target.getAttribute('data-question');
                this.sendPredefinedQuestion(question);
            });
        });
    }

    async toggleRecording() {
        if (this.isRecording) {
            this.stopRecording();
        } else {
            await this.startRecording();
        }
    }

    async startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    sampleRate: 44100
                } 
            });
            
            this.mediaRecorder = new MediaRecorder(stream, { 
                mimeType: 'audio/webm;codecs=opus' 
            });
            this.audioChunks = [];

            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.audioChunks.push(event.data);
                }
            };

            this.mediaRecorder.onstop = () => {
                this.processRecording();
                stream.getTracks().forEach(track => track.stop());
            };

            this.mediaRecorder.start(1000); // Collect data every second
            this.isRecording = true;
            this.updateRecordingUI(true);
            
        } catch (error) {
            console.error('Error starting recording:', error);
            this.showError('Microphone access denied. Please allow microphone permissions and try again.');
        }
    }

    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;
            this.updateRecordingUI(false);
        }
    }

    updateRecordingUI(recording) {
        const recordBtn = document.getElementById('recordBtn');
        const recordText = document.getElementById('recordText');
        const status = document.getElementById('recordingStatus');

        if (recording) {
            recordBtn.classList.add('recording');
            recordText.textContent = 'Stop Recording';
            status.textContent = 'Listening... Speak now!';
            status.style.color = '#dc2626';
        } else {
            recordBtn.classList.remove('recording');
            recordText.textContent = 'Click to Speak';
            status.textContent = 'Click the microphone and ask your question';
            status.style.color = '#64748b';
        }
    }

    async processRecording() {
        this.showTypingIndicator();
        
        const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm;codecs=opus' });
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.webm');

        try {
            const response = await fetch('/api/process', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (result.success) {
                this.displayMessage(result.question, 'user');
                setTimeout(() => {
                    this.removeTypingIndicator();
                    this.displayMessage(result.response, 'bot');
                }, 1000);
            } else {
                this.removeTypingIndicator();
                this.showError(result.error);
            }
        } catch (error) {
            this.removeTypingIndicator();
            console.error('Error processing audio:', error);
            this.showError('Network error. Please check your connection and try again.');
        }
    }

    async sendTextQuestion() {
        const textInput = document.getElementById('textInput');
        const question = textInput.value.trim();

        if (!question) {
            this.showError('Please enter a question');
            return;
        }

        textInput.value = '';
        this.displayMessage(question, 'user');
        this.showTypingIndicator();

        try {
            const response = await fetch('/api/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: question })
            });

            const result = await response.json();
            
            if (result.success) {
                setTimeout(() => {
                    this.removeTypingIndicator();
                    this.displayMessage(result.response, 'bot');
                }, 1000);
            } else {
                this.removeTypingIndicator();
                this.showError(result.error);
            }
        } catch (error) {
            this.removeTypingIndicator();
            console.error('Error sending text:', error);
            this.showError('Network error. Please check your connection and try again.');
        }
    }

    sendPredefinedQuestion(question) {
        this.displayMessage(question, 'user');
        this.showTypingIndicator();

        fetch('/api/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: question })
        })
        .then(response => response.json())
        .then(result => {
            setTimeout(() => {
                this.removeTypingIndicator();
                if (result.success) {
                    this.displayMessage(result.response, 'bot');
                } else {
                    this.showError(result.error);
                }
            }, 1000);
        })
        .catch(error => {
            this.removeTypingIndicator();
            this.showError('Network error. Please try again.');
        });
    }

    displayMessage(content, sender) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = content;
        
        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    showTypingIndicator() {
        const chatMessages = document.getElementById('chatMessages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message';
        typingDiv.id = 'typingIndicator';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content typing-indicator';
        contentDiv.textContent = 'Thinking...';
        
        typingDiv.appendChild(contentDiv);
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    removeTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    showError(message) {
        const chatMessages = document.getElementById('chatMessages');
        const errorDiv = document.createElement('div');
        errorDiv.className = 'message bot-message';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content error-message';
        contentDiv.textContent = `Error: ${message}`;
        
        errorDiv.appendChild(contentDiv);
        chatMessages.appendChild(errorDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

// Initialize the voice bot when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new VoiceBot();
    
    // Test backend connection
    fetch('/api/health')
        .then(response => response.json())
        .then(data => console.log('Backend health:', data))
        .catch(error => console.error('Backend connection failed:', error));
});