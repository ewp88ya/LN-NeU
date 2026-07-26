#!/usr/bin/env bash

set -e

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="./backups/volumes"

mkdir -p "$BACKUP_DIR"

docker run --rm \
  -v ln-neu_postgres_data:/volume \
  -v "$(pwd)/backups/volumes:/backup" \
  alpine \
  tar czf "/backup/postgres_volume_${TIMESTAMP}.tar.gz" -C /volume .

echo "Volume backup created:"
echo "$BACKUP_DIR/postgres_volume_${TIMESTAMP}.tar.gz"
