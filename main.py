import asyncio
from riaApi import RiaApi 
from query import Query


class BrandModelParser:


    def __init__(self) -> None:
        self.api = RiaApi()
        self.q = Query()


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

    def bad_request_handler(self, response):
        if response == 429:
            set_config_result = self.api.set_config()
            if set_config_result:
                print(f"set new api key to api and continue work")
                return True
            else:
                print(f"Can not set new api key -> stop working and write last parsed page to db")
                self.q.upgrade_last_page(self.current_page)
                return False
        else:
            self.q.upgrade_last_page(self.current_page)
            return False

    def brand_exists(self, brand:str, re_call=0) -> int or None:
        brand_id = self.q.get_brand_id(brand)
        if brand_id:
            return brand_id[0]
        elif not brand_id and re_call == 0:
            self.q.save_brand(brand)
            self.brand_exists(brand, 1)
        else:
            self.q.save_unfinded_data('brand', brand, None)
            return None
    
    def model_exists(self, brand:int, brand_name:str, model:str, re_call=0) -> int or None:
        model_id = self.q.get_model_id(model)
        if model_id:
            return model_id[0]
        elif not model_id and re_call == 0:
            self.q.save_model(brand, model)
            self.model_exists(brand, brand_name, model, 1)
        else:
            self.q.save_unfinded_data('model', model, brand_name.lower())
            return None
            
    def gearbox_exists(self, gearbox:str, re_call=0) -> int or None:
        gearbox_id = self.q.get_gear_box_id(gearbox.lower())
        if gearbox_id:
            return gearbox_id[0]
        elif not gearbox_id and re_call == 0:
            self.q.save_gear_box(gearbox.lower())
            self.gearbox_exists(gearbox, 1)
        else:
            self.q.save_unfinded_data('gearbox', gearbox, None)
            return None

    async def get_car_data(self):
        try:
            self.current_page = self.q.get_last_page()[0]
        except:
            self.current_page = 1
        page = 0
        while True:
            page += 1
            ad_ids = await self.api.get_ads_ids(page)
            if isinstance(ad_ids, list) and len(ad_ids) > 0:
                for ad_id in ad_ids:
                    car_data = await self.api.get_ad_info_by_id(ad_id)
                    if isinstance(car_data, dict):
                        brand_id = self.brand_exists(car_data['brand'])
                        if not brand_id:
                            print(f"Some error with getting brandId\nad_id: {ad_id}\nbrand: {car_data['brand']}")
                            continue
                        model_id = self.model_exists(brand_id, car_data['brand'], car_data['model'])
                        if not model_id:
                            print(f"Some error with getting modelId\nad_id: {ad_id}\nbrand: {brand_id}\nmodel:{car_data['model']}")
                            continue
                        gearbox_id = self.gearbox_exists(car_data['carData']['gearBoxName'])
                        if not gearbox_id:
                            print(f"Some error with getting modelId\nad_id: {ad_id}\nbrand: {brand_id}\nmodel:{model_id}\nGearBoxName: {car_data['carData']['gearBoxName']} ")
                            continue
                        self.q.save_car_data(brand_id, model_id, car_data['carData'], gearbox_id)
                    else:
                        desigion = self.bad_request_handler(ad_ids)
                        if desigion:
                            self.get_car_data()
                        break

            elif isinstance(ad_ids, list) and len(ad_ids) < 0:
                print(f'Work is done, current pool of ids are empty')
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


if __name__ == "__main__":
    import logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy').setLevel(logging.CRITICAL)
    logging.getLogger('sqlalchemy').setLevel(logging.CRITICAL)
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.CRITICAL)
    import logging
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)
    loop = asyncio.get_event_loop()
    parser = BrandModelParser()
    loop.run_until_complete(parser.run_car_info_parser())