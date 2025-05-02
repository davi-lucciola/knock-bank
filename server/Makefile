run:
	uv run flask --app knockbankapi run --debug

install:
	uv sync

reinstall: 
	make clean
	rm -rf .venv
	make install

test:
	uv run pytest

lint:
	uv run ruff format

clean: 
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	rm -rf .pytest_cache

image-push:
	docker build -t davilucciola/knockbank-api .
	docker push davilucciola/knockbank-api:latest