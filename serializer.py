
from re import sub

class Serializer:
    
    def __init__(self, log) -> None:
        self.log = log
    
    def brand_model_serializer(self, brand_model:str) -> dict:
        brand_model = brand_model.\
            replace("-", " ").\
                replace(".", " ").\
                    replace("груз", "gruz").\
                        replace("пасс", "pass").\
                            replace("пас", "pass").\
                                replace("model", "").\
                                    replace("id", "").\
                                            replace("(", "").\
                                                replace(")", "")
        
        brand_model = sub(' +', ' ', brand_model)
        brand_model = brand_model.\
                lower().\
                    strip()                                                    
        return {"data": brand_model}

    def car_data_serializer(self, data:dict) -> dict:
        if data["main_data"]['price']:
            
            if data["main_data"]['price']['UAH']:
                data["main_data"]['price']['UAH'] = int(data["main_data"]['price']['UAH'].replace('грн', "").replace(' ', '').strip())
            else:
                data["main_data"]['price']['UAH'] = None
            
            if data["main_data"]['price']['EUR']:
                data["main_data"]['price']['EUR'] = int(data["main_data"]['price']['EUR'].replace('€', "").replace(' ', '').strip())
            else:
                data["main_data"]['price']['EUR'] = None

            if data["main_data"]['price']['USD']:
                data["main_data"]['price']['USD'] = int(data["main_data"]['price']['USD'].replace('$', "").replace(' ', '').strip())
            else:
                data["main_data"]['price']['USD'] = None
        else:
            data["main_data"]['price'] = {}
            data["main_data"]['price']['UAH'] = None
            data["main_data"]['price']['EUR'] = None
            data["main_data"]['price']['USD'] = None
        
        if data["main_data"]['autoId']:
            data["main_data"]['autoId'] = int(data["main_data"]['autoId'])
        
        if data["main_data"]['race']:
            data["main_data"]['race'] = int(data["main_data"]['race'])
        
        if data["main_data"]['fuelValue']:
            data["main_data"]['fuelValue'] = float(data["main_data"]['fuelValue'])
        
        if data["main_data"]['fuelName']:
            fuelName_translitor = {
                "гибрид": "gibrid",
                "бенз": "benzin",
                "газ": "gaz",
                "элек": "elektro",
                "диз": "dizel",
                "метан": "gaz-metan",
                "газ-бенз": "gaz-benzin",
                "бутан": "gaz-propan-butan"
                
            }
            for item in fuelName_translitor.keys():
                if item in data["main_data"]['fuelName'].lower().strip():
                    data["main_data"]['fuelName'] = fuelName_translitor[item]
                    break
        if data["main_data"]['year']:
            data["main_data"]['year'] = int(data["main_data"]['year'])
        if data['gearbox']:
            changed = False
            gear_box_translitor = [
                "автомат",
                "ручная / механика",
                "типтроник",
                "не указано",
                "вариатор",
                "робот"
            ]
            for item in gear_box_translitor:
                if data['gearbox'].lower().strip() in item:
                    data['gearbox'] = item
                    changed = True
                    break
            if not changed:
                self.log.error(f"Can not find gearbox of car: {data['link']}")
        else:
            data['gearbox'] = 'не указано'
        if data['category']:
            category_translitor = {
                "седан": "sedan",
                "лимузин": "limuzin",
                "универсал": "universal",
                "хэтчбек": "khetchbek",
                "внедорожник": "vnedorozhnik-krossover",
                "минивен": "miniven",
                "купе": "kupe",
                "фургон": "legkovoj-furgon-do-1-5-t",
                "лифтбек": "liftbek",
                "пикап": "pikap",
                "комбайн": "kombajn",
                "кабриолет": "kabriolet"
            }
            for item in category_translitor.keys():
                if data['category'].lower().strip() in item:
                    data['category'] = category_translitor[item]
                    break
        else:
            data['category'] = 'drugoj'
        return data
                        