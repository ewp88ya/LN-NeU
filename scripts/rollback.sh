#!/usr/bin/env bash
set -Eeuo pipefail

VERSION="${1:-}"
if [[ -z "$VERSION" ]]; then
  echo "Usage: ./scripts/rollback.sh <known-good-version>" >&2
  exit 2
fi
if [[ ! "$VERSION" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]]; then
  echo "Invalid version: use letters, digits, dot, underscore, or hyphen only." >&2
  exit 2
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${LNNEU_ENV_FILE:-$ROOT/.env.production}"
COMPOSE_FILE="${LNNEU_COMPOSE_FILE:-$ROOT/docker-compose.production.yml}"
DOCKER_BIN="${DOCKER_BIN:-docker}"

[[ -f "$ENV_FILE" ]] || { echo "Missing environment file: $ENV_FILE" >&2; exit 2; }
[[ -f "$COMPOSE_FILE" ]] || { echo "Missing Compose file: $COMPOSE_FILE" >&2; exit 2; }
version_count="$(grep -c '^VERSION=' "$ENV_FILE" || true)"
[[ "$version_count" == "1" ]] || {
  echo "Expected exactly one VERSION= entry in $ENV_FILE; no changes made." >&2
  exit 2
}

original_mode="$(stat -c '%a' "$ENV_FILE")"
backup="$(mktemp "${ENV_FILE}.rollback.XXXXXX")"
candidate="$(mktemp "${ENV_FILE}.candidate.XXXXXX")"
cp "$ENV_FILE" "$backup"
chmod 600 "$backup"
success=false

cleanup() {
  local status=$?
  trap - EXIT
  if [[ "$success" != true ]]; then
    if [[ -f "$backup" ]]; then
      cp "$backup" "$ENV_FILE"
      chmod "$original_mode" "$ENV_FILE"
      # Best-effort restoration of the pre-rollback version after a failed candidate.
      "$DOCKER_BIN" compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" up -d >/dev/null 2>&1 || true
    fi
  fi
  rm -f "$backup" "$candidate"
  exit "$status"
}
trap cleanup EXIT

awk -v version="$VERSION" '
  /^VERSION=/ { print "VERSION=" version; count++; next }
  { print }
  END { if (count != 1) exit 2 }
' "$ENV_FILE" > "$candidate"
chmod "$original_mode" "$candidate"
mv "$candidate" "$ENV_FILE"

echo "Validating rollback configuration for version $VERSION"
"$DOCKER_BIN" compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" config --quiet
echo "Pulling known-good release image(s)"
"$DOCKER_BIN" compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" pull
echo "Starting rollback release and waiting for service readiness"
"$DOCKER_BIN" compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" up -d --wait
"$DOCKER_BIN" compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" ps

success=true
echo "Rollback completed and Compose readiness checks passed: $VERSION"
