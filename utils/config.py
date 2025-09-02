import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.AUDIO_TIMEOUT = 10  # seconds
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set in .env")