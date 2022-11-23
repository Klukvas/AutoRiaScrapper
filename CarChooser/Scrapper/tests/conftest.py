import pytest
from sqlalchemy_utils import drop_database, database_exists
from CarChooser.RestApi.extensions import db
import os
from CarChooser.Configs import ScrapperConfig

@pytest.fixture(scope='session', autouse=True)
def db_drop_afret_tests():
    os.environ.__setitem__("FLASK_ENV", 'testing')
    yield
    config = ScrapperConfig.get_config('testing')
    for db_url in [
        config.get_db_url("CarsDataBase"),
        config.get_db_url("UsersDataBase")
    ]:
        print(f"ANDRIIPX: {db_url}")

        if database_exists(db_url):
            try:
                drop_database(db_url)
            except:
                pass