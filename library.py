"""
This script reads the library.json file and prints the contents in a tabular format.
"""

import json
from tabulate import tabulate
from data_config import LIBRARY_JSON
from logger_config import setup_logger

# Set up logger
logger = setup_logger("library_script")

logger.debug("Loading repository data from library.json")

# Load the model list from the JSON file
try:
    with open(LIBRARY_JSON, "r", encoding="utf-8") as f:
        model_list = json.load(f)
    logger.info("Loaded %d models", len(model_list))
except (IOError, json.JSONDecodeError) as e:
    logger.error("Failed to load library.json: %s", e)
    raise

# Prepare the data for the table
table_data = []
for model in model_list:
    name = model.get("name", "Unknown")
    description = model.get("description", "No description available.")
    url = model.get("url", "N/A")

    # Extract parameter sizes
    if "parameter_sizes" in model:
        # Get sizes as comma-separated values
        sizes = ", ".join(model["parameter_sizes"].keys())
    else:
        sizes = "N/A"

    table_data.append([name, sizes, description, url])

# Define the table headers
headers = ["Model Name", "Sizes", "Description", "URL"]

# Print the table
print(tabulate(table_data, headers=headers, tablefmt="pretty"))
