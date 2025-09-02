import logging

logger = logging.getLogger(__name__)

def generate_feedback(transcript, corrections, pitch, tempo, features):
    try:
        feedback = []
        if corrections:
            feedback.append("Grammar suggestions: " + ", ".join(corrections))
        if pitch < 100:
            feedback.append("Try to raise your pitch for confidence.")
        if tempo > 150:
            feedback.append("Slow down your speaking tempo.")
        if features:
            feedback.append("Pronunciation features look good!")
        return " ".join(feedback)
    except Exception as e:
        logger.error(f"Feedback error: {e}")
        return "Good effort!"