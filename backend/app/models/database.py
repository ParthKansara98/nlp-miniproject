import sqlite3
from datetime import datetime
import json
from typing import List, Dict, Any
import os

class Database:
    def __init__(self, db_path: str = "app_data.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create translations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS translations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_text TEXT NOT NULL,
                    translated_text TEXT NOT NULL,
                    source_lang TEXT NOT NULL,
                    target_lang TEXT NOT NULL,
                    processing_time REAL NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    url_source TEXT,
                    text_length INTEGER
                )
            ''')
            
            # Create summaries table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS summaries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_text TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    compression_ratio REAL NOT NULL,
                    processing_time REAL NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    original_length INTEGER,
                    summary_length INTEGER
                )
            ''')
            
            # Create app_stats table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS app_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    metric_value TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def log_translation(self, original_text: str, translated_text: str, 
                       source_lang: str, target_lang: str, processing_time: float,
                       url_source: str = None):
        """Log a translation to the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO translations 
                (original_text, translated_text, source_lang, target_lang, 
                 processing_time, url_source, text_length)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (original_text, translated_text, source_lang, target_lang, 
                  processing_time, url_source, len(original_text)))
            conn.commit()
    
    def log_summary(self, original_text: str, summary: str, 
                   compression_ratio: float, processing_time: float):
        """Log a summarization to the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO summaries 
                (original_text, summary, compression_ratio, processing_time,
                 original_length, summary_length)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (original_text, summary, compression_ratio, processing_time,
                  len(original_text), len(summary)))
            conn.commit()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get application statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total translations
            cursor.execute("SELECT COUNT(*) FROM translations")
            total_translations = cursor.fetchone()[0]
            
            # Total summaries
            cursor.execute("SELECT COUNT(*) FROM summaries")
            total_summaries = cursor.fetchone()[0]
            
            # Average summary length
            cursor.execute("SELECT AVG(summary_length) FROM summaries")
            avg_summary_length = cursor.fetchone()[0] or 0
            
            # Average processing time for translations
            cursor.execute("SELECT AVG(processing_time) FROM translations")
            avg_translation_time = cursor.fetchone()[0] or 0
            
            # Average processing time for summaries
            cursor.execute("SELECT AVG(processing_time) FROM summaries")
            avg_summary_time = cursor.fetchone()[0] or 0
            
            # Most common URL sources
            cursor.execute('''
                SELECT url_source, COUNT(*) as count 
                FROM translations 
                WHERE url_source IS NOT NULL 
                GROUP BY url_source 
                ORDER BY count DESC 
                LIMIT 5
            ''')
            common_sources = [row[0] for row in cursor.fetchall() if row[0]]
            
            return {
                "total_articles_processed": total_translations,
                "total_translations": total_translations,
                "total_summaries": total_summaries,
                "average_summary_length": round(avg_summary_length, 2),
                "average_processing_time": round((avg_translation_time + avg_summary_time) / 2, 3),
                "most_common_sources": common_sources
            }
    
    def get_recent_activity(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent translations and summaries"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get recent translations
            cursor.execute('''
                SELECT 'translation' as type, original_text, translated_text, 
                       processing_time, timestamp, url_source
                FROM translations 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "type": row[0],
                    "original_text": row[1][:100] + "..." if len(row[1]) > 100 else row[1],
                    "processed_text": row[2][:100] + "..." if len(row[2]) > 100 else row[2],
                    "processing_time": row[3],
                    "timestamp": row[4],
                    "url_source": row[5]
                })
            
            return results

# Global database instance
db = Database()