from bs4 import BeautifulSoup
from scraper import ImageScraper
from model import Image
from typing import List, Dict, Any
import logging
from datetime import datetime
from playwright.sync_api import TimeoutError 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PinterestImageScraper(ImageScraper):
    
    def __init__(self) -> None:
        website = "pinterest"
        search_url = "search/pins/?q="
        selector = f'[data-test-id=pin-closeup-image]'
        try:
            super().__init__(website, search_url, None, selector)
        except Exception as e:
            logger.error(f"Error initializing PinterestScraper: {e}")
            raise


    def extract_links(self, html: BeautifulSoup) -> List[str]:
        try:
            links = []
            div_links = html.select('a[href^="/pin/"]') 
            pins = [div_link.get('href') for div_link in div_links]
            links = [pin for pin in pins if not pin in links]
            img_links = [f"https://pinterest.com{link}" for link in links]
            
            return img_links
        except Exception as e:
            logger.error(f"Error extracting Pinterest links: {e}")
            raise

    

    def extract_img_source(self, html):
        try:
            image_div = html.find('div', attrs={"data-test-id": "pin-closeup-image"})
            image_src = image_div.img.get('src')
            alt = image_div.img.get('alt')

            for pattern in ['/236x/', '/564x/']:
                image_src.replace(pattern, '/736x/')
            return {'source': image_src, 'alt': alt}  
        except Exception as e:
            logger.error(f"Error extracting image source: {e}")
            raise

    

    def extract_img_author(self, html) -> str:
        try:
            creator_div = html.find('div', attrs={"data-test-id": "official-user-attribution"})
            if creator_div:
                user_tag = f"@{creator_div.a['href'].replace('/', '')}"
            else:
                user_tag = "None"
            return user_tag
        except Exception as e:
            logger.error(f"Error extracting image author: {e}")
            raise
    

    def fetch_img_details(self, link: str) -> Image:
        try:
            html = self.parse_search(link, self.selector)
            img_source = self.extract_img_source(html)
            author = self.extract_img_author(html)
            img_format = img_source['source'].split(".")[-1]
            if '?' in img_format:
                img_format = img_format.split("?")[0]
            image = Image('None', link, img_source['source'], 'Pinterest', author, img_source['alt'], img_format, datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            
            return image
        except Exception as e:
            logger.error(f"Error fetching image details {link}: {e}")
            raise

    

if __name__ == "__main__":
    pin_scraper = PinterestImageScraper()
    research_page = pin_scraper.parse_search("https://pinterest.com/search/pins/?q=gojo", "img")
    links = pin_scraper.extract_links(research_page)
    # print(links)
    imgs = pin_scraper.fetch_all_images(links)
    print(imgs)