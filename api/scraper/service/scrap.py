from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import threading
import queue

class Scraper:
    def __init__(self) -> None:
        self.website = "default"
        self.search_url = "search"
        self.search_url_next = None
        self.selector = "selector"
        
    
    def search_parser(self, url: str, selector: str):
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            # context = browser.new_context(viewport={"width": 1920, "height": 1080})
            context = browser.new_context()
            page = context.new_page()
            page.goto(url)  
            page.wait_for_selector(selector)  

            html = BeautifulSoup(page.content(), 'html.parser')
            
        return html
    

    def get_links(self, html) -> list:
        return
    

    def get_img_src(self, html) -> dict:
        return 
    

    def get_img_details(self, link: str, result: None, index: int):
        return


    def get_all_img(self, links: list):
        q = queue.Queue()
        for link in links:
            q.put(link)

        num_threads = 10
        threads = [None] * num_threads
        results = [None] * num_threads 
        all_img = list()

        while not q.empty():
            for i in range(num_threads):
                if not q.empty():
                    link = q.get()
                    threads[i] = threading.Thread(target=self.get_img_info, args=(link, results, i), daemon=True)
                    threads[i].start()
            for i in range(num_threads):
                threads[i].join()
            for result in results:
                if result:
                    all_img.append(result)
            
        return all_img