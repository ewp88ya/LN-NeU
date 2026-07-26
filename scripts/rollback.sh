#!/bin/bash

set -e

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Usage: ./rollback.sh v1.0.0"
    exit 1
fi


echo "=== LN-NeU Rollback ==="

sed -i "s/^VERSION=.*/VERSION=$VERSION/" .env.production


docker compose \
--env-file .env.production \
-f docker-compose.production.yml \
pull


docker compose \
--env-file .env.production \
-f docker-compose.production.yml \
up -d


echo "Rollback completed: $VERSION"

