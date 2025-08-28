"""
Dictionary integration for dynamic vocabulary suggestions.
"""

import requests
import logging
from typing import Dict, List, Any, Optional
import time
import os
#from dotenv import load_dotenv
import re

# Load environment variables
#load_dotenv()

logger = logging.getLogger(__name__)

class DictionaryAPI:
    def __init__(self):
        """Initialize dictionary API with configuration"""
        self.api_key = os.getenv('WORDSAPI_KEY', 'your-rapidapi-key-here')
        self.base_url = "https://wordsapiv1.p.rapidapi.com/words/"
        self.headers = {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': 'wordsapiv1.p.rapidapi.com'
        }
        self.request_delay = 0.1  # Delay between requests to respect rate limits
        self.last_request_time = 0
        
    def _make_request(self, word: str, endpoint: str = "") -> Optional[Dict]:
        """Make API request with rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        # Respect rate limits
        if time_since_last < self.request_delay:
            time.sleep(self.request_delay - time_since_last)
        
        try:
            url = f"{self.base_url}{word}{endpoint}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                self.last_request_time = time.time()
                return response.json()
            elif response.status_code == 404:
                logger.debug(f"Word not found in dictionary: {word}")
            else:
                logger.warning(f"API request failed for {word}: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Dictionary API error for {word}: {e}")
        
        return None
    
    def get_word_info(self, word: str) -> Optional[Dict]:
        """Get comprehensive information about a word"""
        return self._make_request(word)
    
    def get_synonyms(self, word: str, limit: int = 5) -> List[str]:
        """Get synonyms for a word"""
        data = self._make_request(word, "/synonyms")
        if data and 'synonyms' in data:
            return data['synonyms'][:limit]
        return []
    
    def get_definitions(self, word: str, limit: int = 3) -> List[Dict]:
        """Get definitions for a word"""
        data = self._make_request(word)
        if data and 'results' in data:
            return data['results'][:limit]
        return []
    
    def get_pronunciation(self, word: str) -> Optional[str]:
        """Get pronunciation guide"""
        data = self._make_request(word)
        if data and 'pronunciation' in data:
            if isinstance(data['pronunciation'], dict):
                # Return the first pronunciation variant
                return next(iter(data['pronunciation'].values()), None)
            return data['pronunciation']
        return None
    
    def get_syllables(self, word: str) -> Optional[int]:
        """Get syllable count"""
        data = self._make_request(word)
        if data and 'syllables' in data and 'count' in data['syllables']:
            return data['syllables']['count']
        return None
    
    def is_common_word(self, word: str) -> bool:
        """Check if a word is commonly used (basic vocabulary)"""
        data = self._make_request(word)
        if data and 'frequency' in data:
            # Words with higher frequency are more common
            return data['frequency'] > 3.0  # Adjust threshold as needed
        return False
    
    def get_word_complexity(self, word: str) -> str:
        """Assess word complexity based on multiple factors"""
        syllables = self.get_syllables(word)
        frequency_data = self._make_request(word)
        
        if not syllables or not frequency_data:
            return "unknown"
        
        frequency = frequency_data.get('frequency', 0)
        word_length = len(word)
        
        # Complexity assessment logic
        if frequency < 2.0 or syllables >= 4 or word_length >= 10:
            return "advanced"
        elif frequency < 4.0 or syllables >= 3 or word_length >= 8:
            return "intermediate"
        else:
            return "basic"

# Singleton instance
dictionary_api = DictionaryAPI()

# Fallback data for when API is unavailable
FALLBACK_SYNONYMS = {
    'good': ['excellent', 'superb', 'outstanding', 'remarkable'],
    'bad': ['poor', 'terrible', 'awful', 'substandard'],
    'nice': ['pleasant', 'agreeable', 'delightful', 'charming'],
    'happy': ['joyful', 'content', 'pleased', 'delighted'],
    'sad': ['unhappy', 'depressed', 'melancholy', 'sorrowful'],
    'big': ['large', 'substantial', 'considerable', 'sizeable'],
    'small': ['tiny', 'petite', 'compact', 'minuscule'],
    'important': ['significant', 'crucial', 'vital', 'essential'],
}

def get_enhanced_synonyms(word: str, limit: int = 5) -> List[str]:
    """
    Get synonyms from API with fallback to local data
    """
    try:
        synonyms = dictionary_api.get_synonyms(word, limit)
        if synonyms:
            return synonyms
    except Exception as e:
        logger.warning(f"API synonym fetch failed for {word}: {e}")
    
    # Fallback to local data
    return FALLBACK_SYNONYMS.get(word, [])[:limit]

def get_word_definition(word: str) -> Optional[str]:
    """Get a simple definition for a word"""
    try:
        definitions = dictionary_api.get_definitions(word, 1)
        if definitions and 'definition' in definitions[0]:
            return definitions[0]['definition']
    except Exception as e:
        logger.warning(f"API definition fetch failed for {word}: {e}")
    
    return None

def assess_vocabulary_complexity(text: str) -> Dict[str, Any]:
    """Analyze text complexity using dictionary API"""
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    if not words:
        return {"error": "No words found in text"}
    
    complexity_counts = {"basic": 0, "intermediate": 0, "advanced": 0, "unknown": 0}
    unique_words = set(words)
    
    for word in unique_words:
        complexity = dictionary_api.get_word_complexity(word)
        complexity_counts[complexity] += 1
    
    total_analyzed = sum(complexity_counts.values()) - complexity_counts["unknown"]
    if total_analyzed > 0:
        advanced_ratio = complexity_counts["advanced"] / total_analyzed
    else:
        advanced_ratio = 0
    
    return {
        "total_words": len(words),
        "unique_words": len(unique_words),
        "complexity_distribution": complexity_counts,
        "advanced_ratio": round(advanced_ratio, 2),
        "vocabulary_level": _determine_overall_level(advanced_ratio, complexity_counts)
    }

def _determine_overall_level(advanced_ratio: float, complexity_counts: Dict) -> str:
    """Determine overall vocabulary level"""
    if advanced_ratio > 0.3:
        return "Advanced (C1-C2)"
    elif advanced_ratio > 0.15:
        return "Intermediate (B1-B2)"
    else:
        return "Basic (A1-A2)"