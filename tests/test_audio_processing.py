import pytest
from audio.processing.noise_reduction import reduce_noise
from audio.processing.pitch_analysis import analyze_pitch

def test_reduce_noise(tmp_path):
    # Mock audio file (create a dummy wav)
    dummy_file = tmp_path / "dummy.wav"
    dummy_file.write_bytes(b'')
    cleaned = reduce_noise(str(dummy_file))
    assert cleaned == str(dummy_file)  # Fallback

def test_analyze_pitch(tmp_path):
    dummy_file = tmp_path / "dummy.wav"
    dummy_file.write_bytes(b'')
    pitch = analyze_pitch(str(dummy_file))
    assert pitch == 0