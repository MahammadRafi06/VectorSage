import logging
import os
import sys
from datetime import datetime

# Create logs directory if it doesn't exist
logs_dir = "logs"
os.makedirs(logs_dir, exist_ok=True)

# Create a formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create handlers
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# Create a timestamp for the log file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_handler = logging.FileHandler(
    os.path.join(logs_dir, f"rag_sagemaker_{timestamp}.log")
)
file_handler.setFormatter(formatter)

def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Get a logger instance with both console and file handlers.
    
    Args:
        name (str): Name of the logger
        level (int): Logging level (default: logging.INFO)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent duplicate handlers
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger

# Example usage:
# from RAGwithSagemaker.logging.logger import get_logger
# logger = get_logger(__name__)
# logger.info("This is an info message")
# logger.error("This is an error message") 