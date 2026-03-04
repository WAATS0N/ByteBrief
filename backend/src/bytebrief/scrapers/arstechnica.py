"""
Ars Technica Scraper implementation
"""
from ..core.base_scraper import BaseScraper
from ..core.models import Article
from typing import List
from loguru import logger
from bs4 import BeautifulSoup


class ArsTechnicaScraper(BaseScraper):
    """Scraper for Ars Technica (Technology News)"""

    def scrape(self) -> List[Article]:
        articles = []
        source_name = 'arstechnica'
        source_config = self.config.get('news_sources', {}).get(source_name, {})

        if not source_config:
            logger.error(f"Configuration for {source_name} not found")
            return articles

        rss_feed = source_config.get('rss_feed')
        if not rss_feed:
            logger.error(f"RSS feed URL for {source_name} not found")
            return articles

        try:
            logger.info(f"Fetching RSS feed: {rss_feed}")
            response = self.session.get(rss_feed, timeout=self.timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'xml')
        except Exception as e:
            logger.error(f"Failed to fetch Ars Technica RSS feed: {e}")
            return articles

        items = soup.find_all('item')[:10]
        logger.info(f"Found {len(items)} items in Ars Technica RSS feed")

        for item in items:
            try:
                title_elem = item.find('title')
                link_elem = item.find('link')
                desc_elem = item.find('description')

                if not title_elem or not link_elem:
                    continue

                article_title = title_elem.get_text(strip=True)
                article_url = link_elem.get_text(strip=True)
                article_description = BeautifulSoup(
                    desc_elem.get_text(strip=True) if desc_elem else "", 'html.parser'
                ).get_text()

                image_url = self._fetch_image_from_url(article_url)

                article = Article(
                    title=article_title,
                    content=article_description,
                    url=article_url,
                    source=source_config.get('name', 'Ars Technica'),
                    author=None,
                    published_date=None,
                    image_url=image_url,
                    category='Tech'  # Pre-tag tech source
                )
                articles.append(article)
                self._rate_limit(source_name)

            except Exception as e:
                logger.error(f"Error processing Ars Technica RSS item: {e}")
                continue

        return articles
