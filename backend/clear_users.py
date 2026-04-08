from django.contrib.auth import get_user_model
User = get_user_model()
count, _ = User.objects.filter(is_superuser=False).delete()
print(f"Successfully deleted {count} regular user accounts.")
