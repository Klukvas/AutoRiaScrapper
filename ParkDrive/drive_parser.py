import asyncio
from bs4 import BeautifulSoup
import aiohttp
from logger import Logger
from re import search
from main_parser import Parser
from asyncstdlib.builtins import map as amap, tuple as atuple


class ParkDriveParser(Parser):

    def __init__(self, log) -> None:
        super().__init__(log)
        self.main_url = 'https://parkdrive.ua'
        self.start_url = "https://parkdrive.ua/sitemap/"
        self.can_not_find = {"model": [], "brand": [], "modelNbrand": {}}

    async def create_soup(self, url):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    if response.url != url:
                        self.log.error(f"Can not make response to {url}\nRedirect to {response.url}")
                        return
                    return BeautifulSoup(await response.read(), "html.parser")
                else:
                    self.log.error(f"Error with getting response from url: {url} with status code: {response.status}")
    @staticmethod
    def has_next_pagination(
            soup,
            tag='ul',
            tag_class='pagination hide-from-1023',
            sub_tag='li',
            sub_tag_class='page-next'
    ) -> bool:
        try:
            next_page = soup.find(tag, class_=tag_class). \
                findAll(sub_tag, class_=sub_tag_class)
            if not next_page:
                has_next = False
            else:
                has_next = True
        except:
            has_next = False
        return has_next

    def next_page_builder(self, url: str) -> str:
        if "page" in url:
            page = search(r'page-\d+', url).group(0)
            page_num = int(page.split('-')[1]) + 1
            new_url = url.replace(page, f'page-{page_num}')
        else:
            new_url = url + '/page-1/'

        return new_url

    async def start(self):
        has_next = True
        while has_next:
            self.log.info(f"Start parse page: {self.start_url}")
            soup = await self.create_soup(self.start_url)
            if soup:
                has_next = self.has_next_pagination(soup)
                await self.get_adlist_links(soup)
            else:
                self.log.error(f"Error with getting soup\nUrl: {self.start_url}\nSoup: {soup}")
                return
            self.start_url = self.next_page_builder(self.url)

    async def get_adlist_links(self, soup):
        self.log.info(f"Start collecting links from sitemap")
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
        self.log.info(f"Start collecting links of ads of brand: {brand} and model: {model}")
        url = self.main_url + link
        has_next = True
        all_links = []
        while has_next:
            soup = await self.create_soup(url)
            has_next = self.has_next_pagination(soup)
            url = self.next_page_builder(url)
            for item in soup.findAll('div', class_='car-card-info-wrap'):
                item.find('a').get('href')
                all_links.append(item.find('a').get('href'))
        # await self.process_auto(all_links, brand, model)
        await atuple(amap(lambda link: self.process_auto(link, brand, model), all_links))

    async def process_auto(self, link: list, brand: str, model: str):
        # for item in links:
        url = self.main_url + link
        soup = await self.create_soup(url)
        auto_data = self.find_auto_data(soup, url)
        searialized_data = self.serializer.car_data_serializer(auto_data)
        searialized_data['brand'] = brand
        searialized_data['model'] = model
        await self.process_ad_id(searialized_data)

    def find_auto_data(self, soup: str, url: str) -> None or dict:
        auto_data = {
            "carData": {
                "price": {}
            }
        }
        try:
            auto_data['carData']["autoId"] = search(r'\d+', url.split('-')[-1]).group(0)
        except Exception as err:
            self.log.error(f"Can not get id of auto {url}\nError: {err}")
            return
        try:
            prices = soup.find('div', class_='car-prices').findAll('span')
            if len(prices) == 4:
                price_usd = prices[0].text
                if "$" not in price_usd:
                    raise AttributeError('Symbol "$" not is price usd')
                auto_data['carData']["price"]['USD'] = prices[0].text

                price_eur = prices[1].text
                if "€" not in price_eur:
                    raise AttributeError('Symbol "€" not is price eur')
                auto_data['carData']["price"]['EUR'] = prices[1].text

                price_uah = prices[3].text
                if "грн" not in price_uah:
                    raise AttributeError('Symbols "грн" not is price uah')
                auto_data['carData']["price"]['UAH'] = prices[3].text

            elif len(prices) >= 1:
                for item in prices:
                    if "$" in item.text:
                        auto_data['carData']["price"]['USD'] = item.text
                    elif "€" in item.text:
                        auto_data['carData']["price"]['EUR'] = item.text
                    elif "грн" in item.text:
                        auto_data['carData']["price"]['UAH'] = item.text
            else:
                raise AttributeError(f"Can not find prices of car: {url}")
        except Exception as err:
            auto_data['carData']["price"] = None
            self.log.error(f"Some error of getting prices of car: {url}\nError: {err}")
        try:
            main_data = soup.find('div', class_='car-info-wrap').findAll('div')
            if not main_data:
                raise AttributeError(f"Can not find main info of car: {url}")
            for i in range(len(main_data)):
                if "Пробег:" in main_data[i].text:
                    try:
                        auto_data['carData']["race"] = search(r'\d+', main_data[i + 1].text).group(0)
                    except Exception as err:
                        auto_data['carData']["race"] = None
                        self.log.error(f"Error with getting race of car: {url}\nError: {err}")
                elif "Двигатель:" in main_data[i].text:
                    try:
                        fuel_data = main_data[i + 1].text.split(',')
                        try:
                            auto_data['carData']["fuelValue"] = search(r'^\d*\.?\d*', fuel_data[0]).group(0)
                            if len(auto_data['carData']["fuelValue"]) < 1:
                                raise AttributeError
                        except Exception as err:
                            auto_data['carData']["fuelValue"] = None
                            self.log.warning(f"Can not get fuel volume of car: {url}\nError: {err}")
                        auto_data['carData']["fuelName"] = fuel_data[1]
                    except Exception as err:
                        self.log.warning(f"Can not get fuel name of car: {url}\nError: {err}")
                        auto_data['carData']["fuelName"] = None
                elif "Коробка передач:" in main_data[i].text:
                    auto_data['carData']['gearBoxName'] = main_data[i + 1].text
                elif "Тип кузова:" in main_data[i].text:
                    auto_data['carData']['category'] = main_data[i + 1].text
                elif "Год выпуска:" in main_data[i].text:
                    auto_data['carData']["year"] = main_data[i + 1].text

            if "category" not in auto_data['carData'].keys():
                auto_data['carData']['category'] = None

            if "race" not in auto_data['carData'].keys():
                auto_data['carData']['race'] = None

            if "fuelName" not in auto_data['carData'].keys():
                auto_data['carData']['fuelName'] = None

            if "fuelValue" not in auto_data['carData'].keys():
                auto_data['carData']['fuelValue'] = None

            if "year" not in auto_data['carData'].keys():
                auto_data['carData']['year'] = None

            if "gearBoxName" not in auto_data['carData'].keys():
                auto_data['carData']['gearBoxName'] = None

            auto_data["carData"]['hasDamage'] = None
            auto_data["carData"]['vin'] = None
            auto_data["carData"]['from'] = 'ParkDrive'
            auto_data["carData"]['link'] = url
        except Exception as err:
            self.log.error(f"Some error with getting car data: {url}\nError: {err}")
        return auto_data

    def __check_brand_model_exists(self, brand_name, model_name):
        brand_name = self.serializer.brand_model_serializer(brand_name)['data']
        model_name = self.serializer.brand_model_serializer(model_name)['data']
        brand_id = self.q.get_brand_id(brand_name)
        model_id = self.q.get_model_id(model_name)
        if brand_id:
            if model_id:
                self.log.info(f"Sucsess find brand id of brand: {brand_name} and model id of: {model_name}")
            else:
                self.can_not_find['model'].append({"model": model_name, "brand": brand_name})
                self.log.error(
                    f"Brand id finded of brand: {brand_name} finded\nModel id of model name: {model_name} was not found")
        else:
            if model_id:
                self.can_not_find['brand'].append({"brand": brand_name})
                self.log.info(
                    f"Model id finded of model: {model_name} finded\nBrand id of brand name: {brand_name} was not found")
            else:
                self.can_not_find['brand'].append({"model": model_name, "brand": brand_name})
                self.log.error(f"Can not find brand id of: {brand_name} and model id of model: {model_name}")
        return


def run():
    log = Logger().custom_logger()
    parser_example = ParkDriveParser(log)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parser_example.start())


if __name__ == "__main__":
    run()
