import scrapy
import hashlib
from datetime import datetime
from loguru import logger
from app.db.mongo import articles_col
from asgiref.sync import async_to_sync

class APNewsSpider(scrapy.Spider):
    name = "apnews"
    allowed_domains = ["apnews.com"]
    start_urls = ["https://apnews.com/hub/world-news"]

    def parse(self, response):
        for article in response.css('a[data-key="card-headline"]::attr(href)'):
            url = response.urljoin(article)
            yield scrapy.Request(url, callback=self.parse_article)

    def parse_article(self, response):
        title = response.css('h1::text').get()
        if not title:
            return

        url = response.url
        article_id = hashlib.sha256(url.encode()).hexdigest()
        
        article_doc = {
            "article_id": article_id,
            "title": title.strip(),
            "url": url,
            "source_name": "AP News",
            "publish_date": datetime.now(),
            "author": "AP News",
            "scraped_at": datetime.now(),
            "content_raw": response.text,
            "content_clean": " ".join(response.css('p::text').getall()),
            "category": "World",
            "images": [{"url": src, "caption": ""} for src in response.css('img::attr(src)').getall()[:3]],
            "whoosh_indexed": False,
            "digest_generated": False,
            "sentiment_score": 0.0,
            "sentiment_label": "NEUTRAL"
        }

        async_to_sync(articles_col.update_one)(
            {"article_id": article_id},
            {"$set": article_doc},
            upsert=True
        )
        logger.info(f"AP News article saved: {title}")
        
        from app.tasks.nlp_tasks import post_process_article
        post_process_article.delay(article_id)
