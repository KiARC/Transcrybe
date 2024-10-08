FROM python:3.12-bookworm

ENV TRANSCRYBE_HF_TOKEN=PLEASE_ADD_A_TOKEN \
    TRANSCRYBE_MODEL_SIZE=base.en \
    TRANSCRYBE_LANGUAGE=en

# Install poetry and ffmpeg
RUN apt update && \
    apt install -y ffmpeg && \
    curl -sSL https://install.python-poetry.org | python3 -
ENV PATH=/root/.local/bin:$PATH

WORKDIR /app

# Install dependencies 
RUN touch README.md
COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev

COPY transcrybe/ /app/transcrybe

CMD ["poetry", "run", "poe", "serve"]
