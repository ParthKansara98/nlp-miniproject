"""
Gujarati to English Translation Service using deep_translator
"""

import time
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        self.model_name = "deep_translator"
        self.translator = None
        self._load_model()
    
    def _load_model(self):
        """Load the translation model"""
        try:
            logger.info("Loading deep_translator GoogleTranslator")
            from deep_translator import GoogleTranslator
            self.translator = GoogleTranslator(source='gu', target='en')
            logger.info(f"Deep translator loaded successfully: {type(self.translator)}")
            
        except Exception as e:
            logger.error(f"Failed to load deep_translator: {e}")
            self.translator = None
    
    def detect_language(self, text: str) -> str:
        """Detect the language of the input text"""
        try:
            from langdetect import detect
            detected_lang = detect(text)
            return detected_lang
        except Exception as e:
            logger.warning(f"Language detection failed: {str(e)}")
            return "gu"  # Default to Gujarati
    
    def translate_text(self, text: str, source_lang: str = "gu", target_lang: str = "en") -> dict:
        """
        Translate text from Gujarati to English
        
        Args:
            text (str): Text to translate
            source_lang (str): Source language code (default: "gu")
            target_lang (str): Target language code (default: "en")
        
        Returns:
            dict: Translation result with metadata
        """
        start_time = time.time()
        
        if not self.translator:
            return {
                "original_text": text,
                "translated_text": "Translation service unavailable",
                "error": "Model not loaded",
                "processing_time": 0,
                "confidence": 0
            }
        
        try:
            # Detect language if not specified
            if source_lang == "auto":
                detected_lang = self.detect_language(text)
                source_lang = detected_lang
            
            # Clean and prepare text
            cleaned_text = self._preprocess_text(text)
            
            # Translate using deep_translator
            logger.info(f"Translating text with {type(self.translator)}")
            translated_text = self.translator.translate(cleaned_text)
            
            logger.info(f"Translation successful: '{cleaned_text[:50]}...' -> '{translated_text[:50]}...'")
            
            processing_time = time.time() - start_time
            
            # Post-process translation
            translated_text = self._postprocess_text(translated_text)
            
            return {
                "original_text": text,
                "translated_text": translated_text,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "processing_time": processing_time,
                "confidence": 0.85,  # Placeholder confidence score
                "model_used": self.model_name
            }
            
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return {
                "original_text": text,
                "translated_text": f"Translation failed: {str(e)}",
                "error": str(e),
                "processing_time": time.time() - start_time,
                "confidence": 0
            }
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess text before translation"""
        # Remove extra whitespace
        text = " ".join(text.split())
        
        # Limit length for translation service
        if len(text) > 5000:
            text = text[:5000]
        
        return text
    
    def _postprocess_text(self, text: str) -> str:
        """Clean and postprocess translated text"""
        # Remove extra whitespace
        text = " ".join(text.split())
        
        # Capitalize first letter
        if text:
            text = text[0].upper() + text[1:]
        
        return text
    
    def batch_translate(self, texts: list, source_lang: str = "gu", target_lang: str = "en") -> list:
        """
        Translate multiple texts in batch
        
        Args:
            texts (list): List of texts to translate
            source_lang (str): Source language code
            target_lang (str): Target language code
        
        Returns:
            list: List of translation results
        """
        results = []
        for text in texts:
            result = self.translate_text(text, source_lang, target_lang)
            results.append(result)
        
        return results
    
    def get_supported_languages(self) -> dict:
        """Get list of supported languages"""
        return {
            "source_languages": ["gu", "hi", "auto"],
            "target_languages": ["en"],
            "model_info": {
                "name": self.model_name,
                "description": "Gujarati to English translation using Google Translate"
            }
        }
    
    def reload_translator(self) -> dict:
        """Reload the translator and return debug info"""
        self._load_model()
        return {
            "translator_available": self.translator is not None,
            "translator_type": str(type(self.translator)),
            "model_name": self.model_name
        }

# Global translator instance
translator_service = TranslationService()