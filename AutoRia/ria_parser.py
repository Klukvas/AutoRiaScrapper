import asyncio
try:
    from .riaApi import RiaApi
except ImportError:
    from riaApi import RiaApi

from asyncstdlib.builtins import map as amap, tuple as atuple
from main_parser import Parser


class AutoRiaBrandModelParser(Parser):

    def __init__(self, log) -> None:
        self.api = RiaApi(log)
        self.log = log
        super().__init__(log)

    def save_parsed_models(self, models: list, brand_id: int) -> None:
        for model in models:
            if isinstance(model, list):
                for item in model:
                    self.q.save_model(brand_id, item['name'])
            else:
                self.q.save_model(brand_id, model['name'])
        return

    async def get_model_by_brand(self):
        all_brands = await self.api.get_brands()
        for brand in all_brands:
            brand_name = brand['name']
            self.q.save_brand(brand_name)
            brand_id = self.q.get_brand_id(brand_name)
            if brand_id:
                brand_id = brand_id[0]
            else:
                raise AttributeError(f'Can not find id of brand: {brand_name}')
            all_brand_models = await self.api.get_models(brand['value'])
            self.save_parsed_models(all_brand_models, brand_id)

    async def run_brandModel_parser(self):
        self.api.set_config()
        await self.get_model_by_brand()


class AutoRiaParser(Parser):

    def __init__(self, log) -> None:
        self.api = RiaApi(log)
        self.log = log
        super().__init__(log)

    def bad_request_handler(self, response, for_upd=False):
        if response == 429:
            set_config_result = self.api.set_config()
            if set_config_result:
                self.log.info(f"Set new api key to api and continue work")
                return True
            else:
                self.log.critical(f"Can not set new api key -> stop working and write last parsed page to db")
                if not for_upd:
                    self.q.upgrade_last_page(self.current_page)
                return False
        else:
            if not for_upd:
                self.q.upgrade_last_page(self.current_page)
            return False

    async def get_car_data(self):
        self.log.info('Start collect cars data')
        try:
            self.current_page = self.q.get_last_page()[0]
        except Exception as err:
            self.log.warning(f"Can not get last parsed page from db -> set default value(1).\nException: {err}")
            self.current_page = 1
        while True:
            ad_ids = await self.api.get_ads_ids(self.current_page)
            if isinstance(ad_ids, list) and len(ad_ids) > 0:
                await atuple(amap(self.process_ad_id, ad_ids))
            elif isinstance(ad_ids, list) and len(ad_ids) < 0:
                self.log.info(f'Work is done, current pool of ids are empty')
                break
            else:
                desigion = self.bad_request_handler(ad_ids)
                if desigion:
                    await self.get_car_data()
                break
            self.current_page += 1

    async def run_car_info_parser(self):
        print('Start')
        self.api.set_config()
        await self.get_car_data()


def run(logger):
    loop = asyncio.get_event_loop()
    parser = AutoRiaParser(logger)
    loop.run_until_complete(parser.run_car_info_parser())


if __name__ == "__main__":
    from logger import Logger
    log = Logger().custom_logger()
    run(log)
