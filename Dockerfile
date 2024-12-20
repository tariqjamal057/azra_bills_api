FROM python:3.12.7-slim

WORKDIR  /app

COPY . /app

RUN pip install poetry==1.8.3

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev

RUN chmod +x app.sh

EXPOSE 8000

CMD ["./app.sh"]
