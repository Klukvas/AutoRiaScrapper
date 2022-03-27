
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
        if data["carData"]['price']:
            
            if data["carData"]['price']['UAH']:
                data["carData"]['price']['UAH'] = int(data["carData"]['price']['UAH'].replace('грн', "").replace(' ', '').strip())
            else:
                data["carData"]['price']['UAH'] = None
            
            if data["carData"]['price']['EUR']:
                data["carData"]['price']['EUR'] = int(data["carData"]['price']['EUR'].replace('€', "").replace(' ', '').strip())
            else:
                data["carData"]['price']['EUR'] = None

            if data["carData"]['price']['USD']:
                data["carData"]['price']['USD'] = int(data["carData"]['price']['USD'].replace('$', "").replace(' ', '').strip())
            else:
                data["carData"]['price']['USD'] = None
        else:
            data["carData"]['price'] = {}
            data["carData"]['price']['UAH'] = None
            data["carData"]['price']['EUR'] = None
            data["carData"]['price']['USD'] = None
        
        if data["carData"]['autoId']:
            data["carData"]['autoId'] = int(data["carData"]['autoId'])
        
        if data["carData"]['race']:
            data["carData"]['race'] = int(data["carData"]['race'])
        
        if data["carData"]['fuelValue']:
            data["carData"]['fuelValue'] = float(data["carData"]['fuelValue'])
        
        if data["carData"]['fuelName']:
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
                if item in data["carData"]['fuelName'].lower().strip():
                    data["carData"]['fuelName'] = fuelName_translitor[item]
                    break
        if data["carData"]['year']:
            data["carData"]['year'] = int(data["carData"]['year'])
        if data["carData"]['gearBoxName']:
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
                if data["carData"]['gearBoxName'].lower().strip() in item:
                    data["carData"]['gearBoxName'] = item
                    changed = True
                    break
            if not changed:
                self.log.error(f"Can not find gearbox of car: {data['link']}")
        else:
            data["carData"]['gearBoxName'] = 'не указано'
        if data["carData"]['category']:
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
                if data["carData"]['category'].lower().strip() in item:
                    data["carData"]['category'] = category_translitor[item]
                    break
        else:
            data["carData"]['category'] = 'drugoj'
        return data
                        