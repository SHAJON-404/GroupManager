import os
import json
import logging

logger = logging.getLogger(__name__)

def load_json(filepath: str, default_val) -> dict:
    """Loads a JSON file safely. Returns the default value if the file doesn't exist or is corrupted."""
    if not os.path.exists(filepath):
        return default_val
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error reading JSON from {filepath}: {e}")
        return default_val

def save_json(filepath: str, data: dict):
    """Saves data to a JSON file safely."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error saving JSON to {filepath}: {e}")
