"""Simple logging configuration for the application."""
import logging
import os


def setup_logging():
    """Setup simple logging that works in dev and production."""
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    
    # Simple format for both console and file
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create logger
    logger = logging.getLogger('webapp')
    logger.setLevel(getattr(logging, log_level))
    
    # Console handler (always present)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (only if we can write to /var/log, for production)
    if os.path.exists('/var/log') and os.access('/var/log', os.W_OK):
        try:
            file_handler = logging.FileHandler('/var/log/webapp.log')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except (OSError, PermissionError):
            pass  # File logging not available
    
    return logger


def get_logger(name):
    """Get a logger instance."""
    return logging.getLogger(name)