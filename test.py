import speech_recognition as sr
from gtts import gTTS
import playsound
import os

# Initialize recognizer
recognizer = sr.Recognizer()

# Capture audio
with sr.Microphone() as source:
    print("Say something...")
    audio = recognizer.listen(source)

    try:
        # Speech to text
        text = recognizer.recognize_google(audio)
        print("You said:", text)

        # Text to speech
        tts = gTTS(text=text, lang='en')
        tts.save("response.mp3")
        print("🔊 Speaking back...")
        os.system("afplay response.mp3")

        # delete the audio after playing
        os.remove("response.mp3")

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
    except sr.RequestError:
        print("Error connecting to the speech recognition service.")

