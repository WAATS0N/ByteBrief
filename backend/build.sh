#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing project dependencies..."
pip install --upgrade pip
# This will install all dependencies specified in pyproject.toml
pip install -e .

echo "Collecting static files for WhiteNoise..."
python manage.py collectstatic --no-input

echo "Running Database Migrations..."
python manage.py migrate

echo "Ensuring fully functioning allauth Site Object..."
python manage.py shell -c "from django.contrib.sites.models import Site; Site.objects.get_or_create(id=1, defaults={'domain': 'bytebrief-1.onrender.com', 'name': 'ByteBrief'})"
