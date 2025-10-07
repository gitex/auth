#!/usr/bin/env just --justfile

set shell := ["bash", "-euo", "pipefail", "-c"]

docker_deps_profile := 'deps'
docker_service_profile := 'service'
docker_network := 'market_net'

init:
    cp --update=none env.example .env
    uv run pre-commit install
    uv run pre-commit install-hooks

up profile=docker_deps_profile:
    sudo docker network inspect {{ docker_network}} >/dev/null 2>&1 \
        || sudo docker network create {{ docker_network }}
    sudo docker compose --profile {{ profile }} up -d

down profile=docker_deps_profile:
    sudo docker compose --profile {{ profile }} down --remove-orphans

ps:
    sudo docker compose ps --all

logs target:
    sudo docker logs -f {{ target }}

rebuild:
    @just down {{ docker_service_profile }}
    sudo docker compose build auth
    @just up {{ docker_service_profile }}
