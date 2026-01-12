"""
BBC Scraper implementation
"""
from ..core.base_scraper import BaseScraper
from ..core.models import Article
from typing import List
from loguru import logger
from bs4 import BeautifulSoup

class BBCScraper(BaseScraper):
    """Scraper for BBC News"""

    def scrape(self) -> List[Article]:
        """Scrape BBC News"""
        articles = []
        source_name = 'bbc'
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
            # Use XML parser for RSS feeds
            soup = BeautifulSoup(response.content, 'xml')
        except Exception as e:
            logger.error(f"Failed to fetch RSS feed: {e}")
            return articles

        # Extract articles from RSS items
        items = soup.find_all('item')[:10]  # Limit to 10 articles
        logger.info(f"Found {len(items)} items in RSS feed")
        
        for item in items:
            try:
                # Extract basic info from RSS
                title_elem = item.find('title')
                link_elem = item.find('link')
                desc_elem = item.find('description')
                media_thumbnail = item.find('media:thumbnail')
                
                if not title_elem or not link_elem:
                    continue
                    
                article_title = title_elem.get_text(strip=True)
                article_url = link_elem.get_text(strip=True)
                article_description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                # Extract image
                image_url = None
                if media_thumbnail:
                    image_url = media_thumbnail.get('url')
                
                # Fallback: Fetch page to get image if missing
                if not image_url:
                    image_url = self._fetch_image_from_url(article_url)
                
                logger.debug(f"Processing article: {article_title[:50]}...")
                
                # Create article with RSS data
                article = Article(
                    title=article_title,
                    content=article_description,
                    url=article_url,
                    source=source_config.get('name', 'BBC News'),
                    author=None,
                    published_date=None,
                    image_url=image_url
                )

                articles.append(article)
                
                # Rate limit
                self._rate_limit(source_name)
                
            except Exception as e:
                logger.error(f"Error processing RSS item: {e}")
                continue

        return articles
