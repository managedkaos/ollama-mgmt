"""
This script scrapes the Ollama model library page and extracts
the model names, capabilities, sizes, updated dates, and pull counts.
"""

import json

import requests
from bs4 import BeautifulSoup

from data_config import LIBRARY_JSON, MODEL_LIBRARY_URL, setup_data_dirs
from logger_config import setup_logger

# Set up logger
logger = setup_logger(__name__)

# URL of the webpage you want to scrape
url = MODEL_LIBRARY_URL
logger.info("Starting web scraping for URL: %s", url)

try:
    # Send a GET request to fetch the raw HTML content
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    logger.debug(
        "Successfully retrieved page with status code: %s", response.status_code
    )
except requests.exceptions.RequestException as e:
    logger.error("Failed to fetch URL: %s", e)
    raise

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")
logger.debug("HTML content parsed successfully")

# Initialize an empty list to store the dictionaries for each model
repo_list = []

# Select all model entries (they're wrapped in <a> tags)
model_entries = soup.find_all("a", class_="group w-full space-y-5")
if model_entries:
    logger.info("Found %d model entries.", len(model_entries))
else:
    logger.warning("No model entries found - check if page structure has changed")


for index, entry in enumerate(model_entries, 1):
    logger.debug("Processing model entry %d/%d", index, len(model_entries))

    # Extract the name (now using the correct selector)
    name = entry.select_one(".group-hover\\:underline").text.strip()
    if name:
        logger.debug("Extracted name: %s", name)
    else:
        logger.warning("Name not found for entry %d", index)

    # Extract capabilities (tools) and sizes
    capabilities = []
    sizes = []

    # Get capabilities (tools)
    capability_elements = entry.find_all("span", {"x-test-capability": True})
    capabilities = (
        [capability.text.strip() for capability in capability_elements]
        if capability_elements
        else []
    )
    logger.debug("Extracted capabilities: %s", capabilities)

    # Get sizes
    size_elements = entry.find_all("span", {"x-test-size": True})
    sizes = [size.text.strip() for size in size_elements] if size_elements else []
    logger.debug("Extracted sizes: %s", sizes)

    # Extract the updated date
    updated_elem = entry.find("span", {"x-test-updated": True})
    updated = updated_elem.text.strip() if updated_elem else ""
    logger.debug("Extracted update date: %s", updated)

    # Extract pull count
    pull_count_element = entry.find("span", {"x-test-pull-count": True})
    pull_count = pull_count_element.text.strip() if pull_count_element else ""
    logger.debug("Extracted pull count: %s", pull_count)

    # Extract description
    description_element = entry.find(
        "p", {"class": "max-w-lg break-words text-neutral-800 text-md"}
    )
    description = description_element.text.strip() if description_element else ""
    logger.debug("Extracted description: %s", description)

    # Create entry dictionary
    if name:
        entry_data = {
            "name": name,
            "capabilities": capabilities,
            "sizes": sizes,
            "updated": updated,
            "pull_count": pull_count,
            "description": description,
        }
        repo_list.append(entry_data)
        logger.debug("Added entry to repo_list: %s", entry_data)

logger.info("Processed %d models.", len(repo_list))

try:
    setup_data_dirs()
    with open(LIBRARY_JSON, "w", encoding="utf-8") as f:
        json.dump(repo_list, f, ensure_ascii=False, indent=4)
    logger.info("Wrote data to %s", LIBRARY_JSON)
except IOError as e:
    logger.error("Failed to write JSON file: %s", e)
    raise

logger.info("Scraping process complete.")
