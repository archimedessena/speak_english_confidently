import logging
import openai
from utils.config import Config

logger = logging.getLogger(__name__)

def get_openai_response(prompt):
    config = Config()
    client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        return ""