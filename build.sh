#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static assets
python manage.py collectstatic --no-input

# Apply migrations
python manage.py migrate
