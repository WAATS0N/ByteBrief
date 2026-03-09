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
