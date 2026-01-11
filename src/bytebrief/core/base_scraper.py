"""
Base scraper class for ByteBrief news scraping
"""
import requests
from bs4 import BeautifulSoup
import time
import yaml
from typing import List, Dict, Optional, Any
from pathlib import Path
from loguru import logger
import random
from abc import ABC, abstractmethod

from .models import Article

class BaseScraper(ABC):
    """Base class for all news scrapers"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.session = requests.Session()
        self._setup_session()
        
    def _setup_session(self):
        """Setup HTTP session with headers and configuration"""
        scraper_config = self.config.get('scraper_config', {})
        user_agent = scraper_config.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        })
        
        self.timeout = scraper_config.get('timeout', 15)
        self.retries = scraper_config.get('retries', 3)
    
    def _get_page(self, url: str, retry_count: int = 0) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page with error handling"""
        try:
            logger.debug(f"Fetching: {url}")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request failed for {url}: {e}")
            
            # Retry logic
            if retry_count < self.retries:
                wait_time = (retry_count + 1) * 2  # Exponential backoff
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                return self._get_page(url, retry_count + 1)
            else:
                logger.error(f"Max retries exceeded for {url}")
                return None
        
        except Exception as e:
            logger.error(f"Unexpected error fetching {url}: {e}")
            return None
    
    def _extract_text(self, soup: BeautifulSoup, selector: str) -> Optional[str]:
        """Extract text using CSS selector"""
        try:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        except Exception as e:
            logger.debug(f"Failed to extract text with selector '{selector}': {e}")
        return None
    
    def _extract_attribute(self, soup: BeautifulSoup, selector: str, attribute: str) -> Optional[str]:
        """Extract attribute value using CSS selector"""
        try:
            element = soup.select_one(selector)
            if element:
                return element.get(attribute)
        except Exception as e:
            logger.debug(f"Failed to extract attribute '{attribute}' with selector '{selector}': {e}")
        return None
    
    def _extract_image_from_meta(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract image URL from Open Graph or Twitter meta tags"""
        try:
            # Try og:image
            og_image = soup.find('meta', property='og:image')
            if og_image and og_image.get('content'):
                return og_image.get('content')
            
            # Try twitter:image
            twitter_image = soup.find('meta', name='twitter:image')
            if twitter_image and twitter_image.get('content'):
                return twitter_image.get('content')
                
        except Exception as e:
            logger.debug(f"Failed to extract meta image: {e}")
        return None
        
    def _fetch_image_from_url(self, url: str) -> Optional[str]:
        """Visit the URL and extract the best image"""
        soup = self._get_page(url)
        if soup:
            return self._extract_image_from_meta(soup)
        return None
    
    def _rate_limit(self, source_name: str):
        """Apply rate limiting based on source configuration"""
        # Get rate limit from specific source config or default
        source_config = self.config.get('news_sources', {}).get(source_name, {})
        default_limit = self.config.get('scraper_config', {}).get('default_rate_limit', 2)
        
        rate_limit = source_config.get('rate_limit', default_limit)
        
        # Add some randomness to avoid being too predictable
        delay = rate_limit + random.uniform(0, 1)
        logger.debug(f"Rate limiting: waiting {delay:.2f} seconds")
        time.sleep(delay)
    
    @abstractmethod
    def scrape(self) -> List[Article]:
        """Scrape articles from the source"""
        pass
