import os
from pickle import NONE
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from serializer import Serializer
from logger import Logger

class TestSerializer:
    def setup(self):
        self.log = Logger().custom_logger()
        self.s = Serializer(self.log)

    def test_brand_model_1(self):
        data = 'brand-model.serializer-груз'
        new_data = self.s.brand_model_serializer(data)
        assert new_data['data'] == 'brand serializer gruz'
    
    def test_brand_model_2(self):
        data = 'brand-пасс-пас.-(id)'
        new_data = self.s.brand_model_serializer(data)
        assert new_data['data'] == 'brand pass pass'
    
    def test_brand_model_3(self):
        data = 'brand-пасс   -пас.-(id-test-model)'
        new_data = self.s.brand_model_serializer(data)
        assert new_data['data'] == 'brand pass pass test'
    
    def test_car_data_1(self):
        data = {
            'main_data': {
                'price': None,
                'autoId': "2065429",
                'race': "205",
                'fuelValue': "3",
                'fuelName': 'бензин',
                'year': "2012",
            },
            'gearbox': 'ручная / механика',
            'category': 'универс',
            }

        new_data = self.s.car_data_serializer(data)
        assert new_data['main_data']['price']['UAH'] == None
        assert new_data['main_data']['price']['USD'] == None
        assert new_data['main_data']['price']['EUR'] == None
        assert new_data['main_data']['autoId'] == 2065429
        assert new_data['main_data']['race'] == 205
        assert new_data['main_data']['fuelValue'] == 3.0
        assert new_data['main_data']['fuelName'] == 'benzin'
        assert new_data['main_data']['year'] == 2012
        assert new_data['category'] == 'universal'

    
    def test_car_data_2(self):
        data = {
            'main_data': {
                'price': {
                    "UAH": '112',
                    "EUR": "232",
                    "USD": None
                },
                'autoId': "2065429",
                'race': "205",
                'fuelValue': "3",
                'fuelName': None,
                'year': "2012",
            },
            'gearbox': None,
            'category': 'фыв',
            }

        new_data = self.s.car_data_serializer(data)

        assert new_data["category"] == 'фыв'
        assert new_data["gearbox"] == 'не указано'
        assert new_data["main_data"]['year'] == 2012
        assert new_data["main_data"]['fuelName'] == None
        assert new_data["main_data"]['fuelValue'] == 3.0
        assert new_data["main_data"]['price']['EUR'] == 232
        assert new_data["main_data"]['price']['UAH'] == 112
        assert new_data["main_data"]['price']['USD'] == None
    
    def test_car_data_3(self):
        data = {
            'main_data': {
                'price': {
                    "UAH": '112',
                    "EUR": "232",
                    "USD": None
                },
                'autoId': "2065429",
                'race': "205",
                'fuelValue': "3",
                'fuelName': 'TTEESSTT',
                'year': "2012",
            },
            'gearbox': 'paiq',
            'category': 'фыв',
            'link': 'test url'
            }

        new_data = self.s.car_data_serializer(data)

        assert new_data["category"] == 'фыв'
        assert new_data["gearbox"] == 'paiq'
        assert new_data["main_data"]['year'] == 2012
        assert new_data["main_data"]['fuelName'] == 'TTEESSTT'
        assert new_data["main_data"]['fuelValue'] == 3.0
        assert new_data["main_data"]['price']['EUR'] == 232
        assert new_data["main_data"]['price']['UAH'] == 112
        assert new_data["main_data"]['price']['USD'] == None