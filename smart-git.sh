#!/bin/bash

echo "🔍 Smart Git Scanner..."

FILES=$(git status --porcelain | cut -c4-)

ALLOW_PATTERN="^(src|api|backend|lib)/"

for file in $FILES; do

  # skip empty
  [ -z "$file" ] && continue

  if [[ $file =~ $ALLOW_PATTERN ]]; then
    echo "✅ ALLOWED: $file"
    git add "$file"
  else
    echo "⛔ SKIP: $file"
  fi

done

# cek apakah ada staged changes
if git diff --cached --quiet; then
  echo "ℹ️ No valid changes to commit"
  exit 0
fi

git commit -m "auto: smart sync"
git push
