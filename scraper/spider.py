"""
⚠️ DISCLAIMER:
This web scraping tool is intended for educational purposes only. Users are responsible for:
1. Complying with target website terms of service
2. Respecting robots.txt directives
3. Adhering to all applicable laws (copyright, data protection, CFAA, etc.)
4. Avoiding scraping of private or sensitive information

Misuse of this software may result in legal consequences. The developers assume no liability for improper use.
"""
import logging
import time
import random
from urllib.parse import urlparse
from .request_handler import RequestHandler
from .parser import Parser
from utils.database import Database

class Spider:
    def __init__(self, urls, db_config):
        self.urls = urls
        self.db_config = db_config
        self.request_handler = RequestHandler()
        self.parser = Parser()
        self.database = Database()
        logging.info("Web scraper initialized")

    def run(self):
        logging.info(f"Starting scraping of {len(self.urls)} URLs")
        
        # Shuffle URLs to avoid predictable patterns
        random.shuffle(self.urls)
        
        for i, url in enumerate(self.urls):
            try:
                logging.info(f"Processing URL {i+1}/{len(self.urls)}: {url}")
                
                # Fetch page content
                content = self.request_handler.fetch_page(url)
                if not content:
                    self.database.log_request(url, "failed", 0)
                    continue
                
                # Parse content
                parsed_data = self.parser.parse(content, url)
                if not parsed_data:
                    self.database.log_request(url, "parse_failed", len(content))
                    continue
                
                # Save to database - generic content
                success = self.database.save_content(
                    url=url,
                    domain=parsed_data["domain"],
                    title=parsed_data["title"],
                    content=parsed_data["content"],
                    links=parsed_data["links"]
                )
                
                # For IMDb top 250 movies
                if 'imdb.com/chart/top' in url and parsed_data["movies"]:
                    self.database.save_imdb_movies(parsed_data["movies"], url)
                
                if success:
                    self.database.log_request(url, "success", len(content))
                else:
                    self.database.log_request(url, "save_failed", len(content))
                
            except Exception as e:
                logging.error(f"Error processing {url}: {e}", exc_info=True)
                self.database.log_request(url, "error", 0)
            finally:
                # Add random delay between requests (2-5 seconds)
                delay = random.uniform(2, 5)
                logging.info(f"Waiting {delay:.1f} seconds before next request")
                time.sleep(delay)
        
        logging.info("Scraping completed")
        self.request_handler.close()
        self.database.close()
