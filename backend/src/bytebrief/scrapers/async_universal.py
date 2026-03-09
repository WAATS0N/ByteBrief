import asyncio
import aiohttp
from bs4 import BeautifulSoup
from loguru import logger
from typing import List
from ..core.models import Article
from news_brief.models import Publisher

class AsyncUniversalScraper:
    """Universal async scraper that fetches from database Publisher models"""

    def __init__(self, timeout: int = 10, max_articles: int = 10):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.max_articles = max_articles
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

    async def fetch_feed(self, session: aiohttp.ClientSession, publisher: Publisher) -> List[Article]:
        """Fetch and parse a single RSS feed asynchronously"""
        articles = []
        if not publisher.rss_url:
            return articles

        logger.info(f"Fetching {publisher.name} via {publisher.rss_url}")
        try:
            async with session.get(publisher.rss_url, headers={'User-Agent': self.user_agent}) as response:
                response.raise_for_status()
                content = await response.text()
                soup = BeautifulSoup(content, 'xml')
                
                # Support both standard RSS <item> and Atom <entry>
                items = soup.find_all('item')
                if not items:
                    items = soup.find_all('entry')

                for item in items[:self.max_articles]:
                    title_elem = item.find('title')
                    link_elem = item.find('link')
                    desc_elem = item.find('description') or item.find('content')
                    
                    if not title_elem or not link_elem:
                        continue
                        
                    title = title_elem.get_text(strip=True)
                    # Atom links use href attribute
                    url = link_elem.get('href') if not link_elem.get_text(strip=True) else link_elem.get_text(strip=True)
                    content_text = desc_elem.get_text(strip=True) if desc_elem else ""
                    
                    media_thumbnail = item.find('media:thumbnail')
                    image_url = media_thumbnail.get('url') if media_thumbnail else None

                    article = Article(
                        title=title,
                        content=content_text,
                        url=url,
                        source=publisher.name,
                        author=None,
                        published_date=None,
                        image_url=image_url
                    )
                    articles.append(article)
                    
        except Exception as e:
            logger.error(f"Error fetching {publisher.name}: {e}")
            
        return articles

    async def scrape_all(self, publishers: List[Publisher]) -> List[Article]:
        """Concurrently scrape multiple publishers"""
        all_articles = []
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            tasks = [self.fetch_feed(session, pub) for pub in publishers]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, list):
                    all_articles.extend(result)
                    
        return all_articles
