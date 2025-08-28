#!/usr/bin/env python3
"""
Main application entry point for English Conversation Coach
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
from nlp.grammar_check import get_grammar_feedback
from nlp.vocabulary_enhancer import get_vocabulary_feedback, analyze_vocabulary  
from nlp.vocabulary_enhancer import get_vocabulary_feedback, analyze_vocabulary

def main():
    """Main function to run the complete audio processing pipeline"""
    # Record and recognize speech
    text, audio = record_and_recognize()
    
    if text is None:
        return
    
    # Grammar check and feedback
    print("\n" + "="*50)
    print("GRAMMAR ANALYSIS")
    print("="*50)
    grammar_feedback = get_grammar_feedback(text)
    print(grammar_feedback)
    
    
    # Vocabulary enhancement
    print("\n" + "="*50)
    print("VOCABULARY ANALYSIS")
    print("="*50)
    vocabulary_feedback = get_vocabulary_feedback(text)
    print(vocabulary_feedback)
    
    #  Vocabulary level assessment
    vocab_analysis = analyze_vocabulary(text)
    print(f"\n📊 Vocabulary Level: {vocab_analysis['vocabulary_level']}")
    print(f"📈 Diversity Score: {vocab_analysis['diversity_score']} (higher is better)")
    
    # Detailed analysis
    vocab_analysis = analyze_vocabulary(text)
    print(f"\n📊 Detailed Analysis:")
    print(f"   Total words: {vocab_analysis.get('total_words', 0)}")
    print(f"   Unique words: {vocab_analysis.get('unique_words', 0)}")
    print(f"   Advanced ratio: {vocab_analysis.get('advanced_ratio', 0) * 100:.1f}%")

    # Convert text back to speech
    text_to_speech(text)
    
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
    print("\n" + "="*50)
    print("PRONUNCIATION ANALYSIS RESULTS")
    print("="*50)
    print(f"Mean Pitch: {pitch_features['mean_pitch']:.1f} Hz")
    print(f"Pitch Range: {pitch_features['pitch_range'][0]:.1f}-{pitch_features['pitch_range'][1]:.1f} Hz")
    print(f"Speaking Rate: {tempo_features['bpm']:.1f} BPM")
    print(f"Rhythm Consistency: {tempo_features['interval_variability']:.3f} (lower is better)")
    
    # Clean up temporary files
    os.remove(raw_file)
    os.remove(processed_file)
    os.remove(cleaned_file)

if __name__ == "__main__":
    main()