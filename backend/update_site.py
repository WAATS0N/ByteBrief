import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bytebrief_web.settings')
django.setup()

from django.contrib.sites.models import Site

site = Site.objects.get(id=1)
site.domain = '127.0.0.1:8000'
site.name = '127.0.0.1:8000'
site.save()
print(f"Site ID 1 updated to {site.domain}")
