"""
Data processor for filtering, categorizing, and formatting articles based on client config
"""
from typing import List, Dict, Any
from ..core.models import Article, ClientConfig
import json
import csv
from io import StringIO
from pathlib import Path
from loguru import logger

# Keyword map for auto-categorization
CATEGORY_KEYWORDS = {
    'Breaking': ['breaking', 'urgent', 'alert', 'developing', 'just in', 'flash'],
    'Tech': [
        'ai', 'artificial intelligence', 'software', 'apple', 'google', 'microsoft',
        'meta', 'nvidia', 'chip', 'robot', 'cybersecurity', 'hardware', 'startup',
        'programming', 'developer', 'smartphone', 'gadget', 'silicon', 'openai',
        'chatgpt', 'machine learning', 'tech', 'technology',
    ],
    'Business': [
        'economy', 'market', 'stock', 'trade', 'gdp', 'company', 'corporate',
        'acquisition', 'merger', 'ipo', 'revenue', 'profit', 'startup', 'ceo',
        'business', 'commerce', 'industry', 'manufacturing',
    ],
    'Global': [
        'war', 'un ', 'united nations', 'treaty', 'summit', 'diplomat', 'nato',
        'conflict', 'ceasefire', 'refugee', 'sanction', 'invasion', 'global',
        'international', 'foreign', 'world news', 'ukraine', 'middle east',
    ],
    'Health': [
        'vaccine', 'cancer', 'fda', 'hospital', 'mental health', 'drug', 'disease',
        'medicine', 'pandemic', 'virus', 'outbreak', 'health', 'medical', 'surgery',
        'patient', 'therapy', 'clinical', 'treatment',
    ],
    'Sports': [
        'championship', 'league', 'goal', 'player', 'match', 'tournament', 'nba',
        'nfl', 'fifa', 'cricket', 'tennis', 'olympics', 'athlete', 'coach', 'sport',
        'game', 'score', 'season', 'transfer', 'football', 'basketball', 'baseball',
    ],
    'Politics': [
        'election', 'president', 'senate', 'congress', 'vote', 'law', 'policy',
        'government', 'democrat', 'republican', 'parliament', 'prime minister',
        'white house', 'legislation', 'political', 'campaign', 'ballot',
    ],
    'Finance': [
        'crypto', 'bitcoin', 'ethereum', 'bank', 'interest rate', 'inflation',
        'investment', 'hedge fund', 'wall street', 'nasdaq', 'dow jones', 'finance',
        'financial', 'currency', 'dollar', 'federal reserve', 'vc', 'venture capital',
    ],
    'Travel': [
        'flight', 'tourism', 'airline', 'hotel', 'destination', 'travel', 'airport',
        'visa', 'passport', 'vacation', 'cruise', 'resort', 'booking',
    ],
    'Gaming': [
        'playstation', 'xbox', 'steam', 'nintendo', 'game release', 'esports',
        'gaming', 'video game', 'indie game', 'gamer', 'twitch', 'streamer',
    ],
}


class DataProcessor:
    """Process articles according to client configuration"""
    
    def __init__(self, client_config: ClientConfig):
        self.config = client_config
        
    def process(self, articles: List[Article]) -> Any:
        """Filter, categorize, and format articles"""
        filtered_articles = self._filter_articles(articles)
        # Auto-categorize any article that doesn't already have a category
        for article in filtered_articles:
            if not article.category:
                article.category = self._categorize_article(article)
        return self._format_output(filtered_articles)

    def _categorize_article(self, article: Article) -> str:
        """Assign a category to an article using keyword matching."""
        text = (article.title + ' ' + article.content).lower()
        scores: Dict[str, int] = {}
        for category, keywords in CATEGORY_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                scores[category] = score
        if scores:
            return max(scores, key=scores.get)
        return 'Global'  # Default fallback

    def _filter_articles(self, articles: List[Article]) -> List[Article]:
        """Filter articles based on keywords and exclusions"""
        if not articles:
            return []
            
        filtered = []
        for article in articles:
            # Check excluded keywords
            if any(keyword.lower() in article.title.lower() or keyword.lower() in article.content.lower() 
                   for keyword in self.config.excluded_keywords):
                continue
                
            # Check inclusion keywords (if any are specified), but skip if categories only
            if self.config.keywords and not self.config.categories:
                if not any(keyword.lower() in article.title.lower() or keyword.lower() in article.content.lower() 
                           for keyword in self.config.keywords):
                    continue
            
            filtered.append(article)
            
        logger.info(f"Filtered {len(articles)} articles down to {len(filtered)} for client {self.config.name}")
        return filtered
    
    def _format_output(self, articles: List[Article]) -> Any:
        """Format the filtered articles"""
        if self.config.output_format == 'json':
            return json.dumps([a.to_dict() for a in articles], indent=2, default=str)
            
        elif self.config.output_format == 'csv':
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(['Title', 'Source', 'URL', 'Published Date', 'Summary', 'Category'])
            for a in articles:
                writer.writerow([a.title, a.source, a.url, a.published_date, a.content[:200] + '...', a.category])
            return output.getvalue()
            
        elif self.config.output_format == 'markdown':
            md = f"# News Report for {self.config.name}\n\n"
            for a in articles:
                md += f"## [{a.title}]({a.url})\n"
                md += f"**Source:** {a.source} | **Date:** {a.published_date} | **Category:** {a.category}\n\n"
                md += f"{a.content[:500]}...\n\n---\n\n"
            return md
            
        else:
            return articles  # Return raw list if unknown format
