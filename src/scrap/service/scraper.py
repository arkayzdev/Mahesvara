from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import logging
from scrap.model import Image

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ImageScraper(ABC):
    @abstractmethod
    def __init__(self, website: str, search_url: str, search_url_extra: str, selector: str ) -> None:
        self.website = website
        self.search_url = search_url
        self.search_url_extra = search_url_extra
        self.selector = selector
        
    
    async def parse_search(self, url: str, selector: str) -> BeautifulSoup:
        try:
            async with async_playwright() as pw:
                browser = await pw.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                await page.goto(url)  
                await page.wait_for_selector(selector)  
                content = await page.content()
                html = BeautifulSoup(content, 'html.parser')
                await browser.close()
            return html
        except PlaywrightTimeoutError:
            logger.error(f"Timeout while parsing {url}")
            raise
        except Exception as e:
            logger.error(f"Error parsing page {url}: {e}")
            raise

        

    
    @abstractmethod
    def extract_links(self, html: BeautifulSoup) -> List[str]:
        pass
    
    @abstractmethod
    def extract_img_source(self, html: BeautifulSoup) -> dict:
        pass 
    
    @abstractmethod
    def fetch_img_details(self, link: str) -> Image:
        pass


    async def fetch_all_images(self, links: list) -> List[Image]:
        max_threads = int(os.getenv('MAX_THREAD', 10))
        all_imgs = []

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            try:
                futures = {executor.submit(self.fetch_img_details, link) : link for link in links}
                for future in as_completed(futures):
                    if future.exception() is not None:
                        logger.error(f"Error processing img: {e}")
                    all_imgs.append(future.result())
            except Exception as e:
                logger.error(f"Error processing img: {e}")
        return all_imgs

        
       
           


