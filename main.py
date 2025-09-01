#!/usr/bin/env python3
"""
Main application entry point for English Conversation Coach
Now with 100% offline functionality!
"""

import os
import sys
import soundfile as sf
import librosa

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import from our modules
from audio.capture import record_and_recognize
from audio.playback import text_to_speech
from audio.processing.noise_reduction import enhanced_spectral_noise_reduction
from audio.processing.preprocessing import preprocess_audio
from audio.processing.pitch_analysis import analyze_pitch
from audio.processing.tempo_analysis import analyze_tempo
from audio.processing.feature_extraction import extract_spectral_features
from utils.visualization import visualize_features

# Import OFFLINE NLP modules
from nlp.grammar_checker import get_grammar_feedback, check_grammar
from nlp.dictionary_enhancer import get_vocabulary_feedback, enhance_vocabulary

def main():
    """Main function to run the complete offline audio processing pipeline"""
    print("=" * 60)
    print("🎯 English Conversation Coach - OFFLINE MODE")
    print("=" * 60)
    
    # Record and recognize speech
    text, audio = record_and_recognize()
    
    if text is None:
        return
    
    print(f"\n📝 You said: \"{text}\"")
    
    # Grammar check and feedback (OFFLINE)
    print("\n" + "=" * 50)
    print("🔍 GRAMMAR ANALYSIS (Offline)")
    print("=" * 50)
    grammar_feedback = get_grammar_feedback(text)
    print(grammar_feedback)
    
    # Vocabulary enhancement (OFFLINE)
    print("\n" + "=" * 50)
    print("📚 VOCABULARY ANALYSIS (Offline)")
    print("=" * 50)
    vocabulary_feedback = get_vocabulary_feedback(text)
    print(vocabulary_feedback)
    
    # Show detailed enhancements
    enhancements = enhance_vocabulary(text)
    if enhancements:
        print(f"\n💎 Suggested enhancements:")
        for enh in enhancements:
            print(f"   {enh['common_word']} → {enh['suggested_word']} ({enh['complexity']})")
    
    # Convert text back to speech
    print("\n" + "=" * 50)
    print("🗣️  SPEAKING BACK")
    print("=" * 50)
    text_to_speech(text)
    
    # Audio processing and analysis
    print("\n" + "=" * 50)
    print("🎵 AUDIO ANALYSIS")
    print("=" * 50)
    
    # Save raw audio
    raw_file = "raw_audio.wav"
    with open(raw_file, "wb") as f:
        f.write(audio.get_wav_data())
    
    # Preprocess with pydub
    processed_file = preprocess_audio(raw_file)
    
    # Load and further process with librosa
    y, sr = librosa.load(processed_file, sr=16000)
    y_clean = enhanced_spectral_noise_reduction(y, sr)
    
    # Save cleaned audio
    cleaned_file = "cleaned_audio.wav"
    sf.write(cleaned_file, y_clean, sr)
    
    # Extract features
    pitch_features = analyze_pitch(y_clean, sr)
    tempo_features = analyze_tempo(y_clean, sr)
    spectral_features = extract_spectral_features(y_clean, sr)
    
    # Combine all features
    all_features = {
        'pitch': pitch_features,
        'tempo': tempo_features,
        'spectral': spectral_features
    }
    
    # Visualize features
    visualize_features(y_clean, sr, all_features, "Your Speech Analysis")
    
    # Display analysis results
    print("\n" + "=" * 50)
    print("📊 PRONUNCIATION ANALYSIS RESULTS")
    print("=" * 50)
    print(f"🎵 Mean Pitch: {pitch_features['mean_pitch']:.1f} Hz")
    print(f"📏 Pitch Range: {pitch_features['pitch_range'][0]:.1f}-{pitch_features['pitch_range'][1]:.1f} Hz")
    print(f"⏱️  Speaking Rate: {tempo_features['bpm']:.1f} BPM")
    print(f"🎭 Rhythm Consistency: {tempo_features['interval_variability']:.3f} (lower is better)")
    
    # Clean up temporary files
    os.remove(raw_file)
    os.remove(processed_file)
    os.remove(cleaned_file)
    
    print("\n" + "=" * 60)
    print("✅ Analysis complete! Your English coaching session is finished.")
    print("=" * 60)

if __name__ == "__main__":
    main()