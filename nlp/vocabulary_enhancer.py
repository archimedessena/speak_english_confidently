#**Build a simple vocabulary module:** 
# Start with a basic function that identifies the most common words in the user's sentence and suggests one more advanced synonym for each.


     # Text Preprocessing Steps:
#Tokenization: Divide the raw text into individual words or tokens. Libraries like NLTK or SpaCy offer robust tokenization functionalities.
#Normalization: Convert all text to a consistent case (e.g., lowercase).
#Punctuation Removal: Eliminate punctuation marks.
#Stop Word Removal: Remove common words (e.g., "the," "a," "is") that often carry little meaning for analysis.
#Lemmatization/Stemming: Reduce words to their base form (e.g., "running" to "run").


# Vocabulary Enhancement Steps:
#Collect Unique Words: After preprocessing, gather all unique words from the tokenized text. A Python set is efficient for storing unique items.
#Assign Indices (Optional but Recommended): Assign a unique numerical index to each word in the vocabulary. This is crucial for numerical representations of text, such as one-hot encoding or embedding layers in deep learning. A Python dict can be used to map words to indices and vice-versa.


#Module Structure:
#Encapsulate the vocabulary building logic within a Python class or a set of functions within a .py file, making it a reusable module.




"""
Vocabulary enhancement module with dictionary API integration.
"""

from typing import List, Dict, Any, Optional, Tuple
import logging
from collections import Counter
import re
import random
from .dictionary_integration import get_enhanced_synonyms, get_word_definition, assess_vocabulary_complexity

logger = logging.getLogger(__name__)

class VocabularyEnhancer:
    def __init__(self):
        """Initialize vocabulary enhancer with dictionary integration"""
        self.common_words = self._load_common_words()
        self.word_levels = self._load_word_levels()
        
    def _load_common_words(self) -> set:
        """Load common words that are candidates for enhancement"""
        return {
            'good', 'bad', 'nice', 'happy', 'sad', 'big', 'small', 'important',
            'interesting', 'funny', 'easy', 'hard', 'difficult', 'beautiful',
            'ugly', 'smart', 'dumb', 'fast', 'slow', 'old', 'new', 'young',
            'say', 'tell', 'speak', 'talk', 'ask', 'get', 'make', 'do', 'think',
            'know', 'see', 'look', 'want', 'need', 'like', 'love', 'hate',
            'thing', 'stuff', 'person', 'people', 'place', 'time', 'way'
        }
    
    def _load_word_levels(self) -> Dict[str, str]:
        """Vocabulary complexity levels"""
        return {
            'basic': 'A1-A2 (Beginner)',
            'intermediate': 'B1-B2 (Intermediate)',
            'advanced': 'C1-C2 (Advanced)'
        }
    
    def extract_words_from_text(self, text: str) -> List[str]:
        """Extract clean words from text"""
        if not text:
            return []
        cleaned_text = re.sub(r'[^\w\s]', '', text.lower())
        return [word for word in cleaned_text.split() if len(word) > 2]
    
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
        """Suggest vocabulary enhancements using dictionary API"""
        common_words = self.identify_common_words(text)
        if not common_words:
            return []
        
        enhancements = []
        suggested_words = set()
        
        for word, frequency in common_words:
            if word not in suggested_words and len(enhancements) < max_suggestions:
                # Get synonyms from dictionary API
                synonyms = get_enhanced_synonyms(word)
                
                if synonyms:
                    suggested_synonym = random.choice(synonyms)
                    definition = get_word_definition(suggested_synonym)
                    
                    enhancement = {
                        'common_word': word,
                        'suggested_word': suggested_synonym,
                        'frequency': frequency,
                        'definition': definition,
                        'example_usage': self._generate_example(word, suggested_synonym),
                        'complexity': self._assess_complexity(suggested_synonym)
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
        """Simple complexity assessment"""
        # This will be enhanced with dictionary data
        if len(word) > 8:
            return self.word_levels['advanced']
        elif len(word) > 6:
            return self.word_levels['intermediate']
        else:
            return self.word_levels['basic']
    
    def get_vocabulary_feedback(self, text: str) -> str:
        """Generate comprehensive vocabulary feedback"""
        enhancements = self.suggest_enhancements(text)
        
        if not enhancements:
            return "Great job! Your vocabulary is already quite diverse. 🎉"
        
        feedback = []
        feedback.append("💡 **Vocabulary Enhancement Suggestions:**")
        feedback.append("")
        
        for i, enhancement in enumerate(enhancements, 1):
            feedback.append(f"{i}. **{enhancement['common_word']}** → **{enhancement['suggested_word']}**")
            if enhancement['definition']:
                feedback.append(f"   📚 Definition: {enhancement['definition']}")
            feedback.append(f"   📝 {enhancement['example_usage']}")
            feedback.append(f"   🎯 Level: {enhancement['complexity']}")
            feedback.append("")
        
        # Add overall complexity analysis
        complexity = assess_vocabulary_complexity(text)
        feedback.append(f"📊 **Overall Vocabulary Level:** {complexity['vocabulary_level']}")
        feedback.append(f"📈 **Advanced Word Ratio:** {complexity['advanced_ratio'] * 100}%")
        
        feedback.append("\nTry incorporating these words to make your speech more precise!")
        
        return "\n".join(feedback)
    
    def analyze_vocabulary_level(self, text: str) -> Dict[str, Any]:
        """Comprehensive vocabulary analysis"""
        return assess_vocabulary_complexity(text)

# Singleton instance
vocabulary_enhancer = VocabularyEnhancer()

# Convenience functions
def enhance_vocabulary(text: str, max_suggestions: int = 3) -> List[Dict[str, Any]]:
    return vocabulary_enhancer.suggest_enhancements(text, max_suggestions)

def get_vocabulary_feedback(text: str) -> str:
    return vocabulary_enhancer.get_vocabulary_feedback(text)

def analyze_vocabulary(text: str) -> Dict[str, Any]:
    return vocabulary_enhancer.analyze_vocabulary_level(text)