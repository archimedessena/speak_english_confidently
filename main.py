import speech_recognition as sr
from gtts import gTTS
import playsound
import numpy as np
from pydub import AudioSegment
import librosa
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
        print("Speaking back...")
        os.system("afplay response.mp3")

        # delete the audio after playing
        os.remove("response.mp3")

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
    except sr.RequestError:
        print("Error connecting to the speech recognition service.")
        
        

def spectral_noise_reduction(audio_file, threshold=0.1):
    # Load audio with librosa
    y, sr = librosa.load(audio_file, sr=16000)
    
    # Compute short-time Fourier transform
    stft = librosa.stft(y)
    magnitude, phase = np.abs(stft), np.angle(stft)
    
    # Create noise mask (simple threshold-based)
    noise_mask = magnitude < threshold * np.max(magnitude)
    magnitude[noise_mask] = 0  # Zero out noisy frequencies
    
    # Reconstruct audio
    stft_clean = magnitude * np.exp(1j * phase)
    y_clean = librosa.istft(stft_clean)
    
    # Save cleaned audio
    output_file = "cleaned_audio.wav"
    librosa.output.write_wav(output_file, y_clean, sr)
    return output_file

def preprocess_audio(input_file, output_file="processed_audio.wav"):
    # Load with pydub
    audio = AudioSegment.from_wav(input_file)
    
    # Normalize volume
    audio = audio.normalize()
    
    # Apply low-pass filter (remove noise above 3kHz)
    audio = audio.low_pass_filter(3000)
    
    # Export processed audio
    audio.export(output_file, format="wav")
    return output_file

# Initialize recognizer
recognizer = sr.Recognizer()

# Capture audio
with sr.Microphone() as source:
    print("Say something (5 seconds)...")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
    print("Audio captured!")

# Save raw audio
raw_file = "raw_audio.wav"
with open(raw_file, "wb") as f:
    f.write(audio.get_wav_data())

# Preprocess with pydub
processed_file = preprocess_audio(raw_file)

# Further clean with librosa
cleaned_file = spectral_noise_reduction(processed_file)

# Transcribe processed audio
with sr.AudioFile(cleaned_file) as source:
    audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        with open("transcriptions.txt", "a") as f:
            f.write(f"Response: {text}\n")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"API error: {e}")
# Clean up temporary files
os.remove(raw_file)
os.remove(processed_file)
os.remove(cleaned_file)

