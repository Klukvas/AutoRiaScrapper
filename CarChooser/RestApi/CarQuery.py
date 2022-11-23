from CarChooser.Scrapper.models import (
    Car,
    Model,
    Brand,
    GearBox,
    Category,
    DatabaseClient
)


class CarApiQuery:

    def __init__(self, log) -> None:
        self.log = log
        self.db_client = DatabaseClient()

    def __del__(self) -> None:
        try:
            self.db_client.session.commit()
            self.db_client.session.close()
        except:
            pass
    def get_all_car_data(self):
        cars = []
        cars_object = self.db_client.session.query(Car, Model, Category, GearBox, Brand) \
            .join(Model, Model.id == Car.model_id) \
            .join(Brand, Brand.id == Car.brand_id) \
            .join(Category, Category.id == Car.category_id) \
            .join(GearBox, GearBox.id == Car.gearbox_id) \
            .all()
        for car_inf, model, category, gearbox, brand in cars_object:
            cars.append(
                {
                    "price_usd": car_inf.price_usd,
                    "price_uah": car_inf.price_uah,
                    "price_eur": car_inf.price_eur,
                    "race": car_inf.race,
                    "year": car_inf.year,
                    "fuel_name": car_inf.fuel_name,
                    "fuel_value": car_inf.fuel_value,
                    "has_damage": car_inf.has_damage,
                    "link": car_inf.link,
                    "vin": car_inf.vin,
                    "parsed_from": car_inf.parsed_from,
                    "model_name": model.model_name,
                    "brand_name": brand.brand_name,
                    "gearbox_name": gearbox.gearbox_name,
                    "category_name": category.category_name

                }
            )
        return cars

    def get_all_gearboxes(self):
        gearboxes = []
        gearbox_objects = self.db_client.session.query(GearBox) \
            .all()
        for item in gearbox_objects:
            gearboxes.append({
                'gearbox_name': item.gearbox_name,
                'gearbox_id': item.id
            })
        return gearboxes

    def get_all_categories(self):
        categories = []
        category_objects = self.db_client.session.query(Category) \
            .all()
        for item in category_objects:
            categories.append({
                'category_name': item.category_name,
                'category_id': item.id
            })
        return categories

    def get_all_models(self):
        models = []
        models_objects = self.db_client.session.query(Model) \
            .with_entities(Model.model_name, Model.id) \
            .all()
        for item in models_objects:
            models.append({
                'model_name': item[0],
                'model_id': item[1]
            })
        return models

    def get_all_brands(self):
        brands = []
        brands_objects = self.db_client.session.query(Brand) \
            .with_entities(Brand.brand_name, Brand.id) \
            .all()
        for item in brands_objects:
            brands.append({
                'brand_name': item[0],
                'brand_id': item[1]
            })
        return brands

    def get_model_by_brand(self):
        brand_model = []
        models_n_brands = self.db_client.session.query(Brand, Model) \
            .join(Model, Model.brand_id == Brand.id)
        for brand, model in models_n_brands:
            brand_model.append(
                {
                    "brand": brand.brand_name,
                    "model": model.model_name
                }
            )
        return brand_model


if __name__ == "__main__":
    q = CarApiQuery('asd')
    a = q.get_model_by_brand()
    print(a)
