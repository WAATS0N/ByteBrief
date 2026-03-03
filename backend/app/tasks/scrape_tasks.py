from app.tasks.celery_app import app
from loguru import logger
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from app.scraper.spiders.bbc_spider import BBCSpider
from app.scraper.spiders.reuters_spider import ReutersSpider
from app.scraper.spiders.ap_news_spider import APNewsSpider

@app.task(name="app.tasks.scrape_tasks.scrape_all_sources")
def scrape_all_sources():
    logger.info("Starting scrape all sources task...")
    scrape_bbc.delay()
    scrape_reuters.delay()
    scrape_ap_news.delay()
    logger.info("Triggered all scrapers.")

@app.task(bind=True, max_retries=3)
def scrape_bbc(self):
    try:
        logger.info("Scraping BBC News...")
        process = CrawlerProcess(get_project_settings())
        process.crawl(BBCSpider)
        process.start()
    except Exception as exc:
        logger.error(f"Error scraping BBC: {exc}")
        raise self.retry(exc=exc, countdown=60)

@app.task(bind=True, max_retries=3)
def scrape_reuters(self):
    try:
        logger.info("Scraping Reuters...")
        process = CrawlerProcess(get_project_settings())
        process.crawl(ReutersSpider)
        process.start()
    except Exception as exc:
        logger.error(f"Error scraping Reuters: {exc}")
        raise self.retry(exc=exc, countdown=60)

@app.task(bind=True, max_retries=3)
def scrape_ap_news(self):
    try:
        logger.info("Scraping AP News...")
        process = CrawlerProcess(get_project_settings())
        process.crawl(APNewsSpider)
        process.start()
    except Exception as exc:
        logger.error(f"Error scraping AP News: {exc}")
        raise self.retry(exc=exc, countdown=60)
