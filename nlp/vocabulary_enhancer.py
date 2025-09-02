import logging
import nltk
from nltk.corpus import wordnet

nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

logger = logging.getLogger(__name__)

def enhance_vocabulary(text):
    try:
        words = text.split()
        enhanced = []
        for word in words:
            syns = wordnet.synsets(word)
            if syns and syns[0].lemmas():
                enhanced.append(syns[0].lemmas()[0].name())  # Simple replacement with first synonym
            else:
                enhanced.append(word)
        enhanced_text = ' '.join(enhanced)
        logger.info(f"Vocabulary enhanced: {enhanced_text}")
        return enhanced_text
    except Exception as e:
        logger.error(f"Vocab enhancement error: {e}")
        return text