import json

# Read JSON Lines (Scrapy's default format)
with open("./data/models.jl", "r") as f:
    data = [json.loads(line) for line in f]

# Dictionary to store merged data
merged_models = {}

for entry in data:
    model_name = entry["name"]
    model_desc = entry["description"]
    model_url = entry["url"]
    param_size = entry["parameter_size"]
    size_gb = entry["size_gb"]

    # If model is seen for the first time, initialize its entry
    if model_name not in merged_models:
        merged_models[model_name] = {
            "name": model_name,
            "description": model_desc,
            "url": model_url,
            "parameter_sizes": {}
        }

    # Add the parameter size mapping
    merged_models[model_name]["parameter_sizes"][param_size] = size_gb

# Convert merged data to a list for saving
merged_data = list(merged_models.values())

# Save cleaned JSON
with open("./data/merged_models.json", "w") as f:
    json.dump(merged_data, f, indent=4)

print("✅ Merged data saved to merged_models.json")
