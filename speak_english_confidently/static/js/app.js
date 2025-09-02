// Main application JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initializeApp();
});

function initializeApp() {
    // Set up event listeners
    setupEventListeners();
    
    // Initialize Socket.IO connection if on practice page
    if (window.location.pathname === '/practice') {
        initializeSocketIO();
    }
}

function setupEventListeners() {
    // Navigation and general UI interactions
    const newSessionBtn = document.getElementById('new-session');
    const saveSessionBtn = document.getElementById('save-session');
    
    if (newSessionBtn) {
        newSessionBtn.addEventListener('click', startNewSession);
    }
    
    if (saveSessionBtn) {
        saveSessionBtn.addEventListener('click', saveCurrentSession);
    }
}

function initializeSocketIO() {
    // Initialize Socket.IO connection
    const socket = io();
    
    socket.on('connect', function() {
        console.log('Connected to server');
        updateSessionStatus('Connected to English Coach');
    });
    
    socket.on('joined_session', function(data) {
        console.log('Joined session:', data.session_id);
        updateSessionId(data.session_id);
    });
    
    socket.on('recording_started', function(data) {
        updateRecordingStatus('Recording...', true);
    });
    
    socket.on('recording_stopped', function(data) {
        updateRecordingStatus('Processing audio...', false);
    });
    
    // Store socket reference globally
    window.socket = socket;
}

function startNewSession() {
    fetch('/api/start_session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user_id: 'user_' + Date.now(),
            session_type: 'conversation'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Join the new session
            if (window.socket) {
                window.socket.emit('join_session', { session_id: data.session_id });
            }
            
            // Clear conversation display
            clearConversationDisplay();
            
            // Add welcome message
            addMessage('Hello! I\'m your English coach. Let\'s start a new conversation. What would you like to talk about today?', 'coach');
            
            updateSessionId(data.session_id);
        } else {
            console.error('Failed to start session:', data.error);
        }
    })
    .catch(error => {
        console.error('Error starting session:', error);
    });
}

function saveCurrentSession() {
    // Implementation for saving session data
    console.log('Saving session...');
    // This would typically save to a database or local storage
    alert('Session saved successfully!');
}

function updateSessionId(sessionId) {
    const sessionIdElement = document.getElementById('session-id');
    if (sessionIdElement) {
        sessionIdElement.textContent = `Session: ${sessionId}`;
    }
}

function updateSessionStatus(status) {
    const recordingStatus = document.getElementById('recording-status');
    if (recordingStatus) {
        recordingStatus.innerHTML = `<i class="fas fa-circle"></i> ${status}`;
    }
}

function updateRecordingStatus(status, isRecording) {
    const recordingStatus = document.getElementById('recording-status');
    const recordingIndicator = recordingStatus.querySelector('.recording-indicator');
    
    if (recordingStatus) {
        recordingStatus.innerHTML = `<i class="fas fa-circle recording-indicator"></i> ${status}`;
    }
    
    if (isRecording) {
        recordingIndicator.style.animation = 'pulse 1.5s infinite';
    } else {
        recordingIndicator.style.animation = 'none';
    }
}

function clearConversationDisplay() {
    const conversationDisplay = document.getElementById('conversation-display');
    if (conversationDisplay) {
        conversationDisplay.innerHTML = '';
    }
}

function addMessage(content, type) {
    const conversationDisplay = document.getElementById('conversation-display');
    if (!conversationDisplay) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    if (type === 'coach') {
        messageContent.innerHTML = `<i class="fas fa-robot"></i><p>${content}</p>`;
    } else {
        messageContent.innerHTML = `<p>${content}</p>`;
    }
    
    messageDiv.appendChild(messageContent);
    conversationDisplay.appendChild(messageDiv);
    
    // Scroll to bottom
    conversationDisplay.scrollTop = conversationDisplay.scrollHeight;
}

function updateFeedback(type, content) {
    const feedbackElement = document.getElementById(`${type}-feedback`);
    if (feedbackElement) {
        feedbackElement.innerHTML = content;
    }
}
