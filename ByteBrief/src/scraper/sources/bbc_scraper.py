"""
BBCScraper for scraping articles from BBC News
"""
from ..base_scraper import BaseScraper
from ..models import Article
from typing import List
from datetime import datetime
from loguru import logger

class BBCScraper(BaseScraper):
    """Scraper for BBC News"""

    def scrape_source(self, source_name: str = 'bbc') -> List[Article]:
        """Scrape BBC News"""
        articles = []
        source_config = self.config['news_sources'][source_name]

        # Fetch RSS feed with XML parser
        import requests
        from bs4 import BeautifulSoup
        
        try:
            response = self.session.get(source_config['rss_feed'], timeout=self.timeout)
            response.raise_for_status()
            # Use XML parser for RSS feeds
            soup = BeautifulSoup(response.content, 'xml')
        except Exception as e:
            logger.error(f"Failed to fetch RSS feed: {e}")
            return articles

        # Extract articles from RSS items
        items = soup.find_all('item')[:5]  # Limit to 5 articles for demo
        logger.info(f"Found {len(items)} items in RSS feed")
        
        for item in items:
            try:
                # Extract basic info from RSS
                title_elem = item.find('title')
                link_elem = item.find('link')
                desc_elem = item.find('description')
                
                if not title_elem or not link_elem:
                    continue
                    
                article_title = title_elem.get_text(strip=True)
                article_url = link_elem.get_text(strip=True)
                article_description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                logger.info(f"Processing article: {article_title[:50]}...")
                
                # Create article with RSS data (for now, we'll use description as content)
                article = Article(
                    title=article_title,
                    content=article_description,  # Using RSS description as content for now
                    url=article_url,
                    source=source_config['name'],
                    author=None,  # Not available in RSS
                    published_date=None  # Could parse pubDate if needed
                )

                articles.append(article)
                logger.info(f"✅ Successfully scraped: {article_title[:30]}...")

                # Rate limit
                self._rate_limit(source_name)
                
            except Exception as e:
                logger.error(f"Error processing RSS item: {e}")
                continue

        return articles

