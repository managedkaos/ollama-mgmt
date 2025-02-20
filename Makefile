OPEN_WEBUI_HOME = $(shell pwd)/open-webui

status:
	@echo "ollama     : $(shell curl -s localhost:11434 || echo "down")"
	@echo "open-webui : $(shell curl -s -o /dev/null localhost:9595/health && echo "Open-WebUI is running" || echo "down")"

lint:
	flake8 *.py
	pylint *.py
ifeq ($(CI),true)
	isort --check-only *.py
	black --check *.py
else
	actionlint .github/workflows/*.yml
	isort --diff *.py
	black --diff *.py
endif

black:
	black *.py

isort:
	isort *.py

list:
	ollama list

dev-requirements:
	pip3 install --requirement dev-requirements.txt

requirements:
	pip3 install --requirement requirements.txt

curl:
	curl https://ollama.com/library > data/ollama-library.html

scrape:
	python3 scrape.py

library:
	python3 library.py

update: status
	@python3 update.py

start:
	@if [ ! -d $(OPEN_WEBUI_HOME)/data ]; then mkdir -p $(OPEN_WEBUI_HOME)/data; fi
	@docker pull ghcr.io/open-webui/open-webui:main
	-@docker run --detach \
		--network="host" \
		--volume $(OPEN_WEBUI_HOME)/data:/app/backend/data \
		--env PORT=9595 \
		--env OLLAMA_BASE_URL=http://localhost:11434 \
		--restart always \
		--name open-webui \
		ghcr.io/open-webui/open-webui:main || \
	printf "\nIs the container already running?\n\n"
	@printf "http://localhost:9595\n\n"

url:
	@printf "\n\nhttp://localhost:9595\n\n"

stop:
	-docker stop open-webui

clean: stop
	-docker rm open-webui

nuke: stop clean
	@echo "#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#"
	@echo "# WARNING: This will remove all data stored by Open-WebUI."
	@echo "# WARNING: This action is irreversible."
	@echo "#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#"
	@echo
	@echo "Type CTRL+C to abort."
	@echo
	@read -p "Type the current date in YYYY-MM-DD format to confirm: " input_date; \
	if [ "$$input_date" = "$(shell date +%Y-%m-%d)" ]; then \
		echo "Date confirmed. Proceeding with removal..."; \
		rm -rf $(OPEN_WEBUI_HOME)/data || true; \
	else \
		echo "Date confirmation failed. Aborting..."; \
	fi

x_update: $(patsubst %,pull-%, $(shell ollama list | grep -v NAME | cut -d: -f1))
	ollama list
	docker pull ghcr.io/open-webui/open-webui:main

pull-%:
	ollama pull $*

.PHONY: status list requirements scrape library update_models start url stop clean nuke x_update isort
