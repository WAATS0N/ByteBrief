from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
import logging
from .models import Article, UserPreference

logger = logging.getLogger(__name__)
User = get_user_model()

def send_daily_digests():
    """
    Background job that runs every day to send a personalized news digest to users.
    """
    logger.info("Starting scheduled daily digest emailing process...")
    
    # In a real app we'd filter by an 'email_digest_enabled' field, but here we just send to all users with active preferences
    users = User.objects.all()
    
    time_threshold = timezone.now() - timedelta(days=1)
    # Fetch all articles from the last 24 hours
    recent_articles = Article.objects.select_related('publisher').filter(published_at__gte=time_threshold).order_by('-published_at')
    
    # Pre-cache articles by category so we don't do python filtering inefficiently
    articles_by_cat = {}
    for a in recent_articles:
        cat = (a.category or 'Global').lower()
        if cat not in articles_by_cat:
            articles_by_cat[cat] = []
        articles_by_cat[cat].append(a)
        
    emails_sent = 0
    for user in users:
        # Get user email
        if not user.email:
            continue
            
        try:
            prefs = UserPreference.objects.get(user=user)
            categories = prefs.categories
        except UserPreference.DoesNotExist:
            categories = [] # Default to all or none? Let's give them global + breaking
            
        # Collect top 10 articles matching their preferences
        user_feed = []
        
        if categories:
            for cat in categories:
                cat_lower = cat.lower()
                user_feed.extend(articles_by_cat.get(cat_lower, [])[:5])
        else:
            # If no prefs, just give them top 10 recent
            user_feed = list(recent_articles)[:10]
            
        # Deduplicate
        seen_urls = set()
        unique_feed = []
        for a in user_feed:
            if a.url not in seen_urls:
                seen_urls.add(a.url)
                unique_feed.append(a)
                
        # Only send if there are new articles
        if len(unique_feed) > 0:
            html_content = render_to_string('news_brief/digest_email.html', {
                'user': user,
                'articles': unique_feed[:10]
            })
            
            subject = f"Your ByteBrief Daily Digest ({timezone.now().strftime('%b %d')})"
            msg = EmailMultiAlternatives(
                subject=subject,
                body="Please view this email in an HTML email client.",
                from_email=None, # Uses DEFAULT_FROM_EMAIL
                to=[user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            
            try:
                msg.send(fail_silently=False)
                emails_sent += 1
            except Exception as e:
                logger.error(f"Failed to send email to {user.email}: {e}")
                
    logger.info(f"Daily digest emailing process complete. Sent {emails_sent} emails.")
