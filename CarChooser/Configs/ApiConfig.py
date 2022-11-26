from os import getenv
from CarChooser.Configs.DataBaseConfig import (
    ProductionConfig as PROD_DB,
    DevelopmentConfig as DEV_DB,
    TestingConfig as TEST_DB
)


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USERS_DATABASE = None


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    TESTING = True
    FLASK_ENV = "development"
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = DEV_DB.get_db_url('USERS_DB')


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    FLASK_ENV = "testing"
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = TEST_DB.get_db_url('USERS_DB')
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = getenv('SECRET_KEY', 'IFDHDISFhjdsifsahf2387ry9eiowkpd')
    FLASK_ENV = "production"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = PROD_DB.get_db_url('USERS_DB')
