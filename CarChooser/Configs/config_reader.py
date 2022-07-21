import configparser
import os
from .logger import Logger

logger = Logger().custom_logger()


def get_config(key):
    logger.debug(f"Calling get config for: {key}")
    config = configparser.ConfigParser()
    path_to_scrapper_config = os.getenv('path_to_scrapper_config')
    config.read(path_to_scrapper_config)
    if key not in config.sections():
        raise SystemError(f"Can not find {key} in config {path_to_scrapper_config}")
    if 'DataBase' in key:
        db_creds = config[key]
        db_url = '{driver}://{username}:{password}@{host}/{db_name}'.format(
            driver=db_creds["driver"],
            username=db_creds["username"],
            password=db_creds["password"],
            host=db_creds["host"],
            db_name=db_creds["db_name"]
        )
        return db_url
    elif key == 'AutoRia':
        return config

