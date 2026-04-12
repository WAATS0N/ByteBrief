#!/usr/bin/env bash
# ── ByteBrief Production Build Script (Render) ───────────────────────────────
# exit on error
set -o errexit

# ── Step 1: Install Python dependencies ─────────────────────────────────────
echo "🐍 Installing Python dependencies..."
pip install --upgrade pip
# This will install all dependencies specified in pyproject.toml
pip install -e .

# ── Step 2: Collect Django static files ─────────────────────────────────────
# NOTE: React frontend must be pre-built locally and committed to the repo.
# The Frontend/build directory should contain the React production build.
echo "📂 Collecting static files for WhiteNoise..."
python manage.py collectstatic --no-input

# ── Step 3: Run Database Migrations ─────────────────────────────────────────
echo "🗄️  Running database migrations..."
python manage.py migrate

# ── Step 4: Ensure allauth Site object is correct ───────────────────────────
echo "🌐 Ensuring allauth Site object is correctly configured..."
RENDER_HOST="${RENDER_EXTERNAL_HOSTNAME:-bytebrief-1.onrender.com}"
python manage.py shell -c "
from django.contrib.sites.models import Site
site, created = Site.objects.get_or_create(id=1)
site.domain = '${RENDER_HOST}'
site.name = 'ByteBrief'
site.save()
print(f'Site configured: {site.domain}')
"

# ── Step 5: Diagnostics ─────────────────────────────────────────────────────
echo "🔍 Running build-time diagnostics..."
echo "Current directory: $(pwd)"
echo "Listing parent directory:"
ls -F ..
echo "Listing Frontend directory (if exists):"
ls -F ../Frontend || echo "Frontend not found"
echo "Listing Frontend/build directory (if exists):"
ls -F ../Frontend/build || echo "Frontend/build not found"

echo "🚀 ByteBrief build complete! Deploying..."

