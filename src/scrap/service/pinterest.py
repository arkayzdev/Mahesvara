from bs4 import BeautifulSoup
from scraper import ImageScraper
from model import Image
from tools.logger import logger
from typing import List, Dict, Any


class PinterestImageScraper(ImageScraper):
    
    def __init__(self) -> None:
        website = "pinterest"
        search_url = "search/pins/?q="
        selector = "[data-test-id=pin-closeup-image]"
        try:
            super().__init__(website, search_url, selector)
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
        image_src = html.select_one('a[href^="https://d2w9rnfcy7mm78.cloudfront.net/"]').get('href')
        title = html.select_one('img').get('title')
        
        return {'source': image_src, 'title': title}  
    

    def extract_img_author(self, html) -> str:
        creator_div = html.find('div', attrs={"data-test-id": "official-user-attribution"})
        if creator_div:
            user_tag = f"@{creator_div.a['href'].replace('/', '')}"
        else:
            user_tag = "None"
        return user_tag
    

    def fetch_img_details(self, link: str) -> Image:
        html = self.page_parser(link)
        img_source = self.extract_img_source(html)
        author = self.extract_img_author(html)
        img_format = img_source['source'].split(".")[-1]
        if '?' in img_format:
            img_format = img_format.split("?")[0]
        image = Image('None', link, img_source['source'], 'Pinterest', author, img_source['alt'], img_format)
        
        return image