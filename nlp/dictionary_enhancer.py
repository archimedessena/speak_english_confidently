"""
Offline vocabulary enhancement using NLTK and local resources
"""

import nltk
from typing import List, Dict, Any, Tuple
import logging
import random
from collections import Counter
import re

# Download required NLTK data
try:
    nltk.download('wordnet', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except:
    pass

logger = logging.getLogger(__name__)

class OfflineDictionaryEnhancer:
    def __init__(self):
        """Initialize offline vocabulary enhancer"""
        from nltk.corpus import wordnet
        self.wordnet = wordnet
        self.common_words = self._load_common_words()
        self.synonym_cache = {}
        
        logger.info("✅ Offline Dictionary Enhancer initialized")
    
    def _load_common_words(self) -> set:
        """Load common words that could be enhanced"""
        return {
            'good', 'bad', 'nice', 'happy', 'sad', 'big', 'small', 'important',
            'interesting', 'funny', 'easy', 'hard', 'difficult', 'beautiful',
            'ugly', 'smart', 'dumb', 'fast', 'slow', 'old', 'new', 'young',
            'say', 'tell', 'speak', 'talk', 'ask', 'get', 'make', 'do', 'think',
            'know', 'see', 'look', 'want', 'need', 'like', 'love', 'hate',
            'thing', 'stuff', 'person', 'people', 'place', 'time', 'way'
        }
    
    def get_synonyms(self, word: str, limit: int = 5) -> List[str]:
        """Get synonyms using WordNet"""
        if word in self.synonym_cache:
            return self.synonym_cache[word][:limit]
        
        synonyms = set()
        try:
            for syn in self.wordnet.synsets(word):
                for lemma in syn.lemmas():
                    synonym = lemma.name().replace('_', ' ')
                    if synonym.lower() != word.lower() and len(synonym.split()) == 1:
                        synonyms.add(synonym)
            
            # Convert to list and sort for consistency
            synonyms = sorted(list(synonyms))
            self.synonym_cache[word] = synonyms
            
        except Exception as e:
            logger.debug(f"No synonyms found for {word}: {e}")
            synonyms = []
        
        return synonyms[:limit]
    
    def extract_words_from_text(self, text: str) -> List[str]:
        """Extract meaningful words from text"""
        if not text:
            return []
        
        # Remove punctuation and convert to lowercase
        cleaned_text = re.sub(r'[^\w\s]', '', text.lower())
        words = [word for word in cleaned_text.split() if len(word) > 2]
        
        return words
    
    def identify_common_words(self, text: str) -> List[Tuple[str, int]]:
        """Identify common words that could be enhanced"""
        words = self.extract_words_from_text(text)
        if not words:
            return []
        
        word_counts = Counter(words)
        common_words = [
            (word, count) for word, count in word_counts.items() 
            if word in self.common_words
        ]
        
        common_words.sort(key=lambda x: x[1], reverse=True)
        return common_words
    
    def suggest_enhancements(self, text: str, max_suggestions: int = 3) -> List[Dict[str, Any]]:
        """Suggest vocabulary enhancements"""
        common_words = self.identify_common_words(text)
        if not common_words:
            return []
        
        enhancements = []
        suggested_words = set()
        
        for word, frequency in common_words:
            if word not in suggested_words and len(enhancements) < max_suggestions:
                synonyms = self.get_synonyms(word)
                
                if synonyms:
                    suggested_synonym = random.choice(synonyms)
                    
                    enhancement = {
                        'common_word': word,
                        'suggested_word': suggested_synonym,
                        'frequency': frequency,
                        'example_usage': self._generate_example(word, suggested_synonym),
                        'complexity': self._assess_complexity(suggested_synonym),
                        'source': 'wordnet'
                    }
                    
                    enhancements.append(enhancement)
                    suggested_words.add(word)
        
        return enhancements
    
    def _generate_example(self, original: str, suggested: str) -> str:
        """Generate usage example"""
        examples = {
            'good': f"Instead of '{original}', try '{suggested}': 'This is {suggested} work!'",
            'bad': f"Instead of '{original}', try '{suggested}': 'The quality was {suggested}'",
            'big': f"Instead of '{original}', try '{suggested}': 'A {suggested} challenge'",
            'small': f"Instead of '{original}', try '{suggested}': 'A {suggested} amount'",
            'say': f"Instead of '{original}', try '{suggested}': 'She {suggested} her opinion'",
            'think': f"Instead of '{original}', try '{suggested}': 'I {suggested} about it'",
        }
        
        return examples.get(original, 
                           f"Instead of '{original}', try '{suggested}' for better expression")
    
    def _assess_complexity(self, word: str) -> str:
        """Assess word complexity"""
        word_length = len(word)
        
        if word_length > 8:
            return "advanced"
        elif word_length > 6:
            return "intermediate"
        else:
            return "basic"
    
    def get_vocabulary_feedback(self, text: str) -> str:
        """Generate user-friendly vocabulary feedback"""
        enhancements = self.suggest_enhancements(text)
        
        if not enhancements:
            return "Great job! Your vocabulary is already quite diverse. 🎉"
        
        feedback = []
        feedback.append("💡 **Vocabulary Enhancement Suggestions:**")
        feedback.append("")
        
        for i, enhancement in enumerate(enhancements, 1):
            feedback.append(f"{i}. **{enhancement['common_word']}** → **{enhancement['suggested_word']}**")
            feedback.append(f"   📝 {enhancement['example_usage']}")
            feedback.append(f"   🎯 Level: {enhancement['complexity']}")
            feedback.append("")
        
        feedback.append("Try incorporating these words to make your speech more precise and engaging!")
        
        return "\n".join(feedback)

# Singleton instance
dictionary_enhancer = OfflineDictionaryEnhancer()

# Convenience functions
def enhance_vocabulary(text: str, max_suggestions: int = 3) -> List[Dict[str, Any]]:
    return dictionary_enhancer.suggest_enhancements(text, max_suggestions)

def get_vocabulary_feedback(text: str) -> str:
    return dictionary_enhancer.get_vocabulary_feedback(text)