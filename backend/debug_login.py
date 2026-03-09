import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bytebrief_web.settings')
django.setup()

from django.contrib.auth import get_user_model
from dj_rest_auth.tests.utils import get_login_response
from django.test.client import RequestFactory

User = get_user_model()
u = User.objects.get(email='chessuk2609@gmail.com')
print(f"Active: {u.is_active}")

from allauth.account.models import EmailAddress
email = EmailAddress.objects.get(user=u)
print(f"Email verified: {email.verified}")
