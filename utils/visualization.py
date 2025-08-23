import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np

def visualize_features(audio, sr, features, title="Audio Analysis"):
    """Create visualization of audio features"""
    fig, axes = plt.subplots(3, 2, figsize=(15, 10))
    fig.suptitle(title, fontsize=16)
    
    # Waveform
    times = librosa.times_like(audio, sr=sr)
    axes[0, 0].plot(times, audio)
    axes[0, 0].set_title('Waveform')
    axes[0, 0].set_ylabel('Amplitude')
    
    # Spectrogram
    spectrogram = librosa.amplitude_to_db(np.abs(librosa.stft(audio)), ref=np.max)
    img = librosa.display.specshow(spectrogram, sr=sr, x_axis='time', y_axis='log', ax=axes[0, 1])
    axes[0, 1].set_title('Spectrogram')
    fig.colorbar(img, ax=axes[0, 1], format="%+2.0f dB")
    
    # Pitch contour
    times_pitch = librosa.times_like(features['pitch']['f0'], sr=sr)
    axes[1, 0].plot(times_pitch, features['pitch']['f0'])
    axes[1, 0].set_title('Pitch Contour')
    axes[1, 0].set_ylabel('Frequency (Hz)')
    
    # MFCCs
    librosa.display.specshow(features['spectral']['mfccs'], sr=sr, x_axis='time', ax=axes[1, 1])
    axes[1, 1].set_title('MFCCs')
    
    # Spectral features
    times_spec = librosa.times_like(features['spectral']['spectral_centroid'], sr=sr)
    axes[2, 0].plot(times_spec, features['spectral']['spectral_centroid'], label='Centroid')
    axes[2, 0].plot(times_spec, features['spectral']['spectral_bandwidth'], label='Bandwidth')
    axes[2, 0].set_title('Spectral Features')
    axes[2, 0].set_ylabel('Frequency (Hz)')
    axes[2, 0].legend()
    
    # Zero-crossing rate
    times_zcr = librosa.times_like(features['spectral']['zcr'], sr=sr)
    axes[2, 1].plot(times_zcr, features['spectral']['zcr'])
    axes[2, 1].set_title('Zero-Crossing Rate')
    axes[2, 1].set_ylabel('Rate')
    axes[2, 1].set_xlabel('Time (s)')
    
    plt.tight_layout()
    plt.show()