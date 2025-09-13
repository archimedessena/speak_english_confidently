"""
Vocabulary enhancement module for suggesting more advanced word alternatives.
Integrated with the English coaching application.
"""

from typing import List, Dict, Any, Optional, Tuple
import logging
from collections import Counter
import re
import random

logger = logging.getLogger(__name__)

class VocabularyEnhancer:
    def __init__(self):
        """Initialize with common word mappings and synonym resources"""
        self.common_words = self._load_common_words()
        self.synonym_mappings = self._load_synonym_mappings()
        self.word_levels = self._load_word_levels()
        
    def _load_common_words(self) -> set:
        """Load a set of common English words that could be enhanced"""
        return {
            # Basic adjectives
            'good', 'bad', 'nice', 'happy', 'sad', 'big', 'small', 'important',
            'interesting', 'funny', 'easy', 'hard', 'difficult', 'beautiful',
            'ugly', 'smart', 'dumb', 'fast', 'slow', 'old', 'new', 'young',
            'rich', 'poor', 'strong', 'weak', 'hot', 'cold', 'warm', 'cool',
            'clean', 'dirty', 'wet', 'dry', 'full', 'empty', 'heavy', 'light',
            'expensive', 'cheap', 'simple', 'complex', 'quiet', 'loud', 'bright',
            'dark', 'sweet', 'sour', 'bitter', 'salty', 'soft', 'hard', 'smooth',
            'rough', 'thick', 'thin', 'wide', 'narrow', 'deep', 'shallow',
            
            # Basic verbs
            'say', 'tell', 'speak', 'talk', 'ask', 'answer', 'get', 'make',
            'do', 'create', 'build', 'think', 'know', 'understand', 'learn',
            'teach', 'help', 'work', 'play', 'eat', 'drink', 'sleep', 'walk',
            'run', 'jump', 'see', 'look', 'watch', 'hear', 'listen', 'feel',
            
            # Basic nouns
            'thing', 'stuff', 'person', 'people', 'man', 'woman', 'child',
            'place', 'time', 'way', 'day', 'night', 'problem', 'solution',
            'idea', 'thought', 'house', 'home', 'car', 'food', 'water',
        }
    
    def _load_synonym_mappings(self) -> Dict[str, List[str]]:
        """Load mappings from common words to more advanced synonyms"""
        return {
            'good': ['excellent', 'superb', 'outstanding', 'remarkable', 'exceptional'],
            'bad': ['poor', 'terrible', 'awful', 'substandard', 'inferior'],
            'nice': ['pleasant', 'agreeable', 'delightful', 'charming', 'gracious'],
            'happy': ['joyful', 'content', 'pleased', 'delighted', 'ecstatic'],
            'sad': ['unhappy', 'depressed', 'melancholy', 'sorrowful', 'disheartened'],
            'big': ['large', 'substantial', 'considerable', 'sizeable', 'immense'],
            'small': ['tiny', 'petite', 'compact', 'minuscule', 'miniature'],
            'important': ['significant', 'crucial', 'vital', 'essential', 'paramount'],
            'interesting': ['fascinating', 'engaging', 'compelling', 'captivating', 'intriguing'],
            'funny': ['humorous', 'amusing', 'hilarious', 'comical', 'entertaining'],
            'easy': ['simple', 'straightforward', 'effortless', 'uncomplicated', 'elementary'],
            'hard': ['difficult', 'challenging', 'arduous', 'demanding', 'taxing'],
            'beautiful': ['gorgeous', 'stunning', 'lovely', 'exquisite', 'breathtaking'],
            'smart': ['intelligent', 'clever', 'bright', 'brilliant', 'knowledgeable'],
            'fast': ['quick', 'rapid', 'swift', 'speedy', 'brisk'],
            'slow': ['sluggish', 'leisurely', 'gradual', 'unhurried', 'deliberate'],
            'say': ['state', 'declare', 'mention', 'express', 'articulate'],
            'tell': ['inform', 'notify', 'advise', 'apprise', 'brief'],
            'speak': ['talk', 'converse', 'communicate', 'discuss', 'dialog'],
            'think': ['contemplate', 'ponder', 'consider', 'reflect', 'meditate'],
            'know': ['understand', 'comprehend', 'recognize', 'appreciate', 'familiar'],
            'get': ['obtain', 'acquire', 'receive', 'secure', 'procure'],
            'make': ['create', 'produce', 'construct', 'fabricate', 'manufacture'],
            'thing': ['item', 'object', 'element', 'article', 'entity'],
            'stuff': ['materials', 'items', 'belongings', 'possessions', 'equipment'],
            'people': ['individuals', 'persons', 'populace', 'community', 'society'],
        }
    
    def _load_word_levels(self) -> Dict[str, str]:
        """Define complexity levels for vocabulary assessment"""
        return {
            'basic': 'A1-A2 (Beginner)',
            'intermediate': 'B1-B2 (Intermediate)',
            'advanced': 'C1-C2 (Advanced)'
        }
    
    def extract_words_from_text(self, text: str) -> List[str]:
        """
        Extract meaningful words from text, filtering out stopwords and punctuation
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of cleaned words
        """
        if not text:
            return []
        
        # Convert to lowercase and remove punctuation
        cleaned_text = re.sub(r'[^\w\s]', '', text.lower())
        
        # Split into words and filter out very short words
        words = [word for word in cleaned_text.split() if len(word) > 2]
        
        return words
    
    def identify_common_words(self, text: str) -> List[Tuple[str, int]]:
        """
        Identify common words in the text that could be enhanced
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of tuples (word, frequency) for common words
        """
        words = self.extract_words_from_text(text)
        if not words:
            return []
        
        # Count word frequencies
        word_counts = Counter(words)
        
        # Filter for common words that have synonyms available
        common_words = [
            (word, count) for word, count in word_counts.items() 
            if word in self.common_words and word in self.synonym_mappings
        ]
        
        # Sort by frequency (most common first)
        common_words.sort(key=lambda x: x[1], reverse=True)
        
        return common_words
    
    def suggest_enhancements(self, text: str, max_suggestions: int = 3) -> List[Dict[str, Any]]:
        """
        Suggest vocabulary enhancements for common words
        
        Args:
            text: Input text to analyze
            max_suggestions: Maximum number of suggestions to return
            
        Returns:
            List of enhancement suggestions
        """
        common_words = self.identify_common_words(text)
        if not common_words:
            return []
        
        enhancements = []
        suggested_words = set()
        
        for word, frequency in common_words:
            if word not in suggested_words and len(enhancements) < max_suggestions:
                synonyms = self.synonym_mappings.get(word, [])
                if synonyms:
                    # Choose a random synonym for variety
                    suggested_synonym = random.choice(synonyms)
                    
                    enhancement = {
                        'common_word': word,
                        'suggested_word': suggested_synonym,
                        'frequency': frequency,
                        'example_usage': self._generate_example(word, suggested_synonym),
                        'complexity': self._assess_complexity(suggested_synonym)
                    }
                    
                    enhancements.append(enhancement)
                    suggested_words.add(word)
        
        return enhancements
    
    def _generate_example(self, original: str, suggested: str) -> str:
        """Generate an example sentence using the suggested word"""
        examples = {
            'good': f"Instead of 'This is {original}', try 'This is {suggested} work!'",
            'bad': f"Instead of 'That's {original}', try 'That's {suggested} quality'",
            'big': f"Instead of 'a {original} problem', try 'a {suggested} challenge'",
            'small': f"Instead of 'a {original} amount', try 'a {suggested} quantity'",
            'happy': f"Instead of 'I feel {original}', try 'I feel {suggested}'",
            'say': f"Instead of 'He {original}', try 'He {suggested}'",
            'think': f"Instead of 'I {original}', try 'I {suggested}'",
            'get': f"Instead of '{original} it', try '{suggested} it'",
        }
        
        return examples.get(original, 
                           f"Instead of '{original}', try using '{suggested}' for better expression")
    
    def _assess_complexity(self, word: str) -> str:
        """Assess the complexity level of a word"""
        word_length = len(word)
        syllable_estimate = self._estimate_syllables(word)
        
        if word_length > 8 or syllable_estimate > 3:
            return self.word_levels['advanced']
        elif word_length > 6 or syllable_estimate > 2:
            return self.word_levels['intermediate']
        else:
            return self.word_levels['basic']
    
    def _estimate_syllables(self, word: str) -> int:
        """Simple syllable estimation"""
        vowels = "aeiouy"
        count = 0
        prev_char_vowel = False
        
        for char in word.lower():
            if char in vowels:
                if not prev_char_vowel:
                    count += 1
                prev_char_vowel = True
            else:
                prev_char_vowel = False
        
        return max(1, count)
    
    def get_vocabulary_feedback(self, text: str) -> str:
        """
        Generate user-friendly vocabulary feedback
        
        Args:
            text: Input text to analyze
            
        Returns:
            Friendly feedback string
        """
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
    
    def analyze_vocabulary_level(self, text: str) -> Dict[str, Any]:
        """
        Comprehensive vocabulary analysis
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with vocabulary analysis
        """
        words = self.extract_words_from_text(text)
        if not words:
            return {'total_words': 0, 'analysis': 'Insufficient text for analysis'}
        
        total_words = len(words)
        unique_words = len(set(words))
        diversity_score = unique_words / total_words if total_words > 0 else 0
        
        common_words_count = len(self.identify_common_words(text))
        advanced_words_count = sum(1 for word in words if self._assess_complexity(word) == self.word_levels['advanced'])
        
        return {
            'total_words': total_words,
            'unique_words': unique_words,
            'diversity_score': round(diversity_score, 2),
            'common_words_count': common_words_count,
            'advanced_words_count': advanced_words_count,
            'vocabulary_level': self._determine_overall_level(diversity_score, advanced_words_count, total_words)
        }
    
    def _determine_overall_level(self, diversity: float, advanced_count: int, total_words: int) -> str:
        """Determine overall vocabulary level"""
        if total_words == 0:
            return "Unknown"
        
        advanced_ratio = advanced_count / total_words
        
        if advanced_ratio > 0.2 and diversity > 0.7:
            return self.word_levels['advanced']
        elif advanced_ratio > 0.1 and diversity > 0.5:
            return self.word_levels['intermediate']
        else:
            return self.word_levels['basic']

# Singleton instance for easy access
vocabulary_enhancer = VocabularyEnhancer()

# Convenience functions
def enhance_vocabulary(text: str, max_suggestions: int = 3) -> List[Dict[str, Any]]:
    """Quick vocabulary enhancement convenience function"""
    return vocabulary_enhancer.suggest_enhancements(text, max_suggestions)

def get_vocabulary_feedback(text: str) -> str:
    """Quick vocabulary feedback convenience function"""
    return vocabulary_enhancer.get_vocabulary_feedback(text)

def analyze_vocabulary(text: str) -> Dict[str, Any]:
    """Quick vocabulary analysis convenience function"""
    return vocabulary_enhancer.analyze_vocabulary_level(text)