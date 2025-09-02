import os
import logging
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

logger = logging.getLogger(__name__)

def play_text(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang)
        temp_file = "temp.mp3"
        tts.save(temp_file)
        audio = AudioSegment.from_mp3(temp_file)
        play(audio)
        os.remove(temp_file)
        logger.info("Playback successful.")
    except Exception as e:
        logger.error(f"Playback error: {e}")