"""
A script to update all models based on a size filter
"""

import ollama
import requests
import os


# Define constants
OLLAMA_API_URL = os.environ.get("OLLAMA_API_URL", "http://localhost:11434/api")
MAX_MODEL_SIZE = int(os.environ.get("MAX_MODEL_SIZE", 10 * (1024**3)))  # Default: 10 GB


def get_models():
    """
    Get all the models currently installed in the Ollama server
    """
    try:
        response = requests.get(f"{OLLAMA_API_URL}/tags")
        if response.status_code == 200:
            models_data = response.json()
            return models_data.get("models", [])
        else:
            print(f"Error: Received status code {response.status_code}")
            return []
    except requests.RequestException as e:
        print(f"Error fetching models: {e}")
        return []


def select_models_by_size(models):
    """
    Select models based on size in bytes
    """
    return [model for model in models if model["size"] < MAX_MODEL_SIZE]


def pull_models(models):
    """
    Pull models from the Ollama server
    """
    for model in models:
        model_name = model["name"]

        try:
            response = ollama.pull(model_name)
            if response.get("status") == "success":
                print(f"- {model_name} pulled successfully")
            else:
                print(
                    f"- {model_name} pull status: {response.get('status', 'unknown')}"
                )

        except Exception as e:
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
