#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit

echo "Building Portfolio Site..."

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input

# Run migrations if DATABASE_URL is set (for production)
if [ -n "$DATABASE_URL" ]; then
    echo "Running database migrations..."
    python manage.py migrate --no-input
    echo "Migrations complete!"
fi

echo "Build complete!"

