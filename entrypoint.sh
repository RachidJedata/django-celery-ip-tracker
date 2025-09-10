#!/bin/sh
set -e

# Wait for db to be ready
echo "Waiting for database..."
until nc -z db 3306; do
  sleep 2
done

echo "Database is up!"

# Run migrations
python manage.py migrate --noinput

# Start server
exec "$@"
