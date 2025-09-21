"""
Summarization Service using HuggingFace Transformers
"""

import time
from typing import Optional, Dict, Any
from transformers import pipeline
import torch
import logging

logger = logging.getLogger(__name__)

class SummarizationService:
    def __init__(self):
        self.model_name = "facebook/bart-large-cnn"
        self.summarizer = None
        self._load_model()
    
    def _load_model(self):
        """Load the summarization model"""
        try:
            logger.info("Loading summarization model...")
            
            # Try to use GPU if available
            device = 0 if torch.cuda.is_available() else -1
            
            # Load summarization pipeline
            self.summarizer = pipeline(
                "summarization",
                model=self.model_name,
                device=device,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            )
            
            logger.info("Summarization model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading summarization model: {str(e)}")
            # Try alternative model
            try:
                logger.info("Trying alternative summarization model...")
                self.summarizer = pipeline(
                    "summarization",
                    model="google/pegasus-xsum",
                    device=-1  # Use CPU as fallback
                )
                self.model_name = "google/pegasus-xsum"
                logger.info("Alternative summarization model loaded")
            except Exception as e2:
                logger.error(f"Failed to load any summarization model: {str(e2)}")
                self.summarizer = None
    
    def summarize_text(self, text: str, max_length: int = 150, min_length: int = 50) -> Dict[str, Any]:
        """
        Summarize the given text
        
        Args:
            text (str): Text to summarize
            max_length (int): Maximum length of summary
            min_length (int): Minimum length of summary
        
        Returns:
            dict: Summarization result with metadata
        """
        start_time = time.time()
        
        if not self.summarizer:
            return {
                "original_text": text,
                "summary": "Summarization service unavailable",
                "error": "Model not loaded",
                "processing_time": 0,
                "compression_ratio": 0
            }
        
        try:
            # Preprocess text
            cleaned_text = self._preprocess_text(text)
            
            # Check if text is long enough to summarize
            if len(cleaned_text.split()) < min_length:
                return {
                    "original_text": text,
                    "summary": cleaned_text,
                    "compression_ratio": 1.0,
                    "processing_time": time.time() - start_time,
                    "note": "Text too short to summarize effectively"
                }
            
            # Adjust max_length based on input length
            input_length = len(cleaned_text.split())
            adjusted_max_length = min(max_length, input_length // 2)
            adjusted_min_length = min(min_length, adjusted_max_length // 2)
            
            # Perform summarization
            summary_result = self.summarizer(
                cleaned_text,
                max_length=adjusted_max_length,
                min_length=adjusted_min_length,
                do_sample=False,
                truncation=True
            )
            
            summary = summary_result[0]['summary_text']
            processing_time = time.time() - start_time
            
            # Calculate compression ratio
            original_length = len(text.split())
            summary_length = len(summary.split())
            compression_ratio = summary_length / original_length if original_length > 0 else 0
            
            # Post-process summary
            summary = self._postprocess_text(summary)
            
            return {
                "original_text": text,
                "summary": summary,
                "compression_ratio": round(compression_ratio, 3),
                "processing_time": processing_time,
                "original_length": original_length,
                "summary_length": summary_length,
                "model_used": self.model_name
            }
            
        except Exception as e:
            logger.error(f"Summarization error: {str(e)}")
            return {
                "original_text": text,
                "summary": f"Summarization failed: {str(e)}",
                "error": str(e),
                "processing_time": time.time() - start_time,
                "compression_ratio": 0
            }
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess text before summarization"""
        # Remove extra whitespace
        text = " ".join(text.split())
        
        # Remove special characters that might interfere
        # Keep basic punctuation for sentence structure
        
        # Ensure text doesn't exceed model's max input length
        max_input_length = 1024  # BART's typical max length
        words = text.split()
        if len(words) > max_input_length:
            text = " ".join(words[:max_input_length])
        
        return text
    
    def _postprocess_text(self, text: str) -> str:
        """Clean and postprocess summarized text"""
        # Remove extra whitespace
        text = " ".join(text.split())
        
        # Ensure proper capitalization
        if text and not text[0].isupper():
            text = text[0].upper() + text[1:]
        
        # Ensure text ends with proper punctuation
        if text and text[-1] not in '.!?':
            text += '.'
        
        return text
    
    def batch_summarize(self, texts: list, max_length: int = 150, min_length: int = 50) -> list:
        """
        Summarize multiple texts in batch
        
        Args:
            texts (list): List of texts to summarize
            max_length (int): Maximum length of each summary
            min_length (int): Minimum length of each summary
        
        Returns:
            list: List of summarization results
        """
        results = []
        for text in texts:
            result = self.summarize_text(text, max_length, min_length)
            results.append(result)
        
        return results
    
    def extract_key_points(self, text: str, num_points: int = 5) -> Dict[str, Any]:
        """
        Extract key points from text (simplified approach)
        
        Args:
            text (str): Text to extract key points from
            num_points (int): Number of key points to extract
        
        Returns:
            dict: Key points extraction result
        """
        try:
            # Split text into sentences
            sentences = text.split('. ')
            
            # Simple scoring based on sentence length and position
            scored_sentences = []
            for i, sentence in enumerate(sentences):
                if len(sentence.split()) > 5:  # Ignore very short sentences
                    # Simple scoring: longer sentences + position weight
                    score = len(sentence.split()) + (1.0 / (i + 1))
                    scored_sentences.append((sentence, score))
            
            # Sort by score and take top sentences
            scored_sentences.sort(key=lambda x: x[1], reverse=True)
            key_points = [sent[0] for sent in scored_sentences[:num_points]]
            
            return {
                "original_text": text,
                "key_points": key_points,
                "num_points": len(key_points)
            }
            
        except Exception as e:
            logger.error(f"Key points extraction error: {str(e)}")
            return {
                "original_text": text,
                "key_points": [],
                "error": str(e)
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        return {
            "model_name": self.model_name,
            "available": self.summarizer is not None,
            "capabilities": {
                "summarization": True,
                "key_points_extraction": True,
                "batch_processing": True
            }
        }

# Global summarizer instance
summarizer_service = SummarizationService()