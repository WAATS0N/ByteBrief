#!/usr/bin/env python3
"""
Test script for BBC Scraper
This script tests the BBCScraper functionality with various test cases
"""

import sys
from pathlib import Path
import json
from datetime import datetime
import traceback
import yaml

# Add src directory to Python path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from bytebrief.scrapers.bbc import BBCScraper
    from bytebrief.core.models import Article
    print("✓ Successfully imported BBC scraper modules")
except ImportError as e:
    print(f"✗ Failed to import modules: {e}")
    sys.exit(1)


def load_config():
    """Load configuration for testing"""
    config = {}
    try:
        with open("config/settings.yaml", 'r') as f:
            config.update(yaml.safe_load(f))
        with open("config/sources.yaml", 'r') as f:
            config.update(yaml.safe_load(f))
    except Exception as e:
        print(f"Failed to load config: {e}")
    return config

def test_config_loading():
    """Test if configuration file loads correctly"""
    print("\n=== Testing Configuration Loading ===")
    try:
        config = load_config()
        scraper = BBCScraper(config)
        print("✓ Configuration loaded successfully")
        
        # Check if BBC config exists
        if 'bbc' in scraper.config['news_sources']:
            print("✓ BBC configuration found")
            bbc_config = scraper.config['news_sources']['bbc']
            print(f"  - RSS Feed: {bbc_config['rss_feed']}")
            print(f"  - Rate Limit: {bbc_config['rate_limit']} seconds")
        else:
            print("✗ BBC configuration not found")
            return False
        return True
    except Exception as e:
        print(f"✗ Configuration loading failed: {e}")
        return False


def test_rss_feed_access():
    """Test if we can access BBC RSS feed"""
    print("\n=== Testing RSS Feed Access ===")
    try:
        config = load_config()
        scraper = BBCScraper(config)
        rss_url = scraper.config['news_sources']['bbc']['rss_feed']
        
        print(f"Attempting to fetch RSS feed: {rss_url}")
        soup = scraper._get_page(rss_url)
        
        if soup:
            print("✓ Successfully accessed RSS feed")
            
            # Check for RSS elements
            links = soup.find_all('link')
            print(f"✓ Found {len(links)} links in RSS feed")
            
            if len(links) > 1:  # First link is usually RSS self-reference
                print("✓ RSS feed contains article links")
                # Show first few article URLs
                for i, link in enumerate(links[1:6], 1):  # Show first 5 article links
                    article_url = link.text.strip() if link.text else "No URL found"
                    print(f"  {i}. {article_url[:80]}...")
                return True
            else:
                print("✗ No article links found in RSS feed")
                return False
        else:
            print("✗ Failed to access RSS feed")
            return False
            
    except Exception as e:
        print(f"✗ RSS feed access failed: {e}")
        print(f"Error details: {traceback.format_exc()}")
        return False


def test_full_scraping():
    """Test full BBC scraping process"""
    print("\n=== Testing Full BBC Scraping ===")
    try:
        config = load_config()
        scraper = BBCScraper(config)
        print("Starting full BBC scraping...")
        
        # Scrape articles
        articles = scraper.scrape()
        
        if articles:
            print(f"✓ Successfully scraped {len(articles)} articles")
            
            # Display summary of scraped articles
            print("\n--- Scraped Articles Summary ---")
            for i, article in enumerate(articles[:3], 1):  # Show first 3 articles
                print(f"{i}. Title: {article.title[:60]}...")
                print(f"   URL: {article.url[:70]}...")
                print(f"   Author: {article.author or 'N/A'}")
                print(f"   Date: {article.published_date or 'N/A'}")
                print(f"   Content length: {len(article.content) if article.content else 0} characters")
                print()
            
            return True
        else:
            print("✗ No articles were scraped")
            return False
            
    except Exception as e:
        print(f"✗ Full scraping failed: {e}")
        print(f"Error details: {traceback.format_exc()}")
        return False


def main():
    """Run all BBC scraper tests"""
    print("🔍 ByteBrief BBC Scraper Test Suite")
    print("=" * 50)
    
    # Track test results
    tests = [
        ("Configuration Loading", test_config_loading),
        ("RSS Feed Access", test_rss_feed_access),
        ("Full Scraping Process", test_full_scraping)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running test: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Print final results
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! BBC scraper is working correctly.")
    elif passed > 0:
        print("⚠ Some tests passed. BBC scraper has partial functionality.")
    else:
        print("❌ All tests failed. BBC scraper needs debugging.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
