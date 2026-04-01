import os
import sys
from pathlib import Path
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bytebrief_web.settings')
sys.path.append(str(Path(__file__).resolve().parent / "src"))
django.setup()

from news_brief.models import Article
from bytebrief.agent.processor import DataProcessor
from bytebrief.core.models import ClientConfig

print("Reclassifying all existing articles with the new 20-category AI model...")

processor = DataProcessor(ClientConfig(name="Reclassification", categories=[]))

articles = Article.objects.all()
total = articles.count()
print(f"Found {total} articles to reclassify.")

updated_count = 0
for i, article in enumerate(articles):
    # Simulate the core Article model from core.models
    class DummyArticle:
        def __init__(self, title, content):
            self.title = title
            self.content = content
            
    dummy = DummyArticle(article.title, article.summary or article.content or "")
    new_category = processor._categorize_article(dummy)
    
    if article.category != new_category:
        article.category = new_category
        article.save(update_fields=['category'])
        updated_count += 1
        print(f"[{i+1}/{total}] Migrated: '{article.title[:30]}...' -> {new_category}")

print(f"Successfully reclassified {updated_count} articles into the new categories!")
