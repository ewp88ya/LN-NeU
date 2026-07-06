#!/bin/bash

# =========================
# AI COMMIT ENGINE RUN MODE
# =========================

REPO=$(git rev-parse --show-toplevel)

cd "$REPO" || exit

while true; do

  git add -A

  CHANGES=$(git diff --cached --name-only)

  if [ -n "$CHANGES" ]; then

    echo "🧠 Detecting changes..."

    TYPE="chore"
    SCOPE="core"
    MSG="update system"

    if echo "$CHANGES" | grep -E "auth|login|user"; then
      TYPE="feat"
      SCOPE="auth"
      MSG="improve authentication system"

    elif echo "$CHANGES" | grep -E "api|route|controller"; then
      TYPE="fix"
      SCOPE="api"
      MSG="fix API logic"

    elif echo "$CHANGES" | grep -E "ui|frontend|vue|react|vite"; then
      TYPE="feat"
      SCOPE="frontend"
      MSG="update UI components"

    elif echo "$CHANGES" | grep -E "db|database|sql|migration"; then
      TYPE="refactor"
      SCOPE="db"
      MSG="improve database structure"
    fi

    COMMIT="$TYPE($SCOPE): $MSG"

    echo "🚀 COMMIT: $COMMIT"

    git commit -m "$COMMIT" || true
    git push origin main

    echo "✅ SYNCED"

  fi

  sleep 2

done
