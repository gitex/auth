ARG PYTHON_VERSION=3.12
ARG USERNAME=app
ARG USER_UID=1000
ARG USER_GID=${USER_UID}

# ----------- Stage 1: Base ------------
FROM python:${PYTHON_VERSION}-slim AS base

ARG USERNAME
ARG USER_UID
ARG USER_GID

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# ----------- Stage 2: Build -------------
FROM base AS builder

ARG USERNAME

# RUN apt-get update && \
#     apt-get install -y make git build-essential sudo curl apt-transport-https && \
#     rm --recursive --force /var/lib/apt/lists/* &&\
#     echo ${USERNAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USERNAME} \
#     && chmod 0440 /etc/sudoers.d/${USERNAME}

WORKDIR /app

COPY pyproject.toml uv.lock ./

# uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# uv output level: info, debug, trace
ARG UV_LOG_LEVEL=info

ENV UV_COMPILE_BYTECODE=1 \
    UV_NO_CACHE=1 \
    RUST_LOG=$UV_LOG_LEVEL

# Required for 'core' installation
ARG INTERNAL_PYPI_INDEX_URL \
    INTERNAL_PYPI_INDEX_USER \
    INTERNAL_PYPI_INDEX_PASSWORD

ENV UV_EXTRA_INDEX_URL="internal=${INTERNAL_PYPI_INDEX_URL}"  \
    UV_INDEX_INTERNAL_USERNAME=${INTERNAL_PYPI_INDEX_USER} \
    UV_INDEX_INTERNAL_PASSWORD=${INTERNAL_PYPI_INDEX_PASSWORD}

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ARG INSTALL_DEV=false
# RUN if [ "$INSTALL_DEV" = "true" ]; then \
#     uv sync --locked --no-install-project; \
#     else \
#     uv sync --locked --no-dev --no-install-project; \
#     fi
#
COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    if [ "$INSTALL_DEV" = "true" ]; then \
    uv sync --frozen; \
    else \
    uv sync --frozen --no-dev; \
    fi

# ------------- Stage 3: Runtime ------------------
FROM python:${PYTHON_VERSION}-slim AS runtime

ARG USER_UID
ARG USER_GID
ARG USERNAME

ENV PATH="/app/.venv/bin:$PATH"

RUN apt-get update && \
    apt-get install -y curl && \
    rm --recursive --force /var/lib/apt/lists/*

WORKDIR /app

COPY --chown=app:app --from=builder /app /app
COPY --from=builder /app/.venv /app/.venv

# Add for security reasons
# Need to replace because of https://pythonspeed.com/articles/root-capabilities-docker-security
# USER $USERNAME


