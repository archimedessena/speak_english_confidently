import logging
import json

logger = logging.getLogger(__name__)

class ConversationState:
    def __init__(self):
        self.history = []
        self.progress = {"sessions": 0, "improvements": []}

    def update(self, user_input, response, feedback):
        self.history.append({"user": user_input, "bot": response, "feedback": feedback})
        self.progress["sessions"] += 1
        self.progress["improvements"].append(feedback)
        logger.info("State updated.")

    def to_dict(self):
        return {
            "history": self.history,
            "progress": self.progress
        }

    def load_from_dict(self, data):
        self.history = data.get("history", [])
        self.progress = data.get("progress", {})