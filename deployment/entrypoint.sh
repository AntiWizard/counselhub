#!/bin/bash

set -e

# There are some times database is not ready yet!
# We'll check if database is ready and we can connect to it
# then the rest of the code run as well.

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

# ---------- Verify ----------
[ -f "$GDAL_LIBRARY_PATH" ] || echo "⚠️ GDAL not found"
[ -f "$GEOS_LIBRARY_PATH" ] || echo "⚠️ GEOS not found"

echo "=============================="

echo "Waiting for postgres database..."
echo DB_NAME: ${DB_NAME}
echo DB_HOST: ${DB_HOST}
echo DB_PORT: ${DB_PORT}
while ! nc -z ${DB_HOST} ${DB_PORT}; do sleep 1; done
echo "Connected to postgres database."

# database migrations will migrate as soon as database is ready
# as a result the database structure is always matched with the recent changes!
echo "Start migrate"

python manage.py migrate --no-input
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to migrate database: $status"
  exit $status
fi


# This step can't apply in Dockerfile because we don't have access to our
# environment data.
echo "Start collectstatic"

python manage.py collectstatic --no-input
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to collect staticfiles: $status"
  exit $status
fi

echo "End collectstatic"

echo "Creating superuser if not exists..."
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model

User = get_user_model()

username = "admin"
password = "admin"
email = "admin@example.com"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        password=password
    )
    print("Superuser created")
else:
    print("Superuser already exists")
EOF

# Let's start Gunicorn
echo "Starting server..."
exec "$@"