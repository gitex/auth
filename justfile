#!/usr/bin/env just --justfile

set shell := ["bash", "-euo", "pipefail", "-c"]

init:
    cp --update=none env.example .env

up profile='dependency':
    sudo docker compose --profile {{ profile }} up -d

down profile='dependency':
    sudo docker compose --profile {{ profile }} down --remove-orphans

ps:
    sudo docker compose ps --all

logs target:
    sudo docker logs -f {{ target }}


