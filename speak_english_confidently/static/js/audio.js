// Audio recording and processing functionality
class AudioRecorder {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.audioContext = null;
        this.analyser = null;
        
        this.initializeAudio();
        this.setupEventListeners();
    }
    
    initializeAudio() {
        // Initialize audio context for visualization
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        this.analyser = this.audioContext.createAnalyser();
        this.analyser.fftSize = 256;
    }
    
    setupEventListeners() {
        const startBtn = document.getElementById('start-recording');
        const stopBtn = document.getElementById('stop-recording');
        
        if (startBtn) {
            startBtn.addEventListener('click', () => this.startRecording());
        }
        
        if (stopBtn) {
            stopBtn.addEventListener('click', () => this.stopRecording());
        }
    }
    
    async startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];
            
            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };
            
            this.mediaRecorder.onstop = () => {
                this.processRecording();
            };
            
            this.mediaRecorder.start();
            this.isRecording = true;
            
            this.updateUI(true);
            this.startVisualization(stream);
            
            // Emit start recording event
            if (window.socket) {
                window.socket.emit('start_recording', { session_id: this.getCurrentSessionId() });
            }
            
        } catch (error) {
            console.error('Error starting recording:', error);
            alert('Error accessing microphone. Please check permissions.');
        }
    }
    
    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;
            
            this.updateUI(false);
            this.stopVisualization();
            
            // Emit stop recording event
            if (window.socket) {
                window.socket.emit('stop_recording', { session_id: this.getCurrentSessionId() });
            }
        }
    }
    
    processRecording() {
        const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);
        
        // Create audio element for playback
        const audio = new Audio(audioUrl);
        
        // Add user message to conversation
        addMessage('Recording completed. Processing...', 'user');
        
        // Upload audio for processing
        this.uploadAudio(audioBlob);
    }
    
    async uploadAudio(audioBlob) {
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.wav');
        
        try {
            const response = await fetch('/api/process_audio', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Display results
                this.displayResults(result);
            } else {
                console.error('Error processing audio:', result.error);
                addMessage('Sorry, there was an error processing your audio.', 'coach');
            }
            
        } catch (error) {
            console.error('Error uploading audio:', error);
            addMessage('Sorry, there was an error uploading your audio.', 'coach');
        }
    }
    
    displayResults(results) {
        // Display transcript
        addMessage(`You said: "${results.transcript}"`, 'user');
        
        // Display coaching response
        addMessage(results.coaching_response, 'coach');
        
        // Update feedback panels
        this.updateFeedbackPanels(results);
    }
    
    updateFeedbackPanels(results) {
        // Grammar feedback
        if (results.grammar_analysis) {
            const grammarContent = this.formatGrammarFeedback(results.grammar_analysis);
            updateFeedback('grammar', grammarContent);
        }
        
        // Vocabulary feedback
        if (results.vocabulary_suggestions) {
            const vocabContent = this.formatVocabularyFeedback(results.vocabulary_suggestions);
            updateFeedback('vocabulary', vocabContent);
        }
        
        // Pronunciation feedback
        if (results.pronunciation_feedback) {
            const pronContent = this.formatPronunciationFeedback(results.pronunciation_feedback);
            updateFeedback('pronunciation', pronContent);
        }
    }
    
    formatGrammarFeedback(grammar) {
        if (grammar.errors === 0) {
            return '<p class="success">Great! No grammar errors detected.</p>';
        } else {
            let content = `<p class="error">Found ${grammar.errors} grammar issue(s):</p><ul>`;
            grammar.suggestions.forEach(suggestion => {
                content += `<li>${suggestion}</li>`;
            });
            content += '</ul>';
            return content;
        }
    }
    
    formatVocabularyFeedback(vocabulary) {
        if (vocabulary.length === 0) {
            return '<p>No vocabulary suggestions at this time.</p>';
        } else {
            let content = '<ul>';
            vocabulary.forEach(item => {
                content += `<li><strong>${item.word}</strong>: ${item.synonyms.join(', ')}</li>`;
            });
            content += '</ul>';
            return content;
        }
    }
    
    formatPronunciationFeedback(pronunciation) {
        return `<p><strong>Clarity:</strong> ${pronunciation.clarity}</p><p><strong>Pace:</strong> ${pronunciation.pace}</p>`;
    }
    
    updateUI(isRecording) {
        const startBtn = document.getElementById('start-recording');
        const stopBtn = document.getElementById('stop-recording');
        
        if (startBtn) startBtn.style.display = isRecording ? 'none' : 'inline-flex';
        if (stopBtn) stopBtn.style.display = isRecording ? 'inline-flex' : 'none';
    }
    
    startVisualization(stream) {
        // Audio visualization could be implemented here
        console.log('Audio visualization started');
    }
    
    stopVisualization() {
        console.log('Audio visualization stopped');
    }
    
    getCurrentSessionId() {
        const sessionElement = document.getElementById('session-id');
        if (sessionElement) {
            const text = sessionElement.textContent;
            return text.replace('Session: ', '');
        }
        return 'unknown';
    }
}

// Initialize audio recorder when page loads
document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname === '/practice') {
        window.audioRecorder = new AudioRecorder();
    }
});
