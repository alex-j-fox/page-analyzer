install:
	poetry install
	
PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app 
	
dev:
	poetry run flask --app page_analyzer:app run --debug --port 8080
	
lint:
	poetry run flake8 page_analyzer

selfcheck:
	poetry check

check: selfcheck lint

.PHONY: install start dev lint selfcheck check