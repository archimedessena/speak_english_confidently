import os
import logging
import speech_recognition as sr
from datetime import datetime

from utils.config import Config
from utils.helpers import ensure_directory

logger = logging.getLogger(__name__)

def capture_speech():
    config = Config()
    r = sr.Recognizer()
    mic = sr.Microphone()

    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=config.AUDIO_TIMEOUT)

        # Save raw audio
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_dir = "data/audio_samples"
        ensure_directory(audio_dir)
        audio_file = os.path.join(audio_dir, f"raw_{timestamp}.wav")
        with open(audio_file, "wb") as f:
            f.write(audio.get_wav_data())

        transcript = r.recognize_google(audio)
        logger.info(f"Transcribed: {transcript}")
        return audio_file, transcript
    except sr.WaitTimeoutError:
        logger.warning("Listening timed out.")
        return None, None
    except sr.UnknownValueError:
        logger.warning("Could not understand audio.")
        return None, None
    except Exception as e:
        logger.error(f"Capture error: {e}")
        return None, None