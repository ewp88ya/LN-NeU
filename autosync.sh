#!/bin/bash

echo "🚀 Smart Auto Sync Activated"

while true
do
  inotifywait -r -e modify,create,delete --exclude '(.git|node_modules)' .

  echo "📦 Changes detected..."

  git add .

  git commit -m "auto sync $(date +'%H:%M:%S')" || echo "No changes to commit"

  git push origin main

  echo "✅ Synced to GitHub"
done
