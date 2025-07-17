## README.md

```markdown

## ⚠️ Disclaimer: Ethical and Legal Considerations

This web scraping tool is intended for **educational purposes only**. Users must comply with all applicable laws and regulations regarding web scraping, including:

1. **Respect for Website Terms of Service**:
   - Always review a website's Terms of Service (ToS) before scraping
   - Many websites explicitly prohibit scraping in their ToS
   - Violating ToS may result in legal action or permanent bans

2. **Adherence to robots.txt**:
   - The scraper automatically checks robots.txt files
   - Avoid scraping disallowed paths and resources
   - Respect crawl-delay directives

3. **Legal Compliance**:
   - Scraping certain types of data may violate:
     - Copyright laws
     - Data protection regulations (GDPR, CCPA, etc.)
     - Computer Fraud and Abuse Act (CFAA) in the US
   - Never scrape personally identifiable information (PII)
   - Avoid scraping financial data without explicit permission

4. **Ethical Considerations**:
   - Do not overload servers with excessive requests
   - Maintain reasonable request rates (add delays between requests)
   - Scrape only publicly available data
   - Consider the privacy implications of collected data

5. **Prohibited Content**:
   - Do not scrape:
     - Copyrighted content without permission
     - Private user data
     - Login-protected content
     - Government/military websites (.gov, .mil domains)
     - Sites containing illegal content

**Important**: The developers of this software are not responsible for:
- Any misuse of this tool
- Legal consequences resulting from improper use
- Damage caused to target websites
- Violations of terms of service or privacy laws

Use this tool responsibly and at your own risk. When in doubt, consult with legal professionals before scraping any website.

# Web Scraper

![Web Scraping](https://img.shields.io/badge/Web-Scraping-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-green)
![Selenium](https://img.shields.io/badge/Selenium-4.19.0-orange)
![Undetected ChromeDriver](https://img.shields.io/badge/Undetected_ChromeDriver-3.5.7-brightgreen)

A sophisticated web scraping framework designed to extract data from various websites while avoiding bot detection. The scraper uses techniques to mimic human behavior and bypass anti-scraping measures.

## Features

- **Stealth Browsing**: Uses undetected-chromedriver to avoid bot detection
- **Intelligent Parsing**: Domain-specific extraction logic for popular sites
- **Database Storage**: SQLite database for structured data storage
- **Rotating User Agents**: Randomizes user agents to prevent fingerprinting
- **Proxy Support**: Built-in proxy rotation capabilities
- **Detailed Logging**: Comprehensive logging with screenshots on failure
- **IMDB Specialization**: Specialized extraction for IMDB top 250 movies, as of now the Genre column might show missing data.

## Supported Websites

The scraper currently supports:
- IMDb (Top 250 movies with detailed metadata)
- Wikipedia (Category pages)
- GitHub (Topic pages)
- Unsplash (Image metadata)
- General website scraping

## Project Structure
```bash
web_scraper/
├── scraper/
│   ├── __init__.py
│   ├── parser.py
│   ├── request_handler.py
│   ├── spider.py
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   ├── database.py
│   ├── proxy_rotator.py
│   ├── user_agent_manager.py
├── data/
│   └── scraped_data.db  # SQLite database file
├── logs/
│   ├── scraper.log
│   └── failed_screenshots/
├── requirements.txt
├── main.py
├── config.py
└── README.md
```

## Installation

1. Clone the repository

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Chrome browser (if not already installed)

## Configuration

Edit the `config.py` file to customize the scraper:

```python
# config.py

# Target URLs to scrape
TARGET_URLS = [
    "your_website.com"
]

# Database configuration
DATABASE_CONFIG = {
    "type": "sqlite",
    "path": "data/scraped_data.db"
}

# Proxy settings (optional)
PROXY_LIST = [
    # "http://user:pass@host:port",
    # "http://host:port"
]

# User agent settings
USER_AGENT_LIST = [
    # Add custom user agents if needed
]
```

## Usage

Run the scraper:
```bash
python main.py
```

### Command Line Options
```bash
python main.py [--headless] [--urls url1 url2 ...] [--output output.db]
```

- `--headless`: Run browser in headless mode
- `--urls`: Override URLs from config.py
- `--output`: Specify alternative database path

## Database Schema

The scraper uses an SQLite database with the following tables:

### `scraped_content` (General Websites)
| Column    | Type         | Description                     |
|-----------|--------------|---------------------------------|
| id        | INTEGER      | Primary key                     |
| url       | TEXT         | Source URL                      |
| domain    | TEXT         | Website domain                  |
| title     | TEXT         | Page title                      |
| content   | TEXT         | Main content text               |
| links     | TEXT         | JSON array of discovered links  |
| timestamp | DATETIME     | Scrape timestamp                |

### `imdb_movies` (IMDb Top 250)
| Column    | Type         | Description                     |
|-----------|--------------|---------------------------------|
| id        | INTEGER      | Primary key                     |
| rank      | INTEGER      | Movie ranking (1-250)           |
| title     | TEXT         | Movie title                     |
| year      | TEXT         | Release year                    |
| genre     | TEXT         | Genres                          |
| rating    | REAL         | IMDb rating                     |
| duration  | TEXT         | Movie duration                  |
| url       | TEXT         | Source URL                      |
| timestamp | DATETIME     | Scrape timestamp                |

### `scraping_log`
| Column         | Type     | Description                     |
|----------------|----------|---------------------------------|
| id             | INTEGER  | Primary key                     |
| url            | TEXT     | Requested URL                   |
| status         | TEXT     | Success/fail status             |
| bytes          | INTEGER  | Response size in bytes          |
| timestamp      | DATETIME | Request timestamp               |

## Features

### Custom Parsers
To add support for a new website:
1. Create a new method in `parser.py` following the naming convention `_extract_{domain}_content()`
2. Add domain detection logic in the `_extract_main_content()` method
3. Implement specialized data extraction in your new method

### Proxy Rotation
1. Add proxies to `PROXY_LIST` in config.py
2. The proxy rotator will automatically validate and rotate proxies
3. Failed proxies are automatically removed from rotation

### Custom User Agents
1. Add user agents to `USER_AGENT_LIST` in config.py
2. The user agent manager will rotate between custom and generated agents
3. Set rotation frequency in the user_agent_manager.py file

## Troubleshooting

### Common Issues
1. **ChromeDriver version mismatch**:
   - Make sure you have the latest Chrome browser installed
   - Run `undetected-chromedriver install` to install matching driver

2. **Bot detection**:
   - Try increasing delays between requests
   - Use residential proxies
   - Rotate user agents more frequently

3. **Element not found errors**:
   - Check if website structure has changed
   - Update CSS selectors in parser.py
   - Increase SELENIUM_WAIT_TIMEOUT in config.py

### Viewing Logs
Logs are stored in `logs/scraper.log` with detailed information about each scraping operation. Failed requests generate screenshots in `logs/failed_screenshots/`.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch 
3. Commit your changes 
4. Push to the branch 
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by Scrapy, BeautifulSoup, and Selenium projects
- Special thanks to the undetected-chromedriver developers
- Thanks to all contributors who helped improve this project
```

## Project Overview

This web scraping project is designed to be a robust, production-ready framework for extracting data from various websites. Key components include:

### Core Components
1. **Spider** (`spider.py`): 
   - Orchestrates the scraping process
   - Manages URL queue and execution flow
   - Implements politeness policies (delays, retries)

2. **Request Handler** (`request_handler.py`):
   - Uses undetected-chromedriver for stealth browsing
   - Implements advanced bot avoidance techniques
   - Handles page navigation and content retrieval

3. **Parser** (`parser.py`):
   - Extracts structured data from HTML
   - Implements domain-specific extraction logic
   - Handles both general and specialized content

4. **Database** (`database.py`):
   - Stores scraped data in SQLite
   - Maintains different schemas for different content types
   - Logs scraping activities

### Utility Modules
1. **Logger** (`logger.py`):
   - Configures advanced logging
   - Rotates log files to prevent oversized files
   - Captures detailed debugging information

2. **User Agent Manager** (`user_agent_manager.py`):
   - Rotates between user agents
   - Balances between custom and generated agents
   - Helps avoid browser fingerprinting

3. **Proxy Rotator** (`proxy_rotator.py`):
   - Validates and rotates proxies
   - Automatically removes non-working proxies
   - Ensures continuous scraping operations

### Key Features
- **Anti-Detection Techniques**:
  - Randomized mouse movements
  - Human-like typing patterns
  - Browser fingerprint spoofing
  - Headless browser detection bypass

- **Error Handling**:
  - Automatic retries for failed requests
  - Screenshots on failure
  - Comprehensive error logging

- **Scalability**:
  - Modular design for easy extension
  - Support for distributed scraping
  - Database optimization for large datasets

### Best Practices Implemented
1. **Respectful Scraping**:
   - Adheres to robots.txt
   - Implements crawl delays
   - Respects website terms of service

2. **Data Quality**:
   - Data validation before storage
   - Deduplication of records
   - Schema enforcement

3. **Maintainability**:
   - Clean, modular code
   - Comprehensive documentation
   - Config-driven behavior"# Web-Scraper" 
