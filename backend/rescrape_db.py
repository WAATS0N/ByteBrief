import os
import sys
from pathlib import Path
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bytebrief_web.settings')
sys.path.append(str(Path(__file__).resolve().parent / "src"))
django.setup()

from news_brief.models import Article, Bookmark
from bytebrief.agent.orchestrator import AgentOrchestrator
from bytebrief.core.models import ClientConfig

print("Wiping existing short-summary articles from the database...")
# Delete bookmarks first due to foreign key, then articles
Bookmark.objects.all().delete()
Article.objects.all().delete()

print("Triggering the Agent Orchestrator to fetch new articles with 90+ token summaries...")
orchestrator = AgentOrchestrator(config_dir="src/config")
config = ClientConfig(name="Global Rescrape", keywords=[], categories=[], excluded_keywords=[])

orchestrator.run(config)
print("Finished pulling and summarizing fresh articles!")
