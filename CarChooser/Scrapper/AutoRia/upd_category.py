from Configs.logger import Logger
from ria_parser import BrandModelParser
import asyncio
class UpdCatygory(BrandModelParser):
    def __init__(self, log):
        super().__init__(log)

    async def get_category_by_id(self):
        self.api.set_config()
        while True:
            ids = self.q.get_cars_ids_with_empty_category()
            if ids:
                for item in ids:
                    self.log.info(f"Start getting category of car id: {item}")
                    car_info = await self.api.get_ad_info_by_id(item, True)
                    if type(car_info) == int:
                        self.bad_request_handler(car_info, True)
                        continue
                    else:
                        self.upd_car(car_info['carData']['category'], item)
            else:
                self.log.info(f"All cars were updated")
                break

    def upd_car(self, car_category, car_id):
        category_id = self.q.get_category(car_category.lower())
        if category_id:
            self.log.info(f"Start updating new car")
            self.q.upd_car_category(category_id[0], car_id)
            return
        else:
            self.log.warning(f"Can not get category id of: {car_category}. Try to save new category and recall func")
            self.q.save_category(car_category.lower())
            self.upd_car(car_category, car_id)



if __name__ == "__main__":
    log = Logger().custom_logger()
    uc = UpdCatygory(log)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(uc.get_category_by_id())