#import language_tool_python
#from typing import List, Dict, Any
#import logging
#import requests
#import time
#
## Set up logging
#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)
#
#class GrammarChecker:
#    def __init__(self, language='en-US'):
#        """Initialize LanguageTool with robust error handling"""
#        self.language = language  # Set this first
#        self.use_online = False
#        self.api_url = "https://api.languagetool.org/v2/check"
#        
#        try:
#            logger.info("Attempting to initialize offline LanguageTool...")
#            # Try with a longer timeout and explicit temp directory
#            self.tool = language_tool_python.LanguageTool(
#                language,
#                remote_url=None,  # Force offline mode
#                config={'cacheSize': 1000}
#            )
#            logger.info("✓ Offline LanguageTool initialized successfully")
#            
#        except Exception as e:
#            logger.warning(f"Offline LanguageTool failed: {e}")
#            logger.info("Falling back to online API mode")
#            self.tool = None
#            self.use_online = True
#    
#    def check_text(self, text: str) -> List[Dict[str, Any]]:
#        """
#        Check text for grammar and spelling errors
#        
#        Args:
#            text: Input text to check
#            
#        Returns:
#            List of error dictionaries with details
#        """
#        if not text or not text.strip():
#            return []
#            
#        try:
#            if not self.use_online and self.tool is not None:
#                # Use offline version
#                matches = self.tool.check(text)
#                return self._process_matches(matches, text)
#            else:
#                # Use online version
#                return self._check_online(text)
#        except Exception as e:
#            logger.error(f"Error in grammar checking: {e}")
#            return []
#    
#    def _check_online(self, text: str) -> List[Dict[str, Any]]:
#        """Use online LanguageTool API with proper error handling"""
#        try:
#            payload = {
#                'text': text,
#                'language': self.language,
#                'enabledOnly': 'false'
#            }
#            
#            logger.info(f"Using online API for text: '{text}'")
#            response = requests.post(self.api_url, data=payload, timeout=15)
#            response.raise_for_status()
#            data = response.json()
#            
#            logger.info(f"Online API found {len(data.get('matches', []))} errors")
#            return self._process_online_matches(data, text)
#            
#        except requests.exceptions.RequestException as e:
#            logger.error(f"Online API request failed: {e}")
#            return []
#        except Exception as e:
#            logger.error(f"Online grammar processing failed: {e}")
#            return []
#    
#    def _process_online_matches(self, data: dict, text: str) -> List[Dict[str, Any]]:
#        """Process online API response"""
#        matches = data.get('matches', [])
#        processed_errors = []
#        
#        for match in matches:
#            replacements = match.get('replacements', [])
#            suggested_text = replacements[0].get('value') if replacements else None
#            
#            error = {
#                'message': match.get('message', ''),
#                'short_message': match.get('shortMessage', ''),
#                'replacements': [r.get('value') for r in replacements],
#                'offset': match.get('offset', 0),
#                'length': match.get('length', 0),
#                'category': match.get('category', {}).get('id', 'unknown'),
#                'rule_id': match.get('rule', {}).get('id', ''),
#                'context': text[max(0, match.get('offset', 0)-20):match.get('offset', 0) + match.get('length', 0) + 20],
#                'error_text': text[match.get('offset', 0):match.get('offset', 0) + match.get('length', 0)],
#                'suggested_text': suggested_text
#            }
#            processed_errors.append(error)
#            
#        return processed_errors
#    
#    def _process_matches(self, matches: List, text: str) -> List[Dict[str, Any]]:
#        """Process LanguageTool matches into structured data"""
#        processed_errors = []
#        
#        for match in matches:
#            error = {
#                'message': match.message,
#                'short_message': match.short_message,
#                'replacements': match.replacements,
#                'offset': match.offset,
#                'length': match.length,
#                'category': match.category,
#                'rule_id': match.ruleId,
#                'context': text[max(0, match.offset-20):match.offset + match.length + 20],
#                'error_text': text[match.offset:match.offset + match.length],
#                'suggested_text': match.replacements[0] if match.replacements else None
#            }
#            processed_errors.append(error)
#            
#        return processed_errors
#    
#    def categorize_errors(self, errors: List[Dict[str, Any]]) -> Dict[str, List]:
#        """Categorize errors by type for better feedback"""
#        categories = {
#            'grammar': [],
#            'spelling': [],
#            'punctuation': [],
#            'style': [],
#            'typography': [],
#            'other': []
#        }
#        
#        for error in errors:
#            category = error.get('category', '').lower()
#            
#            if 'grammar' in category:
#                categories['grammar'].append(error)
#            elif 'spelling' in category:
#                categories['spelling'].append(error)
#            elif 'punctuation' in category:
#                categories['punctuation'].append(error)
#            elif 'style' in category:
#                categories['style'].append(error)
#            elif 'typography' in category:
#                categories['typography'].append(error)
#            else:
#                categories['other'].append(error)
#                
#        return categories
#    
#    def get_correction_summary(self, text: str) -> Dict[str, Any]:
#        """
#        Get comprehensive correction summary
#        
#        Args:
#            text: Input text to analyze
#            
#        Returns:
#            Dictionary with error summary and suggestions
#        """
#        errors = self.check_text(text)
#        categorized = self.categorize_errors(errors)
#        
#        return {
#            'original_text': text,
#            'total_errors': len(errors),
#            'errors_by_category': {k: len(v) for k, v in categorized.items()},
#            'categorized_errors': categorized,
#            'corrected_text': self.apply_corrections(text, errors),
#            'error_details': errors
#        }
#    
#    def apply_corrections(self, text: str, errors: List[Dict[str, Any]]) -> str:
#        """Apply all corrections to the text"""
#        if not errors:
#            return text
#            
#        # Sort errors by offset in reverse order to avoid offset issues
#        sorted_errors = sorted(errors, key=lambda x: x['offset'], reverse=True)
#        corrected_text = text
#        
#        for error in sorted_errors:
#            if error.get('suggested_text'):
#                start = error['offset']
#                end = start + error['length']
#                corrected_text = corrected_text[:start] + error['suggested_text'] + corrected_text[end:]
#                
#        return corrected_text
#    
#    def get_friendly_feedback(self, text: str) -> str:
#        """
#        Generate user-friendly feedback from grammar analysis
#        
#        Args:
#            text: Input text to analyze
#            
#        Returns:
#            Friendly feedback string
#        """
#        summary = self.get_correction_summary(text)
#        
#        if summary['total_errors'] == 0:
#            return "Excellent! No grammar or spelling errors found. 🎉"
#        
#        feedback = []
#        feedback.append(f"I found {summary['total_errors']} area(s) to improve:")
#        
#        # Add category-specific feedback
#        for category, count in summary['errors_by_category'].items():
#            if count > 0:
#                feedback.append(f"• {count} {category} issue(s)")
#        
#        # Add the most important corrections
#        feedback.append("\nHere are your main corrections:")
#        errors = summary['error_details'][:3]  # Show first 3 errors
#        for i, error in enumerate(errors, 1):
#            feedback.append(f"{i}. '{error.get('error_text', '')}' → '{error.get('suggested_text', '')}'")
#            feedback.append(f"   Reason: {error.get('message', '')}")
#        
#        if summary['total_errors'] > 3:
#            feedback.append(f"\n... and {summary['total_errors'] - 3} more improvements")
#        
#        feedback.append(f"\nCorrected sentence: \"{summary['corrected_text']}\"")
#        
#        return "\n".join(feedback)
#
## Singleton instance for easy access
#grammar_checker = GrammarChecker()
#
## Convenience functions
#def check_grammar(text: str) -> List[Dict[str, Any]]:
#    """Quick grammar check convenience function"""
#    return grammar_checker.check_text(text)
#
#def get_grammar_feedback(text: str) -> str:
#    """Quick feedback convenience function"""
#    return grammar_checker.get_friendly_feedback(text)
#
#def get_correction_summary(text: str) -> Dict[str, Any]:
#    """Get detailed correction summary"""
#    return grammar_checker.get_correction_summary(text)




"""
Robust grammar checker with multiple fallback strategies
"""

import logging
from typing import List, Dict, Any, Optional
import re
import requests
import time
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)

@dataclass
class GrammarError:
    message: str
    short_message: str
    replacements: List[str]
    offset: int
    length: int
    category: str
    rule_id: str
    error_text: str
    suggested_text: Optional[str] = None

class RobustGrammarChecker:
    def __init__(self):
        """Initialize with multiple checking strategies"""
        self.strategies = [
            self._try_language_tool_python,
            self._try_online_api,
            self._try_regex_patterns,
            self._try_llm_fallback
        ]
        self.current_strategy = None
        self.strategy_health = {strategy.__name__: True for strategy in self.strategies}
        
    def check_text(self, text: str) -> List[GrammarError]:
        """
        Robust grammar checking with multiple fallback strategies
        """
        if not text or not text.strip():
            return []
        
        for strategy in self.strategies:
            if self.strategy_health[strategy.__name__]:
                try:
                    self.current_strategy = strategy.__name__
                    errors = strategy(text)
                    if errors:
                        logger.info(f"✅ Used {strategy.__name__} successfully")
                        return errors
                except Exception as e:
                    logger.warning(f"❌ {strategy.__name__} failed: {e}")
                    self.strategy_health[strategy.__name__] = False
                    time.sleep(0.1)  # Brief pause between strategies
        
        logger.warning("All grammar check strategies failed")
        return []

    def _try_language_tool_python(self, text: str) -> List[GrammarError]:
        """Primary: LanguageTool Python package"""
        try:
            import language_tool_python
            tool = language_tool_python.LanguageTool('en-US')
            matches = tool.check(text)
            return self._process_matches(matches, text)
        except ImportError:
            logger.warning("language-tool-python not installed")
            raise
        except Exception as e:
            logger.error(f"LanguageTool failed: {e}")
            raise

    def _try_online_api(self, text: str) -> List[GrammarError]:
        """Fallback 1: Online LanguageTool API"""
        try:
            response = requests.post(
                "https://api.languagetool.org/v2/check",
                data={'text': text, 'language': 'en-US', 'enabledOnly': 'false'},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return self._process_online_matches(data, text)
        except Exception as e:
            logger.warning(f"Online API failed: {e}")
            raise

    def _try_regex_patterns(self, text: str) -> List[GrammarError]:
        """Fallback 2: Regex-based pattern matching"""
        patterns = [
            # Subject-verb agreement
            (r'\b(I|he|she|it) (go|do|have|be)\b', 
             lambda m: f"{m.group(1)} {m.group(2)}s" if m.group(2) != 'be' else f"{m.group(1)} is",
             "Subject-verb agreement"),
            
            (r'\b(you|we|they) (goes|does|has|is)\b',
             lambda m: f"{m.group(1)} {m.group(2)[:-2] if m.group(2).endswith('es') else m.group(2)[:-1]}",
             "Subject-verb agreement"),
            
            # Common confusions
            (r'\btheir\b', "they're", "Their vs they're"),
            (r'\byour\b', "you're", "Your vs you're"),
            (r'\bits\b', "it's", "Its vs it's"),
            (r'\bthere\b', "they're", "There vs they're"),
            (r'\bwhos\b', "who's", "Whos vs who's"),
            
            # Verb tense
            (r'\b(I|you|we|they) (was)\b', lambda m: f"{m.group(1)} were", "Verb tense"),
            (r'\b(he|she|it) (were)\b', lambda m: f"{m.group(1)} was", "Verb tense"),
            
            # Articles
            (r'\ba (a|e|i|o|u)[a-z]*\b', lambda m: f"an {m.group(1)}", "Article usage"),
            (r'\ban ([b-df-hj-np-tv-z])[a-z]*\b', lambda m: f"a {m.group(1)}", "Article usage"),
        ]
        
        errors = []
        for pattern, replacement, message in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                # Handle lambda replacements
                if callable(replacement):
                    suggested = replacement(match)
                else:
                    suggested = replacement
                
                error = GrammarError(
                    message=message,
                    short_message="Grammar error",
                    replacements=[suggested],
                    offset=match.start(),
                    length=len(match.group()),
                    category="grammar",
                    rule_id=f"regex_{hash(pattern) % 1000}",
                    error_text=match.group(),
                    suggested_text=suggested
                )
                errors.append(error)
        
        return errors

    def _try_llm_fallback(self, text: str) -> List[GrammarError]:
        """Fallback 3: Simple rule-based LLM-like approach"""
        # This is a very basic rule-based approach that mimics some LLM capabilities
        errors = []
        
        # Check for missing articles
        article_errors = self._check_articles(text)
        errors.extend(article_errors)
        
        # Check for preposition usage
        preposition_errors = self._check_prepositions(text)
        errors.extend(preposition_errors)
        
        # Check for common mistakes
        common_errors = self._check_common_mistakes(text)
        errors.extend(common_errors)
        
        return errors

    def _check_articles(self, text: str) -> List[GrammarError]:
        """Check article usage"""
        errors = []
        words = text.lower().split()
        
        for i, word in enumerate(words):
            if word in ['a', 'an', 'the'] and i + 1 < len(words):
                next_word = words[i + 1]
                
                # Check if article doesn't match next word
                if word == 'a' and next_word[0] in 'aeiou':
                    errors.append(GrammarError(
                        message="Use 'an' before vowel sounds",
                        short_message="Article error",
                        replacements=['an'],
                        offset=text.lower().find(f"a {next_word}"),
                        length=1,
                        category="grammar",
                        rule_id="article_vowel",
                        error_text="a",
                        suggested_text="an"
                    ))
                elif word == 'an' and next_word[0] not in 'aeiou':
                    errors.append(GrammarError(
                        message="Use 'a' before consonant sounds",
                        short_message="Article error",
                        replacements=['a'],
                        offset=text.lower().find(f"an {next_word}"),
                        length=2,
                        category="grammar",
                        rule_id="article_consonant",
                        error_text="an",
                        suggested_text="a"
                    ))
        
        return errors

    def _check_prepositions(self, text: str) -> List[GrammarError]:
        """Check preposition usage"""
        preposition_rules = [
            (r'\b(in|at|on) (morning|afternoon|evening)\b', 
             lambda m: "in" if m.group(2) in ["morning", "afternoon", "evening"] else m.group(1),
             "Preposition usage"),
            
            (r'\barrive (in|at)\b', 
             lambda m: "at" if any(word in text.lower() for word in ["airport", "station", "home"]) else "in",
             "Preposition usage"),
        ]
        
        errors = []
        for pattern, replacement, message in preposition_rules:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                if callable(replacement):
                    suggested = replacement(match)
                else:
                    suggested = replacement
                
                if suggested != match.group(1):
                    errors.append(GrammarError(
                        message=message,
                        short_message="Preposition error",
                        replacements=[suggested],
                        offset=match.start(1),
                        length=len(match.group(1)),
                        category="grammar",
                        rule_id=f"preposition_{hash(pattern) % 1000}",
                        error_text=match.group(1),
                        suggested_text=suggested
                    ))
        
        return errors

    def _check_common_mistakes(self, text: str) -> List[GrammarError]:
        """Check for common English mistakes"""
        common_mistakes = [
            (r'\bcould of\b', "could have", "Common mistake: could of → could have"),
            (r'\bwould of\b', "would have", "Common mistake: would of → would have"),
            (r'\bshould of\b', "should have", "Common mistake: should of → should have"),
            (r'\bmore then\b', "more than", "Common mistake: more then → more than"),
            (r'\bless then\b', "less than", "Common mistake: less then → less than"),
            (r'\balot\b', "a lot", "Common mistake: alot → a lot"),
        ]
        
        errors = []
        for pattern, replacement, message in common_mistakes:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                errors.append(GrammarError(
                    message=message,
                    short_message="Common mistake",
                    replacements=[replacement],
                    offset=match.start(),
                    length=len(match.group()),
                    category="grammar",
                    rule_id=f"common_{hash(pattern) % 1000}",
                    error_text=match.group(),
                    suggested_text=replacement
                ))
        
        return errors

    def _process_matches(self, matches: List, text: str) -> List[GrammarError]:
        """Process LanguageTool matches"""
        errors = []
        for match in matches:
            error = GrammarError(
                message=getattr(match, 'message', ''),
                short_message=getattr(match, 'short_message', ''),
                replacements=getattr(match, 'replacements', []),
                offset=getattr(match, 'offset', 0),
                length=getattr(match, 'length', 0),
                category=getattr(match, 'category', ''),
                rule_id=getattr(match, 'ruleId', ''),
                error_text=text[getattr(match, 'offset', 0):getattr(match, 'offset', 0) + getattr(match, 'length', 0)],
                suggested_text=match.replacements[0] if match.replacements else None
            )
            errors.append(error)
        return errors

    def _process_online_matches(self, data: dict, text: str) -> List[GrammarError]:
        """Process online API matches"""
        errors = []
        for match in data.get('matches', []):
            replacements = match.get('replacements', [])
            error = GrammarError(
                message=match.get('message', ''),
                short_message=match.get('shortMessage', ''),
                replacements=[r.get('value') for r in replacements],
                offset=match.get('offset', 0),
                length=match.get('length', 0),
                category=match.get('rule', {}).get('category', {}).get('id', ''),
                rule_id=match.get('rule', {}).get('id', ''),
                error_text=text[match.get('offset', 0):match.get('offset', 0) + match.get('length', 0)],
                suggested_text=replacements[0].get('value') if replacements else None
            )
            errors.append(error)
        return errors

    def get_health_status(self) -> Dict[str, bool]:
        """Get health status of all strategies"""
        return self.strategy_health.copy()

    def reset_strategy(self, strategy_name: str):
        """Reset a strategy's health status"""
        if strategy_name in self.strategy_health:
            self.strategy_health[strategy_name] = True

# Singleton instance
grammar_checker = RobustGrammarChecker()

# Convenience functions
def check_grammar(text: str) -> List[Dict[str, Any]]:
    """Check grammar and return dict format for compatibility"""
    errors = grammar_checker.check_text(text)
    return [error.__dict__ for error in errors]

def get_grammar_feedback(text: str) -> str:
    """Generate user-friendly feedback"""
    errors = grammar_checker.check_text(text)
    
    if not errors:
        return "Excellent! No grammar or spelling errors found. 🎉"
    
    feedback = []
    feedback.append(f"I found {len(errors)} area(s) to improve:")
    
    # Group by category
    categories = {}
    for error in errors:
        categories.setdefault(error.category, []).append(error)
    
    for category, category_errors in categories.items():
        feedback.append(f"• {len(category_errors)} {category} issue(s)")
    
    feedback.append("\nMain corrections:")
    for i, error in enumerate(errors[:3], 1):
        feedback.append(f"{i}. '{error.error_text}' → '{error.suggested_text}'")
        feedback.append(f"   Reason: {error.message}")
    
    if len(errors) > 3:
        feedback.append(f"\n... and {len(errors) - 3} more improvements")
    
    return "\n".join(feedback)