FROM python:3.10-slim

RUN apt-get update -y && apt-get install -y libpq-dev gcc

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./alembic /code/alembic

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--root-path", "/siapps-news", "--host", "0.0.0.0", "--port", "8000"]
