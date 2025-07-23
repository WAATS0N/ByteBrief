"""
Main ByteBrief News Scraper Application
"""
import sys
from pathlib import Path
from loguru import logger
from datetime import datetime

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.scraper.sources.bbc_scraper import BBCScraper
from src.scraper.sources.cnn_scraper import CNNScraper
from src.scraper.models import Article


def setup_logging():
    """Configure logging for the scraper"""
    # Remove default logger
    logger.remove()
    
    # Add console logging with colors
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True
    )
    
    # Add file logging
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    logger.add(
        logs_dir / "bytebrief_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
        level="DEBUG",
        rotation="1 day",
        retention="7 days"
    )


def test_bbc_scraper():
    """Test the BBC scraper functionality"""
    logger.info("🚀 Starting ByteBrief BBC News Scraper Test")
    
    try:
        # Initialize BBC scraper
        scraper = BBCScraper()
        logger.info("✅ BBC Scraper initialized successfully")
        
        # Test scraping BBC news
        logger.info("📰 Starting to scrape BBC News...")
        articles = scraper.scrape_source('bbc')
        
        if articles:
            logger.success(f"✅ Successfully scraped {len(articles)} articles from BBC")
            
            # Display first article as sample
            if articles:
                sample_article = articles[0]
                logger.info("📄 Sample Article:")
                logger.info(f"  Title: {sample_article.title}")
                logger.info(f"  URL: {sample_article.url}")
                logger.info(f"  Author: {sample_article.author}")
                logger.info(f"  Source: {sample_article.source}")
                logger.info(f"  Scraped: {sample_article.scraped_date}")
            
            return articles
            
        else:
            logger.warning("⚠️ No articles were scraped from BBC")
            return []
            
    except Exception as e:
        logger.error(f"❌ Error during BBC scraping: {e}")
        return []


def test_cnn_scraper():
    """Test the CNN scraper functionality"""
    logger.info("🚀 Starting ByteBrief CNN News Scraper Test")
    
    try:
        # Initialize CNN scraper
        scraper = CNNScraper()
        logger.info("✅ CNN Scraper initialized successfully")
        
        # Test scraping CNN news
        logger.info("📰 Starting to scrape CNN News...")
        articles = scraper.scrape_source('cnn')
        
        if articles:
            logger.success(f"✅ Successfully scraped {len(articles)} articles from CNN")
            
            # Display first article as sample
            if articles:
                sample_article = articles[0]
                logger.info("📄 Sample CNN Article:")
                logger.info(f"  Title: {sample_article.title}")
                logger.info(f"  URL: {sample_article.url}")
                logger.info(f"  Source: {sample_article.source}")
                logger.info(f"  Published: {sample_article.published_date}")
                logger.info(f"  Scraped: {sample_article.scraped_date}")
            
            return articles
            
        else:
            logger.warning("⚠️ No articles were scraped from CNN")
            return []
            
    except Exception as e:
        logger.error(f"❌ Error during CNN scraping: {e}")
        return []


def scrape_all_sources():
    """Scrape articles from all available news sources"""
    logger.info("🌐 Starting multi-source news scraping...")
    
    all_articles = []
    
    # Scrape BBC News
    logger.info("" + "="*50)
    logger.info("🇬🇧 SCRAPING BBC NEWS")
    logger.info("" + "="*50)
    bbc_articles = test_bbc_scraper()
    all_articles.extend(bbc_articles)
    
    logger.info("")
    
    # Scrape CNN News
    logger.info("" + "="*50)
    logger.info("🇺🇸 SCRAPING CNN NEWS")
    logger.info("" + "="*50)
    cnn_articles = test_cnn_scraper()
    all_articles.extend(cnn_articles)
    
    # Summary and save combined results
    logger.info("")
    logger.info("" + "="*50)
    logger.info("📊 SCRAPING SUMMARY")
    logger.info("" + "="*50)
    logger.info(f"🇬🇧 BBC Articles: {len(bbc_articles)}")
    logger.info(f"🇺🇸 CNN Articles: {len(cnn_articles)}")
    logger.info(f"📈 Total Articles: {len(all_articles)}")
    
    if all_articles:
        # Save all articles to a combined file
        scraper = BBCScraper()  # Use any scraper instance for saving
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = scraper.save_articles(all_articles, f"all_news_{timestamp}.json")
        logger.success(f"💾 All articles saved to: {output_file}")
    
    return all_articles


def main():
    """Main application entry point"""
    setup_logging()
    
    logger.info("🗞️ ByteBrief News Scraper Starting")
    logger.info(f"📅 Current time: {datetime.now()}")
    
    try:
        # Scrape from all available sources (BBC + CNN)
        articles = scrape_all_sources()
        
        if articles:
            logger.success(f"✅ Scraping completed successfully! Total articles: {len(articles)}")
        else:
            logger.warning("⚠️ No articles were scraped from any source")
        
    except KeyboardInterrupt:
        logger.warning("⚠️ Scraping interrupted by user")
        
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)
    
    logger.info("👋 ByteBrief News Scraper finished")


if __name__ == "__main__":
    main()
