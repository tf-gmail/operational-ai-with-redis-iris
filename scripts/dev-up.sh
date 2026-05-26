#!/usr/bin/env bash
set -euo pipefail

if command -v docker-compose >/dev/null 2>&1; then
  docker-compose up --build "$@"
elif docker compose version >/dev/null 2>&1; then
  docker compose up --build "$@"
else
  echo "Neither docker-compose nor docker compose is available."
  echo "Install Docker Compose plugin or docker-compose binary."
  exit 1
fi
