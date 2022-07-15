import configparser
import os


def get_parent_path(path):
    return os.path.abspath(
        os.path.join(
            path, os.pardir, 'config.ini'
        )
    )


def get_config(key):
    config = configparser.ConfigParser()
    config.read('config.ini')
    if key not in config.sections():
        # get path to parent dir
        path = os.getcwd()
        while key not in config.sections():
            path = get_parent_path(path)
            if os.path.exists(path):
                config.read(path)
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

