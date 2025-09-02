import os
import json
import logging

logger = logging.getLogger(__name__)

def ensure_directory(directory):
    try:
        os.makedirs(directory, exist_ok=True)
    except Exception as e:
        logger.error(f"Directory creation error: {e}")

def save_user_progress(data, file_path):
    try:
        ensure_directory(os.path.dirname(file_path))
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        logger.info(f"Progress saved to {file_path}")
    except Exception as e:
        logger.error(f"Save progress error: {e}")