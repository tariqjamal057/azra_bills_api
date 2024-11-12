FROM python:3.12.7-slim

WORKDIR  /app

COPY . /app

RUN pip install poetry==1.8.3

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev

EXPOSE 8000

CMD if [ "$ENVIRONMENT" = "development" ]; then \
        echo "Running application server in development mode" && \
        poetry run fastapi dev main.py --host 0.0.0.0 --port 8000; \
    else \
        echo "Running application server in production mode" && \
        poetry run fastapi run main.py --host 0.0.0.0 --port 8000; \
    fi
