import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bytebrief_web.settings')
django.setup()
from news_brief.models import ReadingHistory, Article
print("Total Articles:", Article.objects.count())
print("Total ReadingHistory:", ReadingHistory.objects.count())
for rh in ReadingHistory.objects.all():
    print("User:", rh.user.username, "Article:", rh.article.id)
