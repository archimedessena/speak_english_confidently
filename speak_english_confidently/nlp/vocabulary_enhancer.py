import nltk
from nltk.corpus import wordnet
class VocabularyEnhancer:
    def enhance_vocabulary(self, text):
        words = nltk.word_tokenize(text)
        suggestions = []
        for word in words[:5]:  # Limit to first 5 words
            synsets = wordnet.synsets(word)
            if synsets:
                suggestions.append({"word": word, "synonyms": [s.name() for s in synsets[:3]]})
        return suggestions
