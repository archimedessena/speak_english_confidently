import logging
from language_tool_python import LanguageTool

logger = logging.getLogger(__name__)

tool = LanguageTool('en-US')

def check_grammar(text):
    try:
        matches = tool.check(text)
        corrections = [m.replacements[0] if m.replacements else m.message for m in matches]
        corrected_text = tool.correct(text)
        logger.info(f"Grammar checked: {corrected_text}")
        return corrections, corrected_text
    except Exception as e:
        logger.error(f"Grammar check error: {e}")
        return [], text