from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from scrap.service.pinterest import PinterestImageScraper
app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}



@app.get("/images/{search}")
async def get_images(search: str) :
    pin_scraper = PinterestImageScraper()
    research_page = await pin_scraper.parse_search(f"https://pinterest.com/search/pins/?q={search}", "img")
    links = pin_scraper.extract_links(research_page)
    imgs = await pin_scraper.fetch_all_images(links)
    print(imgs)
    return {"images": imgs}
