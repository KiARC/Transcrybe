FROM python:3.12-bookworm

ENV TRANSCRYBE_HF_TOKEN=PLEASE_ADD_A_TOKEN

# Install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

# Install dependencies 
RUN touch README.md
COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev

COPY transcrybe ./

CMD ["poetry", "run", "poe", "serve"]
