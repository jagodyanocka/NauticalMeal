#!/bin/sh
set -e

uv sync --frozen --no-dev
uv run python manage.py migrate --noinput
exec uv run python manage.py runserver 0.0.0.0:8000
