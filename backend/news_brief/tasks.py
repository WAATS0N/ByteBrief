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

def automated_pipeline_job():
    """
    ByteBrief Automated Setup:
    1. Clean old news (older than 7 days) preserving bookmarks.
    2. Run scraper logic to fetch, summarize, and deduplicate.
    """
    logger.info("🎬 [AUTOMATION] Starting Daily/Hourly News Pipeline...")
    
    # 1. Cleanup old news
    try:
        cleanup_old_news()
    except Exception as e:
        logger.error(f"❌ [AUTOMATION] Failed to cleanup old news: {e}", exc_info=True)

    # 2. Run Scraping & AI Summaries
    try:
        run_orchestrator_scraper()
    except Exception as e:
        logger.error(f"❌ [AUTOMATION] Failed during scraping/summarization: {e}", exc_info=True)

def cleanup_old_news():
    logger.info("🧹 [CLEANUP] Deleting articles older than 7 days that are not bookmarked...")
    seven_days_ago = timezone.now() - timedelta(days=7)
    
    from .models import Bookmark
    
    old_articles = Article.objects.filter(published_at__lt=seven_days_ago)
    bookmarked_article_ids = Bookmark.objects.values_list('article_id', flat=True)
    unbookmarked_old_articles = old_articles.exclude(id__in=bookmarked_article_ids)
    
    deleted_count, _ = unbookmarked_old_articles.delete()
    logger.info(f"✅ [CLEANUP] Successfully deleted {deleted_count} outdated articles.")

def run_orchestrator_scraper():
    logger.info("🕸️ [SCRAPER] Initializing AgentOrchestrator to fetch fresh data...")
    from bytebrief.core.models import ClientConfig
    from bytebrief.agent.orchestrator import AgentOrchestrator
    import os
    from django.conf import settings
    
    config_dir = os.path.join(settings.BASE_DIR, 'config')
    orch = AgentOrchestrator(config_dir=config_dir)

    config = ClientConfig(name="Automated Background Pull", keywords=[], categories=[], excluded_keywords=[])
    
    results = orch.run(config)
    
    processed_count = len(results) if results else 0
    logger.info(f"✅ [SCRAPER] Successfully pulled and summarized {processed_count} new articles.")
