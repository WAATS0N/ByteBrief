"""
Test script for CNN Scraper
This script tests the CNN scraper functionality and compares it with BBC scraper
"""
import sys
from pathlib import Path
from loguru import logger
from datetime import datetime

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.scraper.sources.cnn_scraper import CNNScraper
from src.scraper.sources.bbc_scraper import BBCScraper


def setup_logging():
    """Configure logging for the test script"""
    # Remove default logger
    logger.remove()
    
    # Add console logging with colors
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True
    )


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
            
            # Display sample articles
            for i, article in enumerate(articles[:3], 1):  # Show first 3 articles
                logger.info(f"📄 Sample Article #{i}:")
                logger.info(f"  Title: {article.title}")
                logger.info(f"  URL: {article.url}")
                logger.info(f"  Source: {article.source}")
                logger.info(f"  Published: {article.published_date}")
                logger.info(f"  Content Preview: {article.content[:100]}...")
                logger.info("")
            
            # Save articles to file
            output_file = scraper.save_articles(articles, "cnn_test_articles.json")
            logger.success(f"💾 CNN Articles saved to: {output_file}")
            
        else:
            logger.warning("⚠️ No articles were scraped from CNN")
            
    except Exception as e:
        logger.error(f"❌ Error during CNN scraping: {e}")
        raise


def compare_scrapers():
    """Compare CNN and BBC scrapers side by side"""
    logger.info("🔄 Comparing CNN and BBC scrapers...")
    
    try:
        # Test both scrapers
        cnn_scraper = CNNScraper()
        bbc_scraper = BBCScraper()
        
        logger.info("📊 Scraping both sources for comparison...")
        
        # Scrape CNN
        cnn_articles = cnn_scraper.scrape_source('cnn')
        logger.info(f"CNN: {len(cnn_articles)} articles")
        
        # Scrape BBC  
        bbc_articles = bbc_scraper.scrape_source('bbc')
        logger.info(f"BBC: {len(bbc_articles)} articles")
        
        # Comparison summary
        logger.info("📈 Scraper Comparison Results:")
        logger.info(f"  🇺🇸 CNN Articles: {len(cnn_articles)}")
        logger.info(f"  🇬🇧 BBC Articles: {len(bbc_articles)}")
        logger.info(f"  📊 Total Articles: {len(cnn_articles) + len(bbc_articles)}")
        
        # Save combined results
        all_articles = cnn_articles + bbc_articles
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = cnn_scraper.save_articles(all_articles, f"combined_news_{timestamp}.json")
        logger.success(f"💾 Combined articles saved to: {output_file}")
        
    except Exception as e:
        logger.error(f"❌ Error during comparison: {e}")


def main():
    """Main test function"""
    setup_logging()
    
    logger.info("🗞️ ByteBrief CNN Scraper Test Starting")
    logger.info(f"📅 Current time: {datetime.now()}")
    
    try:
        # Test CNN scraper individually
        test_cnn_scraper()
        
        logger.info("")
        logger.info("=" * 60)
        logger.info("")
        
        # Compare both scrapers
        compare_scrapers()
        
        logger.success("🎉 All tests completed successfully!")
        
    except KeyboardInterrupt:
        logger.warning("⚠️ Test interrupted by user")
        
    except Exception as e:
        logger.error(f"❌ Fatal error during testing: {e}")
        sys.exit(1)
    
    logger.info("👋 CNN Scraper Test finished")


if __name__ == "__main__":
    main()
