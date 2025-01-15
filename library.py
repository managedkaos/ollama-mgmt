"""
This script reads the library.json file and prints the contents in a tabular format.
"""

import json
from datetime import datetime

import dateparser
from tabulate import tabulate

from data_config import LIBRARY_JSON
from logger_config import setup_logger

# Set up logger
logger = setup_logger(__name__)


# Function to parse the "Updated" string into a datetime object
def parse_updated_time(updated_str):
    """
    Parse the "Updated" string into a datetime object.
    """
    if updated_str:
        parsed_date = dateparser.parse(updated_str)
        logger.debug("Parsed date '%s' to %s", updated_str, parsed_date)
        return parsed_date if parsed_date else datetime.min
    return datetime.min


logger.debug("Loading repository data from library.json")
# Load the repo list from the JSON file
try:
    with open(LIBRARY_JSON, "r", encoding="utf-8") as f:
        repo_list = json.load(f)
    logger.info("Loaded %d repositories", len(repo_list))
except (IOError, json.JSONDecodeError) as e:
    logger.error("Failed to load library.json: %s", e)
    raise

# Convert the "Updated" field to datetime and sort the list
for repo in repo_list:
    repo["parsed_updated"] = parse_updated_time(repo["updated"])

sorted_repo_list = sorted(repo_list, key=lambda x: x["parsed_updated"], reverse=True)

# Remove the 'parsed_updated' key after sorting if it's no longer needed
for repo in sorted_repo_list:
    del repo["parsed_updated"]

# Prepare the data for the table
table_data = []
for repo in sorted_repo_list:
    name = repo["name"]

    # Extract the size value
    size = ", ".join(repo.get("sizes", [])) if repo.get("sizes") else None

    # Get the tools supported
    capabilities = (
        ", ".join(repo.get("capabilities", [])) if repo.get("capabilities") else None
    )

    # Get the updated time
    updated = repo.get("updated", "N/A")

    table_data.append([name, size, capabilities, updated])

# Define the table headers
headers = ["Model Name", "Size", "Capabilities", "Last Updated"]

# Print the table
print(tabulate(table_data, headers=headers, tablefmt="pretty"))
