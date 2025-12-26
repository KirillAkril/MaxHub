#!/usr/bin/env bash
# Build script for Render deployment

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate