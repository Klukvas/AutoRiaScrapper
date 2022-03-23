import asyncio
from bs4 import BeautifulSoup
import aiohttp
from query import Query
from logger import Logger
from asyncstdlib.builtins import map as amap, tuple as atuple
from serializer import Serializer

class ParkDriveParser:

    def __init__(self, log) -> None:
        self.log = log
        self.main_url = 'https://parkdrive.ua'
        self.start_url = "https://parkdrive.ua/sitemap"
        self.q = Query(log)
        self.serializer = Serializer()
        self.can_not_find = {"model": [], "brand": [], "modelNbrand": {}}
        self.has_next = True

    async def create_soup(self, url):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return BeautifulSoup(await response.read(), "html.parser")
                else:
                    self.log.error(f"Error with getting response from url: {url} with status code: {response.status}")
                    
    def has_next_pagination(self, soup):
        try:
            next_page = soup.find("ul", class_='pagination hide-from-1023').\
                findAll('li', class_='page-next')
            if not next_page:
                self.has_next = False
        except:
            self.has_next = False
        return
    async def get_ad_list(self):
        current_page = 0
        while self.has_next:
            current_page += 1
            url = self.start_url + f"/page-{current_page}"
            soup = await self.create_soup(url)
            if soup:
                self.has_next_pagination(soup)
                await self.get_adlist_link(soup)
            else:
                self.log.error(f"Error with getting soup\nUrl: {url}\nSoup: {soup}")
                return

    async def get_adlist_link(self, soup):
        all_ads_lists = soup.find("div", class_="sitemap-data-wrap").findAll("li")
        if all_ads_lists:
            for item in all_ads_lists:
                ad_list = item.find('a')
                href = ad_list.get('href')
                href_data = href.strip().split('/')
                if href_data[1] == 'cars':
                    brand = href_data[3]
                    model = href_data[4]
                    await self.process_adlist(href, brand, model)
                else:
                    self.log.info(f"Category: {href_data[0]} skipped")
                    continue
        else:
            self.log.error(f"Can not find urls of adlist\nSoup: {soup}")

    async def process_adlist(self, link, brand, model):
        url = self.main_url + link
        soup = await self.create_soup(url)
        self.check_brand_model_exists(brand, model)
    
    def check_brand_model_exists(self, brand_name, model_name):
        brand_name = self.serializer.brand_model_serializer(brand_name)['data']
        model_name = self.serializer.brand_model_serializer(model_name)['data']
        brand_id = self.q.get_brand_id(brand_name)
        model_id = self.q.get_model_id(model_name)
        if brand_id:
            if model_id:
                self.log.info(f"Sucsess find brand id of brand: {brand_name} and model id of: {model_name}")
            else:
                self.can_not_find['model'].append({"model": model_name, "brand": brand_name})
                self.log.error(f"Brand id finded of brand: {brand_name} finded\nModel id of model name: {model_name} was not found")
        else:
            if model_id:
                self.can_not_find['brand'].append({"brand": brand_name})
                self.log.info(f"Model id finded of model: {model_name} finded\nBrand id of brand name: {brand_name} was not found")
            else:
                self.can_not_find['brand'].append({"model": model_name, "brand": brand_name})
                self.log.error(f"Can not find brand id of: {brand_name} and model id of model: {model_name}")
        return

    async def start(self):
        await self.get_ad_list()
        self.log.info(self.can_not_find)



def run():
    log = Logger().custom_logger()
    parser_example = ParkDriveParser(log)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parser_example.start())




if __name__ == "__main__":
    run()