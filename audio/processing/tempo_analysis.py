import logging
import librosa

logger = logging.getLogger(__name__)

def analyze_tempo(audio_file):
    try:
        y, sr = librosa.load(audio_file)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        logger.info(f"Estimated tempo: {tempo}")
        return tempo
    except Exception as e:
        logger.error(f"Tempo analysis error: {e}")
        return 0