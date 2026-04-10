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
