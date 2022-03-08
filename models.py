

import asyncio
from xmlrpc.client import Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Boolean, text
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import func

Base = declarative_base()

class DatabaseClient:
    def __init__(self):
        self.engine = create_engine('postgresql://localhost/carChoicePrompt')
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
    model = relationship("Model")
    car = relationship("Car")


class Model(Base):
    __tablename__ = 'models'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    model_name = Column(String(), unique=True)
    brand_id = Column(Integer(), ForeignKey('brands.id'))
    car = relationship("Car")

class Car(Base):
    __tablename__ = 'cars_info'

    id = Column(Integer(), primary_key=True, autoincrement=True)
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

class GearBox(Base):
    __tablename__ = 'gear_box'
    id = Column(Integer(), primary_key=True)
    gearbox_name = Column(String(), unique=True)
    car = relationship('Car')


class AdLastPage(Base):
    __tablename__ = 'ad_last_page'
    page_num = Column(Integer(), primary_key=True)

if __name__ == '__main__':
    db_client = DatabaseClient()