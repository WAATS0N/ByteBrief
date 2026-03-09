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
        full_config = {**self.settings, **self.sources_config}

        # Strategy:
        # 1. Always scrape ALL configured RSS sources first for broad coverage
        # 2. If specific keywords are present, also run Google Search for targeted results

        # Query active publishers from the database
        from news_brief.models import Publisher
        from ..scrapers.async_universal import AsyncUniversalScraper
        import asyncio
        
        publishers = list(Publisher.objects.filter(is_active=True))
        logger.info(f"Scraping {len(publishers)} active news sources concurrently...")
        
        scraper = AsyncUniversalScraper(
            timeout=full_config.get('scraper_config', {}).get('timeout', 10),
            max_articles=full_config.get('scraper_config', {}).get('max_articles_per_source', 10)
        )
        
        # Run async scraper concurrently
        articles = asyncio.run(scraper.scrape_all(publishers))
        all_articles.extend(articles)

        # If keywords also provided, supplement with Google Search
        if client_config.keywords:
            logger.info(f"Supplementing with Google Search for keywords: {client_config.keywords}")
            domains = []
            for pub in publishers:
                if pub.base_url:
                    from urllib.parse import urlparse
                    domain = urlparse(pub.base_url).netloc.replace('www.', '')
                    domains.append(domain)

            search_scraper = GoogleSearchScraper(full_config)
            for keyword in client_config.keywords:
                try:
                    results = search_scraper.scrape(keyword, domains)
                    all_articles.extend(results)
                except Exception as e:
                    logger.error(f"Google Search failed for '{keyword}': {e}")

        # If category filter is set, filter only articles that match a category
        if client_config.categories:
            category_lower = [c.lower() for c in client_config.categories]
            # We'll still return all articles but processor will filter further if keywords set

        # Deduplicate results
        logger.info(f"Collected {len(all_articles)} raw articles. Deduplicating...")
        unique_articles = self.comparer.deduplicate(all_articles)
        logger.info(f"After deduplication: {len(unique_articles)} articles")

        # Process: auto-categorize + filter + format
        processor = DataProcessor(client_config)
        result = processor.process(unique_articles)
        
        return result
