
class Parser:

    def __init__(self, log, query, serializer) -> None:
        self.log = log
        self.q = query
        self.serializer = serializer

    def brand_exists(self, brand: str, re_call=0) -> list or None:
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

    def model_exists(self, brand: int, brand_name: str, model: str, re_call=0) -> list or None:
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

    def gearbox_exists(self, gearbox: str, re_call=0) -> list or None:
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

    def category_exists(self, category: str, re_call=0) -> list or None:
        category_id = self.q.get_category(category.lower())
        if category_id:
            return category_id[0]
        elif not category_id and re_call == 0:
            self.q.save_category(category.lower())
            self.log.debug(f"Recall func of category exists for category: {category}")
            return self.category_exists(category, 1)
        else:
            self.q.save_unfinded_data('category', category, None)
            return None

    async def process_ad_id(self, *args):
        if isinstance(args[0], str):
            car_data = await self.api.get_ad_info_by_id(args[0])
        elif isinstance(args[0], dict):
            car_data = args[0]
        else:
            self.log.error(f"Can not parse car data: {args[0]}")
            return
        if isinstance(car_data, dict):
            self.log.info(
                f"Start processing new auto {car_data['carData']['autoId']}\tParsed form: {car_data['carData']['from']}"
            )
            brand_name = self.serializer.brand_model_serializer(car_data['brand'])['data']
            brand_id = self.brand_exists(brand_name)
            if not brand_id:
                self.log.error(
                    f"Some error with getting brandId\nauto_id: {car_data['carData']['autoId']}\nbrand: {brand_name}\nParsed form: {car_data['carData']['from']}")
                return
            model_name = self.serializer.brand_model_serializer(car_data['model'])['data']
            model_id = self.model_exists(brand_id, brand_name, model_name)
            if not model_id:
                self.log.error(
                    f"Some error with getting modelId\nauto_id: {car_data['carData']['autoId']}\nbrand: {brand_id}\nmodel:{model_name}\tlen model: {len(model_name)}\nParsed form: {car_data['carData']['from']}")
                return
            gearbox_id = self.gearbox_exists(car_data['carData']['gearBoxName'])
            if not gearbox_id:
                self.log.error(
                    f"Some error with getting modelId\nauto_id: {car_data['carData']['autoId']}\nbrand: {brand_id}\nmodel:{model_id}\nGearBoxName: {car_data['carData']['gearBoxName']}\nParsed form: {car_data['carData']['from']}")
                return
            category_id = self.category_exists(car_data['carData']['category'])
            if not category_id:
                self.log.error(
                    f"Some error with getting category id\nauto_id: {car_data['carData']['autoId']}\nbrand: {brand_id}\nmodel:{model_id}\nGear box id:{gearbox_id}\nCategory: {car_data['carData']['category']}\nParsed form: {car_data['carData']['from']}")
                return
            result = True
            result = self.q.save_car_data(brand_id, model_id, car_data['carData'], gearbox_id, category_id)
            if isinstance(result, int):
                self.log.info(
                    f"Car with id: {car_data['carData']['autoId']} saved.\nParsed form: {car_data['carData']['from']}")
            else:
                self.log.error(
                    f"Error while saving car data.\nError:{result}\ncar_data: {car_data['carData']}\nParsed form: {car_data['carData']['from']}")
        else:
            if isinstance(car_data, type) and car_data().__class__.__name__ == 'AutoRiaException':
                desigion = self.bad_request_handler(self.current_page)
                if desigion:
                    self.process_ad_id(car_data)
                return
