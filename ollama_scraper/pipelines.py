import json

class MergeModelsPipeline:
    def __init__(self):
        self.models = {}

    def process_item(self, item, spider):
        model_name = item["name"]
        model_desc = item["description"]
        model_url = item["url"]
        param_size = item["parameter_size"]
        size_gb = item["size_gb"]
        last_updated = item["last_updated"]

        # If model is new, initialize it
        if model_name not in self.models:
            self.models[model_name] = {
                "name": model_name,
                "description": model_desc,
                "url": model_url,
                "last_updated": last_updated,  # Store last updated at the model level
                "parameter_sizes": {}
            }

        # Add parameter size mapping
        self.models[model_name]["parameter_sizes"][param_size] = size_gb

        return item  # Scrapy requires returning the item

    def close_spider(self, spider):
        # Save merged output when Scrapy finishes
        with open("./data/merged_models.json", "w") as f:
            json.dump(list(self.models.values()), f, indent=4)

        spider.logger.info("✅ Merged data saved to merged_models.json")
