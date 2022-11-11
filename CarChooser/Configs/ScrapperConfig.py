import os


class BaseConfig:
    AUTO_RIA_API_KEYS = [
        '8s85MIseNcyqLNhDgRSTZBBgZ1GDKVC5WUQLr1BD',
        'geD4Z8A5je8p3q03jXsjKbgC3VXAFHWfFaK65fYo',
        'aASPp0cdOo5lo9u3hTB8izptGEdg28FmelRMevzA',
        'xMIVf6XFc5usghoZTaBqRbVmtzfqMGxebvLvW3kR',
        'ojvQkThYxgI1yExW3wU58nip26plIxgxsewKnr9m',
        'FpJGiaRzrgcLgXqxrJKyayg3HIm3LwskeR65fFA1',
        'n1RQ0hpcPYDJGTjsMQDNbWRXE6wS2oVAfQBQ7Oca',
        'Tdh72mjcSwYnprZWDrPQYrvYPNVQ5KN5B3pJbHCn',
        'AxcSopVYnJznZ2wgwAFl9r2WhqD1q2EMT8ppZKa3',
        'rBr6EgVK8KGhdBndCe2xEef4wV4BGUy7d0i3Ynte'
    ]
    CARS_DATABASE = {}
    USERS_DATABASE = {}

    @classmethod
    def get_db_url(cls, db_name):
        if db_name == 'CarsDataBase':
            db_creds = cls.CARS_DATABASE
        elif db_name == 'UsersDataBase':
            db_creds = cls.USERS_DATABASE
        else:
            raise SystemError(f"Can not get db creds of database name: {db_name}")
        return '{driver}://{username}:{password}@{host}:{port}/{db_name}'.format(
            driver=db_creds["driver"],
            username=db_creds["username"],
            password=db_creds["password"],
            host=db_creds["host"],
            port=db_creds["port"],
            db_name=db_creds["db_name"]
        )


class TestingConfig(BaseConfig):
    CARS_DATABASE = dict(
        username="postgres",
        password="56457",
        host='localhost',
        port='5430',
        db_name="carChoicePrompt",
        driver="postgresql"
    )
    USERS_DATABASE = dict(
        username="postgres",
        password="56457",
        host="localhost",
        port='5431',
        db_name="SystemAuth",
        driver="postgresql"
    )


class DevelopmentConfig(BaseConfig):
    CARS_DATABASE = dict(
        username=os.getenv('CARS_DB_USERNAME', 'postgres'),
        password=os.getenv('CARS_DB_PASSWORD', '56457'),
        host=os.getenv('CARS_DB_HOST', 'localhost'),
        port=os.getenv('CARS_DB_PORT', '5430'),
        db_name=os.getenv('CARS_DB_NAME', 'carChoicePrompt'),
        driver=os.getenv('CARS_DB_driver', 'postgresql')
    )
    USERS_DATABASE = dict(
        username=os.getenv('USERS_DB_USERNAME', 'postgres'),
        password=os.getenv('USERS_DB_PASSWORD', '56457'),
        host=os.getenv('USERS_DB_HOST', 'localhost'),
        port=os.getenv('USERS_DB_PORT', '5431'),
        db_name=os.getenv('USERS_DB_NAME', 'SystemAuth'),
        driver=os.getenv('USERS_DB_driver', 'postgresql')
    )


class ProductionConfig(BaseConfig):
    CARS_DATABASE = dict(
        username=os.getenv('CARS_DB_USERNAME', 'postgres'),
        password=os.getenv('CARS_DB_PASSWORD', '56457'),
        host=os.getenv('CARS_DB_HOST', 'localhost'),
        port=os.getenv('CARS_DB_PORT', '5431'),
        db_name=os.getenv('CARS_DB_NAME', 'carChoicePrompt'),
        driver=os.getenv('CARS_DB_driver', 'postgresql')
    )
    USERS_DATABASE = dict(
        username=os.getenv('USERS_DB_USERNAME', 'postgres'),
        password=os.getenv('USERS_DB_PASSWORD', '56457'),
        host=os.getenv('USERS_DB_HOST', 'localhost'),
        port=os.getenv('USERS_DB_PORT', '5430'),
        db_name=os.getenv('USERS_DB_NAME', 'SystemAuth'),
        driver=os.getenv('USERS_DB_driver', 'postgresql')
    )


ENV_CONFIG_DICT = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)


def get_config(config_name):
    """Retrieve environment configuration settings."""
    if config_name not in ENV_CONFIG_DICT.keys():
        raise Exception(f"Incorrect config name. Available names: {ENV_CONFIG_DICT.keys()}")
    return ENV_CONFIG_DICT.get(config_name, DevelopmentConfig)


if __name__ == "__main__":
    scrapper_configs = get_config('development')
    db_url = scrapper_configs.get_db_url('UsersDataBase')
    print(db_url)
