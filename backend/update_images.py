import django
import os
import requests
from bs4 import BeautifulSoup
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bytebrief_web.settings')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from news_brief.models import Article

def fetch_og(a):
    try:
        r = requests.get(a.url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            img = soup.find('meta', property='og:image')
            if img:
                a.image_url = img.get('content')
                a.save(update_fields=['image_url'])
                return 1
    except Exception:
        pass
    return 0

def main():
    print("Starting image update script...")
    arts = list(Article.objects.filter(image_url__isnull=True)[:200])
    print(f"Found {len(arts)} articles without images. Updating...")
    
    updated_count = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(fetch_og, arts)
        updated_count = sum(results)
    
    print(f"Successfully retrieved and updated images for {updated_count} articles.")

if __name__ == '__main__':
    main()
