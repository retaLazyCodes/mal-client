FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Configure poetry to not create virtualenvs inside docker
RUN poetry config virtualenvs.create false

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies (no interaction, no ansi, no root)
RUN poetry install --no-interaction --no-ansi --no-root

# Copy application code
COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
