from CarChooser.Configs.DataBaseConfig import (
    ProductionConfig as PROD_DB,
    DevelopmentConfig as DEV_DB,
    TestingConfig as TEST_DB
)

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
    DB_URL = None
    MAX_PULL = None


class TestingConfig(BaseConfig):
    DB_URL = TEST_DB.get_db_url('CARS_DB')
    MAX_PULL = 10    


class DevelopmentConfig(BaseConfig):
    DB_URL = DEV_DB.get_db_url('CARS_DB')
    MAX_PULL = 50


class ProductionConfig(BaseConfig):
    DB_URL = PROD_DB.get_db_url('CARS_DB')
    MAX_PULL = 100
