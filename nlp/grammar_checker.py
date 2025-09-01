"""
Offline grammar checker using language-tool-python
"""

import language_tool_python
from typing import List, Dict, Any
import logging
import re

logger = logging.getLogger(__name__)

class OfflineGrammarChecker:
    def __init__(self, language='en-US'):
        """Initialize offline LanguageTool"""
        try:
            self.tool = language_tool_python.LanguageTool(language)
            logger.info("✅ Offline LanguageTool initialized successfully")
            self.available = True
        except Exception as e:
            logger.error(f"❌ Failed to initialize LanguageTool: {e}")
            self.available = False
            self.tool = None
    
    def check_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Check text for grammar errors offline
        
        Args:
            text: Text to check
            
        Returns:
            List of error dictionaries
        """
        if not text or not text.strip() or not self.available:
            return []
        
        try:
            matches = self.tool.check(text)
            return self._process_matches(matches, text)
        except Exception as e:
            logger.error(f"Grammar check failed: {e}")
            return []
    
    def _process_matches(self, matches: List, text: str) -> List[Dict[str, Any]]:
        """Process LanguageTool matches into structured data"""
        processed_errors = []
        
        for match in matches:
            error = {
                'message': match.message,
                'short_message': getattr(match, 'short_message', ''),
                'replacements': match.replacements,
                'offset': match.offset,
                'length': match.length,
                'category': getattr(match, 'category', ''),
                'rule_id': getattr(match, 'ruleId', ''),
                'context': text[max(0, match.offset-20):match.offset + match.length + 20],
                'error_text': text[match.offset:match.offset + match.length],
                'suggested_text': match.replacements[0] if match.replacements else None
            }
            processed_errors.append(error)
            
        return processed_errors
    
    def categorize_errors(self, errors: List[Dict[str, Any]]) -> Dict[str, List]:
        """Categorize errors by type"""
        categories = {
            'grammar': [],
            'spelling': [],
            'punctuation': [],
            'style': [],
            'typography': [],
            'other': []
        }
        
        for error in errors:
            category = error.get('category', '').lower()
            
            if 'grammar' in category:
                categories['grammar'].append(error)
            elif 'spelling' in category:
                categories['spelling'].append(error)
            elif 'punctuation' in category:
                categories['punctuation'].append(error)
            elif 'style' in category:
                categories['style'].append(error)
            elif 'typography' in category:
                categories['typography'].append(error)
            else:
                categories['other'].append(error)
                
        return categories
    
    def get_correction_summary(self, text: str) -> Dict[str, Any]:
        """Get comprehensive correction summary"""
        errors = self.check_text(text)
        categorized = self.categorize_errors(errors)
        
        return {
            'original_text': text,
            'total_errors': len(errors),
            'errors_by_category': {k: len(v) for k, v in categorized.items()},
            'categorized_errors': categorized,
            'corrected_text': self.apply_corrections(text, errors),
            'error_details': errors
        }
    
    def apply_corrections(self, text: str, errors: List[Dict[str, Any]]) -> str:
        """Apply all corrections to the text"""
        if not errors:
            return text
            
        sorted_errors = sorted(errors, key=lambda x: x['offset'], reverse=True)
        corrected_text = text
        
        for error in sorted_errors:
            if error['suggested_text']:
                start = error['offset']
                end = start + error['length']
                corrected_text = corrected_text[:start] + error['suggested_text'] + corrected_text[end:]
                
        return corrected_text
    
    def get_friendly_feedback(self, text: str) -> str:
        """Generate user-friendly feedback"""
        summary = self.get_correction_summary(text)
        
        if summary['total_errors'] == 0:
            return "Excellent! No grammar or spelling errors found. 🎉"
        
        feedback = []
        feedback.append(f"I found {summary['total_errors']} area(s) to improve:")
        
        for category, count in summary['errors_by_category'].items():
            if count > 0:
                feedback.append(f"• {count} {category} issue(s)")
        
        feedback.append("\nHere are your main corrections:")
        errors = summary['error_details'][:3]
        for i, error in enumerate(errors, 1):
            feedback.append(f"{i}. '{error['error_text']}' → '{error['suggested_text']}'")
            feedback.append(f"   Reason: {error['message']}")
        
        if summary['total_errors'] > 3:
            feedback.append(f"\n... and {summary['total_errors'] - 3} more improvements")
        
        feedback.append(f"\nCorrected sentence: \"{summary['corrected_text']}\"")
        
        return "\n".join(feedback)

# Singleton instance
grammar_checker = OfflineGrammarChecker()

# Convenience functions
def check_grammar(text: str) -> List[Dict[str, Any]]:
    return grammar_checker.check_text(text)

def get_grammar_feedback(text: str) -> str:
    return grammar_checker.get_friendly_feedback(text)

def get_correction_summary(text: str) -> Dict[str, Any]:
    return grammar_checker.get_correction_summary(text)