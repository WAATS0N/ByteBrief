"""
Management command to manually trigger a news scrape.

Usage:
    python manage.py scrape_news
"""
import logging
import sys
from pathlib import Path
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Manually scrape all active news publishers and save articles to the DB."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting manual news scrape..."))

        # Ensure src directory is on the path
        sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent / "src"))

        try:
            from bytebrief.core.models import ClientConfig
            from bytebrief.agent.orchestrator import AgentOrchestrator

            orch = AgentOrchestrator()
            result = orch.run(ClientConfig(name="ManualScrape", categories=["global"]))

            count = len(result) if result else 0
            self.stdout.write(self.style.SUCCESS(f"Scrape complete. Processed {count} articles."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Scrape failed: {e}"))
            logger.error(f"manual scrape_news failed: {e}", exc_info=True)
            raise
