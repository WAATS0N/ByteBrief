"""
Factory for creating scraper instances
"""
from typing import Dict, Any, Optional
from ..core.base_scraper import BaseScraper
from .bbc import BBCScraper
from .cnn import CNNScraper
from .reuters import ReutersScraper
from .techcrunch import TechCrunchScraper
from .guardian import GuardianScraper

class ScraperFactory:
    """Factory class to create scrapers based on source name"""
    
    _scrapers = {
        'bbc': BBCScraper,
        'cnn': CNNScraper,
        'reuters': ReutersScraper,
        'techcrunch': TechCrunchScraper,
        'guardian': GuardianScraper
    }
    
    @classmethod
    def create_scraper(cls, source_name: str, config: Dict[str, Any]) -> Optional[BaseScraper]:
        """Create a scraper instance"""
        scraper_class = cls._scrapers.get(source_name)
        if scraper_class:
            return scraper_class(config)
        return None
    
    @classmethod
    def register_scraper(cls, source_name: str, scraper_class: type):
        """Register a new scraper"""
        cls._scrapers[source_name] = scraper_class
