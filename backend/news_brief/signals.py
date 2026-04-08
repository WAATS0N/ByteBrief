from allauth.account.signals import email_confirmed
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .utils import send_welcome_email, send_login_alert_email
import logging

logger = logging.getLogger(__name__)

@receiver(email_confirmed)
def email_confirmed_handler(request, email_address, **kwargs):
    """
    Triggered by allauth when a user clicks the confirmation link in their email.
    Sends them the welcome email.
    """
    try:
        user = email_address.user
        send_welcome_email(user)
        logger.info(f"Welcome email sent to {user.email}")
    except Exception as e:
        logger.error(f"Failed to send welcome email to {user.email}: {e}")

@receiver(user_logged_in)
def login_alert(sender, request, user, **kwargs):
    """
    Triggered by Django when a user successfully logs in.
    Sends a login alert email.
    """
    try:
        # Check if the user is actually active/verified before sending alerts
        if user.is_active:
            send_login_alert_email(user)
            logger.info(f"Login alert email sent to {user.email}")
    except Exception as e:
        logger.error(f"Failed to send login alert email to {user.email}: {e}")

from django.db.models.signals import post_save
from .models import Article, Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Article)
def auto_push_breaking_news_notification(sender, instance, created, **kwargs):
    """
    Whenever a new Article is saved into the database, this pipeline kicks in!
    If we detect it as "Breaking" or highly important news, it broadcasts
    a notification directly to all ByteBrief users automatically.
    """
    if created and instance.category:
        if instance.category.lower() == 'breaking' or instance.category.lower() == 'urgent':
            users = User.objects.all()
            
            notifications = [
                Notification(
                    user=user,
                    title="🚨 New Breaking News!",
                    message=f"Just In: {instance.title[:60]}... Open ByteBrief to learn more."
                )
                for user in users
            ]
            
            # Efficiently write to Database at scale
            if notifications:
                Notification.objects.bulk_create(notifications)
