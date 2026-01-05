FROM python:3.11.10-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2 \
    POETRY_HOME=/opt/poetry \
    PATH="/opt/poetry/bin:$PATH"

WORKDIR /app

# ---- System deps (before poetry install) ----
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    unzip \
    netcat-traditional \
    gettext \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# ---- Install Poetry (OFFICIAL way) ----
RUN curl -sSL https://install.python-poetry.org | python3 -

# ---- Verify poetry ----
RUN poetry --version


# ---- Dependencies ----
COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# ---- App ----
COPY . .

# Create necessary directories and set permissions BEFORE switching user
RUN mkdir -p /app/logs /app/static /app/media \
    && adduser --disabled-password --gecos '' app \
    && chown app:app -R /app \
    && chmod +x /app/deployment/entrypoint.sh

USER app

EXPOSE 8000

ENTRYPOINT ["sh", "/app/deployment/entrypoint.sh"]

CMD ["gunicorn", "counsel_hub.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]