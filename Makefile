OPEN_WEBUI_HOME = $(shell pwd)/open-webui

status:
	@echo "ollama     : $(shell curl -s localhost:11434 || echo "down")"
	@echo "open-webui : $(shell curl -s -o /dev/null localhost:9595/health && echo "Open-WebUI is running" || echo "down")"

list:
	ollama list

requirements:
	pip3 install -r requirements.txt

scrape:
	python3 scrape.py

library: scrape
	python3 library.py

start:
	if [ ! -d $(OPEN_WEBUI_HOME)/data ]; then mkdir $(OPEN_WEBUI_HOME)/data; fi

	docker run --detach \
		--network="host" \
		--volume $(OPEN_WEBUI_HOME)/data:/app/backend/data \
		--env PORT=9595 \
		--env OLLAMA_BASE_URL=http://localhost:11434 \
		--restart always \
		--name open-webui \
		ghcr.io/open-webui/open-webui:main

stop:
	-docker stop open-webui

clean: stop
	-docker rm open-webui

nuke: stop clean
	-rm -rf $(OPEN_WEBUI_HOME)/data

update: $(patsubst %,pull-%, $(shell ollama list | grep -v NAME | cut -d: -f1))
	ollama list
	docker pull ghcr.io/open-webui/open-webui:main

pull-%:
	ollama pull $*
