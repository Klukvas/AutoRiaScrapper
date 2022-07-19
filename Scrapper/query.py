from Scrapper.models import Brand, Category, DatabaseClient, Model, Car, AdLastPage, GearBox, UndefinedData
from sqlalchemy import text
import json
from .serializer import Serializer
from psycopg2 import errors as postgres_errors
from sqlalchemy.exc import IntegrityError
class Query:

    def __init__(self, log) -> None:
        self.db_client = DatabaseClient()
        self.log = log

    def __del__(self) -> None:
        self.db_client.session.commit()
        self.db_client.session.close()

    def save_brand(self, brand):
        new_brand = Brand(
            brand_name=brand
        )
        try:
            self.db_client.session.add(new_brand)
            self.db_client.session.commit()
        except Exception as err:
            self.log.error(f'Some error with saving brand: {brand};\nError: {err}')
            self.db_client.session.rollback()
        return

    def save_unfinded_data(self, data_type, value_data, additional):
        new_unfinded_data = UndefinedData(
            type_data=data_type.lower(),
            data_value=value_data.lower(),
            additional_data=additional
        )
        try:
            self.db_client.session.add(new_unfinded_data)
            self.db_client.session.commit()
        except Exception as err:
            self.log.error(f'Some error with saving unfinded data: {data_type} | {value_data};\nError: {err}')
            self.db_client.session.rollback()
        return

    def upgrade_last_page(self, page):
        page_num = self.db_client.session.query(AdLastPage).all()
        if page_num:

            self.db_client.session.query(AdLastPage). \
                filter(AdLastPage.page_num > -1). \
                update({"page_num": page})
            self.db_client.session.commit()
        else:
            new_page = AdLastPage(
                page_num=page
            )
            self.db_client.session.add(new_page)
            self.db_client.session.commit()

    def save_model(self, brandId: int, model: str):
        new_model = Model(
            model_name=model,
            brand_id=brandId
        )
        try:
            self.db_client.session.add(new_model)
            self.db_client.session.commit()
            self.log.debug(f"Model: {model} saved")
        except Exception as err:
            self.log.error(f'Some error with saving model: {model}; brand id: {brandId};\nError: {err}')
            self.db_client.session.rollback()
        return

    def get_brand_id(self, brand_name):
        brand_id = self.db_client.session.query(Brand).filter(
            text(f"brands.brand_name like '{brand_name.lower()}'")
        )
        ids = []
        for object_ in brand_id:
            ids.append(object_.id)
        return ids

    def get_last_page(self):
        page = self.db_client.session.query(AdLastPage).all()
        ids = []
        for object_ in page:
            ids.append(object_.page_num)
        return ids

    def get_gear_box_id(self, gearbox_name):
        gearBox_id = self.db_client.session.query(GearBox).filter(
            text(f"gear_box.gearbox_name like '{gearbox_name.lower()}'")
        )
        ids = []
        for object_ in gearBox_id:
            ids.append(object_.id)
        return ids

    def save_gear_box(self, gearbox):
        new_gearbox = GearBox(
            gearbox_name=gearbox
        )
        try:
            self.db_client.session.add(new_gearbox)
            self.db_client.session.commit()
        except Exception as err:
            self.log.error(f'Some error with saving gearBox: {gearbox};\nError: {err.orig}')
            self.db_client.session.rollback()
        return

    def get_model_id(self, model_name):
        model_id = self.db_client.session.query(Model).filter(
            text(f"LOWER(models.model_name) like '{model_name}'")
        )
        ids = []
        for object_ in model_id:
            ids.append(object_.id)
        return ids

    def save_car_data(self, brand, model, car_data, gearbox_id, category_id):
        new_car = Car(
            brand_id=brand,
            model_id=model,
            auto_id=car_data['autoId'],
            price_usd=car_data['price']['USD'],
            price_uah=car_data['price']['UAH'],
            price_eur=car_data['price']['EUR'],
            race=car_data['race'],
            year=car_data['year'],
            fuel_name=car_data['fuelName'],
            fuel_value=car_data['fuelValue'],
            gearbox_id=gearbox_id,
            has_damage=car_data['hasDamage'],
            link=car_data['link'],
            vin=car_data['vin'],
            parsed_from=car_data['from'],
            category_id=category_id
        )
        try:
            self.db_client.session.add(new_car)
            self.db_client.session.commit()
            return True
        except IntegrityError as err:
            '''
            todo: add Enums of response
            '''
            if isinstance(err.orig, postgres_errors.UniqueViolation):
                self.db_client.session.rollback()
                return True
            self.db_client.session.rollback()
            return err,
        except Exception as err:
            self.db_client.session.rollback()
            return err,

    def get_cars_ids_with_empty_category(self, limit=10):
        car_ids = self.db_client.session.query(Car).filter(
            Car.category_id.is_(None)
        ).limit(limit)
        ids = []
        for object_ in car_ids:
            ids.append(object_.auto_id)
        self.log.info(f"Getting new {limit} ids: {ids}")
        return ids

    def save_category(self, category):
        new_category = Category(
            category_name=category
        )
        try:
            self.db_client.session.add(new_category)
            self.db_client.session.commit()
        except Exception as err:
            self.log.error(f'Some error with saving gearBox: {category};\nError: {err.orig}')
            self.db_client.session.rollback()
        return

    def get_category(self, category):
        category_id = self.db_client.session.query(Category).filter(
            text(f"LOWER(category.category_name) like '{category.lower()}'")
        )
        ids = []
        for object_ in category_id:
            ids.append(object_.id)
        return ids

    def upd_car_category(self, id: int, car_id: int):
        try:

            self.db_client.session.query(Car). \
                filter(Car.auto_id == car_id). \
                update({"category_id": id})
            self.db_client.session.commit()
            self.log.info(f"Done with upd category of car with id: {car_id}")
        except Exception as err:
            self.log.error(f"Some error with saving updated category of car with id: {car_id}\nError: {err}")
        return


class OneTimeQuery:

    def __init__(self, log) -> None:
        self.db_client = DatabaseClient()
        self.serializer = Serializer()
        self.log = log

    def update_models(self):
        # models = self.db_client.session.query(Model).filter(
        #         text(f"models.model_name like '%-%'")
        #     )
        models = self.db_client.session.query(Model).all()
        for object_ in models:
            try:
                new_model_name = self.serializer.brand_model_serializer(object_.model_name)['data']
                self.db_client.session.query(Model). \
                    filter(Model.id == object_.id). \
                    update({"model_name": new_model_name})
                self.db_client.session.commit()
                self.log.info(f"Upd model: {object_.model_name} to {new_model_name}")
            except:
                self.db_client.session.rollback()
                self.log.warning(f"Can not update model: {object_.model_name}")
                continue

    def update_models(self):
        # models = self.db_client.session.query(Model).filter(
        #         text(f"models.model_name like '%-%'")
        #     )
        models = self.db_client.session.query(Model).all()
        for object_ in models:
            try:
                new_model_name = self.serializer.brand_model_serializer(object_.model_name)['data']
                self.db_client.session.query(Model). \
                    filter(Model.id == object_.id). \
                    update({"model_name": new_model_name})
                self.db_client.session.commit()
                self.log.info(f"Upd model: {object_.model_name} to {new_model_name}")
            except:
                self.db_client.session.rollback()
                self.log.warning(f"Can not update model: {object_.model_name}")
                continue

    def upd_unexists_brand_model_file(self):
        q2 = Query('asd')
        unf = []
        with open('data.json') as f:
            data = json.load(f)
        for item in data['model']:
            mid = q2.get_model_id(item['model'])
            if mid:
                pass
            else:
                unf.append(item)
        unf_models = json.dumps(item)
        with open('unfindet_models.json', 'w') as f:
            f.write(unf_models)


if __name__ == "__main__":
    from logger import Logger

    log = Logger().custom_logger()
    q = Query(log)
    models = q.get_model_id('test')
    print(models)
