import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bytebrief_web.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
users = User.objects.all()
for u in users:
    print(f"Email: {u.email}, Username: {u.username}, Active: {u.is_active}, Password: {'Set' if u.has_usable_password() else 'Not Set'}")
