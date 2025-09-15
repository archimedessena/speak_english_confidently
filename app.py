#!/usr/bin/env python3
#"""
#Main application entry point for English Conversation Coach
#"""
#
#import os
#import sys
#import soundfile as sf
#import librosa
#
## Add the current directory to Python path
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#
## Import from our modules
#from audio.capture import record_and_recognize
#from audio.playback import text_to_speech
#from audio.processing.noise_reduction import enhanced_spectral_noise_reduction
#from audio.processing.preprocessing import preprocess_audio
#from audio.processing.pitch_analysis import analyze_pitch
#from audio.processing.tempo_analysis import analyze_tempo
#from audio.processing.feature_extraction import extract_spectral_features
#from utils.visualization import visualize_features
#from nlp.grammar_checker import get_grammar_feedback
#from nlp.vocabulary_enhancer import get_vocabulary_feedback, analyze_vocabulary  # NEW IMPORT
#
#def main():
#    """Main function to run the complete audio processing pipeline"""
#    # Record and recognize speech
#    text, audio = record_and_recognize()
#    
#    if text is None:
#        return
#    
#    # Grammar check and feedback
#    print("\n" + "="*50)
#    print("GRAMMAR ANALYSIS")
#    print("="*50)
#    grammar_feedback = get_grammar_feedback(text)
#    print(grammar_feedback)
#    
#    # NEW: Vocabulary enhancement
#    print("\n" + "="*50)
#    print("VOCABULARY ANALYSIS")
#    print("="*50)
#    vocabulary_feedback = get_vocabulary_feedback(text)
#    print(vocabulary_feedback)
#    
#    # NEW: Vocabulary level assessment
#    vocab_analysis = analyze_vocabulary(text)
#    print(f"\n📊 Vocabulary Level: {vocab_analysis['vocabulary_level']}")
#    print(f"📈 Diversity Score: {vocab_analysis['diversity_score']} (higher is better)")
#    
#    # Convert text back to speech
#    text_to_speech(text)
#    
#    # Save raw audio
#    raw_file = "raw_audio.wav"
#    with open(raw_file, "wb") as f:
#        f.write(audio.get_wav_data())
#    
#    # Preprocess with pydub
#    processed_file = preprocess_audio(raw_file)
#    
#    # Load and further process with librosa
#    y, sr = librosa.load(processed_file, sr=16000)
#    y_clean = enhanced_spectral_noise_reduction(y, sr)
#    
#    # Save cleaned audio
#    cleaned_file = "cleaned_audio.wav"
#    sf.write(cleaned_file, y_clean, sr)
#    
#    # Extract features
#    pitch_features = analyze_pitch(y_clean, sr)
#    tempo_features = analyze_tempo(y_clean, sr)
#    spectral_features = extract_spectral_features(y_clean, sr)
#    
#    # Combine all features
#    all_features = {
#        'pitch': pitch_features,
#        'tempo': tempo_features,
#        'spectral': spectral_features
#    }
#    
#    # Visualize features
#    visualize_features(y_clean, sr, all_features, "Your Speech Analysis")
#    
#    # Display analysis results
#    print("\n" + "="*50)
#    print("PRONUNCIATION ANALYSIS RESULTS")
#    print("="*50)
#    print(f"Mean Pitch: {pitch_features['mean_pitch']:.1f} Hz")
#    print(f"Pitch Range: {pitch_features['pitch_range'][0]:.1f}-{pitch_features['pitch_range'][1]:.1f} Hz")
#    print(f"Speaking Rate: {tempo_features['bpm']:.1f} BPM")
#    print(f"Rhythm Consistency: {tempo_features['interval_variability']:.3f} (lower is better)")
#    
#    # Clean up temporary files
#    os.remove(raw_file)
#    os.remove(processed_file)
#    os.remove(cleaned_file)
#
#if __name__ == "__main__":
#    main()



#!/usr/bin/env python3
"""
English Conversation Coach - Main Application
Robust offline version with comprehensive error handling
"""

import os
import sys
import time
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def setup_environment():
    """Setup and verify environment"""
    logger.info("Setting up environment...")
    
    # Check essential directories
    required_dirs = ['audio', 'nlp', 'utils']
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            logger.warning(f"Directory {dir_name} not found. Creating...")
            os.makedirs(dir_name, exist_ok=True)
    
    # Check for __init__.py files
    for dir_name in required_dirs:
        init_file = os.path.join(dir_name, '__init__.py')
        if not os.path.exists(init_file):
            logger.warning(f"Creating {init_file}")
            with open(init_file, 'w') as f:
                f.write("# Package initialization\n")
    
    return True

def import_with_fallback(module_name, class_name=None):
    """Robust import with fallback handling"""
    try:
        if class_name:
            module = __import__(module_name, fromlist=[class_name])
            return getattr(module, class_name)
        else:
            return __import__(module_name)
    except ImportError as e:
        logger.warning(f"Failed to import {module_name}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected import error: {e}")
        return None

# Import core components with fallbacks
try:
    # Audio processing components
    from audio.capture import record_and_recognize
    from audio.playback import text_to_speech
    from audio.processing.noise_reduction import enhanced_spectral_noise_reduction
    from audio.processing.preprocessing import preprocess_audio
    from audio.processing.pitch_analysis import analyze_pitch
    from audio.processing.tempo_analysis import analyze_tempo
    from audio.processing.feature_extraction import extract_spectral_features
    from utils.visualization import visualize_features
    
    # NLP components
    from nlp.grammar_checker import get_grammar_feedback, check_grammar
    from nlp.vocabulary_enhancer import get_vocabulary_feedback, enhance_vocabulary
    
    logger.info("✅ All modules imported successfully")
    
except ImportError as e:
    logger.error(f"Critical import failure: {e}")
    logger.info("Attempting to continue with fallback components...")
    
    # Define fallback functions for critical components
    def record_and_recognize():
        """Fallback audio recording"""
        logger.error("Audio capture not available")
        return None, None
    
    def text_to_speech(text):
        """Fallback text-to-speech"""
        logger.error("Text-to-speech not available")
        print(f"Text to speak: {text}")
    
    # Continue with other fallbacks as needed...

class EnglishCoach:
    """Main application class for English conversation coaching"""
    
    def __init__(self):
        self.setup_complete = False
        self.audio_available = True
        self.nlp_available = True
        
    def initialize(self):
        """Initialize the application"""
        logger.info("Initializing English Coach...")
        
        if not setup_environment():
            logger.error("Environment setup failed")
            return False
        
        # Check component availability
        self.audio_available = self._check_audio_components()
        self.nlp_available = self._check_nlp_components()
        
        self.setup_complete = True
        logger.info("✅ English Coach initialized successfully")
        return True
    
    def _check_audio_components(self):
        """Check if audio components are available"""
        try:
            # Test audio imports
            import soundfile as sf
            import librosa
            import numpy as np
            return True
        except ImportError as e:
            logger.warning(f"Audio components not available: {e}")
            return False
    
    def _check_nlp_components(self):
        """Check if NLP components are available"""
        try:
            # Test basic NLP functionality
            test_text = "I goes to the store."
            check_grammar(test_text)
            return True
        except Exception as e:
            logger.warning(f"NLP components not available: {e}")
            return False
    
    def run_conversation_session(self):
        """Run a complete conversation session"""
        if not self.setup_complete:
            logger.error("Application not initialized")
            return False
        
        print("\n" + "="*60)
        print("🎯 English Conversation Coach")
        print("="*60)
        
        try:
            # Record and process speech
            text, audio = self.record_speech()
            if not text:
                return False
            
            # Analyze language
            self.analyze_language(text)
            
            # Process audio features
            if self.audio_available and audio:
                self.analyze_pronunciation(audio)
            
            # Provide feedback and respond
            self.provide_feedback(text)
            
            return True
            
        except Exception as e:
            logger.error(f"Session failed: {e}")
            return False
    
    def record_speech(self):
        """Record and transcribe speech"""
        print("\n🎤 Ready to record...")
        print("Please speak clearly after the beep")
        
        try:
            text, audio = record_and_recognize()
            if text:
                print(f"📝 You said: \"{text}\"")
                return text, audio
            else:
                print("❌ Could not understand speech. Please try again.")
                return None, None
                
        except Exception as e:
            logger.error(f"Speech recording failed: {e}")
            print("❌ Audio recording error. Please check your microphone.")
            return None, None
    
    def analyze_language(self, text):
        """Analyze grammar and vocabulary"""
        if not self.nlp_available:
            print("❌ Language analysis unavailable")
            return
        
        print("\n" + "="*50)
        print("🔍 LANGUAGE ANALYSIS")
        print("="*50)
        
        # Grammar analysis
        try:
            grammar_feedback = get_grammar_feedback(text)
            print(grammar_feedback)
        except Exception as e:
            logger.error(f"Grammar analysis failed: {e}")
            print("❌ Grammar check unavailable")
        
        # Vocabulary analysis
        try:
            vocabulary_feedback = get_vocabulary_feedback(text)
            print(vocabulary_feedback)
        except Exception as e:
            logger.error(f"Vocabulary analysis failed: {e}")
            print("❌ Vocabulary analysis unavailable")
    
    def analyze_pronunciation(self, audio):
        """Analyze pronunciation and audio features"""
        if not self.audio_available:
            print("❌ Pronunciation analysis unavailable")
            return
        
        print("\n" + "="*50)
        print("🎵 PRONUNCIATION ANALYSIS")
        print("="*50)
        
        try:
            # Save and process audio
            raw_file = "raw_audio.wav"
            with open(raw_file, "wb") as f:
                f.write(audio.get_wav_data())
            
            # Preprocess audio
            processed_file = preprocess_audio(raw_file)
            
            # Load and analyze
            import librosa
            import soundfile as sf
            
            y, sr = librosa.load(processed_file, sr=16000)
            y_clean = enhanced_spectral_noise_reduction(y, sr)
            
            # Extract features
            pitch_features = analyze_pitch(y_clean, sr)
            tempo_features = analyze_tempo(y_clean, sr)
            spectral_features = extract_spectral_features(y_clean, sr)
            
            # Display results
            print(f"🎵 Mean Pitch: {pitch_features.get('mean_pitch', 'N/A'):.1f} Hz")
            print(f"📏 Pitch Range: {pitch_features.get('pitch_range', ('N/A', 'N/A'))[0]:.1f}-{pitch_features.get('pitch_range', ('N/A', 'N/A'))[1]:.1f} Hz")
            print(f"⏱️ Speaking Rate: {tempo_features.get('bpm', 'N/A'):.1f} BPM")
            
            # Clean up
            os.remove(raw_file)
            os.remove(processed_file)
            
        except Exception as e:
            logger.error(f"Pronunciation analysis failed: {e}")
            print("❌ Could not analyze pronunciation")
    
    def provide_feedback(self, text):
        """Provide overall feedback and respond"""
        print("\n" + "="*50)
        print("💡 FEEDBACK & RESPONSE")
        print("="*50)
        
        try:
            # Convert text to speech
            text_to_speech("Thank you for your response. Let me provide some feedback.")
            
            # Simple AI response based on content
            response = self.generate_response(text)
            print(f"💬 Coach: {response}")
            
            # Speak the response
            text_to_speech(response)
            
        except Exception as e:
            logger.error(f"Feedback generation failed: {e}")
            print("❌ Could not generate feedback")
    
    def generate_response(self, text):
        """Generate a contextual response"""
        # Simple rule-based response generation
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! How are you doing today?"
        elif any(word in text_lower for word in ['how are you', 'how do you do']):
            return "I'm doing well, thank you for asking! How can I help you practice English today?"
        elif any(word in text_lower for word in ['thank', 'thanks']):
            return "You're welcome! Keep up the good work with your English practice."
        elif any(word in text_lower for word in ['goodbye', 'bye', 'see you']):
            return "Goodbye! It was great practicing with you. See you next time!"
        else:
            return "That's interesting! Tell me more about that, or we can practice another sentence if you'd like."

def main():
    """Main application entry point"""
    print("Starting English Conversation Coach...")
    
    # Create application instance
    coach = EnglishCoach()
    
    # Initialize
    if not coach.initialize():
        print("❌ Failed to initialize application")
        return 1
    
    # Run session
    try:
        success = coach.run_conversation_session()
        if success:
            print("\n" + "="*60)
            print("✅ Session completed successfully!")
            print("="*60)
        else:
            print("\n❌ Session failed. Please check the logs for details.")
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n\n🛑 Session interrupted by user")
        return 0
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
        print(f"\n💥 Critical error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)