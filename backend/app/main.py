"""Ultra-compact Gujarati News Translator API"""
import socket
import logging
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager

# Set up logging with UTF-8 encoding to handle Unicode characters properly
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Embedded translation service
class Translator:
    def __init__(self):
        # Try to initialize online translator first
        self.gt = None
        try:
            from deep_translator import GoogleTranslator
            self.gt = GoogleTranslator(source='gu', target='en')
            logger.info("Translation service: OK (online)")
        except Exception as e:
            logger.warning(f"Online translator failed: {e}, using offline method")
        
        # Simple character mapping for basic Gujarati to English transliteration
        self.gujarati_to_english = {
            'અ': 'a', 'આ': 'aa', 'ઇ': 'i', 'ઈ': 'ii', 'ઉ': 'u', 'ઊ': 'uu',
            'એ': 'e', 'ઐ': 'ai', 'ઓ': 'o', 'ઔ': 'au',
            'ક': 'ka', 'ખ': 'kha', 'ગ': 'ga', 'ઘ': 'gha', 'ઙ': 'nga',
            'ચ': 'cha', 'છ': 'chha', 'જ': 'ja', 'ઝ': 'jha', 'ઞ': 'nja',
            'ટ': 'ta', 'ઠ': 'tha', 'ડ': 'da', 'ઢ': 'dha', 'ણ': 'na',
            'ત': 'ta', 'થ': 'tha', 'દ': 'da', 'ધ': 'dha', 'ન': 'na',
            'પ': 'pa', 'ફ': 'pha', 'બ': 'ba', 'ભ': 'bha', 'મ': 'ma',
            'ય': 'ya', 'ર': 'ra', 'લ': 'la', 'વ': 'va',
            'શ': 'sha', 'ષ': 'sha', 'સ': 'sa', 'હ': 'ha',
            '।': '.', '?': '?', '!': '!', ',': ',', ';': ';', ':': ':'
        }
        
        # Common Gujarati words and their English translations
        self.word_translations = {
            'સમાચાર': 'news', 'ખબર': 'news', 'આજ': 'today', 'આજે': 'today',
            'ગુજરાત': 'Gujarat', 'ભારત': 'India', 'અહીં': 'here', 'ત્યાં': 'there',
            'લોકો': 'people', 'જનતા': 'public', 'સરકાર': 'government',
            'મુખ્યમંત્રી': 'Chief Minister', 'પ્રધાનમંત્રી': 'Prime Minister',
            'વર્ષ': 'year', 'મહિનો': 'month', 'દિવસ': 'day', 'સમય': 'time',
            'પૈસા': 'money', 'રૂપિયા': 'rupees', 'હજાર': 'thousand', 
            'લાખ': 'lakh', 'કરોડ': 'crore', 'અબજ': 'billion',
            'શહેર': 'city', 'ગામ': 'village', 'રાજ્ય': 'state',
            'કોર્ટ': 'court', 'ન્યાય': 'justice', 'કાયદો': 'law',
            'પોલીસ': 'police', 'ચૂંટણી': 'election', 'પાર્ટી': 'party'
        }
        
        if not self.gt:
            logger.info("Translation service: OK (offline transliteration)")
    
    def _offline_translate(self, text: str) -> str:
        """Offline translation using transliteration and word mapping"""
        words = text.split()
        translated_words = []
        
        for word in words:
            # Check if word exists in our dictionary
            if word in self.word_translations:
                translated_words.append(self.word_translations[word])
            else:
                # Transliterate character by character
                transliterated = ""
                for char in word:
                    if char in self.gujarati_to_english:
                        transliterated += self.gujarati_to_english[char]
                    else:
                        transliterated += char  # Keep as is if not in mapping
                translated_words.append(transliterated)
        
        result = " ".join(translated_words)
        return f"[Transliterated] {result}"
    
    def translate(self, text: str) -> str:
        if not text or not text.strip():
            return "No text to translate"
        
        # Try online translation first
        if self.gt:
            try:
                result = self.gt.translate(text)
                return result
            except Exception as e:
                logger.warning(f"Online translation failed: {e}, falling back to offline method")
        
        # Fall back to offline translation
        try:
            return self._offline_translate(text)
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return f"Translation unavailable - showing original text: {text}"

# Embedded summarization service
class Summarizer:
    def __init__(self):
        # Use simple extractive summarization - no external dependencies
        self.summarizer = None
        logger.info("Summarization service: OK (offline extractive method)")
    
    def summarize(self, text: str, max_length: int = 150) -> str:
        if not text.strip():
            return "No content to summarize"
        
        try:
            # Advanced extractive summarization
            import re
            
            # Clean the text first
            text = re.sub(r'\s+', ' ', text.strip())
            
            # Split into sentences using multiple delimiters
            sentences = re.split(r'[.!?।]+', text)
            sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
            
            if len(sentences) <= 2:
                return text[:max_length] + "..." if len(text) > max_length else text
            
            # Score sentences based on position and length
            scored_sentences = []
            for i, sentence in enumerate(sentences):
                score = 0
                
                # Position scoring (first and last sentences are important)
                if i == 0:
                    score += 3  # First sentence is very important
                elif i == len(sentences) - 1:
                    score += 2  # Last sentence is important
                elif i < len(sentences) // 3:
                    score += 1  # Early sentences are somewhat important
                
                # Length scoring (medium length sentences are good)
                length = len(sentence)
                if 50 <= length <= 200:
                    score += 2
                elif 20 <= length <= 50:
                    score += 1
                
                # Keyword scoring (simple keyword detection)
                keywords = ['સમાચાર', 'ખબર', 'મહત્વપૂર્ણ', 'મુખ્ય', 'પ્રમુખ', 'સરકાર', 'આજે', 'news', 'important', 'main', 'today']
                for keyword in keywords:
                    if keyword in sentence.lower():
                        score += 1
                
                scored_sentences.append((score, sentence, i))
            
            # Sort by score and select top sentences
            scored_sentences.sort(key=lambda x: (-x[0], x[2]))  # Sort by score desc, then by position
            
            # Select sentences for summary
            selected_sentences = []
            total_length = 0
            
            for score, sentence, original_index in scored_sentences:
                if total_length + len(sentence) <= max_length:
                    selected_sentences.append((sentence, original_index))
                    total_length += len(sentence)
                if len(selected_sentences) >= 3:  # Limit to 3 sentences max
                    break
            
            # Sort selected sentences by original position
            selected_sentences.sort(key=lambda x: x[1])
            summary_text = '. '.join([s[0] for s in selected_sentences])
            
            # Ensure proper ending
            if not summary_text.endswith(('.', '!', '?', '।')):
                summary_text += '.'
            
            return summary_text if summary_text else text[:max_length] + "..."
            
        except Exception as e:
            logger.error(f"Summarization error: {e}")
            # Fallback to simple truncation
            return text[:max_length] + "..." if len(text) > max_length else text

# Embedded URL extractor
class URLExtractor:
    def is_divya_bhaskar(self, url: str) -> bool:
        """Check if URL is from Divya Bhaskar"""
        return 'divyabhaskar.co.in' in url.lower() or 'divyabhaskar' in url.lower()
    
    def extract_divya_bhaskar_content(self, url: str) -> str:
        """Specialized extraction for Divya Bhaskar to avoid copyright issues"""
        try:
            import requests
            from bs4 import BeautifulSoup
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove ALL unwanted elements aggressively
            unwanted_elements = [
                'script', 'style', 'nav', 'header', 'footer', 'aside', 'form', 
                'button', 'input', 'select', 'textarea', 'iframe', 'advertisement',
                'ads', 'social-share', 'comments', 'related-articles', 'more-news'
            ]
            
            for element_type in unwanted_elements:
                for element in soup.find_all(element_type):
                    element.decompose()
            
            # Remove by class/id patterns (very aggressive)
            unwanted_selectors = [
                '[class*="footer"]', '[class*="header"]', '[class*="nav"]',
                '[class*="menu"]', '[class*="sidebar"]', '[class*="ad"]',
                '[class*="social"]', '[class*="share"]', '[class*="comment"]',
                '[class*="copyright"]', '[class*="disclaimer"]', '[class*="terms"]',
                '[class*="division"]', '[class*="corp"]', '[class*="dnpa"]',
                '[class*="ethics"]', '[class*="reserved"]'
            ]
            
            for selector in unwanted_selectors:
                for element in soup.select(selector):
                    element.decompose()
            
            # Find main content - try multiple strategies
            content_text = ""
            
            # Strategy 1: Look for article content specifically
            content_selectors = [
                'article .story-content',
                'article .article-content', 
                '.story-body',
                '.article-body',
                '.post-content',
                '.entry-content',
                '[class*="story-text"]',
                '[class*="article-text"]'
            ]
            
            for selector in content_selectors:
                content_area = soup.select_one(selector)
                if content_area:
                    content_text = content_area.get_text(separator=' ', strip=True)
                    break
            
            # Strategy 2: If no specific content area found, look for paragraphs in article
            if not content_text:
                article = soup.find('article')
                if article:
                    paragraphs = article.find_all('p')
                    content_text = ' '.join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20])
            
            # Strategy 3: Last resort - get all paragraphs but filter heavily
            if not content_text:
                all_paragraphs = soup.find_all('p')
                filtered_paragraphs = []
                for p in all_paragraphs:
                    p_text = p.get_text(strip=True)
                    if len(p_text) > 30 and not any(word in p_text.lower() for word in ['copyright', 'division', 'corp', 'reserved', 'ethics']):
                        filtered_paragraphs.append(p_text)
                content_text = ' '.join(filtered_paragraphs[:10])  # Take only first 10 relevant paragraphs
            
            return self.super_clean_content(content_text)
            
        except Exception as e:
            logger.error(f"Divya Bhaskar extraction failed: {e}")
            return f"Failed to extract content from Divya Bhaskar: {str(e)}"
    
    def super_clean_content(self, text: str) -> str:
        """SUPER AGGRESSIVE cleaning specifically for Divya Bhaskar content"""
        if not text:
            return ""
        
        import re
        
        # NUCLEAR OPTION: Remove any text containing these exact phrases
        nuclear_removal_phrases = [
            "Our Divisions Copyright",
            "DB Corp ltd",
            "All Rights Reserved", 
            "DNPA Code of Ethics",
            "This website follows",
            "Our Divisions",
            "Copyright ©",
            "2024-25",
            "2023-24",
            "2025-26"
        ]
        
        # Split into sentences and filter out any sentence containing nuclear phrases
        sentences = re.split(r'[.!?।]', text)
        clean_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 15:  # Skip very short sentences
                continue
                
            # REJECT any sentence containing nuclear phrases
            contains_nuclear = any(phrase.lower() in sentence.lower() for phrase in nuclear_removal_phrases)
            if contains_nuclear:
                logger.info(f"REJECTED sentence: {sentence[:50]}...")
                continue
                
            # Additional word-based filtering
            words = sentence.lower().split()
            bad_word_count = sum(1 for word in words if word in ['copyright', 'corp', 'division', 'reserved', 'ethics', 'dnpa'])
            
            # If more than 20% bad words, reject
            if len(words) > 0 and (bad_word_count / len(words)) > 0.2:
                logger.info(f"REJECTED high bad-word sentence: {sentence[:50]}...")
                continue
                
            clean_sentences.append(sentence)
        
        # Join clean sentences
        result = '. '.join(clean_sentences)
        
        # Final regex cleanup
        result = re.sub(r'Our Divisions.*?Ethics\.?', '', result, flags=re.IGNORECASE | re.DOTALL)
        result = re.sub(r'Copyright.*?Reserved', '', result, flags=re.IGNORECASE | re.DOTALL)
        result = re.sub(r'DB Corp.*?Ethics', '', result, flags=re.IGNORECASE | re.DOTALL)
        
        # Clean up whitespace
        result = re.sub(r'\s+', ' ', result).strip()
        result = re.sub(r'\.{2,}', '.', result)
        
        logger.info(f"Final cleaned content length: {len(result)}")
        return result if len(result) > 50 else "No meaningful content found after aggressive cleaning"
    
    def extract(self, url: str) -> str:
        logger.info(f"Extracting content from URL: {url}")
        
        # SPECIAL HANDLING FOR DIVYA BHASKAR - Use specialized extraction
        if self.is_divya_bhaskar(url):
            logger.info("Detected Divya Bhaskar URL - using specialized extraction")
            return self.extract_divya_bhaskar_content(url)
        
        # For other news sites, use standard extraction
        try:
            from newspaper import Article
            article = Article(url)
            article.download()
            article.parse()
            
            # Use newspaper's text if available and clean it
            if article.text:
                cleaned = self.super_clean_content(article.text)
                return cleaned if cleaned else "No meaningful content extracted"
            
        except Exception as e:
            logger.warning(f"Newspaper extraction failed: {e}, trying BeautifulSoup...")
            
        try:
            import requests
            from bs4 import BeautifulSoup
            response = requests.get(url, timeout=15, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements aggressively
            unwanted_tags = ['script', 'style', 'nav', 'header', 'footer', 'aside', 
                           'form', 'button', 'input', 'select', 'textarea', 'iframe',
                           'advertisement', 'ads', 'social-share', 'comments']
            
            for tag in unwanted_tags:
                for element in soup.find_all(tag):
                    element.decompose()
            
            # Get main content
            main_content = None
            content_selectors = [
                'article', '[class*="story-content"]', '[class*="article-content"]',
                '[class*="post-content"]', '[class*="entry-content"]', 
                '[class*="content-body"]', '[class*="article-body"]',
                'main', '.main-content', '[role="main"]'
            ]
            
            for selector in content_selectors:
                content_area = soup.select_one(selector)
                if content_area:
                    main_content = content_area.get_text(separator=' ', strip=True)
                    break
            
            if not main_content:
                main_content = soup.get_text(separator=' ', strip=True)
            
            # Use super cleaning for all content
            cleaned = self.super_clean_content(main_content)
            logger.info(f"Final content length: {len(cleaned) if cleaned else 0}")
            
            return cleaned[:5000] if cleaned else "No meaningful content found"
            
        except Exception as e2:
            logger.error(f"URL extraction failed: {e2}")
            return f"Extraction failed: {str(e2)}"

# Initialize services
translator = Translator()
summarizer = Summarizer()
extractor = URLExtractor()

# Request/Response models
class TranslateRequest(BaseModel):
    text: str

class SummarizeRequest(BaseModel):
    text: str
    max_length: int = 150

class ProcessRequest(BaseModel):
    content: str
    inputType: str = "text"
    translate: bool = True
    summarize: bool = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Gujarati News Translator API...")
    logger.info("Initializing ML models...")
    yield
    logger.info("Shutting down...")

def find_free_port(start_port=8000, max_attempts=10):
    """Find a free port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except OSError:
                continue
    return start_port  # fallback

# Create app
app = FastAPI(
    title="Gujarati News Translator API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Gujarati Translator API", "status": "active"}

@app.post("/translate")
async def translate_text(request: TranslateRequest):
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        translated = translator.translate(request.text)
        return {
            "original_text": request.text,
            "translated_text": translated,
            "source_lang": "gu",
            "target_lang": "en"
        }
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
async def summarize_text(request: SummarizeRequest):
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        summary = summarizer.summarize(request.text, request.max_length)
        return {
            "original_text": request.text,
            "summary": summary,
            "compression_ratio": len(summary) / len(request.text) if request.text else 0
        }
    except Exception as e:
        logger.error(f"Summarization error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process")
async def process_content(request: ProcessRequest):
    try:
        text = request.content
        if request.inputType == "url":
            logger.info(f"Extracting content from URL: {request.content}")
            text = extractor.extract(request.content)
            logger.info(f"Extracted text length: {len(text)}")
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="No content to process")
        
        result = {"original_text": text}
        
        if request.translate:
            logger.info("Translating content...")
            result["translated_text"] = translator.translate(text)
        
        if request.summarize:
            logger.info("Summarizing content...")
            text_to_summarize = result.get("translated_text", text)
            result["summary"] = summarizer.summarize(text_to_summarize)
        
        return result
    except Exception as e:
        logger.error(f"Process error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = find_free_port()
    print(f"Starting server on http://127.0.0.1:{port}")
    uvicorn.run(app, host="127.0.0.1", port=port)
