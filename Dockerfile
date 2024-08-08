FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install

COPY . .

COPY wait_for_db.sh .
RUN chmod +x wait_for_db.sh

CMD ["./wait_for_db.sh", "poetry", "run", "hypercorn", "app.main:app", "--bind", "0.0.0.0:8000"]
