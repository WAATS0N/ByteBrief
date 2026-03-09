import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bytebrief_web.settings')
django.setup()

from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

User = get_user_model()
count, _ = User.objects.all().delete()
EmailAddress.objects.all().delete()

print(f"Successfully deleted {count} users and all associated email records.")
