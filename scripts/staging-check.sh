#!/bin/bash

set -e

echo "LN-NeU Staging Validation"

echo "Checking docker compose..."

docker compose \
--env-file .env.staging \
-f docker-compose.production.yml \
config > /dev/null

echo "Compose validation OK"

echo "Checking environment..."

grep ENVIRONMENT .env.staging

echo "Environment OK"

echo "Staging preparation complete"
