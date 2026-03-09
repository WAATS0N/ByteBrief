from django.core.management.base import BaseCommand
from news_brief.models import Publisher

class Command(BaseCommand):
    help = 'Seeds the database with 20+ regional RSS feeds for expanded global coverage'

    def handle(self, *args, **kwargs):
        sources = [
            # India - National/Regional
            {"name": "The Hindu", "country": "India", "rss_url": "https://www.thehindu.com/news/national/feeder/default.rss", "base_url": "https://www.thehindu.com"},
            {"name": "Times of India", "country": "India", "rss_url": "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms", "base_url": "https://timesofindia.indiatimes.com"},
            {"name": "NDTV", "country": "India", "rss_url": "https://feeds.feedburner.com/ndtvnews-top-stories", "base_url": "https://www.ndtv.com"},
            {"name": "India Today", "country": "India", "rss_url": "https://www.indiatoday.in/rss/home", "base_url": "https://www.indiatoday.in"},
            {"name": "Hindustan Times", "country": "India", "rss_url": "https://www.hindustantimes.com/rss/topnews/rssfeed.xml", "base_url": "https://www.hindustantimes.com"},
            {"name": "Mint (Finance)", "country": "India", "rss_url": "https://www.livemint.com/rss/news", "base_url": "https://www.livemint.com"},
            
            # USA - Regional/National
            {"name": "New York Times", "country": "USA", "rss_url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml", "base_url": "https://www.nytimes.com"},
            {"name": "Washington Post", "country": "USA", "rss_url": "https://feeds.washingtonpost.com/rss/national", "base_url": "https://www.washingtonpost.com"},
            {"name": "Los Angeles Times", "country": "USA", "rss_url": "https://www.latimes.com/california/rss2.0.xml", "base_url": "https://www.latimes.com"},
            {"name": "Chicago Tribune", "country": "USA", "rss_url": "https://www.chicagotribune.com/arc/outboundfeeds/rss/", "base_url": "https://www.chicagotribune.com"},
            {"name": "NPR National", "country": "USA", "rss_url": "https://feeds.npr.org/1001/rss.xml", "base_url": "https://www.npr.org"},
            {"name": "Fox News", "country": "USA", "rss_url": "https://moxie.foxnews.com/google-publisher/latest.xml", "base_url": "https://www.foxnews.com"},
            
            # Europe / Global Setup
            {"name": "The Guardian (UK)", "country": "Europe", "rss_url": "https://www.theguardian.com/uk/rss", "base_url": "https://www.theguardian.com"},
            {"name": "BBC Europe", "country": "Europe", "rss_url": "https://feeds.bbci.co.uk/news/world/europe/rss.xml", "base_url": "https://www.bbc.com/news"},
            {"name": "Le Monde (English)", "country": "Europe", "rss_url": "https://www.lemonde.fr/en/rss/une.xml", "base_url": "https://www.lemonde.fr/en/"},
            {"name": "Deutsche Welle", "country": "Europe", "rss_url": "https://rss.dw.com/rdf/rss-en-all", "base_url": "https://www.dw.com/en/"},
            {"name": "France 24", "country": "Europe", "rss_url": "https://www.france24.com/en/rss", "base_url": "https://www.france24.com/en/"},
            
            # Tech / Specialized
            {"name": "The Verge", "country": "Global", "rss_url": "https://www.theverge.com/rss/index.xml", "base_url": "https://www.theverge.com"},
            {"name": "Wired", "country": "Global", "rss_url": "https://www.wired.com/feed/rss", "base_url": "https://www.wired.com"},
            {"name": "Bloomberg", "country": "Global", "rss_url": "https://feeds.bloomberg.com/markets/news.rss", "base_url": "https://www.bloomberg.com"},
        ]
        
        count = 0
        for s in sources:
            pub, created = Publisher.objects.update_or_create(
                name=s["name"],
                defaults={
                    "country": s["country"],
                    "rss_url": s["rss_url"],
                    "base_url": s["base_url"],
                    "is_active": True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created {s["name"]}'))
                count += 1
                
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} new regional feeds.'))
