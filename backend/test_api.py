import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bytebrief_web.settings')
django.setup()
from django.test import RequestFactory
from news_brief.views import generate_digest_api
import json

factory = RequestFactory()
request = factory.post('/api/generate-digest/', data=json.dumps({'categories': ['Tech']}), content_type='application/json')
response = generate_digest_api(request)
data = json.loads(response.content)
print(f"Total articles returned: {len(data['articles'])}")
categories = set(a['category'] for a in data['articles'])
print(f"Categories found: {categories}")
