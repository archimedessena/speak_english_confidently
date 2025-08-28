#!/usr/bin/env python3
"""Test script for vocabulary enhancement functionality"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from nlp.vocabulary_enhancer import get_vocabulary_feedback, analyze_vocabulary

def test_vocabulary_enhancer():
    """Test the vocabulary enhancer with various sentences"""
    
    test_cases = [
        "This is a good thing that makes me happy.",
        "I think it's important to say what you want to get from life.",
        "The big house had small windows and old furniture.",
        "She is smart and knows how to make people feel good.",
        "It was a beautiful day with nice weather and happy people."
    ]
    
    print("Testing Vocabulary Enhancement")
    print("=" * 60)
    
    for i, sentence in enumerate(test_cases, 1):
        print(f"\nTest {i}: '{sentence}'")
        print("-" * 40)
        
        # Get vocabulary feedback
        feedback = get_vocabulary_feedback(sentence)
        print(feedback)
        
        # Get detailed analysis
        analysis = analyze_vocabulary(sentence)
        print(f"\nDetailed Analysis:")
        print(f"  Total words: {analysis['total_words']}")
        print(f"  Unique words: {analysis['unique_words']}")
        print(f"  Diversity score: {analysis['diversity_score']}")
        print(f"  Common words: {analysis['common_words_count']}")
        print(f"  Advanced words: {analysis['advanced_words_count']}")
        print(f"  Overall level: {analysis['vocabulary_level']}")

if __name__ == "__main__":
    test_vocabulary_enhancer()