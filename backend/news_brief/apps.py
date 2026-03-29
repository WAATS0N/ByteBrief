import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)


class NewsBriefConfig(AppConfig):
    name = 'news_brief'

    def ready(self):
        import news_brief.signals
        import os

        # Start the scheduler only in the main thread to prevent duplicate instances
        if os.environ.get('RUN_MAIN', None) == 'true':
            try:
                from .scheduler import start_scheduler
                start_scheduler()
            except Exception as e:
                # Log so errors are visible in the console instead of being silently swallowed
                logger.error(f"Failed to start news scheduler: {e}", exc_info=True)
