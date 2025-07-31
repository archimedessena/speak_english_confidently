import speech_recognition as sr
# Initialize recognizer
recognizer = sr.Recognizer()

# Capture audio from microphone
with sr.Microphone() as source:
    print("Say something...")
    audio = recognizer.listen(source, timeout=5)  # 5-second recording
    print("Audio captured!")