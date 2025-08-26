import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from collections import Counter
import re
import json
import os

# Ensure NLTK data is downloaded
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

def preprocess_text(text):
    """Clean and tokenize text, removing punctuation and stopwords."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    return [word for word in words if word not in stop_words and word.isalpha()]

def get_word_frequencies(words, top_n=10):
    """Return the top N most frequent words and their counts."""
    word_counts = Counter(words)
    return word_counts.most_common(top_n)

def get_synonyms(word):
    """Retrieve up to 3 synonyms for a word using WordNet."""
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonym = lemma.name().lower()
            if synonym != word and '_' not in synonym:  # Exclude multi-word phrases
                synonyms.add(synonym)
    return list(synonyms)[:3]

def suggest_enhancements(word_frequencies):
    """Suggest synonyms for each word in the frequency list."""
    return {word: get_synonyms(word) for word, freq in word_frequencies}

def load_vocabulary_tracker(file_path='vocab_tracker.json'):
    """Load the vocabulary tracker from a JSON file."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return {"learned_words": [], "replacements": {}}

def save_vocabulary_tracker(vocab_tracker, file_path='vocab_tracker.json'):
    """Save the vocabulary tracker to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(vocab_tracker, f, indent=4)

def track_vocabulary(word, synonym, vocab_tracker):
    """Track a word and its chosen synonym in the vocabulary tracker."""
    vocab_tracker["learned_words"].append(word)
    if word in vocab_tracker["replacements"]:
        vocab_tracker["replacements"][word].append(synonym)
    else:
        vocab_tracker["replacements"][word] = [synonym]
    return vocab_tracker

def vocabulary_enhancers(text, top_n=10, vocab_file='vocab_tracker.json'):
    """Main function to analyze text, suggest synonyms, and track vocabulary."""
    # Initialize vocabulary tracker
    vocab_tracker = load_vocabulary_tracker(vocab_file)
    
    # Preprocess text
    words = preprocess_text(text)
    
    # Perform word frequency analysis
    frequencies = get_word_frequencies(words, top_n)
    
    # Suggest synonyms
    enhancements = suggest_enhancements(frequencies)
    
    # Print frequency analysis
    print("\nTop Word Frequencies:")
    for word, count in frequencies:
        print(f"{word}: {count}")
    
    # Print thesaurus suggestions
    print("\nThesaurus Suggestions:")
    for word, synonyms in enhancements.items():
        print(f"Word: {word}, Suggested Synonyms: {', '.join(synonyms) if synonyms else 'None'}")
    
    # Simulate user selecting synonyms to track (for demo, pick first synonym if available)
    print("\nTracking Vocabulary:")
    for word, synonyms in enhancements.items():
        if synonyms:  # Only track if synonyms exist
            chosen_synonym = synonyms[0]  # For simplicity, pick first synonym
            vocab_tracker = track_vocabulary(word, chosen_synonym, vocab_tracker)
            print(f"Tracked: Replaced '{word}' with '{chosen_synonym}'")
    
    # Save vocabulary tracker
    save_vocabulary_tracker(vocab_tracker, vocab_file)
    
    # Print current vocabulary tracker state
    print("\nCurrent Vocabulary Tracker:")
    print(f"Learned Words: {vocab_tracker['learned_words']}")
    print("Replacements:")
    for word, syns in vocab_tracker["replacements"].items():
        print(f"{word}: {syns}")

# Example usage
#if __name__ == "__main__":
#    sample_text = """
#    This is a sample text. We're keeping this text short to keep things manageable.
#    The text includes some repeated words to demonstrate frequency analysis.
#    """
#    vocabulary_enhancers(sample_text)