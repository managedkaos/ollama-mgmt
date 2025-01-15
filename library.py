import json
import dateparser
from datetime import datetime
from tabulate import tabulate


# Function to parse the "Updated" string into a datetime object
def parse_updated_time(updated_str):
    if updated_str:
        parsed_date = dateparser.parse(updated_str)
        return parsed_date if parsed_date else datetime.min
    return datetime.min


# Load the repo list from the JSON file
with open("library.json", "r", encoding="utf-8") as f:
    repo_list = json.load(f)

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
    size = repo.get("sizes", ["N/A"])[0] if repo.get("sizes") else "N/A"

    # Check if tools are supported
    has_tools = "Yes" if "tools" in repo.get("capabilities", []) else "No"

    # Get the updated time
    updated = repo.get("updated", "N/A")

    table_data.append([name, size, has_tools, updated])

# Define the table headers
headers = ["Model Name", "Size", "Tools Support", "Last Updated"]

# Print the table
print(tabulate(table_data, headers=headers, tablefmt="pretty"))
