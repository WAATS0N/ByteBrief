import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)


class NewsBriefConfig(AppConfig):
    name = 'news_brief'

    def ready(self):
        import news_brief.signals
        import os
        import sys

        # Prevent running on management commands (migrate, collectstatic, etc.)
        # Only start scheduler in actual server processes (dev server OR Gunicorn)
        is_management_cmd = (
            'migrate' in sys.argv or
            'collectstatic' in sys.argv or
            'shell' in sys.argv or
            'createsuperuser' in sys.argv or
            'makemigrations' in sys.argv
        )

        if is_management_cmd:
            return

        # In Django dev server, RUN_MAIN=true on the reloader child process.
        # In Gunicorn, RUN_MAIN is NOT set — so we check for either condition.
        run_main = os.environ.get('RUN_MAIN', None) == 'true'
        is_gunicorn = 'gunicorn' in os.environ.get('SERVER_SOFTWARE', '').lower() or \
                      any('gunicorn' in arg for arg in sys.argv)

        if run_main or is_gunicorn:
            try:
                from .scheduler import start_scheduler
                start_scheduler()
                logger.info("✅ APScheduler started successfully.")
            except Exception as e:
                logger.error(f"Failed to start news scheduler: {e}", exc_info=True)

            # On cold-start: if article DB is empty, trigger immediate scrape in background
            try:
                from .models import Article
                if Article.objects.count() == 0:
                    logger.info("📭 Database is empty on startup — triggering background scrape...")
                    import threading
                    from django.core.management import call_command

                    def initial_scrape():
                        try:
                            call_command('scrape_news')
                            logger.info("✅ Cold-start scrape completed.")
                        except Exception as ex:
                            logger.error(f"❌ Cold-start scrape failed: {ex}", exc_info=True)

                    thread = threading.Thread(target=initial_scrape, daemon=True)
                    thread.start()
            except Exception as e:
                logger.error(f"Could not check article DB on startup: {e}", exc_info=True)
