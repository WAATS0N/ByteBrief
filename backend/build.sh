#!/usr/bin/env bash
# ── ByteBrief Production Build Script (Render) ───────────────────────────────
# exit on error
set -o errexit

# ── Step 1: Build React Frontend ────────────────────────────────────────────
echo "📦 Installing frontend dependencies..."
cd ../Frontend
npm ci --silent

echo "⚛️  Building React app..."
npm run build

echo "✅ React build complete."
cd ../backend

# ── Step 2: Install Python dependencies ─────────────────────────────────────
echo "🐍 Installing Python dependencies..."
pip install --upgrade pip
pip install -e .

# ── Step 3: Collect Django static files ─────────────────────────────────────
echo "📂 Collecting static files for WhiteNoise..."
python manage.py collectstatic --no-input

# ── Step 4: Run Database Migrations ─────────────────────────────────────────
echo "🗄️  Running database migrations..."
python manage.py migrate

# ── Step 5: Ensure allauth Site object is correct ───────────────────────────
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

# ── Step 6: Seed the database if empty ──────────────────────────────────────
echo "📰 Checking if database needs initial news seeding..."
python manage.py shell -c "
from news_brief.models import Article
count = Article.objects.count()
if count == 0:
    print('Database is empty — will seed on startup via cold-start scraper.')
else:
    print(f'Database has {count} articles — no seeding needed.')
"

echo "🚀 ByteBrief build complete! Deploying..."
