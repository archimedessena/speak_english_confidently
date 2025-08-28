
"""
NLP module for grammar checking and language processing.
"""

from .grammar_check import (
    GrammarChecker,
    check_grammar,
    get_grammar_feedback,
    get_correction_summary,
    grammar_checker
)

from .vocabulary_enhancer import (
    VocabularyEnhancer,
    enhance_vocabulary,
    get_vocabulary_feedback,
    analyze_vocabulary,
    vocabulary_enhancer
)

__all__ = [
    'GrammarChecker',
    'check_grammar',
    'get_grammar_feedback', 
    'get_correction_summary',
    'grammar_checker',
    'VocabularyEnhancer',
    'enhance_vocabulary',
    'get_vocabulary_feedback',
    'analyze_vocabulary',
    'vocabulary_enhancer'
]