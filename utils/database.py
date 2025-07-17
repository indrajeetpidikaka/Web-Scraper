"""
⚠️ DISCLAIMER:
This web scraping tool is intended for educational purposes only. Users are responsible for:
1. Complying with target website terms of service
2. Respecting robots.txt directives
3. Adhering to all applicable laws (copyright, data protection, CFAA, etc.)
4. Avoiding scraping of private or sensitive information

Misuse of this software may result in legal consequences. The developers assume no liability for improper use.
"""
import sqlite3
import logging
import os
import json
from config import DATABASE_CONFIG

class Database:
    def __init__(self):
        self.db_path = DATABASE_CONFIG["path"]
        self.connection = None
        self.cursor = None
        self._initialize_database()

    def _initialize_database(self):
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            
            # Table for storing scraped content
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS scraped_content (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    title TEXT,
                    content TEXT,
                    links TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table for top 250 IMDb movies
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS imdb_movies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rank INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    year TEXT,
                    genre TEXT,
                    rating REAL,
                    duration TEXT,
                    url TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table for logging requests
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS scraping_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    status TEXT NOT NULL,
                    bytes INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.connection.commit()
            logging.info("Database initialized.")
        except Exception as e:
            logging.error(f"Database initialization failed: {e}", exc_info=True)
            raise

    def save_content(self, url, domain, title, content, links):
        """Saves scraped content to the database"""
        try:
            # Serialize links list to JSON string
            links_json = json.dumps(links)
            
            self.cursor.execute(
                """INSERT INTO scraped_content 
                (url, domain, title, content, links) 
                VALUES (?, ?, ?, ?, ?)""",
                (url, domain, title, content, links_json)
            )
            self.connection.commit()
            logging.info(f"Saved content from {domain}")
            return True
        except Exception as e:
            logging.error(f"Failed to save content: {e}", exc_info=True)
            self.connection.rollback()
            return False

    def save_imdb_movies(self, movies, url):
        """Saves IMDb movies data to the database"""
        try:
            for rank, movie in enumerate(movies, 1):
                self.cursor.execute(
                    """INSERT INTO imdb_movies 
                    (rank, title, year, genre, rating, duration, url)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (rank, movie['title'], movie['year'], 
                     movie['genre'], movie['rating'], 
                     movie['duration'], url)
                )
            self.connection.commit()
            logging.info(f"Saved {len(movies)} IMDb movies")
            return True
        except Exception as e:
            logging.error(f"Failed to save IMDb movies: {e}", exc_info=True)
            self.connection.rollback()
            return False

    def log_request(self, url, status, bytes_transferred):
        try:
            self.cursor.execute(
                "INSERT INTO scraping_log (url, status, bytes) VALUES (?, ?, ?)",
                (url, status, bytes_transferred)
            )
            self.connection.commit()
        except Exception as e:
            logging.error(f"Failed to log request: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
            logging.info("Database connection closed")
