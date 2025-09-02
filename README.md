# Speak English Confidently

A Python app to help non-native speakers practice English conversation with AI feedback on pronunciation, grammar, and vocabulary.

## Features
- Real-time speech capture and transcription.
- Audio processing: noise reduction, pitch/tempo analysis.
- NLP: Grammar checking, vocabulary suggestions.
- AI-powered conversation coaching using OpenAI.
- Personalized feedback and progress tracking.
- Text-to-speech playback for responses.

## Installation
1. Clone the repo: `git clone <repo-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Download NLTK data: Run `python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"`
4. Set up environment variables in `.env` (e.g., OPENAI_API_KEY=your_key)
5. Run the app: `python app.py`

## Usage
- The app starts a conversation loop.
- Speak into your microphone when prompted.
- Receive feedback and continue practicing.
- Exit with 'quit' (typed or spoken).

## Data Storage
- Audio samples saved in `data/audio_samples/`.
- User progress in `data/user_progress/user.json`.

## Tests
Run `pytest` in the root directory.

## License
MIT