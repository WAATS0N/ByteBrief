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
            
            # Save articles to file
            output_file = scraper.save_articles(articles, "bbc_test_articles.json")
            logger.success(f"💾 Articles saved to: {output_file}")
            
        else:
            logger.warning("⚠️ No articles were scraped from BBC")
            
    except Exception as e:
        logger.error(f"❌ Error during scraping: {e}")
        raise


def main():
    """Main application entry point"""
    setup_logging()
    
    logger.info("🗞️ ByteBrief News Scraper Starting")
    logger.info(f"📅 Current time: {datetime.now()}")
    
    try:
        # For now, just test BBC scraper
        test_bbc_scraper()
        
        logger.success("✅ Scraping completed successfully!")
        
    except KeyboardInterrupt:
        logger.warning("⚠️ Scraping interrupted by user")
        
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)
    
    logger.info("👋 ByteBrief News Scraper finished")


if __name__ == "__main__":
    main()
