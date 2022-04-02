

from enum import unique
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Boolean, text, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import func
import configparser
from datetime import datetime
Base = declarative_base()
config = configparser.ConfigParser()
config.read('config.ini')
db_creds = config['DataBase']
class DatabaseClient:
    def __init__(self):
        self.engine = create_engine(f'{db_creds["driver"]}://{db_creds["host"]}/{db_creds["db_name"]}')
        try:
            if not database_exists(self.engine.url):
                create_database(self.engine.url)
        except Exception as err:
            print(f"Some error with creatin database client: {err}")
       
        Base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

class UnfindedDta(Base):
    __tablename__ = 'unfinded_data'
    
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