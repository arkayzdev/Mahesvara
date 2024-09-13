from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from scraper import Scraper
import queue
import threading

class ArenaScraper(Scraper):
    def __init__(self) -> None:
        self.website = "are.na"
        self.search_url = "search/"
        self.search_url_next = "/blocks?block_filter=IMAGE"
        self.selector = "img"


    def get_links(self, html):
        div_links = html.select('a[href^="/block/"]')
        img_links = [f"https://are.na{div_link.get('href')}" for div_link in div_links]

        return img_links
    

    def get_img_src(self, html):
        image_src = html.select_one('a[href^="https://d2w9rnfcy7mm78.cloudfront.net/"]').get('href')
        title = html.select_one('img').get('title')
        
        return {'source': image_src, 'title': title}  