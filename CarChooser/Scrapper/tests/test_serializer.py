from Scrapper.serializer import Serializer
try:
    from Configs.logger import Logger
except ImportError:
    import sys
    import os
    sys.path.append("..")
    from Configs.logger import Logger


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
            'carData': {
                'price': None,
                'category': 'универс',
                'autoId': "2065429",
                'race': "205",
                'fuelValue': "3",
                'fuelName': 'бензин',
                'year': "2012",
            },
            'gearbox': 'ручная / механика',
        }

        new_data = self.s.car_data_serializer(data)
        assert new_data['carData']['price']['UAH'] is None
        assert new_data['carData']['price']['USD'] is None
        assert new_data['carData']['price']['EUR'] is None
        assert new_data['carData']['autoId'] == 2065429
        assert new_data['carData']['race'] == 205
        assert new_data['carData']['fuelValue'] == 3.0
        assert new_data['carData']['fuelName'] == 'benzin'
        assert new_data['carData']['year'] == 2012
        assert new_data['carData']['category'] == 'universal'

    def test_car_data_2(self):
        data = {
            'carData': {
                'price': {
                    "UAH": '112',
                    "EUR": "232",
                    "USD": None
                },
                'gearBoxName': None,
                'autoId': "2065429",
                'race': "205",
                'fuelValue': "3",
                'fuelName': None,
                'year': "2012",
            },

            'category': 'фыв',
        }

        new_data = self.s.car_data_serializer(data)

        assert new_data["category"] == 'фыв'
        assert new_data["carData"]["gearBoxName"] == 'не указано'
        assert new_data["carData"]['year'] == 2012
        assert new_data["carData"]['fuelName'] is None
        assert new_data["carData"]['fuelValue'] == 3.0
        assert new_data["carData"]['price']['EUR'] == 232
        assert new_data["carData"]['price']['UAH'] == 112
        assert new_data["carData"]['price']['USD'] is None

    def test_car_data_3(self):
        data = {
            'carData': {
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
        assert new_data["carData"]['year'] == 2012
        assert new_data["carData"]['fuelName'] == 'TTEESSTT'
        assert new_data["carData"]['fuelValue'] == 3.0
        assert new_data["carData"]['price']['EUR'] == 232
        assert new_data["carData"]['price']['UAH'] == 112
        assert new_data["carData"]['price']['USD'] is None
