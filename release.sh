#!/usr/bin/env bash
# Release command for Render - runs migrations

set -o errexit

echo "Running database migrations..."

python manage.py migrate --no-input

echo "Migrations complete!"

