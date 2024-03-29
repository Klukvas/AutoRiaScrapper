import json
import aiohttp
# try:
#     from ..exceptions import AutoRiaException
# except ImportError:
import sys
from os.path import abspath, dirname
path = dirname(dirname(abspath(__file__)))
print(path)
sys.path.append(path)
from exceptions import AutoRiaException

class RiaApi:

    def __init__(self, log, config) -> None:
        self.main_url = 'https://developers.ria.com/auto/'
        self.log = log
        self.config = config
        self.api_key = None

    def set_config(self) -> bool:
        # set curret api key for use
        if self.api_key is None:
            self.api_key = self.config[0]
        else:
            #change existing api key
            current_key_index = self.config.index(self.api_key)
            if len(self.config) - 1 == current_key_index:
                self.log.warning(
                    f"All keys of AutoRia`s api was used"
                )
                return False
            else:
                self.api_key = self.config[current_key_index + 1]
                return True

    async def get_brands(self) -> dict or int:
        """
        https://developers.ria.com/auto/categories/:categoryId/marks?api_key=YOUR_API_KEY
        """
        url = self.main_url + f'categories/1/marks?api_key={self.api_key}'
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    json_response = json.loads(await resp.read())
                    return json_response
                else:
                    self.log.error(
                        f"Error of getting brand with status code: {resp.status}\nResponse text: {resp.read()}"
                    )
                    return resp.status

    async def get_models(self, mark_id: int) -> dict or int:
        """
        http://api.auto.ria.com/categories/:categoryId/marks/:markId/models?api_key=YOUR_API_KEY
        """
        url = self.main_url + f'categories/1/marks/{mark_id}/models?api_key={self.api_key}'
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    json_response = json.loads(await resp.read())
                    return json_response
                else:
                    self.log.error(
                        f"Error of getting model with status code: {resp.status}; url: {resp.url}\nResponse text: {resp.read()}")
                    return resp.status

    async def get_ads_ids(self, page=1, countpage=50) -> list or int:
        """
        https://developers.ria.com/auto/search?api_key=YOUR_API_KEY&category_id=1&
        https://developers.ria.com/auto/search?api_key=YOUR_API_KEY&category_id=1&countpage=100
        """
        if self.api_key is None:
            self.set_config()
        url = self.main_url + f'search?api_key={self.api_key}&category_id=1&countpage={countpage}&page={page}'
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    json_response = json.loads(await resp.read())
                    searchec_ids = json_response['result']['search_result']['ids']
                    return searchec_ids
                else:
                    self.log.error(
                        f"Error of getting ids of ads with status code: {resp.status}; url: {resp.url}\nResponse text: {await resp.read()}")
                    return resp.status

    async def get_ad_info_by_id(self, _id: int, for_upd=False) -> list or int:
        """
        https://developers.ria.com/auto/info?api_key=YOUR_API_KEY&auto_id=YOUR_ID
        """
        url = self.main_url + f'info?api_key={self.api_key}&auto_id={_id}'
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    json_response = json.loads(await resp.read())
                    try:
                        brand = json_response['markNameEng']
                    except Exception as err:
                        self.log.error(f"Can not find 'markNameEng' of car with id: {_id}")
                        AutoRiaException(f"Can not find 'markNameEng' of car with id: {_id}")

                    try:
                        model = json_response['modelNameEng']
                    except Exception as err:
                        self.log.error(f"Can not find 'modelNameEng' of car with id: {_id}")
                        AutoRiaException(f"Can not find 'modelNameEng' of car with id: {_id}")

                    try:
                        if for_upd:
                            ad_data = {
                                "category": json_response['autoData']['subCategoryNameEng']
                            }
                        else:

                            try:
                                gearBoxId = json_response['autoData']['gearBoxId']
                            except:
                                gearBoxId = -1
                            ad_data = {
                                "category": json_response['autoData']['subCategoryNameEng'],
                                "price": {
                                    'USD': json_response['USD'],
                                    'EUR': json_response['EUR'],
                                    'UAH': json_response['UAH'],
                                },
                                "autoId": json_response['autoData']['autoId'],
                                "race": json_response['autoData']['raceInt'],
                                "year": json_response['autoData']['year'],
                                "fuelName": json_response['autoData']['fuelNameEng'],
                                "fuelValue": json_response['autoData']['fuelId'],
                                "gearBoxId": gearBoxId,
                                "gearBoxName": json_response['autoData']['gearboxName'],
                                "hasDamage": json_response['autoInfoBar']['damage'],
                                "link": json_response['linkToView'],
                                "vin": json_response['VIN'],
                                "from": 'AutoRia'
                            }
                    except Exception as err:
                        self.log.error(f"Some error to collect data abt car\nError: {err}\nId: {_id}")
                        AutoRiaException(f"Some error to collect data abt car\nError: {err}\nId: {_id}")
                    return {"carData": ad_data, "brand": brand, "model": model}
                else:
                    self.log.error(
                        f"""
                            Error of getting ids of ads with status code: {resp.status}; 
                            url: {resp.url}\nResponse text: {resp.read()}
                        """
                    )
                    AutoRiaException(
                        f"""
                            Error of getting ids of ads with status code: {resp.status}; 
                            url: {resp.url}\nResponse text: {resp.read()}
                        """
                    )


if __name__ == "__main__":
    import asyncio

    t = RiaApi()
    t.set_config()
    asyncio.run(t.get_brands())
