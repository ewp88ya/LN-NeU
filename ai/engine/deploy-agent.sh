#!/bin/bash

# =========================
# REAL SAAS DEPLOY ENGINE
# =========================

VPS_USER="ubuntu"
VPS_IP="YOUR_VPS_IP"
VPS_PATH="/var/www/ln-neu"

echo "🚀 SAAS DEPLOY ENGINE STARTED"

echo "📦 Pushing latest code..."

git add -A
git commit -m "deploy: production update $(date +'%H:%M:%S')" || true
git push origin main

echo "🔗 Connecting to VPS..."

ssh $VPS_USER@$VPS_IP << 'EOF'

cd /var/www/ln-neu

echo "📥 Pulling latest code..."
git pull origin main

echo "🐳 Rebuilding containers..."
docker compose down
docker compose up -d --build

echo "✅ Deployment complete"

EOF

echo "🎯 SAAS SYSTEM UPDATED ON VPS"
