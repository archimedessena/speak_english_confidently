import librosa

def extract_spectral_features(audio, sr):
    """Extract comprehensive spectral features"""
    # MFCCs
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    
    # Spectral centroid
    spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
    
    # Spectral bandwidth
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=sr)[0]
    
    # Spectral contrast
    spectral_contrast = librosa.feature.spectral_contrast(y=audio, sr=sr)[0]
    
    # Zero-crossing rate
    zcr = librosa.feature.zero_crossing_rate(audio)[0]
    
    return {
        'mfccs': mfccs,
        'spectral_centroid': spectral_centroid,
        'spectral_bandwidth': spectral_bandwidth,
        'spectral_contrast': spectral_contrast,
        'zcr': zcr
    }