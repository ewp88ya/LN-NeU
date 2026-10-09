#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/bin"
cat > "$TMP/bin/docker" <<'FAKE_DOCKER'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "$DOCKER_LOG"
if [[ "${DOCKER_FAIL_ON_PULL:-0}" == "1" && " $* " == *" pull "* ]]; then
  exit 37
fi
FAKE_DOCKER
chmod +x "$TMP/bin/docker"
export DOCKER_BIN="$TMP/bin/docker"
export DOCKER_LOG="$TMP/docker.log"
export LNNEU_ENV_FILE="$TMP/.env.production"
export LNNEU_COMPOSE_FILE="$TMP/docker-compose.production.yml"
printf 'ENVIRONMENT=production\nVERSION=current\n' > "$LNNEU_ENV_FILE"
printf 'services: {}\n' > "$LNNEU_COMPOSE_FILE"

echo '[rollback-test] successful rollback path'
bash "$ROOT/scripts/rollback.sh" v1.2.3
grep -qx 'VERSION=v1.2.3' "$LNNEU_ENV_FILE"
grep -q 'config --quiet' "$DOCKER_LOG"
grep -q ' pull' "$DOCKER_LOG"
grep -q 'up -d --wait' "$DOCKER_LOG"
grep -q ' ps' "$DOCKER_LOG"

echo '[rollback-test] invalid version is rejected without mutating config'
if bash "$ROOT/scripts/rollback.sh" '../invalid' >/dev/null 2>&1; then
  echo 'Expected invalid version to be rejected.' >&2
  exit 1
fi
grep -qx 'VERSION=v1.2.3' "$LNNEU_ENV_FILE"

echo '[rollback-test] failed pull restores prior env and best-effort service config'
: > "$DOCKER_LOG"
printf 'ENVIRONMENT=production\nVERSION=current\n' > "$LNNEU_ENV_FILE"
if DOCKER_FAIL_ON_PULL=1 bash "$ROOT/scripts/rollback.sh" v9.9.9 >/dev/null 2>&1; then
  echo 'Expected simulated pull failure.' >&2
  exit 1
fi
grep -qx 'VERSION=current' "$LNNEU_ENV_FILE"
grep -q 'up -d' "$DOCKER_LOG"
echo 'PASS: rollback validation, version guard, failure restoration, and safe recovery path'
