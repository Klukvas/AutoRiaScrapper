import os
from CarChooser.Configs.ScrapperConfig import get_config

def get_db_url(env_name):
    scrapper_configs = get_config(
        env_name
    )
    db_url = scrapper_configs.get_db_url('UsersDataBase')
    return db_url

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
    SQLALCHEMY_DATABASE_URI = get_db_url(FLASK_ENV)


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    FLASK_ENV = "testing"
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = get_db_url(FLASK_ENV)
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'my_precious'
    FLASK_ENV = "production"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = get_db_url(FLASK_ENV)


ENV_CONFIG_DICT = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)


def get_config(config_name):
    """Retrieve environment configuration settings."""
    if config_name not in ENV_CONFIG_DICT.keys():
        raise Exception(f"Incorrect config name. Available names: {ENV_CONFIG_DICT.keys()}")
    return ENV_CONFIG_DICT.get(config_name, DevelopmentConfig)
