import logging
import librosa

logger = logging.getLogger(__name__)

def analyze_pitch(audio_file):
    try:
        y, sr = librosa.load(audio_file)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch = pitches[magnitudes > 0].mean() if magnitudes.any() else 0
        logger.info(f"Average pitch: {pitch}")
        return pitch
    except Exception as e:
        logger.error(f"Pitch analysis error: {e}")
        return 0