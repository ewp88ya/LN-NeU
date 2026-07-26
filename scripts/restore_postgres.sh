#!/usr/bin/env bash

set -e

if [ -z "$1" ]; then
    echo "Usage:"
    echo "./scripts/restore_postgres.sh <backup.sql>"
    exit 1
fi

BACKUP_FILE="$1"

cat "$BACKUP_FILE" | docker exec -i \
    -e PGPASSWORD="$POSTGRES_PASSWORD" \
    ln-neu-postgres \
    psql \
    -U "$POSTGRES_USER" \
    -d "$POSTGRES_DB"

echo "Restore completed."
