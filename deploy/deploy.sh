#!/bin/sh
# Deploy ungovernable.tech on the server: fetch, hard-reset to origin/<branch>,
# rebuild and restart the systemd unit.
# Usage: deploy/deploy.sh [branch]   (default: site-v2)
set -eu

BRANCH="${1:-site-v2}"
REPO=/home/exedev/ungovernable.tech

cd "$REPO"
git fetch
git checkout "$BRANCH"
git reset --hard "origin/$BRANCH"
python3 scripts/build.py
python3 scripts/site_check.py
sudo systemctl restart ungovernable-site
echo "deployed $BRANCH"
