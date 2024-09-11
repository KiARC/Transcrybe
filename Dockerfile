FROM python:3.12-bookworm

ENV TRANSCRYBE_HF_TOKEN=PLEASE_ADD_A_TOKEN

# Install pipx, used to install poetry
RUN sudo apt update && \
    sudo apt install pipx && \
    pipx ensurepath && \
    sudo pipx ensurepath --global

# Install poetry
RUN pipx install poetry

WORKDIR /app

# Install dependencies 
RUN touch README.md
COPY pyproject.toml poetry.lock .
RUN poetry install --without dev

COPY transcrybe .

CMD ["poetry", "run", "poe", "serve"]