"""
⚠️ DISCLAIMER:
This web scraping tool is intended for educational purposes only. Users are responsible for:
1. Complying with target website terms of service
2. Respecting robots.txt directives
3. Adhering to all applicable laws (copyright, data protection, CFAA, etc.)
4. Avoiding scraping of private or sensitive information

Misuse of this software may result in legal consequences. The developers assume no liability for improper use.
"""
import random
import logging
import requests
from config import PROXY_LIST

class ProxyRotator:
    def __init__(self):
        # Validate proxies upon initialization
        self.proxies = self._validate_proxies(PROXY_LIST)
        if not self.proxies:
            logging.warning("No valid proxies available. Using direct connections")
            
    def _validate_proxies(self, proxies):
        """
        Checks if the provided proxies are working by attempting to connect to a test URL.
        Returns a list of valid proxies.
        """
        valid_proxies = []
        for proxy in proxies:
            try:
                test_url = "https://www.google.com" # A reliable URL to test proxy connectivity
                response = requests.get(
                    test_url, 
                    proxies={"http": proxy, "https": proxy}, # Specify proxy for both http and https
                    timeout=5 # Short timeout for quick validation
                )
                if response.status_code == 200:
                    valid_proxies.append(proxy)
                    logging.info(f"Proxy validated: {proxy}")
                else:
                    logging.warning(f"Proxy {proxy} returned status code {response.status_code}")
            except requests.exceptions.RequestException as e:
                logging.warning(f"Proxy failed to connect: {proxy} - {e}")
            except Exception as e:
                logging.warning(f"An unexpected error occurred during proxy validation for {proxy}: {e}")
                
        # If no proxies are valid, return the original list so the scraper can still attempt direct connections
        # This prevents the scraper from completely failing if proxies are misconfigured or unavailable.
        return valid_proxies or proxies

    def get_proxy(self):
        """
        Returns a random proxy from the list of validated proxies.
        Returns None if no proxies are available.
        """
        if not self.proxies:
            return None
        return random.choice(self.proxies)
