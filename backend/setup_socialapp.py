import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bytebrief_web.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
import os as std_os

# Ensure the site exists
site, _ = Site.objects.get_or_create(id=1)
site.domain = '127.0.0.1:8000'
site.name = '127.0.0.1:8000'
site.save()

# Create or update the SocialApp for Google
client_id = std_os.environ.get('GOOGLE_CLIENT_ID', 'placeholder_id')
secret = std_os.environ.get('GOOGLE_CLIENT_SECRET', 'placeholder_secret')

app, created = SocialApp.objects.get_or_create(
    provider='google',
    defaults={
        'name': 'Google Login',
        'client_id': client_id,
        'secret': secret,
    }
)

if not created:
    app.client_id = client_id
    app.secret = secret
    app.save()

# Crucial step: Link the SocialApp to the Site
app.sites.add(site)

print(f"SocialApp '{app.name}' linked to Site '{site.domain}' successfully.")
