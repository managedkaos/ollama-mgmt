MODELS := mistral llama3 moondream tinyllama orca-mini

pull:
	$(foreach model, $(MODELS), ollama pull $(model) && echo "Model $(model) updated successfully"; )

start up:
	docker run --rm \
		--detach \
		--publish 3000:8080 \
		--add-host=host.docker.internal:host-gateway \
		--volume $(PWD)/data:/app/backend/data \
		--name open-webui \
		ghcr.io/open-webui/open-webui:main

stop down:
	docker stop open-webui
