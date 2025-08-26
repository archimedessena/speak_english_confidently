#!/usr/bin/env python3
"""
Main application entry point for English Conversation Coach
"""

import os
import soundfile as sf
import librosa


from audio.capture import record_and_recognize
from audio.playback import text_to_speech
from audio.processing.noise_reduction import enhanced_spectral_noise_reduction
from audio.processing.preprocessing import preprocess_audio
from audio.processing.pitch_analysis import analyze_pitch
from audio.processing.tempo_analysis import analyze_tempo
from audio.processing.feature_extraction import extract_spectral_features
from utils.visualization import visualize_features

from nlp.grammar_check import check_text
from nlp.vocabulary_enhancer import preprocess_text, suggest_synonyms, load_vocabulary_tracker, save_vocabulary_tracker, track_vocabulary, vocabulary_enhancers 

def main():
    """Main function to run the complete audio processing pipeline"""
    # Record and recognize speech
    text, audio = record_and_recognize()
    
    if text is None:
        return
    
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
    print("\n=== PRONUNCIATION ANALYSIS RESULTS ===")
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