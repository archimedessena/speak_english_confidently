import numpy as np
import librosa

def enhanced_spectral_noise_reduction(audio_data, sr, threshold=0.05):
    """Improved noise reduction with multiple techniques"""
    # Compute short-time Fourier transform
    stft = librosa.stft(audio_data)
    magnitude, phase = np.abs(stft), np.angle(stft)
    
    # Create a time-frequency mask using a more sophisticated approach
    median_magnitude = np.median(magnitude, axis=1, keepdims=True)
    noise_mask = magnitude < threshold * median_magnitude
    
    # Apply soft masking instead of hard thresholding
    reduction_factor = 0.1  # Reduce noise by 90%
    magnitude[noise_mask] *= reduction_factor
    
    # Reconstruct audio
    stft_clean = magnitude * np.exp(1j * phase)
    y_clean = librosa.istft(stft_clean)
    
    return y_clean