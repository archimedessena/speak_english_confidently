import logging
from nlp.language_models import get_openai_response

logger = logging.getLogger(__name__)

def generate_response(user_text):
    try:
        prompt = f"Respond conversationally to: {user_text}. Keep it encouraging for English practice."
        response = get_openai_response(prompt)
        logger.info(f"Generated response: {response}")
        return response
    except Exception as e:
        logger.error(f"Response generation error: {e}")
        return "Let's continue practicing!"