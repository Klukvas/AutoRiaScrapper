import pytest
from sqlalchemy_utils import drop_database, database_exists
from os import environ 
from CarChooser.Configs.DataBaseConfig import TestingConfig


@pytest.fixture(scope='session', autouse=True)
def db_drop_afret_tests():
    environ.__setitem__("FLASK_ENV", 'Testing')
    yield
    dbs = (
            TestingConfig.get_db_url('CARS_DB'),
            TestingConfig.get_db_url('USERS_DB')
    )
    for db_url in dbs:
        if database_exists(db_url):
            try:
                drop_database(db_url)
            except:
                pass