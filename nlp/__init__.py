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

__all__ = [
    'GrammarChecker',
    'check_grammar',
    'get_grammar_feedback', 
    'get_correction_summary',
    'grammar_checker'
]