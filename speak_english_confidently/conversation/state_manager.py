import json
import os
from datetime import datetime
class ConversationStateManager:
    def __init__(self):
        self.sessions = {}
        self.user_progress = {}
    def start_session(self, user_id, session_type):
        session_id = f"{user_id}_{int(datetime.now().timestamp())}"
        self.sessions[session_id] = {
            "user_id": user_id,
            "session_type": session_type,
            "start_time": datetime.now(),
            "interactions": []
        }
        return session_id
    def add_interaction(self, transcript, response, grammar, vocabulary):
        interaction = {
            "timestamp": datetime.now(),
            "transcript": transcript,
            "response": response,
            "grammar": grammar,
            "vocabulary": vocabulary
        }
        # Add to all active sessions for now
        for session in self.sessions.values():
            session["interactions"].append(interaction)
    def get_user_progress(self, user_id):
        user_sessions = [s for s in self.sessions.values() if s["user_id"] == user_id]
        total_interactions = sum(len(s["interactions"]) for s in user_sessions)
        return {"total_sessions": len(user_sessions), "total_interactions": total_interactions}
