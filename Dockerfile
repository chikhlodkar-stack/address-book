# Stage 1: Build dependencies
FROM python:3.12-slim-bookworm AS builder

# Set environment variables for Poetry
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PATH="/opt/poetry/bin:$PATH"

# Install Poetry
RUN pip install poetry

# Set working directory
WORKDIR /app

# Copy project definition and lock file
COPY pyproject.toml poetry.lock ./

# Install project dependencies
# --no-root: Don't install the project itself yet
# --only main: Only install main dependencies, not dev dependencies
RUN poetry install --no-root --only main

# Stage 2: Final image for runtime
FROM python:3.12-slim-bookworm AS runtime

# Set environment variables for Poetry (needed for poetry run later, even if poetry isn't fully installed)
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PATH="/opt/poetry/bin:$PATH" \
    PYTHONUNBUFFERED=1 
    # Ensures Python output is sent directly to terminal without buffering

# Set working directory
WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /app/.venv /app/.venv
# Copy application code (excluding .venv from .dockerignore)
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application
# Use Poetry to run Uvicorn, pointing to app.main:app
# --host 0.0.0.0 is crucial to make the app accessible from outside the container
CMD ["/app/.venv/bin/python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]