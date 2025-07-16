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
