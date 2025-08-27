import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

def record_and_recognize():
    """Record audio and convert to text"""
    with sr.Microphone() as source:
        print("Start talking, Sena is listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        
        try:
            # Speech to text
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text, audio
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return None, None
        except sr.RequestError:
            print("Error connecting to the speech recognition service.")
            return None, None