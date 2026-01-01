#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit

echo "Building Portfolio Site..."

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input

echo "Build complete!"

