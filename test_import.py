#!/usr/bin/env python3
"""Test script to verify imports work correctly"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from nlp.grammar_check import get_grammar_feedback, check_grammar
    print("✓ Successfully imported get_grammar_feedback and check_grammar")
    
    # Test the functions work
    test_text = "He need my assista."
    result = check_grammar(test_text)
    feedback = get_grammar_feedback(test_text)
    
    print(f"✓ Functions work correctly")
    print(f"Input: '{test_text}'")
    print(f"Errors found: {len(result)}")
    print(f"Feedback: {feedback}")
    
except ImportError as e:
    print(f"✗ Import failed: {e}")
    print("Checking what's available...")
    
    # See what's actually in the module
    try:
        from nlp import grammar_check
        print("Available names in grammar_check:")
        for name in dir(grammar_check):
            if not name.startswith('_'):
                print(f"  - {name}")
    except Exception as e2:
        print(f"Could not inspect module: {e2}")