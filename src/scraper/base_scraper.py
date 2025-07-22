"""
Base scraper class for ByteBrief news scraping
"""
import requests
from bs4 import BeautifulSoup
import time
import yaml
from typing import List, Dict, Optional
from pathlib import Path
from loguru import logger
from datetime import datetime
import random

from .models import Article


class BaseScraper:
    """Base class for all news scrapers"""
    
    def __init__(self, config_path: str = "config/news_sources.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.session = requests.Session()
        self._setup_session()
        
    def _load_config(self) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise
    
    def _setup_session(self):
        """Setup HTTP session with headers and configuration"""
        scraper_config = self.config.get('scraper_config', {})
        user_agent = scraper_config.get('user_agent', 'ByteBrief/1.0')
        
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        self.timeout = scraper_config.get('timeout', 10)
        self.retries = scraper_config.get('retries', 3)
    
    def _get_page(self, url: str, retry_count: int = 0) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page with error handling"""
        try:
            logger.info(f"Fetching: {url}")
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
    
    def _rate_limit(self, source_name: str):
        """Apply rate limiting based on source configuration"""
        source_config = self.config['news_sources'].get(source_name, {})
        rate_limit = source_config.get('rate_limit', self.config['scraper_config']['default_rate_limit'])
        
        # Add some randomness to avoid being too predictable
        delay = rate_limit + random.uniform(0, 1)
        logger.debug(f"Rate limiting: waiting {delay:.2f} seconds")
        time.sleep(delay)
    
    def scrape_source(self, source_name: str) -> List[Article]:
        """Scrape articles from a specific news source (to be implemented by subclasses)"""
        raise NotImplementedError("Subclasses must implement scrape_source method")
    
    def scrape_all_sources(self) -> List[Article]:
        """Scrape articles from all configured sources"""
        all_articles = []
        
        for source_name in self.config['news_sources'].keys():
            try:
                logger.info(f"Scraping {source_name}...")
                articles = self.scrape_source(source_name)
                all_articles.extend(articles)
                logger.info(f"Scraped {len(articles)} articles from {source_name}")
            except Exception as e:
                logger.error(f"Failed to scrape {source_name}: {e}")
                continue
        
        logger.info(f"Total articles scraped: {len(all_articles)}")
        return all_articles
    
    def save_articles(self, articles: List[Article], filename: str = None) -> str:
        """Save articles to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scraped_articles_{timestamp}.json"
        
        # Create output directory if it doesn't exist
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        filepath = output_dir / filename
        
        # Convert articles to dictionaries
        articles_data = [article.to_dict() for article in articles]
        
        # Save to JSON file
        import json
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(articles_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(articles)} articles to {filepath}")
        return str(filepath)
