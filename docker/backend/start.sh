#!/usr/bin/env sh
# Backend entrypoint: wait for Postgres (when configured), apply migrations,
# collect static files, then exec the container CMD (gunicorn or runserver).
set -eu

if [ -n "${POSTGRES_HOST:-}" ]; then
  echo "Waiting for Postgres ${POSTGRES_HOST}:${POSTGRES_PORT:-5432}..."
  for i in $(seq 1 30); do
    if python -c "import socket; socket.create_connection((\"${POSTGRES_HOST}\", int(\"${POSTGRES_PORT:-5432}\")), timeout=2)" 2>/dev/null; then
      echo "Postgres is reachable."
      break
    fi
    if [ "$i" -eq 30 ]; then
      echo "Postgres not reachable after 30 attempts — continuing anyway."
    fi
    sleep 1
  done
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput 2>/dev/null || true

exec "$@"
