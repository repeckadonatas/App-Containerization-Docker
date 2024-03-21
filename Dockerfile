FROM python:3.10

RUN pip install -U \
    pip \
    setuptools \
    wheel

ENV POETRY_VERSION=1.8.1
ENV POETRY_HOME=/usr/local
ENV POETRY_VIRTUALENVS_CREATE=false

RUN curl -sSL https://install.python-poetry.org | python3 - --version=$POETRY_VERSION

WORKDIR /app

RUN python -m venv /venv

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root

COPY . .

ENV KAGGLE_USERNAME=${KAGGLE_USERNAME}
ENV KAGGLE_KEY=${KAGGLE_KEY}

RUN pip install --upgrade kaggle

RUN ls -la /app
RUN ls -la /app/Source

RUN chmod +x ./init.sql

RUN echo ~
RUN pwd
RUN whoami

EXPOSE 5432

CMD ["poetry", "run", "python3", "/app/main.py"]