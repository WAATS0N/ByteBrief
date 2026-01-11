"""
Data models for ByteBrief news scraper
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
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
    scraped_date: datetime = None
    category: Optional[str] = None
    tags: List[str] = None
    
    def __post_init__(self):
        """Set default values after initialization"""
        if self.scraped_date is None:
            self.scraped_date = datetime.now()
        if self.tags is None:
            self.tags = []
    
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
            'tags': self.tags
        }
    
    def to_json(self) -> str:
        """Convert article to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Article':
        """Create Article from dictionary"""
        # Handle datetime fields
        if data.get('published_date'):
            data['published_date'] = datetime.fromisoformat(data['published_date'])
        if data.get('scraped_date'):
            data['scraped_date'] = datetime.fromisoformat(data['scraped_date'])
        
        return cls(**data)
    
    def __str__(self) -> str:
        return f"Article(title='{self.title[:50]}...', source='{self.source}')"
    
    def __repr__(self) -> str:
        return self.__str__()
