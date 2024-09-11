FROM python:3.12-bookworm

ENV TRANSCRYBE_HF_TOKEN=PLEASE_ADD_A_TOKEN

# Install pipx, used to install poetry
RUN apt-get update && \
    apt-get install -y pipx && \
    pipx ensurepath

# Install poetry
RUN pipx install poetry

WORKDIR /app

# Install dependencies 
RUN touch README.md
COPY pyproject.toml poetry.lock .
RUN poetry install --without dev

COPY transcrybe .

CMD ["poetry", "run", "poe", "serve"]
