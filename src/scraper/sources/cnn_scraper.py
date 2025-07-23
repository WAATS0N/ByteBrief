"""
CNN Scraper for scraping articles from CNN News
This scraper implements RSS feed parsing and article content extraction for CNN
"""
from ..base_scraper import BaseScraper
from ..models import Article
from typing import List
from datetime import datetime
from loguru import logger
import re


class CNNScraper(BaseScraper):
    """Scraper for CNN News - handles RSS feed parsing and article content extraction"""

    def scrape_source(self, source_name: str = 'cnn') -> List[Article]:
        """
        Scrape CNN News using RSS feed
        
        Args:
            source_name: The source identifier (defaults to 'cnn')
            
        Returns:
            List of Article objects containing scraped news data
        """
        articles = []
        source_config = self.config['news_sources'][source_name]

        # Fetch RSS feed with XML parser for proper RSS handling
        import requests
        from bs4 import BeautifulSoup
        
        try:
            logger.info(f"📡 Fetching CNN RSS feed: {source_config['rss_feed']}")
            response = self.session.get(source_config['rss_feed'], timeout=self.timeout)
            response.raise_for_status()
            
            # Use XML parser specifically for RSS feeds (more reliable than html.parser)
            soup = BeautifulSoup(response.content, 'xml')
        except Exception as e:
            logger.error(f"❌ Failed to fetch CNN RSS feed: {e}")
            return articles

        # Extract articles from RSS items - limiting to prevent overwhelming
        items = soup.find_all('item')[:8]  # Get first 8 articles for testing
        logger.info(f"📰 Found {len(items)} items in CNN RSS feed")
        
        for item in items:
            try:
                # Extract basic RSS data
                title_elem = item.find('title')
                link_elem = item.find('link')
                desc_elem = item.find('description')
                pub_date_elem = item.find('pubDate')
                
                # Skip items without essential data
                if not title_elem or not link_elem:
                    logger.warning("⚠️ Skipping item - missing title or link")
                    continue
                    
                article_title = title_elem.get_text(strip=True)
                article_url = link_elem.get_text(strip=True)
                article_description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                # Clean up HTML tags from description if present
                article_description = re.sub(r'<[^>]+>', '', article_description)
                
                # Parse publication date if available
                pub_date_str = None
                if pub_date_elem:
                    try:
                        # CNN RSS typically uses standard RFC 2822 format
                        from dateutil import parser
                        pub_date_parsed = parser.parse(pub_date_elem.get_text(strip=True))
                        pub_date_str = pub_date_parsed.isoformat()
                    except Exception as e:
                        logger.debug(f"📅 Could not parse date: {e}")
                        # Fallback to raw date string
                        pub_date_str = pub_date_elem.get_text(strip=True)
                
                logger.info(f"🔄 Processing CNN article: {article_title[:50]}...")
                
                # Attempt to get more detailed content from the actual article page
                full_content = self._extract_article_content(article_url, source_config)
                
                # Use full content if available, otherwise fall back to RSS description
                content = full_content if full_content else article_description
                
                # Create Article object with all available data
                article = Article(
                    title=article_title,
                    content=content,
                    url=article_url,
                    source=source_config['name'],
                    author=None,  # CNN RSS doesn't typically include author info
                    published_date=pub_date_str
                )

                articles.append(article)
                logger.success(f"✅ Successfully scraped CNN article: {article_title[:40]}...")

                # Apply rate limiting to be respectful to CNN's servers
                self._rate_limit(source_name)
                
            except Exception as e:
                logger.error(f"❌ Error processing CNN RSS item: {e}")
                continue

        logger.success(f"🎉 CNN scraping completed! Retrieved {len(articles)} articles")
        return articles
    
    def _extract_article_content(self, url: str, source_config: dict) -> str:
        """
        Extract full article content from CNN article page
        
        Args:
            url: The article URL to scrape
            source_config: Configuration for CNN selectors
            
        Returns:
            Extracted article content or empty string if failed
        """
        try:
            # Get the full article page
            soup = self._get_page(url)
            if not soup:
                return ""
            
            # Try multiple CNN content selectors (they change their structure sometimes)
            content_selectors = [
                'div.l-container p',  # Primary selector from config
                'div.zn-body__paragraph',  # Alternative CNN paragraph selector
                'div.BasicArticle__paragraph p',  # Another common CNN structure
                'section[data-zone="BasicArticle"] p',  # Yet another CNN pattern
                'div.Article__content p'  # Backup selector
            ]
            
            content_parts = []
            
            # Try each selector until we find content
            for selector in content_selectors:
                paragraphs = soup.select(selector)
                if paragraphs:
                    content_parts = [p.get_text(strip=True) for p in paragraphs[:5]]  # First 5 paragraphs
                    break
            
            # Join paragraphs with double newline for readability
            full_content = '\n\n'.join(content_parts) if content_parts else ""
            
            if full_content:
                logger.debug(f"📄 Extracted {len(content_parts)} paragraphs from CNN article")
            else:
                logger.debug("⚠️ No content extracted from CNN article page")
                
            return full_content
            
        except Exception as e:
            logger.debug(f"⚠️ Failed to extract full content from CNN article: {e}")
            return ""
