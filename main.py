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
import sys
import time
import os
from scraper.spider import Spider
from utils.logger import setup_logger
from config import TARGET_URLS, DATABASE_CONFIG

def main():
    setup_logger(level=logging.INFO)
    logging.info("Starting web scraper")
    
    try:
        os.makedirs("data", exist_ok=True)
        
        start_time = time.time()
        
        spider = Spider(
            urls=TARGET_URLS,
            db_config=DATABASE_CONFIG
        )
        
        spider.run()
        duration = time.time() - start_time
        
        logging.info(f"Scraping completed in {duration:.2f} seconds")
        
        db_path = DATABASE_CONFIG["path"]
        logging.info(f"Data stored in database: {db_path}")

    except KeyboardInterrupt:
        logging.warning("Scraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        logging.critical(f"Critical failure: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
