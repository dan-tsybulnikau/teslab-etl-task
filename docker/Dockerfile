FROM python:slim as base

RUN mkdir -p /app

# create the app user
RUN addgroup --system app && adduser --system --group app

ENV APP_HOME=/home/src
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT prod

RUN apt-get update \
    && apt-get -y install curl netcat gcc libpq-dev \
    && apt-get clean

RUN pip install --upgrade pip
RUN pip install -U setuptools
COPY ./docker/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN chown -R app:app $APP_HOME
USER app

EXPOSE 8080
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--port", "8080"]