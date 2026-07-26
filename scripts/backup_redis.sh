#!/usr/bin/env bash

set -e

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="./backups/redis"

mkdir -p "$BACKUP_DIR"

docker exec ln-neu-redis redis-cli BGSAVE

sleep 3

docker cp \
    ln-neu-redis:/data/dump.rdb \
    "$BACKUP_DIR/redis_${TIMESTAMP}.rdb"

echo "Backup created:"
echo "$BACKUP_DIR/redis_${TIMESTAMP}.rdb"
