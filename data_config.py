"""
Configuration module for data-related settings and paths.
"""
import os
from pathlib import Path

# Base directory is the parent directory of this file
BASE_DIR = Path(__file__).parent

# Data directory configuration
DATA_DIR = BASE_DIR / "data"
LIBRARY_JSON = DATA_DIR / "library.json"

# Model library URL configuration
MODEL_LIBRARY_URL = os.environ.get("MODEL_LIBRARY_URL", "https://ollama.com/library")

def setup_data_dirs():
    """
    Create necessary data directories if they don't exist.
    Returns the data directory path.
    """
    DATA_DIR.mkdir(exist_ok=True)
    return DATA_DIR
