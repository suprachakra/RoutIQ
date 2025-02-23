"""
Loads configuration settings across environments.

This module provides functions to load configuration from a YAML file,
environment variables, or a combination of both. It ensures that the application
can be configured easily across development, testing, and production environments.

Dependencies:
- pyyaml: To install, run `pip install pyyaml`.
"""

import os
import yaml
import logging

logger = logging.getLogger(__name__)

def load_config(config_path: str = "config.yaml") -> dict:
    """
    Load configuration settings from a YAML file and override with environment variables.
    
    Args:
        config_path (str): Path to the YAML configuration file.
    
    Returns:
        dict: Dictionary containing the merged configuration.
    """
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
    except Exception as e:
        logger.error(f"Error loading configuration file: {e}")
        config = {}
    
    # Override configuration with environment variables if present.
    for key in config.keys():
        env_value = os.getenv(key.upper())
        if env_value is not None:
            config[key] = env_value
            logger.info(f"Overridden {key} with environment variable.")
    return config

# Example usage:
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    config = load_config("config.yaml")
    print("Loaded Configuration:", config)
