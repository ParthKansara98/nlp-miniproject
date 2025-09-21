from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "gu"
    target_lang: str = "en"

class SummarizationRequest(BaseModel):
    text: str
    max_length: Optional[int] = 150
    min_length: Optional[int] = 50

class ProcessRequest(BaseModel):
    inputType: str  # "url" or "text"  
    content: str
    translate: Optional[bool] = True
    summarize: Optional[bool] = True

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_lang: str
    target_lang: str
    confidence: Optional[float] = None

class SummarizationResponse(BaseModel):
    original_text: str
    summary: str
    compression_ratio: float

class ProcessResponse(BaseModel):
    original_text: str
    translated_text: Optional[str] = None
    summary: Optional[str] = None
    url_extracted: Optional[bool] = False
    processing_time: float
    timestamp: datetime

class StatsResponse(BaseModel):
    total_articles_processed: int
    total_translations: int
    total_summaries: int
    average_summary_length: float
    average_processing_time: float
    most_common_sources: List[str]

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None
    code: int