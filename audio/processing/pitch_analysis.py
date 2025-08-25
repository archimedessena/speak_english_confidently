import numpy as np
import librosa

def analyze_pitch(audio, sr, fmin=75, fmax=400):
    """Extract pitch information using librosa"""
    # Extract pitch using PYIN algorithm
    f0, voiced_flag, voiced_probs = librosa.pyin(
        audio, 
        fmin=fmin, 
        fmax=fmax, 
        sr=sr
    )
    
    # Convert to semitones for musical analysis
    f0_clean = f0[voiced_flag]
    if len(f0_clean) > 0:
        f0_semitones = 12 * np.log2(f0_clean / 440) + 69  # MIDI note numbers
    else:
        f0_semitones = np.array([])
    
    return {
        'f0': f0,
        'voiced_flag': voiced_flag,
        'mean_pitch': np.mean(f0_clean) if len(f0_clean) > 0 else 0,
        'pitch_std': np.std(f0_clean) if len(f0_clean) > 0 else 0,
        'pitch_range': (np.min(f0_clean), np.max(f0_clean)) if len(f0_clean) > 0 else (0, 0),
        'semitones': f0_semitones
    }
    
    

