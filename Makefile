up:
	docker run --detach --publish 3000:8080 \
		--add-host=host.docker.internal:host-gateway \
		-v open-webui:/app/backend/data \
		--restart always \
		--name open-webui \
		ghcr.io/open-webui/open-webui:main
