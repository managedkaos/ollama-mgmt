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
                model_name = model_name.strip()  # Ensure whitespace is removed
            
            model_desc = model.css("p::text").get()
            if model_desc:
                model_desc = model_desc.strip()  # Ensure whitespace is removed
            
            model_url = response.urljoin(model.attrib["href"])  # Absolute URL

            # Follow the link to the model's detail page
            yield response.follow(
                model_url,
                callback=self.parse_model_page,
                meta={'model_name': model_name, 'model_desc': model_desc, 'model_url': model_url}
            )

    def parse_model_page(self, response):
        model_name = response.meta["model_name"]
        model_desc = response.meta["model_desc"]
        model_url = response.meta["model_url"]

        # Extract model size (with better regex handling for floating-point numbers)
        model_size_text = response.css("p::text").re_first(r"([\d.]+)\s*GB")
        model_size = float(model_size_text) if model_size_text else None

        yield {
            "name": model_name,
            "description": model_desc,
            "url": model_url,
            "size_gb": model_size,
        }
