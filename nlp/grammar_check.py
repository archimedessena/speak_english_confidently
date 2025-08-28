import language_tool_python
from typing import List, Dict, Any
import logging
import requests
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GrammarChecker:
    def __init__(self, language='en-US'):
        """Initialize LanguageTool with robust error handling"""
        self.language = language  
        self.use_online = False
        self.api_url = "https://api.languagetool.org/v2/check"
        
        try:
            logger.info("Attempting to initialize offline LanguageTool...")
         
            self.tool = language_tool_python.LanguageTool(
                language,
                remote_url=None,  # Force offline mode
                config={'cacheSize': 1000}
            )
            logger.info("✓ Offline LanguageTool initialized successfully")
            
        except Exception as e:
            logger.warning(f"Offline LanguageTool failed: {e}")
            logger.info("Falling back to online API mode")
            self.tool = None
            self.use_online = True
    
    def check_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Check text for grammar and spelling errors
        
        Args:
            text: Input text to check
            
        Returns:
            List of error dictionaries with details
        """
        if not text or not text.strip():
            return []
            
        try:
            if not self.use_online and self.tool is not None:
                # Use offline version
                matches = self.tool.check(text)
                return self._process_matches(matches, text)
            else:
                # Use online version
                return self._check_online(text)
        except Exception as e:
            logger.error(f"Error in grammar checking: {e}")
            return []
    
    def _check_online(self, text: str) -> List[Dict[str, Any]]:
        """Use online LanguageTool API with proper error handling"""
        try:
            payload = {
                'text': text,
                'language': self.language,
                'enabledOnly': 'false'
            }
            
            logger.info(f"Using online API for text: '{text}'")
            response = requests.post(self.api_url, data=payload, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"Online API found {len(data.get('matches', []))} errors")
            return self._process_online_matches(data, text)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Online API request failed: {e}")
            return []
        except Exception as e:
            logger.error(f"Online grammar processing failed: {e}")
            return []
    
    def _process_online_matches(self, data: dict, text: str) -> List[Dict[str, Any]]:
        """Process online API response"""
        matches = data.get('matches', [])
        processed_errors = []
        
        for match in matches:
            replacements = match.get('replacements', [])
            suggested_text = replacements[0].get('value') if replacements else None
            
            error = {
                'message': match.get('message', ''),
                'short_message': match.get('shortMessage', ''),
                'replacements': [r.get('value') for r in replacements],
                'offset': match.get('offset', 0),
                'length': match.get('length', 0),
                'category': match.get('category', {}).get('id', 'unknown'),
                'rule_id': match.get('rule', {}).get('id', ''),
                'context': text[max(0, match.get('offset', 0)-20):match.get('offset', 0) + match.get('length', 0) + 20],
                'error_text': text[match.get('offset', 0):match.get('offset', 0) + match.get('length', 0)],
                'suggested_text': suggested_text
            }
            processed_errors.append(error)
            
        return processed_errors
    
    def _process_matches(self, matches: List, text: str) -> List[Dict[str, Any]]:
        """Process LanguageTool matches into structured data"""
        processed_errors = []
        
        for match in matches:
            error = {
                'message': match.message,
                'short_message': match.short_message,
                'replacements': match.replacements,
                'offset': match.offset,
                'length': match.length,
                'category': match.category,
                'rule_id': match.ruleId,
                'context': text[max(0, match.offset-20):match.offset + match.length + 20],
                'error_text': text[match.offset:match.offset + match.length],
                'suggested_text': match.replacements[0] if match.replacements else None
            }
            processed_errors.append(error)
            
        return processed_errors
    
    def categorize_errors(self, errors: List[Dict[str, Any]]) -> Dict[str, List]:
        """Categorize errors by type for better feedback"""
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
        """
        Get comprehensive correction summary
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with error summary and suggestions
        """
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
            
        # Sort errors by offset in reverse order to avoid offset issues
        sorted_errors = sorted(errors, key=lambda x: x['offset'], reverse=True)
        corrected_text = text
        
        for error in sorted_errors:
            if error.get('suggested_text'):
                start = error['offset']
                end = start + error['length']
                corrected_text = corrected_text[:start] + error['suggested_text'] + corrected_text[end:]
                
        return corrected_text
    
    def get_friendly_feedback(self, text: str) -> str:
        """
        Generate user-friendly feedback from grammar analysis
        
        Args:
            text: Input text to analyze
            
        Returns:
            Friendly feedback string
        """
        summary = self.get_correction_summary(text)
        
        if summary['total_errors'] == 0:
            return "Excellent! No grammar or spelling errors found. 🎉"
        
        feedback = []
        feedback.append(f"I found {summary['total_errors']} area(s) to improve:")
        
        # Add category-specific feedback
        for category, count in summary['errors_by_category'].items():
            if count > 0:
                feedback.append(f"• {count} {category} issue(s)")
        
        # Add the most important corrections
        feedback.append("\nHere are your main corrections:")
        errors = summary['error_details'][:3]  # Show first 3 errors
        for i, error in enumerate(errors, 1):
            feedback.append(f"{i}. '{error.get('error_text', '')}' → '{error.get('suggested_text', '')}'")
            feedback.append(f"   Reason: {error.get('message', '')}")
        
        if summary['total_errors'] > 3:
            feedback.append(f"\n... and {summary['total_errors'] - 3} more improvements")
        
        feedback.append(f"\nCorrected sentence: \"{summary['corrected_text']}\"")
        
        return "\n".join(feedback)

# Singleton instance for easy access
grammar_checker = GrammarChecker()

# Convenience functions
def check_grammar(text: str) -> List[Dict[str, Any]]:
    """Quick grammar check convenience function"""
    return grammar_checker.check_text(text)

def get_grammar_feedback(text: str) -> str:
    """Quick feedback convenience function"""
    return grammar_checker.get_friendly_feedback(text)

def get_correction_summary(text: str) -> Dict[str, Any]:
    """Get detailed correction summary"""
    return grammar_checker.get_correction_summary(text)