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

# Lazy-loaded text summariation pipeline
_summarizer = None

def get_summarizer():
    import os
    if os.environ.get('RENDER'):
        logger.warning("Bypassing ML Summarizer on Render Free Tier to prevent 512MB RAM limit OOM crash.")
        return None
        
    global _summarizer
    if _summarizer is None:
        try:
            from transformers import pipeline
            logger.info("Loading ML summarization model (this might take a minute on first run)...")
            # We use a very small, fast distilled model for quick news summarization
            _summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=-1)
            logger.info("ML summarizer loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load ML summarizer: {e}")
            _summarizer = "failed"
            
    return _summarizer if _summarizer != "failed" else None

_classifier = None

def get_classifier():
    import os
    if os.environ.get('RENDER'):
        logger.warning("Bypassing ML Classifier on Render Free Tier to prevent 512MB RAM limit OOM crash.")
        return None

    global _classifier
    if _classifier is None:
        try:
            from transformers import pipeline
            logger.info("Loading ML Zero-Shot Classifier model for categorization...")
            # We use a fast, distilled model for quick news classification
            _classifier = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-3", device=-1)
            logger.info("ML Classifier loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load ML classifier: {e}")
            _classifier = "failed"
            
    return _classifier if _classifier != "failed" else None

# The categories available in the frontend UI
AVAILABLE_CATEGORIES = [
    'Tech', 'Business', 'Global', 'Health', 'Sports',
    'Politics', 'Finance', 'Travel', 'Gaming', 'Entertainment',
    'Breaking', 'Startups & Innovation', 'AI & Future Tech', 
    'Climate & Environment', 'Cybersecurity', 'Digital Life', 
    'Space & Research', 'Psychology & Mind', 'Global Affairs', 'Science'
]

# Removed CATEGORY_KEYWORDS dictionary in favor of ML classification


class DataProcessor:
    """Process articles according to client configuration"""
    
    def __init__(self, client_config: ClientConfig):
        self.config = client_config
        
    def process(self, articles: List[Article]) -> Any:
        """Filter, categorize, save to DB, and format articles"""
        filtered_articles = self._filter_articles(articles)
        # Auto-categorize any article that doesn't already have a category
        for article in filtered_articles:
            if not article.category:
                article.category = self._categorize_article(article)
                
        # Generate ML Summaries
        summarizer = get_summarizer()
        if summarizer:
            logger.info("Generating AI summaries for new articles...")
            for article in filtered_articles:
                if article.content and len(article.content) > 150:
                    try:
                        # Limit input to 1024 chars to avoid token limits
                        res = summarizer(article.content[:1024], max_length=250, min_length=90, do_sample=False)
                        if res and len(res) > 0:
                            article.content = res[0]['summary_text']  # Replace long content with crisp AI summary
                    except Exception as e:
                        logger.warning(f"Summarizer failed for {article.title}: {e}")
                
        # Save to Django Database
        from news_brief.models import Article as DBArticle, Publisher
        from django.utils import timezone
        
        publishers = {p.name: p for p in Publisher.objects.all()}
        db_articles_to_create = []
        
        for article in filtered_articles:
            publisher = publishers.get(article.source)
            if not publisher:
                logger.warning(f"Could not find publisher {article.source} in DB, skipping.")
                continue
                
            db_articles_to_create.append(DBArticle(
                title=article.title[:500],
                summary=(article.content[:497] + '...') if article.content and len(article.content) > 500 else article.content or 'No summary available.',
                content=article.content,
                category=article.category,
                url=article.url[:1000],
                image_url=getattr(article, 'image_url', None)[:1000] if hasattr(article, 'image_url') and article.image_url else None,
                publisher=publisher,
                published_at=article.published_date or timezone.now()
            ))
            
        try:
            if db_articles_to_create:
                DBArticle.objects.bulk_create(db_articles_to_create, ignore_conflicts=True)
                logger.info(f"Successfully bulk saved {len(db_articles_to_create)} unique articles to DB.")
        except Exception as e:
            logger.error(f"Error bulk saving articles to DB: {e}")
            
        return self._format_output(filtered_articles)

    def _categorize_article(self, article: Article) -> str:
        """Assign a category to an article using ML Zero-Shot Classification."""
        text = f"{article.title}. {article.content}"[:1024]  # Limit to 1024 chars for speed
        
        # Check for breaking news urgency first using simple heuristics
        urgency_keywords = ['breaking', 'urgent', 'alert', 'developing', 'just in', 'flash', 'live']
        if any(kw in text.lower() for kw in urgency_keywords[:5]):
            return 'Breaking'
            
        classifier = get_classifier()
        if classifier:
            try:
                # Perform zero-shot classification
                result = classifier(text, candidate_labels=AVAILABLE_CATEGORIES, multi_label=False)
                best_label = result['labels'][0]
                best_score = result['scores'][0]
                
                # Only use the AI classification if it's reasonably confident
                if best_score > 0.2:
                    return best_label
            except Exception as e:
                logger.warning(f"Classification failed for {article.title}: {e}")
                
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
