#!/usr/bin/env bash
set -euo pipefail

# Stop other containers to avoid conflict
docker stop $(docker ps -aq)

# Start dependency containers
just up deps

# Start tmux with .tmuxp.yml configuration
tmuxp load -y .

# Stop all containers
just down deps
just down service
