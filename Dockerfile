FROM python:3.9

RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc \libsndfile1

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./templates /code/templates

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


