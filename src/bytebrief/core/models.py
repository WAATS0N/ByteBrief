"""
Data models for ByteBrief news scraper
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
import json

@dataclass
class Article:
    """Represents a news article with all relevant metadata"""
    
    title: str
    content: str
    url: str
    source: str
    author: Optional[str] = None
    published_date: Optional[datetime] = None
    scraped_date: datetime = field(default_factory=datetime.now)
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    image_url: Optional[str] = None
    related_articles: List['Article'] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert article to dictionary for JSON serialization"""
        # Handle published_date - it could be datetime object or string
        pub_date = None
        if self.published_date:
            if hasattr(self.published_date, 'isoformat'):
                pub_date = self.published_date.isoformat()
            else:
                pub_date = str(self.published_date)
        
        return {
            'title': self.title,
            'content': self.content,
            'url': self.url,
            'source': self.source,
            'author': self.author,
            'published_date': pub_date,
            'scraped_date': self.scraped_date.isoformat(),
            'category': self.category,
            'tags': self.tags,
            'image_url': self.image_url,
            'related_articles': [a.to_dict() for a in self.related_articles] if self.related_articles else []
        }
    
    def to_json(self) -> str:
        """Convert article to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Article':
        """Create Article from dictionary"""
        # Handle datetime fields
        if data.get('published_date'):
            try:
                data['published_date'] = datetime.fromisoformat(data['published_date'])
            except (ValueError, TypeError):
                pass
                
        if data.get('scraped_date'):
            try:
                data['scraped_date'] = datetime.fromisoformat(data['scraped_date'])
            except (ValueError, TypeError):
                data['scraped_date'] = datetime.now()
        
        # Handle related articles (recursive)
        related_data = data.pop('related_articles', [])
        article = cls(**data)
        if related_data:
            article.related_articles = [cls.from_dict(r) for r in related_data]
            
        return article
    
    def __str__(self) -> str:
        return f"Article(title='{self.title[:50]}...', source='{self.source}')"


@dataclass
class ClientConfig:
    """Configuration for client-specific processing"""
    name: str
    keywords: List[str] = field(default_factory=list)
    excluded_keywords: List[str] = field(default_factory=list)
    preferred_sources: List[str] = field(default_factory=list)
    output_format: str = "json"  # json, csv, markdown
    categories: List[str] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ClientConfig':
        return cls(
            name=data.get('name', 'default'),
            keywords=data.get('keywords', []),
            excluded_keywords=data.get('excluded_keywords', []),
            preferred_sources=data.get('preferred_sources', []),
            output_format=data.get('output_format', 'json'),
            categories=data.get('categories', [])
        )
