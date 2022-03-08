from models import Brand, DatabaseClient, Model, Car, AdLastPage, GearBox, UnfindedDta
from sqlalchemy import text

class Query:

    def __init__(self) -> None:
        self.db_client = DatabaseClient()

    def __del__(self) -> None:
        self.db_client.session.commit()
        self.db_client.session.close()

    def save_brand(self, brand):
        new_brand = Brand(
            brand_name = brand.lower()
        )
        try:
            self.db_client.session.add(new_brand)
            self.db_client.session.commit()
        except Exception as err:
            print(f'Some error with saving brand: {brand};\nError: {err}')
            self.db_client.session.rollback()
        return
     
    def save_unfinded_data(self, data_type, value_data, additional):
        new_unfinded_data = UnfindedDta(
            type_data = data_type.lower(),
            data_value = value_data.lower(),
            additional_data = additional
        )
        try:
            self.db_client.session.add(new_unfinded_data)
            self.db_client.session.commit()
        except Exception as err:
            print(f'Some error with saving unfinded data: {data_type} | {value_data};\nError: {err}')
            self.db_client.session.rollback()
        return
   
    def upgrade_last_page(self, page):
        page_num = self.db_client.session.query(AdLastPage).all()
        if page_num:
            
            self.db_client.session.query(AdLastPage).\
                filter(AdLastPage.page_num > -1).\
                    update({"page_num": page})
            self.db_client.session.commit()
        else:
            new_page = AdLastPage(
                page_num = page
            )
            self.db_client.session.add(new_page)
            self.db_client.session.commit()
        print(f"page_num: {page_num}")

    def save_model(self, brandId, model):
        new_model = Model(
            model_name = model.lower(),
            brand_id = brandId
        )
        try:
            self.db_client.session.add(new_model)
            self.db_client.session.commit()
        except Exception as err:
            print(f'Some error with saving model: {model}; brand id: {brandId};\nError: {err}')
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
            gearbox_name = gearbox
        )
        try:
            self.db_client.session.add(new_gearbox)
            self.db_client.session.commit()
        except Exception as err:
            print(f'Some error with saving gearBox: {gearbox};\nError: {err}')
            self.db_client.session.rollback()
        return
    
    def get_model_id(self, model_name):
        model_id = self.db_client.session.query(Model).filter(
                text(f"LOWER(models.model_name) like '{model_name.lower()}'")
            )
        ids = []
        for object_ in model_id:
            ids.append(object_.id)
        return ids

    def save_car_data(self, brand, model, car_data, gearbox_id):
        new_car = Car(
            brand_id      = brand,
            model_id      = model,
            auto_id       = car_data['autoId'],
            price_usd     = car_data['price']['USD'],
            price_uah     = car_data['price']['UAH'],
            price_eur     = car_data['price']['EUR'],
            race          = car_data['race'],
            year          = car_data['year'],
            fuel_name     = car_data['fuelName'],
            fuel_value    = car_data['fuelValue'],
            gearbox_id    = gearbox_id,
            has_damage    = car_data['hasDamage'],
            link          = car_data['link'],
            vin           = car_data['vin'],
            parsed_from   = car_data['from'],
        )
        try:
            self.db_client.session.add(new_car)
            self.db_client.session.commit()
            return 1
        except Exception as err:
            self.db_client.session.rollback()
            return err,
            print(f"Error while saving car data.\nError:{err}\nbrand: {brand}, model: {model}, car_data: {car_data}")
            
if __name__ == "__main__":
    d = DatabaseClient()
    q = Query()
    # q.upgrade_last_page(113)
    w = q.get_last_page()
    print(w)