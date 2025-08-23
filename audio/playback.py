from gtts import gTTS
import os

def text_to_speech(text):
    """Convert text to speech and play it"""
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    print("Speaking back...")
    os.system("afplay response.mp3")
    os.remove("response.mp3")