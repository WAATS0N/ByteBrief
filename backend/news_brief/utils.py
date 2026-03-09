import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_custom_html_email(subject, template_name, context, to_email):
    """
    Helper function to send HTML emails.
    """
    html_content = render_to_string(template_name, context)
    
    msg = EmailMultiAlternatives(
        subject=subject,
        body="Please view this email in an HTML-compatible client.", # Text fallback
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_welcome_email(user):
    send_custom_html_email(
        subject="Welcome to ByteBrief",
        template_name="emails/welcome_email.html",
        context={"user": user, "frontend_url": "http://localhost:3000"},
        to_email=user.email
    )

def send_login_alert_email(user):
    # In a real app we might get the device/IP from the request context,
    # but for simplicity we'll just send a general alert.
    send_custom_html_email(
        subject="New login detected on your ByteBrief account",
        template_name="emails/login_alert_email.html",
        context={"user": user, "frontend_url": "http://localhost:3000"},
        to_email=user.email
    )

def send_daily_digest_email(user, news_list):
    """
    Utility to send a daily digest. To be triggered by a cron job later.
    """
    send_custom_html_email(
        subject="Today's Top Stories on ByteBrief",
        template_name="emails/daily_digest_email.html",
        context={"user": user, "news_list": news_list, "frontend_url": "http://localhost:3000"},
        to_email=user.email
    )
