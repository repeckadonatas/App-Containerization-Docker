FROM python:3.10

ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD

ENV PGUSER=$POSTGRES_USER
ENV PGPASSWORD=$POSTGRES_PASSWORD
ENV PGHOST=$PGHOST
ENV PGPORT=$PGPORT
ENV PGDATABASE=$PGDATABASE

ENV KAGGLE_USERNAME=$KAGGLE_USERNAME
ENV KAGGLE_KEY=$KAGGLE_KEY

ENV POETRY_VERSION=1.8.1
ENV POETRY_HOME=/usr/local
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update
RUN pip install -U pip \
    setuptools \
    wheel

RUN mkdir -p /root/.kaggle
COPY Source/.kaggle/kaggle.json /root/.kaggle
COPY init.sql /docker-entrypoint-initdb.d/

RUN chmod +x /docker-entrypoint-initdb.d/init.sql
RUN chmod 600 /root/.kaggle/kaggle.json

RUN curl -sSL https://install.python-poetry.org | python3 - --version=$POETRY_VERSION

WORKDIR /app

RUN python3 -m venv /venv

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root

COPY . .

EXPOSE 5432

CMD ["poetry", "run", "python3", "/app/main.py"]