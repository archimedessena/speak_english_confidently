import logging
import librosa
import noisereduce as nr
import soundfile as sf

logger = logging.getLogger(__name__)

def reduce_noise(audio_file):
    try:
        y, sr = librosa.load(audio_file)
        reduced = nr.reduce_noise(y=y, sr=sr)
        cleaned_file = audio_file.replace("raw", "cleaned")
        sf.write(cleaned_file, reduced, sr)
        logger.info(f"Noise reduced: {cleaned_file}")
        return cleaned_file
    except Exception as e:
        logger.error(f"Noise reduction error: {e}")
        return audio_file  # Fallback to original