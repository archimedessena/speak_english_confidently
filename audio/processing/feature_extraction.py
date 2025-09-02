import logging
import librosa
import numpy as np

logger = logging.getLogger(__name__)

def extract_features(audio_file):
    try:
        y, sr = librosa.load(audio_file)
        mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr), axis=1)
        logger.info("Features extracted.")
        return mfcc.tolist()
    except Exception as e:
        logger.error(f"Feature extraction error: {e}")
        return []