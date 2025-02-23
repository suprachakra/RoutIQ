"""
Centralized logging configuration for the fleet optimization platform.

This module sets up a consistent logging configuration for all services.
It includes a function to retrieve the configured logger for use across modules.
"""

import logging
import sys

def setup_logger(name: str = None, level: int = logging.INFO) -> logging.Logger:
    """
    Set up and return a logger with the specified name and log level.
    
    Args:
        name (str, optional): Name of the logger. Defaults to the root logger.
        level (int): Logging level (e.g., logging.INFO, logging.DEBUG).
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create console handler with the specified log level.
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    
    # Create formatter and add it to the handler.
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    
    # Add the handler to the logger if not already added.
    if not logger.handlers:
        logger.addHandler(ch)
    
    return logger

# Example usage:
if __name__ == "__main__":
    logger = setup_logger("core_logger", logging.DEBUG)
    logger.info("Logger setup complete. This is an INFO message.")
    logger.debug("This is a DEBUG message.")
