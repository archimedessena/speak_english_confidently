from pydub import AudioSegment

def preprocess_audio(input_file, output_file="processed_audio.wav"):
    """Enhanced audio preprocessing"""
    # Load with pydub
    audio = AudioSegment.from_wav(input_file)
    
    # Normalize volume
    audio = audio.normalize()
    
    # Apply band-pass filter (300Hz-3000Hz) for speech frequencies
    audio = audio.high_pass_filter(300)
    audio = audio.low_pass_filter(3000)
    
    # Compress dynamic range for clearer speech
    audio = audio.compress_dynamic_range()
    
    # Export processed audio
    audio.export(output_file, format="wav")
    return output_file