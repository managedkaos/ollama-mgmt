"""
A script to update all models based on a size filter
"""

import os

import ollama
import requests

from logger_config import setup_logger

# Set up logger
logger = setup_logger(__name__)

# Define constants
OLLAMA_API_URL = os.environ.get("OLLAMA_API_URL", "http://localhost:11434/api")
MAX_MODEL_SIZE = int(os.environ.get("MAX_MODEL_SIZE", 10 * (1024**3)))  # Default: 10 GB


def get_models():
    """
    Get all the models currently installed in the Ollama server
    """
    try:
        logger.debug("Fetching models from %s", OLLAMA_API_URL)
        response = requests.get(f"{OLLAMA_API_URL}/tags", timeout=30)
        if response.status_code == 200:
            models_data = response.json()
            logger.debug("Successfully fetched %d models", len(models_data.get("models", [])))
            return models_data.get("models", [])
        logger.error("Failed to fetch models. Status code: %d", response.status_code)
        return []
    except requests.RequestException as e:
        logger.error("Error fetching models: %s", e)
        return []


def select_models_by_size(model_list):
    """
    Select models based on size in bytes
    """
    return [model for model in model_list if model["size"] < MAX_MODEL_SIZE]


def pull_models(model_list):
    """
    Pull models from the Ollama server
    """
    for model_item in model_list:
        model_name = model_item["name"]

        try:
            response = ollama.pull(model_name)
            if response.get("status") == "success":
                print(f"- {model_name} pulled successfully")
            else:
                print(
                    f"- {model_name} pull status: {response.get('status', 'unknown')}"
                )

        except (ollama.ResponseError, requests.RequestException) as e:
            print(f"Error pulling model {model_name}: {e}")


if __name__ == "__main__":
    models = get_models()
    print(f"Found {len(models)} models...")

    selected_models = select_models_by_size(models)
    print(f"Found {len(selected_models)} models smaller than {MAX_MODEL_SIZE} Bytes...")

    pull_models(selected_models)

    skipped_models = [model for model in models if model not in selected_models]

    if skipped_models:
        print("\nModels not updated due to size:")

        for model in skipped_models:
            print(f"- {model['name']} (Size: {model['size'] / (1024 ** 3):.2f} GB)")
