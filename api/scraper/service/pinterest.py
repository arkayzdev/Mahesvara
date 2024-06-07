from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from scrap import Scraper
from model import Scrap
import queue
import threading

class ArenaScraper(Scraper):
    def __init__(self) -> None:
        self.website = "pinterest"
        self.search_url = "search/pins/?q="
        self.search_url_next = None
        self.selector = "[data-test-id=pin-closeup-image]"


    def get_links(self, html):
        links = []
        div_links = html.select('a[href^="/pin/"]') 
        pins = [div_link.get('href') for div_link in div_links]
        links = [pin for pin in pins if not pin in links]
        img_links = [f"https://pinterest.com{link}" for link in links]
        
        return img_links
    

    def get_img_src(self, html):
        image_src = html.select_one('a[href^="https://d2w9rnfcy7mm78.cloudfront.net/"]').get('href')
        title = html.select_one('img').get('title')
        
        return {'source': image_src, 'title': title}  
    

    def get_user_tag(self, html) -> str:
        creator_div = html.find('div', attrs={"data-test-id": "official-user-attribution"})
        if creator_div:
            user_tag = f"@{creator_div.a['href'].replace('/', '')}"
        else:
            user_tag = "None"
        return user_tag
    

    def get_img_details(self, link: str, result: None, index: int) -> Scrap:
        """Get all informations needed for images

        Args:
            link (str): _description_
            result (None): _description_
            index (int): _description_

        Returns:
            Image: _description_
        """
        html = self.page_parser(link)
        img_src = self.get_img_src(html)
        author = self.get_user_tag(html)
        img_format = img_src['source'].split(".")[-1]
        if '?' in img_format:
            img_format = img_format.split("?")[0]
        image = Scrap('None', link, img_src['source'], 'Pinterest', author, img_src['alt'], img_format)
        
        result[index] = image
        return image