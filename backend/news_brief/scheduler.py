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


from .tasks import automated_pipeline_job

def start_scheduler():
    """Initialize and start the APScheduler background scheduler."""
    scheduler = BackgroundScheduler(timezone=timezone.get_current_timezone())
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # ── Run Automation Pipeline every 6 hours ─────────────────────────────────
    scheduler.add_job(
        automated_pipeline_job,
        trigger=IntervalTrigger(hours=6),
        id="automated_pipeline_job",
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
    logger.info("APScheduler started — Pipeline automation runs every 6 hours, digest emailed daily at 8 AM.")
