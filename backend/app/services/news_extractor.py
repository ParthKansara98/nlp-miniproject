"""
News Extraction Service using newspaper3k
"""

import time
from typing import Optional, Dict, Any
import requests
from newspaper import Article
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class NewsExtractorService:
    def __init__(self):
        self.timeout = 30  # Request timeout in seconds
        
    def extract_from_url(self, url: str) -> Dict[str, Any]:
        """
        Extract article content from a news URL
        
        Args:
            url (str): URL of the news article
        
        Returns:
            dict: Extracted article data
        """
        start_time = time.time()
        
        try:
            # Validate URL
            if not self._is_valid_url(url):
                return {
                    "success": False,
                    "error": "Invalid URL format",
                    "url": url,
                    "processing_time": time.time() - start_time
                }
            
            # Create Article object with better configuration
            article = Article(url, language='hi')  # Use Hindi for Gujarati content
            
            # Download and parse the article
            article.download()
            article.parse()
            
            # Check if we got any content
            if not article.text or len(article.text.strip()) < 50:
                # Try fallback method with requests
                logger.info(f"Primary extraction failed, trying fallback method for {url}")
                fallback_result = self._extract_with_requests(url)
                if fallback_result.get("text"):
                    article.text = fallback_result["text"]
                    article.title = fallback_result.get("title", article.title)
            
            # Extract NLP features if possible
            try:
                if article.text and len(article.text) > 100:
                    article.nlp()
            except Exception as e:
                logger.warning(f"NLP processing failed for {url}: {str(e)}")
            
            processing_time = time.time() - start_time
            
            # Extract article data
            result = {
                "success": True,
                "url": url,
                "title": article.title or "No title found",
                "text": article.text or "No content extracted",
                "authors": list(article.authors) if article.authors else [],
                "publish_date": article.publish_date.isoformat() if article.publish_date else None,
                "summary": article.summary or "",
                "keywords": list(article.keywords) if hasattr(article, 'keywords') else [],
                "top_image": article.top_image or "",
                "source_url": self._get_source_domain(url),
                "article_length": len(article.text) if article.text else 0,
                "processing_time": processing_time,
                "extraction_method": "newspaper3k"
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error extracting article from {url}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "url": url,
                "processing_time": time.time() - start_time
            }
    
    def extract_from_multiple_urls(self, urls: list) -> list:
        """
        Extract articles from multiple URLs
        
        Args:
            urls (list): List of URLs to extract
        
        Returns:
            list: List of extraction results
        """
        results = []
        for url in urls:
            result = self.extract_from_url(url)
            results.append(result)
        
        return results
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Validate if the given string is a valid URL
        
        Args:
            url (str): URL to validate
        
        Returns:
            bool: True if valid URL, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def _get_source_domain(self, url: str) -> str:
        """
        Extract the domain name from URL
        
        Args:
            url (str): URL to extract domain from
        
        Returns:
            str: Domain name
        """
        try:
            parsed_url = urlparse(url)
            return parsed_url.netloc
        except Exception:
            return "unknown"
    
    def get_article_metadata(self, url: str) -> Dict[str, Any]:
        """
        Get metadata about an article without full extraction
        
        Args:
            url (str): URL of the article
        
        Returns:
            dict: Article metadata
        """
        try:
            # Make a simple HEAD request to get basic info
            response = requests.head(url, timeout=self.timeout)
            
            return {
                "url": url,
                "status_code": response.status_code,
                "content_type": response.headers.get('content-type', ''),
                "content_length": response.headers.get('content-length', ''),
                "last_modified": response.headers.get('last-modified', ''),
                "server": response.headers.get('server', ''),
                "accessible": response.status_code == 200
            }
            
        except Exception as e:
            logger.error(f"Error getting metadata for {url}: {str(e)}")
            return {
                "url": url,
                "error": str(e),
                "accessible": False
            }
    
    def clean_extracted_text(self, text: str) -> str:
        """
        Clean and preprocess extracted text
        
        Args:
            text (str): Raw extracted text
        
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace and newlines
        text = " ".join(text.split())
        
        # Remove common unwanted patterns
        unwanted_patterns = [
            "Click here to",
            "Read more",
            "Subscribe to",
            "Follow us on",
            "Advertisement",
            "ADVERTISEMENT"
        ]
        
        for pattern in unwanted_patterns:
            text = text.replace(pattern, "")
        
        # Remove multiple consecutive periods
        text = text.replace("...", ".")
        text = text.replace("..", ".")
        
        return text.strip()
    
    def _extract_with_requests(self, url: str) -> Dict[str, Any]:
        """
        Fallback extraction method using requests and basic HTML parsing
        
        Args:
            url (str): URL to extract from
        
        Returns:
            dict: Extraction result
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            
            # Simple text extraction from HTML
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
            except ImportError:
                logger.error("BeautifulSoup4 not available for fallback extraction")
                return {"text": "", "title": "", "error": "BeautifulSoup4 not available"}
            
            # Remove script and style elements
            for script in soup.find_all(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Try to find main content
            content_selectors = [
                'article', '.article-content', '.post-content', 
                '.news-content', '.story-body', '.content', 
                'main', '.main-content', 'p'
            ]
            
            text = ""
            title = ""
            
            # Extract title
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text().strip()
            
            # Extract content
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    text = " ".join([elem.get_text().strip() for elem in elements])
                    if len(text) > 100:  # If we found substantial content
                        break
            
            return {
                "title": title,
                "text": text,
                "method": "requests_fallback"
            }
            
        except Exception as e:
            logger.error(f"Fallback extraction failed for {url}: {str(e)}")
            return {"text": "", "title": "", "error": str(e)}
    
    def extract_and_clean(self, url: str) -> Dict[str, Any]:
        """
        Extract article and return cleaned text
        
        Args:
            url (str): URL to extract from
        
        Returns:
            dict: Extraction result with cleaned text
        """
        result = self.extract_from_url(url)
        
        if result.get("success") and result.get("text"):
            result["text"] = self.clean_extracted_text(result["text"])
            result["cleaned"] = True
        
        return result
    
    def get_supported_sources(self) -> Dict[str, Any]:
        """
        Get information about supported news sources
        
        Returns:
            dict: Information about supported sources
        """
        return {
            "supported_languages": ["gujarati", "hindi", "english"],
            "common_gujarati_sources": [
                "divyabhaskar.co.in",
                "gujaratsamachar.com",
                "sandesh.com",
                "tv9gujarati.com"
            ],
            "extraction_capabilities": {
                "title": True,
                "text": True,
                "authors": True,
                "publish_date": True,
                "images": True,
                "keywords": True
            }
        }

# Global news extractor instance
news_extractor = NewsExtractorService()