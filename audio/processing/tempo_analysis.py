import numpy as np
import librosa

def analyze_tempo(audio, sr):
    """Extract tempo and rhythm features"""
    # Onset detection
    onset_env = librosa.onset.onset_strength(y=audio, sr=sr)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    
    # Rhythm patterns
    pulse = librosa.beat.plp(onset_envelope=onset_env, sr=sr)
    
    # Beat intervals
    beat_times = librosa.frames_to_time(beats, sr=sr)
    if len(beat_times) > 1:
        intervals = np.diff(beat_times)
        interval_variability = np.std(intervals)
    else:
        intervals = np.array([])
        interval_variability = 0
    
    return {
        'bpm': tempo,
        'beats': beats,
        'beat_times': beat_times,
        'intervals': intervals,
        'interval_variability': interval_variability,
        'pulse': pulse
    }