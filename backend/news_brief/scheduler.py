import logging
import sys
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone

logger = logging.getLogger(__name__)

# Add src to path so AgentOrchestrator can be imported
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))


def scrape_news_job():
    """Periodic task: scrape all active publishers and save new articles to DB."""
    logger.info("=== Background news scraping job starting ===")
    try:
        from bytebrief.core.models import ClientConfig
        from bytebrief.agent.orchestrator import AgentOrchestrator
        orch = AgentOrchestrator()
        result = orch.run(ClientConfig(name="Background Worker", categories=["global"]))
        logger.info(f"=== Background scraping done. Processed {len(result) if result else 0} articles ===")
    except Exception as e:
        logger.error(f"Background scraping failed: {e}", exc_info=True)


def start_scheduler():
    """Initialize and start the APScheduler background scheduler."""
    scheduler = BackgroundScheduler(timezone=timezone.get_current_timezone())
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # ── Scrape news every 15 minutes ─────────────────────────────────────────
    scheduler.add_job(
        scrape_news_job,
        trigger=IntervalTrigger(minutes=15),
        id="scrape_news_job",
        max_instances=1,
        replace_existing=True,
    )

    # ── Send daily email digest at 8:00 AM ──────────────────────────────────
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
    logger.info("APScheduler started — news scraped every 15 min, digest emailed daily at 8 AM.")
