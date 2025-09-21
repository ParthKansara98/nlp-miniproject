"""
Utility functions for the application
"""

import re
from typing import Dict, Any, List
import time
from datetime import datetime
import hashlib

def validate_gujarati_text(text: str) -> bool:
    """
    Check if text contains Gujarati characters
    
    Args:
        text (str): Text to validate
    
    Returns:
        bool: True if contains Gujarati characters
    """
    # Gujarati Unicode range: U+0A80-U+0AFF
    gujarati_pattern = re.compile(r'[\u0A80-\u0AFF]')
    return bool(gujarati_pattern.search(text))

def estimate_reading_time(text: str, wpm: int = 200) -> int:
    """
    Estimate reading time for text
    
    Args:
        text (str): Text to analyze
        wpm (int): Words per minute reading speed
    
    Returns:
        int: Estimated reading time in minutes
    """
    word_count = len(text.split())
    reading_time = max(1, word_count // wpm)
    return reading_time

def truncate_text(text: str, max_length: int = 500, suffix: str = "...") -> str:
    """
    Truncate text to specified length
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
        suffix (str): Suffix to add if truncated
    
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def generate_text_hash(text: str) -> str:
    """
    Generate hash for text content
    
    Args:
        text (str): Text to hash
    
    Returns:
        str: MD5 hash of text
    """
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def format_processing_time(seconds: float) -> str:
    """
    Format processing time for display
    
    Args:
        seconds (float): Time in seconds
    
    Returns:
        str: Formatted time string
    """
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.2f}s"

def extract_sentences(text: str, max_sentences: int = 5) -> List[str]:
    """
    Extract sentences from text
    
    Args:
        text (str): Text to extract sentences from
        max_sentences (int): Maximum number of sentences
    
    Returns:
        list: List of sentences
    """
    # Simple sentence splitting (can be improved with proper NLP)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return sentences[:max_sentences]

def clean_url(url: str) -> str:
    """
    Clean and normalize URL
    
    Args:
        url (str): URL to clean
    
    Returns:
        str: Cleaned URL
    """
    url = url.strip()
    
    # Add https:// if no protocol specified
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    return url

def calculate_text_statistics(text: str) -> Dict[str, Any]:
    """
    Calculate various statistics for text
    
    Args:
        text (str): Text to analyze
    
    Returns:
        dict: Text statistics
    """
    words = text.split()
    sentences = extract_sentences(text, max_sentences=1000)  # Get all sentences
    
    # Character counts
    char_count = len(text)
    char_count_no_spaces = len(text.replace(' ', ''))
    
    # Word statistics
    word_count = len(words)
    avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
    
    # Sentence statistics
    sentence_count = len(sentences)
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
    
    return {
        "character_count": char_count,
        "character_count_no_spaces": char_count_no_spaces,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "average_word_length": round(avg_word_length, 2),
        "average_sentence_length": round(avg_sentence_length, 2),
        "estimated_reading_time": estimate_reading_time(text)
    }

def format_datetime(dt: datetime) -> str:
    """
    Format datetime for display
    
    Args:
        dt (datetime): Datetime object
    
    Returns:
        str: Formatted datetime string
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def is_gujarati_heavy(text: str, threshold: float = 0.3) -> bool:
    """
    Check if text is predominantly in Gujarati
    
    Args:
        text (str): Text to check
        threshold (float): Minimum ratio of Gujarati characters
    
    Returns:
        bool: True if text is Gujarati-heavy
    """
    if not text:
        return False
    
    gujarati_chars = len(re.findall(r'[\u0A80-\u0AFF]', text))
    total_chars = len(re.findall(r'[^\s]', text))  # Non-whitespace chars
    
    if total_chars == 0:
        return False
    
    gujarati_ratio = gujarati_chars / total_chars
    return gujarati_ratio >= threshold

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file operations
    
    Args:
        filename (str): Original filename
    
    Returns:
        str: Sanitized filename
    """
    # Remove invalid characters for filenames
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Limit length
    if len(sanitized) > 255:
        sanitized = sanitized[:255]
    
    return sanitized.strip()

class Timer:
    """Context manager for timing operations"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
    
    @property
    def elapsed_time(self) -> float:
        """Get elapsed time in seconds"""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0