from msilib.schema import Error
import os
from CarChooser.Configs.config_reader import get_config


db_url = get_config('UsersDataBase')


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    TESTING = True
    FLASK_ENV = "development"
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = db_url


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = db_url + '_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'my_precious'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = db_url


ENV_CONFIG_DICT = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)


def get_config(config_name):
    """Retrieve environment configuration settings."""
    if config_name not in ENV_CONFIG_DICT.keys():
        raise Exception(f"Incorrect config name. Available names: {ENV_CONFIG_DICT.keys()}")
    return ENV_CONFIG_DICT.get(config_name, DevelopmentConfig)
