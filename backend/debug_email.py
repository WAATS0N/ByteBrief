import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bytebrief_web.settings')
django.setup()

from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

User = get_user_model()
try:
    user = User.objects.get(email='chessuk2609@gmail.com')
    print(f"User email: {user.email}")
    email_address = EmailAddress.objects.get(user=user)
    print(f"Allauth email_address user: {email_address.user}")
    print(f"Allauth email_address email: {email_address.email}")
except Exception as e:
    print(e)
