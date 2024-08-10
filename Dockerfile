FROM python:3.10-slim

# Install necessary system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Create a non-root user to run the application
RUN useradd -ms /bin/bash appuser

# Set the working directory
WORKDIR /app

# Copy and install Python dependencies using Poetry
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

# Copy the application code
COPY . .

# Create the logs directory and set permissions
RUN mkdir -p /app/app/logs
RUN chown -R appuser:appuser /app
RUN chmod -R 777 /app/app/logs

# Switch to the non-root user
USER appuser

# Start the application using Hypercorn (if you're using Uvicorn, you can change the CMD accordingly)
CMD ["poetry", "run", "hypercorn", "app.main:app", "--bind", "0.0.0.0:8000"]
