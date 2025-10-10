#!/usr/bin/env just --justfile

set shell := ["bash", "-euo", "pipefail", "-c"]

docker_deps_profile := 'deps'
docker_service_profile := 'service'
docker_network := 'market_net'

[private]
@default:
    just --list

# Первичная подготовка проекта для работы
init:
    cp --update=none .env.template .env
    uv run pre-commit install
    uv run pre-commit install-hooks
    just venv

# Запуск docker compose по profile
up profile=docker_deps_profile:
    sudo docker network inspect {{ docker_network}} >/dev/null 2>&1 \
        || sudo docker network create {{ docker_network }}
    sudo docker compose --profile {{ profile }} up -d

# Остановка docker compose по profile
down profile=docker_deps_profile:
    sudo docker compose --profile {{ profile }} down --remove-orphans

# Alias для docker compose ps
ps:
    sudo docker compose ps --all

# Alias для docker logs
logs target:
    sudo docker logs -f {{ target }}

# Пересобрать сервис
rebuild:
    just down {{ docker_service_profile }}
    sudo docker compose build auth
    just up {{ docker_service_profile }}

# Пересобрать .venv
venv:
    rm -rf .venv
    uv venv
    uv sync
