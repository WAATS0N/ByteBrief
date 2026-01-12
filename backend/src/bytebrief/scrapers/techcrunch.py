"""
TechCrunch Scraper implementation
"""
from ..core.base_scraper import BaseScraper
from ..core.models import Article
from typing import List
from loguru import logger
from bs4 import BeautifulSoup
import re
from dateutil import parser

class TechCrunchScraper(BaseScraper):
    """Scraper for TechCrunch"""

    def scrape(self) -> List[Article]:
        """Scrape TechCrunch"""
        articles = []
        source_name = 'techcrunch'
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
            logger.error(f"Failed to fetch RSS feed: {e}")
            return articles

        items = soup.find_all('item')[:10]
        logger.info(f"Found {len(items)} items in RSS feed")
        
        for item in items:
            try:
                title_elem = item.find('title')
                link_elem = item.find('link')
                desc_elem = item.find('description')
                pub_date_elem = item.find('pubDate')
                creator_elem = item.find('dc:creator')
                media_content = item.find('media:content')
                
                if not title_elem or not link_elem:
                    continue
                    
                article_title = title_elem.get_text(strip=True)
                article_url = link_elem.get_text(strip=True)
                article_description = desc_elem.get_text(strip=True) if desc_elem else ""
                author = creator_elem.get_text(strip=True) if creator_elem else None
                
                # Clean up HTML tags
                article_description = re.sub(r'<[^>]+>', '', article_description)
                
                # Extract image
                image_url = None
                if media_content:
                    image_url = media_content.get('url')
                
                # Fallback: Fetch page to get image if missing
                if not image_url:
                    image_url = self._fetch_image_from_url(article_url)
                
                # Parse date
                pub_date = None
                if pub_date_elem:
                    try:
                        pub_date = parser.parse(pub_date_elem.get_text(strip=True))
                    except Exception:
                        pass
                
                # Attempt to get full content
                full_content = self._extract_article_content(article_url)
                content = full_content if full_content else article_description
                
                article = Article(
                    title=article_title,
                    content=content,
                    url=article_url,
                    source=source_config.get('name', 'TechCrunch'),
                    author=author,
                    published_date=pub_date,
                    image_url=image_url
                )

                articles.append(article)
                self._rate_limit(source_name)
                
            except Exception as e:
                logger.error(f"Error processing RSS item: {e}")
                continue

        return articles
    
    def _extract_article_content(self, url: str) -> str:
        """Extract full article content"""
        try:
            soup = self._get_page(url)
            if not soup:
                return ""
            
            # Selectors for TechCrunch content
            selectors = [
                "div.article-content p",
                "div.entry-content p",
                "div.wp-block-post-content p"
            ]
            
            for selector in selectors:
                paragraphs = soup.select(selector)
                if paragraphs:
                    return '\n\n'.join([p.get_text(strip=True) for p in paragraphs[:10]])
            
            return ""
            
        except Exception as e:
            logger.debug(f"Failed to extract content from {url}: {e}")
            return ""
