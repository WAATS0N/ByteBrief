"""
Google Search Scraper for keyword-based news
"""
from ..core.base_scraper import BaseScraper
from ..core.models import Article
from typing import List
from loguru import logger
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime
from dateutil import parser
import re

class GoogleSearchScraper(BaseScraper):
    """Scraper that uses Google News RSS to find articles matching keywords"""

    def scrape(self, query: str, domains: List[str] = None) -> List[Article]:
        """
        Scrape Google News for a query, optionally restricted to specific domains
        
        Args:
            query: The search query
            domains: List of domains to restrict search to (e.g., ['bbc.com', 'cnn.com'])
        """
        articles = []
        
        # Construct search query
        search_query = query
        if domains:
            # Create a site: OR query
            site_query = " OR ".join([f"site:{d}" for d in domains])
            search_query = f"{query} ({site_query})"
            
        encoded_query = urllib.parse.quote(search_query)
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
        
        try:
            logger.info(f"Fetching Google News RSS for query: {query}")
            response = self.session.get(rss_url, timeout=self.timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'xml')
        except Exception as e:
            logger.error(f"Failed to fetch Google News RSS: {e}")
            return articles

        items = soup.find_all('item')[:20]  # Get top 20 results
        logger.info(f"Found {len(items)} items in Google News RSS")
        
        for item in items:
            try:
                title_elem = item.find('title')
                link_elem = item.find('link')
                pub_date_elem = item.find('pubDate')
                source_elem = item.find('source')
                desc_elem = item.find('description')
                
                if not title_elem or not link_elem:
                    continue
                    
                article_title = title_elem.get_text(strip=True)
                # Google News titles often look like "Title - Source Name", let's clean it if possible
                source_name = source_elem.get_text(strip=True) if source_elem else "Google News"
                
                if f" - {source_name}" in article_title:
                    article_title = article_title.replace(f" - {source_name}", "")
                
                article_url = link_elem.get_text(strip=True)
                
                # Extract image from description if available
                image_url = None
                if desc_elem:
                    desc_text = desc_elem.get_text()
                    # Google News RSS descriptions often contain an img tag
                    img_match = re.search(r'src="([^"]+)"', desc_text)
                    if img_match:
                        image_url = img_match.group(1)
                
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
                
                article = Article(
                    title=article_title,
                    content="", # Google RSS doesn't give content
                    url=article_url,
                    source=source_name,
                    author=None,
                    published_date=pub_date,
                    image_url=image_url
                )

                articles.append(article)
                
            except Exception as e:
                logger.error(f"Error processing Google News item: {e}")
                continue

        return articles
