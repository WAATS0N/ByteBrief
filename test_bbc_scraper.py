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

# Add src directory to Python path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from scraper.sources.bbc_scraper import BBCScraper
    from scraper.models import Article
    print("✓ Successfully imported BBC scraper modules")
except ImportError as e:
    print(f"✗ Failed to import modules: {e}")
    sys.exit(1)


def test_config_loading():
    """Test if configuration file loads correctly"""
    print("\n=== Testing Configuration Loading ===")
    try:
        scraper = BBCScraper()
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
        scraper = BBCScraper()
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


def test_single_article_scraping():
    """Test scraping a single article"""
    print("\n=== Testing Single Article Scraping ===")
    try:
        scraper = BBCScraper()
        rss_url = scraper.config['news_sources']['bbc']['rss_feed']
        
        # Get RSS feed to find an article URL
        soup = scraper._get_page(rss_url)
        if not soup:
            print("✗ Cannot access RSS feed for article testing")
            return False
            
        links = soup.find_all('link')[1:3]  # Get first 2 article links
        if not links:
            print("✗ No article links found in RSS feed")
            return False
        
        for i, link in enumerate(links, 1):
            article_url = link.text.strip()
            print(f"\nTesting article {i}: {article_url[:60]}...")
            
            # Try to scrape the article page
            article_soup = scraper._get_page(article_url)
            if article_soup:
                print("✓ Successfully accessed article page")
                
                # Test selectors
                source_config = scraper.config['news_sources']['bbc']
                selectors = source_config['selectors']
                
                # Test title extraction
                title = scraper._extract_text(article_soup, selectors['headline'])
                if title:
                    print(f"✓ Title extracted: {title[:50]}...")
                else:
                    print("⚠ Could not extract title")
                
                # Test content extraction
                content = scraper._extract_text(article_soup, selectors['content'])
                if content:
                    print(f"✓ Content extracted: {len(content)} characters")
                else:
                    print("⚠ Could not extract content")
                
                # Test author extraction
                author = scraper._extract_text(article_soup, selectors['author'])
                if author:
                    print(f"✓ Author extracted: {author}")
                else:
                    print("⚠ Could not extract author (this is often normal)")
                
                # Test date extraction
                date_str = scraper._extract_attribute(article_soup, selectors['date'], 'datetime')
                if date_str:
                    print(f"✓ Date extracted: {date_str}")
                else:
                    print("⚠ Could not extract date")
                
                return True
            else:
                print(f"✗ Failed to access article page {i}")
                
        return False
        
    except Exception as e:
        print(f"✗ Single article scraping failed: {e}")
        print(f"Error details: {traceback.format_exc()}")
        return False


def test_full_scraping():
    """Test full BBC scraping process"""
    print("\n=== Testing Full BBC Scraping ===")
    try:
        scraper = BBCScraper()
        print("Starting full BBC scraping...")
        
        # Scrape articles
        articles = scraper.scrape_source('bbc')
        
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
            
            # Test saving articles
            print("--- Testing Article Saving ---")
            output_file = scraper.save_articles(articles, "test_bbc_articles.json")
            print(f"✓ Articles saved to: {output_file}")
            
            # Verify saved file
            if Path(output_file).exists():
                print("✓ Output file created successfully")
                
                # Check file content
                with open(output_file, 'r', encoding='utf-8') as f:
                    saved_data = json.load(f)
                print(f"✓ Saved {len(saved_data)} articles to JSON file")
            else:
                print("✗ Output file not found")
            
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
        ("Single Article Scraping", test_single_article_scraping),
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
