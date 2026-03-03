import feedparser
import hashlib
from datetime import datetime
from loguru import logger
from app.db.mongo import articles_col
from app.tasks.nlp_tasks import post_process_article

async def fetch_rss_feed(feed_url: str, source_name: str, category: str = "World"):
    logger.info(f"Fetching RSS feed from {feed_url}")
    feed = feedparser.parse(feed_url)
    
    for entry in feed.entries:
        title = entry.title
        url = entry.link
        article_id = hashlib.sha256(url.encode()).hexdigest()
        
        content_clean = entry.get('summary', '') or entry.get('description', '')
        content_raw = entry.get('content', [{}])[0].get('value', content_clean)
        
        article_doc = {
            "article_id": article_id,
            "title": title,
            "url": url,
            "source_name": source_name,
            "publish_date": datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else datetime.now(),
            "author": entry.get('author', 'Unknown'),
            "scraped_at": datetime.now(),
            "content_raw": content_raw,
            "content_clean": content_clean,
            "category": category,
            "images": [{"url": link.href, "caption": ""} for link in entry.get('links', []) if link.get('rel') == 'enclosure'],
            "whoosh_indexed": False,
            "digest_generated": False,
            "sentiment_score": 0.0,
            "sentiment_label": "NEUTRAL"
        }
        
        await articles_col.update_one(
            {"article_id": article_id},
            {"$set": article_doc},
            upsert=True
        )
        logger.info(f"RSS article saved: {title}")
        post_process_article.delay(article_id)
