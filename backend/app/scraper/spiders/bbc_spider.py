import scrapy
import hashlib
from datetime import datetime
from loguru import logger
from app.db.mongo import articles_col
from asgiref.sync import async_to_sync

class BBCSpider(scrapy.Spider):
    name = "bbc"
    allowed_domains = ["bbc.com"]
    start_urls = ["https://www.bbc.com/news/world"]

    def parse(self, response):
        for article in response.css('a[href*="/news/"]'):
            url = response.urljoin(article.attrib['href'])
            yield scrapy.Request(url, callback=self.parse_article)

    def parse_article(self, response):
        title = response.css('h1::text').get()
        if not title:
            return

        url = response.url
        article_id = hashlib.sha256(url.encode()).hexdigest()
        content_raw = response.text
        
        # Simple content extraction (trafilatura etc. in post-processing)
        content_clean = " ".join(response.css('p::text').getall()) 

        # Parsing date from time element
        dt_str = response.css('time::attr(datetime)').get()
        publish_date = datetime.fromisoformat(dt_str.replace('Z', '+00:00')) if dt_str else datetime.now()

        article_doc = {
            "article_id": article_id,
            "title": title.strip(),
            "url": url,
            "source_name": "BBC News",
            "publish_date": publish_date,
            "author": response.css('meta[name="author"]::attr(content)').get() or "Unknown",
            "scraped_at": datetime.now(),
            "content_raw": content_raw,
            "content_clean": content_clean,
            "category": "World",
            "images": [{"url": src, "caption": ""} for src in response.css('img::attr(src)').getall()[:3]],
            "whoosh_indexed": False,
            "digest_generated": False,
            "sentiment_score": 0.0,
            "sentiment_label": "NEUTRAL"
        }

        # Save to MongoDB (Sync call via async_to_sync)
        async_to_sync(articles_col.update_one)(
            {"article_id": article_id},
            {"$set": article_doc},
            upsert=True
        )
        logger.info(f"Scraped and saved: {title}")
        
        # Trigger post-processing task
        from app.tasks.nlp_tasks import post_process_article
        post_process_article.delay(article_id)
