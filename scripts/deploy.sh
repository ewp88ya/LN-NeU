#!/bin/bash

set -e

echo "=== LN-NeU Production Deploy ==="

echo "Pulling latest GHCR images..."

docker compose \
--env-file .env.production \
-f docker-compose.production.yml \
pull


echo "Starting services..."

docker compose \
--env-file .env.production \
-f docker-compose.production.yml \
up -d


echo "Checking containers..."

docker compose \
--env-file .env.production \
-f docker-compose.production.yml \
ps


echo "Deployment completed."
