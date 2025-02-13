# build with
#   docker build -t some_tag_sse_api -f Dockerfile ../..
FROM python:3.9.18-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    # Versions:
    POETRY_VERSION=1.7.1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PATH="$PATH:/root/.local/bin"

# System deps:
RUN apt-get update \
    && apt-get install -y build-essential unzip wget make \
    libicu-dev ffmpeg libavcodec-extra libsndfile1 llvm pkg-config \
    poppler-utils procps htop \
    && rm -rf /var/lib/apt/lists/*
RUN pip install -U pip
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /src
COPY services/sse-api/poetry.lock ./services/sse-api/poetry.lock
COPY services/sse-api/pyproject.toml ./services/sse-api/pyproject.toml
COPY libs/libcommon ./libs/libcommon
COPY libs/libapi ./libs/libapi
WORKDIR /src/services/sse-api/
RUN poetry install --no-cache
COPY services/sse-api/src ./src
RUN poetry install --no-cache

ENTRYPOINT ["poetry", "run", "python", "src/sse_api/main.py"]
