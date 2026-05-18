"""
config.py

Loads application configuration from the .env file.

Configuration includes:
- web server host and port
- TCP server host and port
- log directory
- log file name
- maximum log file size
- logging interval
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_int(name: str, default: int) -> int:
    """
    Read an integer value from environment variables.
    If the variable does not exist, return the default value.
    """
    value = os.getenv(name)

    if value is None:
        return default
    
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer, but got: {value}") from exc
    

def get_float(name: str, default: float) -> float:
    """
    Read a float value from environment variables.
    If the variable does not exist, return the default value.
    """
    value = os.getenv(name)

    if value is None:
        return default
    
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be a float, but got: {value}") from exc
    

def get_str(name: str, default: str) -> str:
    """
    Read a string value from environment variables.
    If the variable does not exist, return the default value.
    """
    return os.getenv(name, default)


# Web Server configuration
WEB_SERVER_HOST = get_str("WEB_SERVER_HOST", "0.0.0.0")
WEB_SERVER_PORT = get_int("WEB_SERVER_PORT", 8000)

# TCP Server configuration
TCP_SERVER_HOST = get_str("TCP_SERVER_HOST", "0.0.0.0")
TCP_SERVER_PORT = get_int("TCP_SERVER_PORT", 9000)

# Logging configuration
LOG_DIR = Path(get_str("LOG_DIR", "logs"))
LOG_FILE = get_str("LOG_FILE", "log.csv")
LOG_MAX_BYTES = get_int("MAX_LOG_SIZE_MB", 5 * 1024 * 1024) # Convert MB to bytes 
LOG_WRITE_INTERVAL_SECONDS = get_float("LOG_WRITE_INTERVAL_SECONDS", 2.0)

# Full path to the active CSV log file
LOG_FILE_PATH = LOG_DIR / LOG_FILE

def ensure_log_dir_exists() -> None:
    """
    Ensure that the log directory exists. If it does not exist, create it.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)