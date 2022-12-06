from CarChooser.Scrapper.models import (
    Car,
    Model,
    Brand,
    GearBox,
    Category,
    DatabaseClient
)
from sqlalchemy import func

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

    def get_model_by_brand(self, brand=None):
        result = []
        if brand:
            """
                select count(cars_info.id), m.model_name
                from cars_info
                join models m on cars_info.model_id = m.id
                where cars_info.brand_id = (select id from brands where brand_name ={{ brand }})
                group by m.model_name;
            """
            searched_brand_id = self.db_client.session.query(
                Brand.id
            ).\
                filter(Brand.brand_name == brand)
                
            data = self.db_client.session.query(
                func.count(Car.id), Model.model_name ) \
                .join(Model, Model.id == Car.model_id)\
                    .filter(Car.brand_id == searched_brand_id) \
                    .group_by(Model.model_name).all()
            for cnt, mod_name in data:
                result.append(
                        dict(
                                label=mod_name, column_value=cnt
                            ) 
                    )

            return result
        else:
            models_n_brands = self.db_client.session.query(Brand, Model) \
                .join(Model, Model.brand_id == Brand.id)
            for brand, model in models_n_brands:
                result.append(
                    {
                        "brand": brand.brand_name,
                        "model": model.model_name
                    }
                )
        return result

    def get_model_by_brand_old(self):
        brand_model = {}
        models_n_brands = self.db_client.session.query(Brand, Model) \
            .join(Model, Model.brand_id == Brand.id)
        for brand, model in models_n_brands:
            if brand.brand_name in brand_model.keys():
                brand_model[brand.brand_name].append(model.model_name)
            else:
                brand_model[brand.brand_name] = [model.model_name,]
        return brand_model

    def get_count_by_category(self):
        """
            select count(cars_info.id) as cnt, c.category_name from cars_info
            join category c on c.id = cars_info.category_id
            group by c.category_name
        """
        result = []
        data = self.db_client.session.query(
            func.count(Car.id), Category.category_name ) \
            .join(Category, Category.id == Car.category_id)\
                .group_by(Category.category_name).all()
        for cnt, cat_name in data:
            result.append(
                    dict(
                            label=cat_name, value=cnt
                        ) 
                )

        return result
    def get_brand_count(self) -> list:
        """
            select count(cars_info.id), b.brand_name
            from cars_info
            join brands b on cars_info.brand_id = b.id
            group by b.brand_name;
        """
        result = []
        data = self.db_client.session.query(
            func.count(Car.id), Brand.brand_name ) \
            .join(Brand, Brand.id == Car.brand_id)\
                .group_by(Brand.brand_name).all()
        print(data)
        for cnt, cat_name in data:
            result.append(
                    dict(
                            label=cat_name, value=cnt
                        ) 
                )

        return result
    
        
    def get_data_by_price_n_count(self, data_type) -> list:
        """
            select count(cars_info.id) as cnt,  c.category_name, avg(cars_info.price_usd)
            from cars_info
            join category c on c.id = cars_info.category_id
            group by cars_info.category_id, c.category_name;

            return list like [
                                {
                                "column_value": 22,
                                "label": "khetchbek",
                                "line_value": 6627
                                },
                                ...
                                {
                                "column_value": 17,
                                "label": "",
                                "line_value": 8909
                                }
                            ]
        """
        print(f"|{data_type}|")
        if data_type == 'category':
            data_table = Category
            data_name = Category.category_name
        elif data_type == 'gearbox':
            data_table = GearBox
            data_name = GearBox.gearbox_name
        elif data_type == 'fuel':
            pass
        else:
            raise AttributeError(f"Received data type( {data_type} ) is not supported")
        result = []
        data = self.db_client.session.query(
            func.count(Car.id), data_name, func.avg(Car.price_usd) ) \
            .join(data_table, data_table.id == Car.category_id)\
                .group_by(data_name).all()
        print(data)
        for cnt, cat_name, price in data:
            result.append(
                    dict(
                            label=cat_name, column_value=cnt, line_value=int(price)
                        ) 
                )

        return result
    


if __name__ == "__main__":
    q = CarApiQuery('asd')
    a = q.get_count_by_category()
