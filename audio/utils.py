import logging

logger = logging.getLogger(__name__)

# Audio helper functions
def load_audio(file_path):
    try:
        import librosa
        y, sr = librosa.load(file_path)
        return y, sr
    except Exception as e:
        logger.error(f"Load audio error: {e}")
        return None, None