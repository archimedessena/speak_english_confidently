import os
import logging
from dotenv import load_dotenv

from audio.capture import capture_speech
from audio.playback import play_text
from audio.processing.noise_reduction import reduce_noise
from audio.processing.pitch_analysis import analyze_pitch
from audio.processing.tempo_analysis import analyze_tempo
from audio.processing.feature_extraction import extract_features

from nlp.grammar_checker import check_grammar
from nlp.vocabulary_enhancer import enhance_vocabulary
from nlp.response_generator import generate_response

from conversation.state_manager import ConversationState
from conversation.dialog_manager import manage_dialog
from conversation.feedback_engine import generate_feedback

from utils.config import Config
from utils.logger import setup_logging
from utils.helpers import save_user_progress

load_dotenv()
setup_logging()

logger = logging.getLogger(__name__)

def main():
    config = Config()
    state = ConversationState()

    logger.info("Starting Speak English Confidently app...")

    try:
        while True:
            # Prompt user
            prompt = manage_dialog(state)
            play_text(prompt)
            print(prompt)  # For CLI visibility

            # Capture speech
            audio_file, transcript = capture_speech()
            if not transcript:
                continue

            if "quit" in transcript.lower():
                break

            # Process audio
            cleaned_audio = reduce_noise(audio_file)
            pitch = analyze_pitch(cleaned_audio)
            tempo = analyze_tempo(cleaned_audio)
            features = extract_features(cleaned_audio)

            # NLP processing
            corrections = check_grammar(transcript)
            enhanced_text = enhance_vocabulary(transcript)

            # Generate response and feedback
            response = generate_response(enhanced_text)
            feedback = generate_feedback(transcript, corrections, pitch, tempo, features)

            # Update state and save progress
            state.update(transcript, response, feedback)
            save_user_progress(state.to_dict(), "data/user_progress/user.json")

            # Playback
            play_text(response + " " + feedback)
            print(response + "\nFeedback: " + feedback)
    except Exception as e:
        logger.error(f"App error: {e}")
    finally:
        logger.info("App shutdown.")

if __name__ == "__main__":
    main()