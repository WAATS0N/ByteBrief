"""
News Comparer for deduplicating articles
"""
from typing import List
from ..core.models import Article
from difflib import SequenceMatcher
from loguru import logger

class NewsComparer:
    """Logic to compare and group similar articles"""
    
    def __init__(self, similarity_threshold: float = 0.6):
        self.similarity_threshold = similarity_threshold
        
    def deduplicate(self, articles: List[Article]) -> List[Article]:
        """
        Group similar articles and return a list of unique stories.
        Duplicates are added to the 'related_articles' field of the primary article.
        """
        if not articles:
            return []
            
        # Sort by date (newest first) so we keep the most recent as primary
        # Note: We need to handle None dates
        articles.sort(key=lambda x: x.published_date if x.published_date else x.scraped_date, reverse=True)
        
        unique_articles = []
        
        for current in articles:
            is_duplicate = False
            
            for unique in unique_articles:
                if self._is_similar(current, unique):
                    # It's a duplicate! Add to related
                    if not hasattr(unique, 'related_articles'):
                        unique.related_articles = []
                    unique.related_articles.append(current)
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                # Initialize related_articles list
                current.related_articles = []
                unique_articles.append(current)
                
        logger.info(f"Deduplication: Reduced {len(articles)} articles to {len(unique_articles)} unique stories")
        return unique_articles
    
    def _is_similar(self, a1: Article, a2: Article) -> bool:
        """Check if two articles are similar based on title"""
        # Simple title similarity
        ratio = SequenceMatcher(None, a1.title.lower(), a2.title.lower()).ratio()
        return ratio >= self.similarity_threshold
