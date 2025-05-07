FROM python:3.12-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apk update && \
  pip install --upgrade pip

WORKDIR /knockbank_api

COPY pyproject.toml uv.lock /knockbank_api/

RUN uv sync --no-dev

COPY /src /knockbank_api/

EXPOSE 5000

CMD uv run alembic upgrade head ; uv run fastapi run main.py