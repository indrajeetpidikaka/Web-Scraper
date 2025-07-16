from bs4 import BeautifulSoup
import logging
from urllib.parse import urlparse, urljoin
import re

class Parser:
    def parse(self, html_content, url):
        """Parse content from any website"""
        if not html_content:
            logging.error(f"Parser received no HTML content for URL: {url}")
            return None
        
        try:
            soup = BeautifulSoup(html_content, 'lxml')
            domain = urlparse(url).netloc
            
            # Extract title
            title = soup.title.string.strip() if soup.title else ""
            
            # Extract main content text
            content = self._extract_main_content(soup, domain)
            
            # Extract all links and make them absolute
            links = self._extract_links(soup, url)
            
            # For IMDb top 250 movies
            movies = []
            if 'imdb.com/chart/top' in url:
                movies = self._extract_imdb_movies(soup)
            
            return {
                "domain": domain,
                "title": title,
                "content": content,
                "links": links,
                "movies": movies  # Only populated for IMDb top chart
            }
        except Exception as e:
            logging.error(f"Error parsing content from {url}: {e}", exc_info=True)
            return None

    def _extract_imdb_movies(self, soup):
        """Extracts movie data from IMDb top 250 chart page"""
        try:
            movies = []
            movie_list = soup.select('.ipc-metadata-list-summary-item')
            
            if not movie_list:
                # Try old layout as fallback
                movie_list = soup.select('.lister-list tr')
                
            for movie in movie_list:
                # New layout extraction
                title_elem = movie.select_one('.ipc-title__text')
                if title_elem:
                    title_text = title_elem.get_text(strip=True)
                    # Remove ranking number from title
                    if '. ' in title_text:
                        title = title_text.split('. ', 1)[1]
                    else:
                        title = title_text
                else:
                    # Old layout fallback
                    title_elem = movie.select_one('.titleColumn a')
                    title = title_elem.get_text(strip=True) if title_elem else "Unknown"
                
                # Extract year
                year_elem = movie.select_one('.cli-title-metadata-item')
                if not year_elem:
                    year_elem = movie.select_one('.titleColumn span')
                year = year_elem.get_text(strip=True).strip('()') if year_elem else "N/A"
                
                # Extract rating
                rating_elem = movie.select_one('.ipc-rating-star')
                if not rating_elem:
                    rating_elem = movie.select_one('.imdbRating strong')
                rating = rating_elem.get_text(strip=True) if rating_elem else "N/A"
                
                # Extract duration
                duration_elem = None
                if len(movie.select('.cli-title-metadata-item')) > 1:
                    duration_elem = movie.select('.cli-title-metadata-item')[1]
                duration = duration_elem.get_text(strip=True) if duration_elem else "N/A"
                
                # Extract genre
                genre_elem = movie.select_one('.ipc-chip-list')
                genre = genre_elem.get_text(strip=True) if genre_elem else "N/A"
                
                movies.append({
                    'title': title,
                    'year': year,
                    'genre': genre,
                    'rating': rating,
                    'duration': duration
                })
            
            logging.info(f"Extracted {len(movies)} IMDb movies")
            return movies
        except Exception as e:
            logging.error(f"IMDB movie extraction failed: {e}")
            return []

    def _extract_main_content(self, soup, domain):
        """Extract main content using domain-specific strategies"""
        # Domain-specific extraction
        if 'imdb.com' in domain:
            return self._extract_imdb_content(soup)
        if 'wikipedia.org' in domain:
            return self._extract_wikipedia_content(soup)
        if 'github.com' in domain:
            return self._extract_github_content(soup)
        if 'unsplash.com' in domain:
            return self._extract_unsplash_content(soup)
        
        # Generic content extraction
        return self._extract_generic_content(soup)

    def _extract_imdb_content(self, soup):
        """For IMDb"""
        try:
            # Try to extract top movie data
            content_lines = []
            movie_list = soup.select('.ipc-metadata-list-summary-item') or soup.select('.lister-list tr')
            
            if movie_list:
                for movie in movie_list[:10]:  # Get top 10 movies
                    title_elem = movie.select_one('.ipc-title__text') or movie.select_one('.titleColumn a')
                    year_elem = movie.select_one('.cli-title-metadata-item') or movie.select_one('.titleColumn span')
                    rating_elem = movie.select_one('.ipc-rating-star') or movie.select_one('.imdbRating strong')
                    
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        if '. ' in title:
                            title = title.split('. ', 1)[1]
                    else:
                        title = "Unknown"
                    
                    year = year_elem.get_text(strip=True).strip('()') if year_elem else "N/A"
                    rating = rating_elem.get_text(strip=True) if rating_elem else "N/A"
                    
                    content_lines.append(f"{title} ({year}) - Rating: {rating}")
                
                if content_lines:
                    return "\n".join(content_lines)
            
            # Fallback to generic content extraction
            return self._extract_generic_content(soup)
        except Exception as e:
            logging.error(f"IMDB content extraction failed: {e}")
            return self._extract_generic_content(soup)

    def _extract_wikipedia_content(self, soup):
        """For Wikipedia"""
        try:
            content = []
            # Extract category links
            categories = [a.get_text(strip=True) for a in soup.select('#mw-subcategories a')]
            if categories:
                content.append("Categories: " + ", ".join(categories))
            
            # Extract algorithm names
            algorithms = [li.get_text(strip=True) for li in soup.select('#mw-pages li')]
            if algorithms:
                content.append("Algorithms: " + ", ".join(algorithms))
            
            return "\n".join(content) if content else self._extract_generic_content(soup)
        except:
            return self._extract_generic_content(soup)

    def _extract_github_content(self, soup):
        """For GitHub"""
        try:
            content = []
            # Extract topic titles
            topics = [h3.get_text(strip=True) for h3 in soup.select('.topic-tag')]
            if topics:
                content.append("Topics: " + ", ".join(topics))
            
            # Extract repository names
            repos = [a.get_text(strip=True) for a in soup.select('.text-bold.wb-break-word')]
            if repos:
                content.append("Repositories: " + ", ".join(repos))
            
            return "\n".join(content) if content else self._extract_generic_content(soup)
        except:
            return self._extract_generic_content(soup)

    def _extract_unsplash_content(self, soup):
        """For Unsplash"""
        try:
            content = []
            # Extract image titles
            titles = [img.get('alt', '') for img in soup.select('img[alt]')]
            if titles:
                content.append("Images: " + ", ".join(titles))
            
            return "\n".join(content) if content else self._extract_generic_content(soup)
        except:
            return self._extract_generic_content(soup)

    def _extract_generic_content(self, soup):
        """For general sites"""
        try:
            # Try to find common content containers
            content_containers = [
                soup.find('main'),
                soup.find('article'),
                soup.find('div', class_='content'),
                soup.find('div', class_='main-content'),
                soup.find('div', id='content'),
                soup.body  # Fallback to entire body
            ]
            
            # Use the first valid container found
            container = next((c for c in content_containers if c), None)
            
            if container:
                # Clean up by removing unwanted elements
                for element in container(['script', 'style', 'header', 'footer', 'nav', 'aside']):
                    element.decompose()
                
                return container.get_text(separator=' ', strip=True)
            return ""
        except:
            return ""

    def _extract_links(self, soup, base_url):
        """Extract all links and convert to absolute URLs"""
        links = set()
        for link in soup.find_all('a', href=True):
            href = link['href'].strip()
            if href and not href.startswith(('javascript:', 'mailto:', 'tel:')):
                absolute_url = urljoin(base_url, href)
                # Filter out non-HTTP links and common tracking links
                if absolute_url.startswith('http') and not any(x in absolute_url for x in ['/ad/', '/track/', '/click?']):
                    links.add(absolute_url)
        return list(links)
