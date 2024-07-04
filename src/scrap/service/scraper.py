from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
import os
from abc import ABC, abstractmethod
from tools.logger import logger



class Scraper(ABC):
    @abstractmethod
    def __init__(self, website: str, search_url: str, search_url_extra: str, selector: str ) -> None:
        self.website = website
        self.search_url = search_url
        self.search_url_extra = search_url_extra
        self.selector = selector
        
    
    def parse_search(self, url: str, selector: str) -> BeautifulSoup:
        try:
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                page.goto(url)  
                page.wait_for_selector(selector)  

                html = BeautifulSoup(page.content(), 'html.parser')
                browser.close()
            return html
        except Exception as e:
            logger.error(f"Error parsing page {url}: {e}")
            raise
    
    @abstractmethod
    def extract_links(self, html: BeautifulSoup) -> list[str]:
        pass
    
    @abstractmethod
    def extract_img_source(self, html) -> dict:
        pass 
    
    @abstractmethod
    def fetch_image_details(self, link: str):
        pass


    def fetch_all_images(self, links: list):
        try:
            num_threads = int(os.getenv('NUMBER_THREADS', 4))  
            all_images = list()

            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                future_to_link = {executor.submit(self.fetch_image_details, link): link for link in links}
                for future in as_completed(future_to_link):
                    link = future_to_link[future]
                    try:
                        result = future.result()
                        if result:
                            all_images.append(result)
                    except Exception as e:
                        logger.error(f"Error processing {link}: {e}")
            
            return all_images
        
        except Exception as e:
            logger.error(f"Error in fetch_all_images: {e}")
            raise