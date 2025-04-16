"""
This script reads the library.json file and prints the contents in a tabular format.
"""

import json
import re

from tabulate import tabulate

from data_config import LIBRARY_JSON
from logger_config import setup_logger

# Set up logger
logger = setup_logger("library_script")


def convert_to_days(time_str):
    """Convert relative time string to number of days ago."""
    if not time_str or time_str == "-":
        return float("inf")  # Return infinity for missing or invalid dates

    # Extract number and unit
    match = re.match(r"(\d+)\s+(day|week|month|year)s?\s+ago", time_str)
    if not match:
        return float("inf")

    number = int(match.group(1))
    unit = match.group(2)

    # Convert to days
    if unit == "day":
        return_val = number
    elif unit == "week":
        return_val = number * 7
    elif unit == "month":
        return_val = number * 30  # Approximate
    elif unit == "year":
        return_val = number * 365  # Approximate
    else:
        return_val = float("inf")

    return return_val


def load_model_data():
    """Load model data from library.json file."""
    logger.debug("Loading repository data from library.json")
    try:
        with open(LIBRARY_JSON, "r", encoding="utf-8") as f:
            model_list = json.load(f)
        logger.info("Loaded %d models", len(model_list))
        return model_list
    except (IOError, json.JSONDecodeError) as e:
        logger.error("Failed to load library.json: %s", e)
        raise


def process_model_data(model_list):
    """Process model data and return formatted table data."""
    table_data = []
    for model in model_list:
        name = model.get("name", "Unknown")
        last_updated = model.get("last_updated", "-")

        # Hold on to these for later...
        # description = model.get("description", "-")
        # url = model.get("url", "-")

        # Extract parameter sizes
        if "parameter_sizes" in model:
            # Get sizes as comma-separated values
            sizes = ", ".join(model["parameter_sizes"].keys())
        else:
            sizes = "-"

        # Convert last_updated to days
        days_ago = convert_to_days(last_updated)

        # Only include models updated in the last 3 months (90 days)
        if days_ago <= 90:
            table_data.append([name, sizes, last_updated, days_ago])

    return table_data


def print_table(table_data):
    """Print the formatted table data."""
    headers = ["Model Name", "Parameter Sizes", "Last Updated"]

    # Sort the table data by days_ago (ascending) and then by model name
    table_data.sort(key=lambda x: (x[3], x[0]))

    # Remove the days_ago column before printing
    table_data = [row[:3] for row in table_data]

    # Print the table
    print(tabulate(table_data, headers=headers, tablefmt="pretty"))


def main():
    """Main function to orchestrate the script execution."""
    model_list = load_model_data()
    table_data = process_model_data(model_list)
    print_table(table_data)


if __name__ == "__main__":
    main()
