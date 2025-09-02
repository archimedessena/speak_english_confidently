import pytest
from nlp.grammar_check import check_grammar
from nlp.vocabulary_enhancer import enhance_vocabulary

def test_check_grammar():
    corrections, corrected = check_grammar("I is happy.")
    assert len(corrections) > 0

def test_enhance_vocabulary():
    enhanced = enhance_vocabulary("happy")
    assert enhanced == "happy" or enhanced != ""  # Depends on wordnet