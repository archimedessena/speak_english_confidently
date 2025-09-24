#!/usr/bin/env python3
"""
Speak English Confidently - Conversational English Coaching Web App
"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/practice')
def practice():
    return render_template('practice.html')

@app.route('/progress')
def progress():
    return render_template('progress.html')

@app.route('/api/start_session', methods=['POST'])
def start_session():
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'anonymous')
        session_type = data.get('session_type', 'conversation')
        
        session_id = f"{user_id}_{int(datetime.now().timestamp())}"
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Session started successfully'
        })
    except Exception as e:
        logger.error(f"Error starting session: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/process_audio', methods=['POST'])
def process_audio():
    try:
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Mock processing for now
        transcript = "Hello, this is a test recording."
        grammar_analysis = {"errors": 0, "suggestions": []}
        vocabulary_suggestions = []
        pronunciation_feedback = {"clarity": "good", "pace": "moderate"}
        coaching_response = "Great job! Your pronunciation is clear and your pace is good."
        
        return jsonify({
            'success': True,
            'transcript': transcript,
            'grammar_analysis': grammar_analysis,
            'vocabulary_suggestions': vocabulary_suggestions,
            'pronunciation_feedback': pronunciation_feedback,
            'coaching_response': coaching_response
        })
        
    except Exception as e:
        logger.error(f"Error processing audio: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get_feedback', methods=['GET'])
def get_feedback():
    try:
        user_id = request.args.get('user_id', 'anonymous')
        feedback = {
            "message": "Great progress! Keep practicing regularly.",
            "suggestions": ["Try speaking for longer periods", "Practice with different topics"]
        }
        
        return jsonify({
            'success': True,
            'feedback': feedback
        })
    except Exception as e:
        logger.error(f"Error getting feedback: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get_progress', methods=['GET'])
def get_progress():
    try:
        user_id = request.args.get('user_id', 'anonymous')
        progress = {"total_sessions": 1, "total_interactions": 5}
        
        return jsonify({
            'success': True,
            'progress': progress
        })
    except Exception as e:
        logger.error(f"Error getting progress: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@socketio.on('connect')
def handle_connect():
    logger.info(f"Client connected: {request.sid}")
    emit('connected', {'data': 'Connected to English Coach'})

@socketio.on('join_session')
def handle_join_session(data):
    session_id = data.get('session_id')
    if session_id:
        join_room(session_id)
        emit('joined_session', {'session_id': session_id})

@socketio.on('start_recording')
def handle_start_recording(data):
    session_id = data.get('session_id')
    emit('recording_started', {'session_id': session_id}, room=session_id)

@socketio.on('stop_recording')
def handle_stop_recording(data):
    session_id = data.get('session_id')
    emit('recording_stopped', {'session_id': session_id}, room=session_id)

@socketio.on('disconnect')
def handle_disconnect():
    logger.info(f"Client disconnected: {request.sid}")

if __name__ == '__main__':
    logger.info("Starting Speak English Confidently application...")
    
    # Create necessary directories
    os.makedirs('data/audio_samples', exist_ok=True)
    os.makedirs('data/user_progress', exist_ok=True)
    os.makedirs('data/models', exist_ok=True)
    
    # Run the application
    socketio.run(
        app,
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )
