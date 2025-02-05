import scrapy
import json

class OllamaModelsSpider(scrapy.Spider):
    name = "ollama_models"
    start_urls = ["https://ollama.com/library"]

    def parse(self, response):
        # Select all model elements from the page
        for model in response.css("a[href^='/library/']"):
            model_name = model.css("span.group-hover\\:underline::text").get()
            if model_name:
                model_name = model_name.strip()

            model_desc = model.css("p::text").get()
            if model_desc:
                model_desc = model_desc.strip()

            model_base_url = response.urljoin(model.attrib["href"])  # Base model URL
            model_slug = model_base_url.split("/")[-1]  # Extract the model name slug

            # Extract available parameter sizes (e.g., ["1.5b", "7b", "8b"])
            parameter_sizes = model.css("span[x-test-size]::text").getall()
            parameter_sizes = [size.strip().lower() for size in parameter_sizes]  # Normalize

            # Generate a new URL for each parameter size and request it
            for param_size in parameter_sizes:
                model_variant_url = f"https://ollama.com/library/{model_slug}:{param_size}"
                yield response.follow(
                    model_variant_url,
                    callback=self.parse_model_page,
                    meta={
                        'model_name': model_name,
                        'model_desc': model_desc,
                        'model_url': model_base_url,
                        'param_size': param_size
                    }
                )

    def parse_model_page(self, response):
        model_name = response.meta["model_name"]
        model_desc = response.meta["model_desc"]
        model_url = response.meta["model_url"]
        param_size = response.meta["param_size"]

        # Extract size in GB for the specific parameter size
        model_size_text = response.css("p::text").re_first(r"([\d.]+)\s*GB")
        model_size = float(model_size_text) if model_size_text else None

        # Extract last updated time
        last_updated = response.css("span[x-test-updated]::text").get()
        if last_updated:
            last_updated = last_updated.strip()

        yield {
            "name": model_name,
            "description": model_desc,
            "url": model_url,
            "parameter_size": param_size,
            "size_gb": model_size,
            "last_updated": last_updated,  # New field added!
        }
