import logging

logger = logging.getLogger(__name__)

def manage_dialog(state):
    try:
        if len(state.history) == 0:
            return "Hello! Let's practice English. Tell me about your day."
        else:
            return "Great! Now, respond to this: What are your hobbies?"
        # Can expand to more dynamic flows
    except Exception as e:
        logger.error(f"Dialog manager error: {e}")
        return "Tell me something."