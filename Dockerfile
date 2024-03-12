FROM python:3.11

RUN pip install -U \
    pip \
    setuptools \
    wheel

WORKDIR /app

RUN mkdir -p ~/.kaggle

COPY . /app
COPY Source/.kaggle/kaggle.json ~/.kaggle

RUN pip install poetry
RUN poetry install --no-root

CMD ["python", "main.py"]