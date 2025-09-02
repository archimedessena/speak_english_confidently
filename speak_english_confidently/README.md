# Speak English Confidently

A comprehensive conversational English coaching web application that helps users improve their English speaking skills through real-time conversation practice, AI-powered feedback, and personalized vocabulary enhancement.

## Features

- **Real-time Speech Analysis**: Get instant feedback on pronunciation, grammar, and vocabulary
- **AI-Powered Coaching**: Personalized responses and suggestions using OpenAI's GPT models
- **Vocabulary Enhancement**: Discover synonyms, antonyms, and better word choices
- **Progress Tracking**: Monitor your improvement with detailed analytics
- **Interactive Practice Sessions**: Engage in natural conversations with the AI coach
- **Audio Recording & Playback**: Practice speaking and receive immediate feedback

## Technology Stack

- **Backend**: Python Flask with SocketIO for real-time communication
- **Frontend**: HTML5, CSS3, JavaScript with modern UI/UX design
- **Audio Processing**: Speech recognition, text-to-speech, and audio analysis
- **NLP**: Grammar checking, vocabulary enhancement, and AI response generation
- **Real-time Communication**: WebSocket connections for live interaction

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd speak_english_confidently
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file with your API keys
```

5. Run the application:
```bash
python app.py
```

## Environment Variables

Create a `.env` file with the following variables:

```env
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key
PORT=5000
FLASK_ENV=development
```

## Usage

1. **Home Page**: Overview of features and navigation to different sections
2. **Practice Session**: Start a new conversation practice session
3. **Progress Tracking**: View your learning progress and analytics
4. **Audio Recording**: Record your voice and get instant feedback
5. **AI Coaching**: Receive personalized suggestions and corrections

## Project Structure

```
speak_english_confidently/
├── app.py                          # Main application entry point
├── requirements.txt                # Project dependencies
├── README.md                       # Project documentation
├── audio/                          # Audio processing modules
├── nlp/                            # Natural Language Processing
├── conversation/                   # Conversation management
├── data/                           # Data storage
├── utils/                          # General utilities
├── templates/                      # HTML templates
├── static/                         # CSS, JS, and static assets
└── tests/                          # Test suite
```

## API Endpoints

- `GET /` - Home page
- `GET /practice` - Practice session page
- `GET /progress` - Progress tracking page
- `POST /api/start_session` - Start a new practice session
- `POST /api/process_audio` - Process uploaded audio
- `GET /api/get_feedback` - Get personalized feedback
- `GET /api/get_progress` - Get user progress statistics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in the repository or contact the development team.
