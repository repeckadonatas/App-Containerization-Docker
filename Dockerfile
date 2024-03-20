FROM python:3.11-bookworm

ENV POETRY_VERSION=1.8.1
ENV POETRY_HOME=/opt/poetry
ENV PATH="${PATH}:${POETRY_HOME}/bin/poetry"

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -U \
    pip \
    setuptools \
    wheel

RUN pip install poetry==$POETRY_VERSION

ENV HOME=/root

RUN mkdir -p $HOME/.kaggle
COPY Source/.kaggle/kaggle.json $HOME/.kaggle

RUN ls -la $HOME
RUN ls -la $HOME/.kaggle/

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root

COPY . ./

RUN ls -la /app
RUN ls -la /app/Source
RUN ls -la /app/Source/.kaggle/

RUN chmod +x ./init.sql
RUN chmod +x init.sql

RUN echo ~
RUN pwd
RUN whoami

EXPOSE 5432

CMD ["poetry", "run", "python3", "/app/main.py"]