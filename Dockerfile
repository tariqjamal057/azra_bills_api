FROM python:3.12.7-slim

WORKDIR  /app

COPY . /app

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev 

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
