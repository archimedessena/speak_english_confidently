import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PORT = int(os.getenv("PORT", 5000))
