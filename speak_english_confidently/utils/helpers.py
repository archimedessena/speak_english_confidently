def format_duration(seconds):
    """Format duration in seconds to human readable format"""
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}m {seconds}s"
