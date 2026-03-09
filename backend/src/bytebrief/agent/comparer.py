"""
News Comparer for deduplicating articles
"""
from typing import List
from ..core.models import Article
from simhash import Simhash
from loguru import logger
import re
from news_brief.models import Article as DBArticle

class NewsComparer:
    """Logic to compare and group similar articles using Simhash"""
    
    def __init__(self, threshold: int = 3):
        # Difference in bits. Typically 3 for simhash text comparison
        self.threshold = threshold
        
    def get_features(self, text: str):
        width = 3
        text = text.lower()
        text = re.sub(r'[^\w]+', '', text)
        return [text[i:i + width] for i in range(max(len(text) - width + 1, 1))]
        
    def deduplicate(self, articles: List[Article]) -> List[Article]:
        """
        Group similar articles using Simhash and drop articles already stored in DB.
        """
        if not articles:
            return []
            
        # 1. Filter out exact URL duplicates from the database
        db_urls = set(DBArticle.objects.filter(url__in=[a.url for a in articles]).values_list('url', flat=True))
        new_articles = [a for a in articles if a.url not in db_urls]
        
        if len(new_articles) < len(articles):
            logger.info(f"Dropped {len(articles) - len(new_articles)} articles already existing in database.")
            
        if not new_articles:
            return []
            
        # Sort by date
        new_articles.sort(key=lambda x: x.published_date if x.published_date else '1970', reverse=True)
        
        unique_articles = []
        
        for current in new_articles:
            # Create a simhash from title + content
            text_to_hash = current.title + " " + (current.content or "")
            current.simhash = Simhash(self.get_features(text_to_hash))
            
            is_duplicate = False
            for unique in unique_articles:
                # Compare bit difference
                distance = current.simhash.distance(unique.simhash)
                if distance <= self.threshold:
                    if not hasattr(unique, 'related_articles'):
                        unique.related_articles = []
                    unique.related_articles.append(current)
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                current.related_articles = []
                unique_articles.append(current)
                
        logger.info(f"Simhash: Reduced {len(new_articles)} raw incoming articles to {len(unique_articles)} unique stories")
        return unique_articles
