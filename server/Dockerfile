FROM python:3.12-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apk update && \
  pip install --upgrade pip

WORKDIR /knockbank_api

# Copy the project into the image
COPY pyproject.toml uv.lock /knockbank_api/

# Sync the project
RUN uv sync --no-dev
RUN uv add gunicorn

COPY knockbankapi /knockbank_api/knockbankapi/
COPY migrations /knockbank_api/migrations/

EXPOSE 5000

CMD uv run flask --app knockbankapi db upgrade ; uv run gunicorn -b 0.0.0.0:5000 'knockbankapi:create_app()'