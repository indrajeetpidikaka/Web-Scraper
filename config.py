"""
⚠️ DISCLAIMER:
This web scraping tool is intended for educational purposes only. Users are responsible for:
1. Complying with target website terms of service
2. Respecting robots.txt directives
3. Adhering to all applicable laws (copyright, data protection, CFAA, etc.)
4. Avoiding scraping of private or sensitive information

Misuse of this software may result in legal consequences. The developers assume no liability for improper use.
"""
import os
import random

TARGET_URLS = [
    # "https://unsplash.com/", 
    # "https://en.wikipedia.org/wiki/Category:Machine_learning_algorithms", 
    # "https://github.com/topics/machine-learning", 
    # "https://www.imdb.com/chart/top", 
]

DATABASE_CONFIG = {
    "type": "sqlite",
    "path": "data/scraped_data.db"
}

# Define request timeout and max retries
REQUEST_TIMEOUT = 30
MAX_RETRIES = 5

# Selenium WebDriver settings
SELENIUM_HEADLESS = False # Run browser in headless mode
SELENIUM_WAIT_TIMEOUT = 30 # Max time to wait for page elements to load

PROXY_LIST = []
