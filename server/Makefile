run:
	cd src && uv run fastapi dev main.py

install:
	uv sync

reinstall: 
	make clean
	rm -rf .venv
	make install

test:
	uv run pytest --cov=./src/app ./src/tests

test-func:
	uv run pytest -vm $(mark)

lint:
	uv run ruff format

clean: 
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf .ruff_cache

revision:
	cd src && uv run alembic revision --autogenerate -m $(name)

migrate:
	cd src && uv run alembic upgrade head

image-push:
	docker build -t davilucciola/knockbank-api .
	docker push davilucciola/knockbank-api:latest