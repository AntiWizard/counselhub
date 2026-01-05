#!/bin/bash

set -e

echo "=== Detecting GIS libraries ==="

# ---------- GDAL ----------
if [ ! -f "$GDAL_LIBRARY_PATH" ]; then
  GDAL_LIBRARY_PATH="$(ldconfig -p | grep libgdal.so | head -n1 | awk '{print $NF}')"
fi

if [ ! -f "$GDAL_LIBRARY_PATH" ]; then
  GDAL_LIBRARY_PATH="/usr/lib/x86_64-linux-gnu/libgdal.so"
fi

export GDAL_LIBRARY_PATH

# ---------- GEOS ----------
if [ ! -f "$GEOS_LIBRARY_PATH" ]; then
  GEOS_LIBRARY_PATH="$(ldconfig -p | grep libgeos_c.so | head -n1 | awk '{print $NF}')"
fi

if [ ! -f "$GEOS_LIBRARY_PATH" ]; then
  GEOS_LIBRARY_PATH="/usr/lib/x86_64-linux-gnu/libgeos_c.so"
fi

export GEOS_LIBRARY_PATH

echo "GDAL_LIBRARY_PATH=$GDAL_LIBRARY_PATH"
echo "GEOS_LIBRARY_PATH=$GEOS_LIBRARY_PATH"
echo "=============================="

# Compile messages. build `django.po` file, it will ignore in the code base
python manage.py compilemessages -l fa
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to compilemessages: $status"
  exit $status
fi

echo "Waiting for postgres database..."
echo DB_NAME: ${DB_NAME}
echo DB_HOST: ${DB_HOST}
echo DB_PORT: ${DB_PORT}
while ! nc -z ${DB_HOST} ${DB_PORT}; do sleep 1; done
echo "Connected to postgres database."

echo "Start migrate"
python manage.py migrate --no-input

echo "Ensuring static and media directories exist..."
mkdir -p /app/static /app/media /app/logs
chmod 755 /app/static /app/media /app/logs

echo "Start collectstatic"
python manage.py collectstatic --no-input
echo "End collectstatic"

echo "Creating superuser if not exists..."
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(username="admin", password="admin")
    print("Superuser created")
else:
    print("Superuser already exists")
EOF

# Let's start Gunicorn
echo "Starting server..."
exec "$@"