from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_utils import database_exists, create_database

from datetime import datetime

from alembic.script import ScriptDirectory
from alembic.config import Config
from alembic import command

import sys                                             
from os.path import abspath, dirname
sys.path.append(dirname(dirname(abspath(__file__))))
try:
    from CarChooser.Configs.ScrapperConfig import get_config
except ModuleNotFoundError:
    from Configs.ScrapperConfig import get_config

from Scrapper.utils import files_utils


from os import getenv


Base = declarative_base()


class DatabaseClient:
    def __init__(self):
        db_url = get_config(
            getenv('FLASK_ENV', 'development')
        ).get_db_url('CarsDataBase')
        self.engine = create_engine(db_url)

        try:
            if not database_exists(self.engine.url):
                create_database(self.engine.url)
        except Exception as err:
            print(f"Some error with creating database client: {err}")

        Base.metadata.create_all(self.engine)
        
        
        path_to_alembic_ini = files_utils.find_file("alembic.ini")
        if not path_to_alembic_ini:
            raise FileNotFoundError(f"Can not find path to alembic.ini")
        alembic_cfg = Config(path_to_alembic_ini)
        script = ScriptDirectory.from_config(alembic_cfg)
        last_revision_id = script.get_heads()
        command.stamp(alembic_cfg, last_revision_id)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

class UndefinedData(Base):
    __tablename__ = 'undefined_data'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    type_data = Column(String())
    additional_data = Column(String())
    data_value = Column(String())


class Brand(Base):
    __tablename__ = 'brands'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    brand_name = Column(String(), unique=True)
    last_update = Column(DateTime(), default=datetime.utcnow())
    model = relationship("Model")
    car = relationship("Car")


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    category_name = Column(String(), unique=True)
    car = relationship("Car")


class Model(Base):
    __tablename__ = 'models'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    model_name = Column(String(), unique=True)
    brand_id = Column(Integer(), ForeignKey('brands.id'))
    last_update = Column(DateTime(), default=datetime.utcnow())
    car = relationship("Car")


class Car(Base):
    __tablename__ = 'cars_info'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    last_update = Column(DateTime(), default=datetime.utcnow())
    brand_id = Column(Integer(), ForeignKey('brands.id'))
    model_id = Column(Integer(), ForeignKey('models.id'))
    auto_id = Column(Integer(), unique=True)
    price_usd = Column(Integer())
    price_uah = Column(Integer())
    price_eur = Column(Integer())
    race = Column(Integer())
    year = Column(Integer())
    fuel_name = Column(String())
    fuel_value = Column(Integer())
    gearbox_id = Column(Integer(), ForeignKey('gear_box.id'))
    has_damage = Column(Boolean())
    link = Column(String())
    vin = Column(String())
    parsed_from = Column(String())
    category_id = Column(Integer(), ForeignKey('category.id'))


class GearBox(Base):
    __tablename__ = 'gear_box'
    id = Column(Integer(), primary_key=True)
    gearbox_name = Column(String(), unique=True)
    last_update = Column(DateTime(), default=datetime.utcnow())
    car = relationship('Car')


class AdLastPage(Base):
    __tablename__ = 'ad_last_page'
    page_num = Column(Integer(), primary_key=True)


if __name__ == '__main__':
    
    db_client = DatabaseClient()
