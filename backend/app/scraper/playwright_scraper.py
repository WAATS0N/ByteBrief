import asyncio
import hashlib
from datetime import datetime
from playwright.async_api import async_playwright
from loguru import logger
from app.db.mongo import articles_col
from app.tasks.nlp_tasks import post_process_article

async def scrape_with_playwright(url: str, source_name: str, category: str = "World"):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        logger.info(f"Navigating to {url}")
        try:
            await page.goto(url, wait_until="networkidle")
            content_raw = await page.content()
            title = await page.title()
            
            article_id = hashlib.sha256(url.encode()).hexdigest()
            
            article_doc = {
                "article_id": article_id,
                "title": title,
                "url": url,
                "source_name": source_name,
                "publish_date": datetime.now(),
                "author": "Unknown",
                "scraped_at": datetime.now(),
                "content_raw": content_raw,
                "content_clean": " ".join(await page.inner_text('body').split('\n')),
                "category": category,
                "images": [], # Could extract images here
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
            logger.info(f"Playwright article saved: {title}")
            post_process_article.delay(article_id)
            
        except Exception as e:
            logger.error(f"Playwright error for {url}: {e}")
        finally:
            await browser.close()
