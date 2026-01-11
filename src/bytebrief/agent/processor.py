"""
Data processor for filtering and formatting articles based on client config
"""
from typing import List, Dict, Any
from ..core.models import Article, ClientConfig
import json
import csv
from io import StringIO
from pathlib import Path
from loguru import logger

class DataProcessor:
    """Process articles according to client configuration"""
    
    def __init__(self, client_config: ClientConfig):
        self.config = client_config
        
    def process(self, articles: List[Article]) -> Any:
        """Filter and format articles"""
        filtered_articles = self._filter_articles(articles)
        return self._format_output(filtered_articles)
    
    def _filter_articles(self, articles: List[Article]) -> List[Article]:
        """Filter articles based on keywords and exclusions"""
        if not articles:
            return []
            
        filtered = []
        for article in articles:
            # Check source preference
            if self.config.preferred_sources and article.source.lower() not in [s.lower() for s in self.config.preferred_sources]:
                continue
                
            # Check excluded keywords
            if any(keyword.lower() in article.title.lower() or keyword.lower() in article.content.lower() 
                   for keyword in self.config.excluded_keywords):
                continue
                
            # Check inclusion keywords (if any are specified)
            if self.config.keywords:
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
            writer.writerow(['Title', 'Source', 'URL', 'Published Date', 'Summary'])
            for a in articles:
                writer.writerow([a.title, a.source, a.url, a.published_date, a.content[:200] + '...'])
            return output.getvalue()
            
        elif self.config.output_format == 'markdown':
            md = f"# News Report for {self.config.name}\n\n"
            for a in articles:
                md += f"## [{a.title}]({a.url})\n"
                md += f"**Source:** {a.source} | **Date:** {a.published_date}\n\n"
                md += f"{a.content[:500]}...\n\n---\n\n"
            return md
            
        else:
            return articles  # Return raw list if unknown format
