FROM python:3.11

ENV <environmental-variable-1=variable-1>
    <environmental-variable-2=variable-2>

RUN mkdir -p <container-directory>

RUN pip install poetry
RUN poetry install --no-root

COPY <source> <container-directory>
COPY . <container-directory>

CMD ["param1", "param2"]