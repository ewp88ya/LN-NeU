#!/usr/bin/env bash

set -e

set -a
source .env.production
set +a

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="./backups/postgres"

mkdir -p "$BACKUP_DIR"

docker exec ln-neu-postgres \
    pg_dump \
    -U "$POSTGRES_USER" \
    "$POSTGRES_DB" \
    > "$BACKUP_DIR/postgres_${TIMESTAMP}.sql"

echo "Backup created:"
echo "$BACKUP_DIR/postgres_${TIMESTAMP}.sql"
