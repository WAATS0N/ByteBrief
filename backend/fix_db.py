import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bytebrief_web.settings')
django.setup()

from news_brief.models import Article

articles = Article.objects.all()
updated = 0
for a in articles:
    if a.summary and a.summary.endswith('...'):
        # Remove the ellipsis and add a period to ensure the frontend split regex works
        a.summary = a.summary[:-3]
        if not a.summary.endswith('.'):
            a.summary += '.'
        a.save()
        updated += 1
        
print(f"Removed trailing ellipsis from {updated} existing articles to enable bullet-point splitting.")
