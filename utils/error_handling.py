"""
Enhanced error handling utilities for robust operations
"""

import time
from typing import Callable, Any, TypeVar
from functools import wraps
import logging

T = TypeVar('T')
logger = logging.getLogger(__name__)

def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """Retry decorator with exponential backoff"""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            delay = initial_delay
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        logger.error(f"Failed after {max_retries} attempts: {e}")
                        raise
                    
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.1f}s...")
                    time.sleep(delay)
                    delay *= backoff_factor
            return func(*args, **kwargs)  # Should never reach here
        return wrapper
    return decorator

def fallback_on_error(fallback_func: Callable[..., T], exceptions: tuple = (Exception,)):
    """Fallback to another function on error"""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                logger.warning(f"Primary function failed, using fallback: {e}")
                return fallback_func(*args, **kwargs)
        return wrapper
    return decorator