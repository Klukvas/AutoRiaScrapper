from CarChooser.Scrapper.serializer import Serializer
from CarChooser.Scrapper.main_parser import Parser
from CarChooser.Scrapper.query import Query
from CarChooser.Scrapper.models import *
try:
    from Configs.logger import Logger
except ImportError:
    import sys
    import os
    sys.path.append(
        ".."
    )
    from Configs.logger import Logger


class TestMainParser:
    def setup_method(self):
        self.log = Logger().custom_logger()
        self.s = Serializer(self.log)
        self.q = Query(self.log)
        self.parser = Parser(self.log, self.q, self.s)
        self.db_client = DatabaseClient()

   
    def test_brand_exists_2(self):
        """
        Проверяем что не сохранит, если попыток сохранить >= 1
        """
        res = self.parser.brand_exists("brandbrand_name", 1)
        assert res is None

    def test_brand_exists_3(self):
        """
        Проверяем что сохранит - после удаляем + Проверяем что найдет существующий бренд
        """
        brand_name = "brandbrand_name"
        res = self.parser.brand_exists(brand_name)
        assert type(res) == int
        brand = self.db_client.session.query(Brand).limit(1)
        assert self.parser.brand_exists(brand[0].brand_name)
        self.db_client.session.query(Brand)\
            .filter(
            Brand.brand_name == brand_name
        ).delete()
        self.db_client.session.commit()