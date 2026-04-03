# ====> BASE <=== #
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \

# ====> DEPENDENCIES <=== #
FROM base AS deps
RUN pip install poetry
RUN poetry config virtualenvs.in-project true
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-dev --no-interaction --no-ansi


# ====> DEVELOPMENT <=== #
FROM base AS dev
RUN pip install poetry
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-interaction --no-ansi
COPY . .
CMD ["/app/.venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]

# ====> TEST <==== #
FROM base AS test
RUN pip install poetry
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.in-project true
RUN poetry install --with test --no-interaction --no-ansi
COPY . .
CMD ["/app/.venv/bin/pytest"]

# ====> PRODUCTION <=== #
FROM base AS production
COPY --from=deps /app /app
COPY . .
RUN useradd -m appuser
USER appuser
EXPOSE 8000
CMD ["/app/.venv/bin/gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
