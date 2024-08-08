FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install

COPY . .

CMD ["poetry", "run", "hypercorn", "app.main:app", "--bind", "0.0.0.0:8000"]
