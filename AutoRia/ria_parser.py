import asyncio
from time import sleep
from .riaApi import RiaApi 
from query import Query
from logger import Logger
from asyncstdlib.builtins import map as amap, tuple as atuple
from serializer import Serializer
from time import sleep

class BrandModelParser:


    def __init__(self, log) -> None:
        self.api = RiaApi(log)
        self.q = Query(log)
        self.serializer = Serializer()
        self.log = log

    def save_parsed_models(self, models:list, brand_id:int) -> None:
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

    def brand_exists(self, brand:str, re_call=0) -> list or None:
        brand_id = self.q.get_brand_id(brand)
        if brand_id:
            return brand_id[0]
        elif not brand_id and re_call == 0:
            self.log.debug(f"Recall func of brand exists for brand: {brand}")
            self.q.save_brand(brand)
            return self.brand_exists(brand, 1)
        else:
            self.log.warning(f"Can not save brand: {brand}")
            self.q.save_unfinded_data('brand', brand, None)
            return None
    
    def model_exists(self, brand:int, brand_name:str, model:str, re_call=0) -> list or None:
        model_id = self.q.get_model_id(model)
        if model_id:
            return model_id[0]
        elif not model_id and re_call == 0:
            self.log.debug(f"Recall func of model exists for model: {model}")
            self.q.save_model(brand, model)
            return self.model_exists(brand, brand_name, model, 1)
        else:
            self.log.error(f"Can not find model: {model} after saving")
            self.q.save_unfinded_data('model', model, brand_name.lower())
            return None
            
    def gearbox_exists(self, gearbox:str, re_call=0) -> list or None:
        gearbox_id = self.q.get_gear_box_id(gearbox.lower())
        if gearbox_id:
            return gearbox_id[0]
        elif not gearbox_id and re_call == 0:
            self.log.debug(f"Recall func of gearbox exists for gearbox: {gearbox}")
            self.q.save_gear_box(gearbox.lower())
            return self.gearbox_exists(gearbox, 1)
        else:
            self.q.save_unfinded_data('gearbox', gearbox, None)
            return None
    
    def caregory_exists(self, category:str, re_call=0) -> list or None:
        category_id = self.q.get_category(category.lower())
        if category_id:
            return category_id[0]
        elif not category_id and re_call == 0:
            self.q.save_category(category.lower())
            self.log.debug(f"Recall func of category exists for category: {category}")
            return self.caregory_exists(category, 1)
        else:
            self.q.save_unfinded_data('category', category, None)
            return None

    async def process_ad_id(self, id:int):
        self.log.info(f"Start processing new ad id: {id}")
        car_data = await self.api.get_ad_info_by_id(id)
        if isinstance(car_data, dict):
            brand_name = self.serializer.brand_model_serializer(car_data['brand'])['data']
            brand_id = self.brand_exists(brand_name)
            if not brand_id:
                self.log.error(f"Some error with getting brandId\nad_id: {id}\nbrand: {brand_name}")
                return
            model_name = self.serializer.brand_model_serializer(car_data['model'])['data']
            model_id = self.model_exists(brand_id, brand_name, model_name)
            if not model_id:
                self.log.error(f"Some error with getting modelId\nad_id: {id}\nbrand: {brand_id}\nmodel:{model_name}\tlen model: {len(model_name)}")
                return
            gearbox_id = self.gearbox_exists(car_data['carData']['gearBoxName'])
            if not gearbox_id:
                self.log.error(f"Some error with getting modelId\nad_id: {id}\nbrand: {brand_id}\nmodel:{model_id}\nGearBoxName: {car_data['carData']['gearBoxName']} ")
                return
            category_id = self.caregory_exists(car_data['carData']['category'])
            if not category_id:
                self.log.error(f"Some error with getting category id\nad_id: {id}\nbrand: {brand_id}\nmodel:{model_id}\nGear box id:{gearbox_id}\nCategory: {car_data['carData']['category']} ")
                return
            result = self.q.save_car_data(brand_id, model_id, car_data['carData'], gearbox_id, category_id)
            if isinstance(result, int):
                self.log.info(f"Car with id: {car_data['carData']['autoId']} saved.")
            else:
                self.log.error(f"Error while saving car data.\nError:{result}\npage of car: {self.current_page}.\ncar_data: {car_data['carData']['autoId']}")
        else:
            desigion = self.bad_request_handler(id)
            if desigion:
                self.process_ad_id(id)
            return

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



    async def run_brandModel_parser(self):
        self.api.set_config()
        await self.get_model_by_brand()


    async def run_car_info_parser(self):
        self.api.set_config()
        await self.get_car_data()

def run(logger):
    loop = asyncio.get_event_loop()
    parser = BrandModelParser(logger)
    loop.run_until_complete(parser.run_car_info_parser())









if __name__ == "__main__":
    run()