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
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import MAX_RETRIES, SELENIUM_HEADLESS, SELENIUM_WAIT_TIMEOUT
from utils.user_agent_manager import UserAgentManager

class RequestHandler:
    def __init__(self):
        self.user_agent_manager = UserAgentManager()
        self.driver = self._init_selenium()

    def _init_selenium(self):
        """Initializes an undetected-chromedriver"""
        try:
            options = uc.ChromeOptions()
            
            # Get a random user agent
            user_agent = self.user_agent_manager.get_user_agent()
            options.add_argument(f'user-agent={user_agent}')
            logging.info(f"Using user agent: {user_agent}")
            
            if SELENIUM_HEADLESS:
                options.add_argument("--headless=new")
            
            #Set of essential options
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-notifications")
            
            logging.info("Initializing undetected-chromedriver...")
            driver = uc.Chrome(
                options=options, 
                use_subprocess=True,
                headless=SELENIUM_HEADLESS
            )
            
            # Set window size to appear natural
            driver.set_window_size(1366, 768)
            
            
            # # Or Randomize window size by ±10–20 pixels
            # default_width = 1366
            # default_height = 768
            # width_variation = random.randint(-20, 20)
            # height_variation = random.randint(-20, 20)

            # window_width = default_width + width_variation
            # window_height = default_height + height_variation

            # driver.set_window_size(window_width, window_height)
            
            
            # Execute stealth scripts to hide automation
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})
            
            logging.info("Undetected-chromedriver initialized successfully")
            return driver
        except Exception as e:
            logging.error(f"Failed to initialize undetected-chromedriver: {e}", exc_info=True)
            return None

    def fetch_page(self, url):
        """Fetches page content using Selenium"""
        if not self.driver:
            logging.error("Undetected-chromedriver is not available")
            return None

        domain = url.split('//')[-1].split('/')[0]  # Extract domain for special handling
        for attempt in range(MAX_RETRIES):
            try:
                logging.info(f"Fetching {url} (attempt {attempt+1}/{MAX_RETRIES})")
                
                # Navigate to URL with randomized timing
                time.sleep(random.uniform(1, 3))
                self.driver.get(url)
                
                # Domain-specific waiting strategies
                if 'imdb.com' in domain:
                    # try multiple selectors
                    try:
                        WebDriverWait(self.driver, SELENIUM_WAIT_TIMEOUT * 2).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '.ipc-metadata-list')))
                    except TimeoutException:
                        # Fallback to other selectors
                        WebDriverWait(self.driver, SELENIUM_WAIT_TIMEOUT).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '.lister-list, [data-testid="chart-layout-main-column"]')))
                else:
                    # Generic waiting strategy
                    WebDriverWait(self.driver, SELENIUM_WAIT_TIMEOUT).until(
                        EC.presence_of_element_located((By.TAG_NAME, 'body')))
                    WebDriverWait(self.driver, SELENIUM_WAIT_TIMEOUT).until(
                        lambda driver: driver.execute_script('return document.readyState') == 'complete')
                
                # Scroll to trigger lazy-loaded content
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)  # Allow time for content to load
                self.driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(0.5)
                
                content = self.driver.page_source
                if content and len(content) > 1000:
                    logging.info(f"Successfully fetched content from {url} ({len(content)} bytes)")
                    return content
                
                logging.warning(f"Fetched page but content is small: {len(content)} bytes")
                time.sleep(3)  # Longer delay before retry
            except Exception as e:
                logging.warning(f"Attempt {attempt+1} failed: {e}")
                # Take screenshot for debugging
                try:
                    domain_clean = domain.replace('.', '_')
                    self.driver.save_screenshot(f"logs/failed_{domain_clean}_{attempt+1}.png")
                    logging.info("Saved screenshot for debugging")
                except:
                    pass
                time.sleep(5)  # Longer delay on failure
        
        logging.error(f"All attempts failed for {url}")
        return None

    def close(self):
        if self.driver:
            self.driver.quit()
            logging.info("Undetected-chromedriver closed")
