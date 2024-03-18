FROM python:3.11-bookworm

ENV POETRY_VERSION=1.8.1
#ENV POETRY_HOME=/opt/poetry
#ENV PATH="${PATH}:${POETRY_HOME}/bin/poetry"
#
#ENV VIRTUAL_ENV=/opt/venv
#RUN python3 -m venv $VIRTUAL_ENV
#ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -U \
    pip \
    setuptools \
    wheel

RUN pip install poetry==$POETRY_VERSION

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN ls -la ./
RUN ls -la /

RUN poetry install --no-root

RUN mkdir -p /home/.kaggle
RUN ls -la /home

COPY . ./
COPY ./Source/.kaggle/kaggle.json /home/.kaggle/

RUN ls -la ./Source/.kaggle/
RUN ls -la /home/.kaggle/

RUN ls -la /app
RUN ls -la /app/Source

RUN chmod 600 /home/.kaggle/kaggle.json

RUN pwd
RUN whoami

EXPOSE 5432

CMD ["poetry", "run", "python3", "/app/main.py"]