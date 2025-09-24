import logging
import os
from datetime import datetime
def setup_logger():
    logger = logging.getLogger("english_coach")
    logger.setLevel(logging.INFO)
    return logger
