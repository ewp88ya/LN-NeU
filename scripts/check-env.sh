#!/bin/bash

set -e

echo "================================="
echo " LN-NeU Production Environment Check"
echo "================================="

ENV_FILE=".env.production"


if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Missing $ENV_FILE"
    exit 1
fi


echo ""
echo "[1] Checking required variables..."

source $ENV_FILE


REQUIRED_VARS=(
ENVIRONMENT
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
REDIS_URL
GHCR_OWNER
VERSION
)


for VAR in "${REQUIRED_VARS[@]}"
do

    VALUE=${!VAR}

    if [ -z "$VALUE" ]; then
        echo "❌ Missing $VAR"
        exit 1
    fi

    echo "✅ $VAR=$VALUE"

done


echo ""
echo "[2] Checking dangerous placeholders..."

if [[ "$POSTGRES_PASSWORD" == "CHANGE_ME"* ]]; then

    echo "⚠️ WARNING:"
    echo "POSTGRES_PASSWORD still uses placeholder"

    exit 1

fi


echo ""
echo "[3] Checking Docker..."

if ! docker --version >/dev/null 2>&1
then
    echo "❌ Docker unavailable"
    exit 1
fi

echo "✅ Docker OK"


echo ""
echo "[4] Checking Docker Compose..."

if ! docker compose version >/dev/null 2>&1
then
    echo "❌ Docker Compose unavailable"
    exit 1
fi

echo "✅ Compose OK"


echo ""
echo "[5] Checking production compose..."

docker compose \
--env-file .env.production \
-f docker-compose.production.yml \
config >/dev/null


echo "✅ docker-compose.production.yml valid"


echo ""
echo "================================="
echo " Environment validation completed"
echo "================================="
