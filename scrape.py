import logging
from bs4 import BeautifulSoup
import requests
import json
import os

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/scraper.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# URL of the webpage you want to scrape
url = "https://ollama.com/library"
logger.info(f"Starting web scraping for URL: {url}")

try:
    # Send a GET request to fetch the raw HTML content
    response = requests.get(url)
    response.raise_for_status()
    logger.debug(
        f"Successfully retrieved page with status code: {response.status_code}"
    )
except requests.exceptions.RequestException as e:
    logger.error(f"Failed to fetch URL: {e}")
    raise

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")
logger.debug("HTML content parsed successfully")

# Initialize an empty list to store the dictionaries for each model
repo_list = []

# Select all model entries (they're wrapped in <a> tags)
model_entries = soup.find_all("a", class_="group w-full space-y-5")
if model_entries:
    logger.info(f"Found {len(model_entries)} model entries")
else:
    logger.warning("No model entries found - check if page structure has changed")


# Function to clean up text
def clean_text(text):
    original = text
    cleaned = " ".join(text.split()).replace("\xa0", " ")
    return cleaned


for index, entry in enumerate(model_entries, 1):
    logger.debug(f"Processing model entry {index}/{len(model_entries)}")

    # Extract the name (now using the correct selector)
    name_elem = entry.select_one("h2 span")
    name = clean_text(name_elem.text) if name_elem else None
    if name:
        logger.debug(f"Extracted name: {name}")
    else:
        logger.warning(f"Name not found for entry {index}")

    # Extract capabilities (tools) and sizes
    capabilities = []
    sizes = []

    # Get capabilities (tools)
    capability_elems = entry.find_all("span", attrs={"x-test-capability": ""})
    capabilities = [clean_text(elem.text) for elem in capability_elems]
    logger.debug(f"Extracted capabilities: {capabilities}")

    # Get sizes
    size_elems = entry.find_all("span", attrs={"x-test-size": ""})
    sizes = [clean_text(elem.text) for elem in size_elems]
    logger.debug(f"Extracted sizes: {sizes}")

    # Extract the updated date
    updated_elem = entry.find("span", attrs={"x-test-updated": ""})
    updated = clean_text(updated_elem.text) if updated_elem else None
    if updated:
        logger.debug(f"Extracted update date: {updated}")
    else:
        logger.warning(f"Update date not found for entry {index}")

    # Extract pull count and tag count
    pull_count_elem = entry.find("span", attrs={"x-test-pull-count": ""})
    pull_count = clean_text(pull_count_elem.text) if pull_count_elem else None

    tag_count_elem = entry.find("span", attrs={"x-test-tag-count": ""})
    tag_count = clean_text(tag_count_elem.text) if tag_count_elem else None

    # Create entry dictionary
    if name:
        entry_data = {
            "name": name,
            "capabilities": capabilities,
            "sizes": sizes,
            "updated": updated,
            "pull_count": pull_count,
            "tag_count": tag_count,
        }
        repo_list.append(entry_data)
        logger.debug(f"Added entry to repo_list: {entry_data}")

logger.info(f"Processed {len(repo_list)} models successfully")

try:
    # Write the repo_list to a JSON file
    os.makedirs("data", exist_ok=True)
    with open("data/library.json", "w", encoding="utf-8") as f:
        json.dump(repo_list, f, ensure_ascii=False, indent=4)
    logger.info("Successfully wrote data to library.json")
except OSError as e:
    logger.error(f"Failed to create directory: {e}")
    raise
except IOError as e:
    logger.error(f"Failed to write JSON file: {e}")
    raise

logger.info("Scraping process completed!")
print("# Scrape complete!")
