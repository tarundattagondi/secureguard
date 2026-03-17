#!/bin/bash
set -e

echo "Waiting for database..."
sleep 3

echo "Running migrations..."
if [ ! -d "migrations" ]; then
    flask db init
    flask db migrate -m "initial models"
fi
flask db upgrade

echo "Seeding database..."
python scripts/seed_controls.py

echo "Starting application..."
exec gunicorn --bind 0.0.0.0:5001 --workers 3 run:app