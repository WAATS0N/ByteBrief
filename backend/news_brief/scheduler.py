import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from bytebrief.core.models import ClientConfig
from bytebrief.agent.orchestrator import AgentOrchestrator

logger = logging.getLogger(__name__)

def scrape_news_job():
    """The periodic task that runs the news scraper"""
    logger.info("Starting background news scraping job...")
    try:
        orch = AgentOrchestrator()
        # We process 'global' news to scrape everything active in DB
        result = orch.run(ClientConfig(name="Background Worker", categories=["global"]))
        logger.info(f"Background scraping completed. Generated {len(result)} articles.")
    except Exception as e:
        logger.error(f"Background scraping failed: {e}")

from django._apscheduler.jobstores import DjangoJobStore, register_events
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

def start_scheduler():
    """Initializes and starts the APScheduler"""
    scheduler = BackgroundScheduler(timezone=timezone.get_current_timezone())
    scheduler.add_jobstore(DjangoJobStore(), "default")
    
    # 1. Run the scraper every 15 minutes
    scheduler.add_job(
        scrape_news_job,
        trigger=IntervalTrigger(minutes=15),
        id="scrape_news_job",
        max_instances=1,
        replace_existing=True,
    )
    
    # 2. Run the email digest every morning at 8:00 AM
    from .tasks import send_daily_digests
    scheduler.add_job(
        send_daily_digests,
        trigger=CronTrigger(hour=8, minute=0),
        id="send_daily_digests",
        max_instances=1,
        replace_existing=True,
    )
    
    register_events(scheduler)
    scheduler.start()
    logger.info("APScheduler started! News scraped every 15m. Emails sent daily at 8AM.")
