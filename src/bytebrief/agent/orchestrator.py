"""
Agent Orchestrator - The Brain
"""
from typing import Dict, Any, List
from ..core.models import Article, ClientConfig
from ..scrapers.factory import ScraperFactory
from ..scrapers.google_search import GoogleSearchScraper
from .processor import DataProcessor
from .comparer import NewsComparer
from loguru import logger
import yaml
from pathlib import Path

class AgentOrchestrator:
    """Orchestrates the scraping and processing workflow"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.settings = self._load_settings()
        self.sources_config = self._load_sources()
        self.comparer = NewsComparer()
        
    def _load_settings(self) -> Dict[str, Any]:
        """Load general settings"""
        try:
            with open(self.config_dir / "settings.yaml", 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return {}
            
    def _load_sources(self) -> Dict[str, Any]:
        """Load source configurations"""
        try:
            with open(self.config_dir / "sources.yaml", 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return {}

    def run(self, client_config: ClientConfig) -> Any:
        """Run the agent for a specific client"""
        logger.info(f"Starting agent run for client: {client_config.name}")
        
        all_articles = []
        
        # Strategy:
        # 1. If keywords are present, use Google Search Scraper for targeted results
        # 2. If no keywords, scrape RSS feeds from preferred sources
        
        sources_to_scrape = client_config.preferred_sources or self.sources_config.get('news_sources', {}).keys()
        
        # Get domains for Google Search if needed
        domains = []
        for source in sources_to_scrape:
            source_cfg = self.sources_config.get('news_sources', {}).get(source.lower())
            if source_cfg and 'base_url' in source_cfg:
                # Extract domain from base_url (e.g., "https://www.bbc.com/news" -> "bbc.com")
                from urllib.parse import urlparse
                domain = urlparse(source_cfg['base_url']).netloc.replace('www.', '')
                domains.append(domain)
        
        if client_config.keywords:
            # Use Google Search Scraper
            logger.info(f"Keywords detected: {client_config.keywords}. Using Google Search Scraper.")
            search_scraper = GoogleSearchScraper({**self.settings, **self.sources_config})
            
            for keyword in client_config.keywords:
                try:
                    logger.info(f"Searching for '{keyword}' across {len(domains)} domains")
                    articles = search_scraper.scrape(keyword, domains)
                    all_articles.extend(articles)
                except Exception as e:
                    logger.error(f"Search failed for keyword '{keyword}': {e}")
        else:
            # Fallback to standard RSS scraping
            logger.info("No keywords detected. Scraping RSS feeds.")
            for source_name in sources_to_scrape:
                source_name = source_name.lower()
                if source_name not in self.sources_config.get('news_sources', {}):
                    logger.warning(f"Source {source_name} not configured, skipping.")
                    continue
                    
                logger.info(f"Dispatching scraper for {source_name}")
                
                # Create scraper with merged config
                full_config = {**self.settings, **self.sources_config}
                scraper = ScraperFactory.create_scraper(source_name, full_config)
                
                if scraper:
                    try:
                        articles = scraper.scrape()
                        all_articles.extend(articles)
                    except Exception as e:
                        logger.error(f"Scraper {source_name} failed: {e}")
                else:
                    logger.warning(f"No scraper implementation found for {source_name}")
        
        # Deduplicate results
        logger.info(f"Collected {len(all_articles)} raw articles. Deduplicating...")
        unique_articles = self.comparer.deduplicate(all_articles)
        
        # Process results (filtering is less needed if we used search, but good for safety)
        processor = DataProcessor(client_config)
        result = processor.process(unique_articles)
        
        return result
