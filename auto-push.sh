#!/bin/bash

while true; do
  inotifywait -r -e modify,create,delete --exclude 'node_modules|dist|.git' .

  git add .

  # cek apakah ada perubahan
  if ! git diff --cached --quiet; then
    git commit -m "auto sync $(date +%H:%M:%S)"
    git pull --rebase origin main
    git push origin main
  fi
done
