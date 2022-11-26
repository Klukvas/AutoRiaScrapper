from CarChooser.Configs.ApiConfig import(
    ProductionConfig as ProdApi,
    DevelopmentConfig as DevApi,
    TestingConfig as TestApi
)

from CarChooser.Configs.ScrapperConfig import(
    ProductionConfig as ProdScr,
    DevelopmentConfig as DevScr,
    TestingConfig as TestScr
)

from enum import Enum


class Config_type(Enum):
    SCRAPPER = 'Scrapper'
    API = 'API'

class Config_env(Enum):
    Testing = 'Testing'
    Production = 'Production'
    Development = 'Development'


API_CONFIG = dict(
    Testing = TestApi,
    Production = ProdApi,
    Development = DevApi
)

SCRAPPER_CONFIG = dict(
    Testing = TestScr,
    Production = ProdScr,
    Development = DevScr
) 


def get_config(config_type: str, config_env:str) -> type:
    if config_type == 'Scrapper':
        return SCRAPPER_CONFIG[config_env]
    elif config_type == 'API':
        return API_CONFIG[config_env]
    else:
        raise KeyError(f"{config_env} is not valid configuration enviroment")