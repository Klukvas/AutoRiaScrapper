from os import getenv


class BaseConfig:
    CARS_DB = {}
    USERS_DB = {}

    @classmethod
    def get_db_url(cls, db_name: str) -> str:
        if db_name == "USERS_DB":
            db_data = cls.USERS_DB
        elif db_name == "CARS_DB":
            db_data = cls.CARS_DB
        else: raise AttributeError(f"URL of {db_name} is not exists")

        db_url = '{driver}://{username}:{password}@{host}:{port}/{db_name}'.format(
            driver=db_data["driver"],
            username=db_data["username"],
            password=db_data["password"],
            host=db_data["host"],
            port=db_data["port"],
            db_name=db_data["db_name"]
        )
        return db_url

    
    
class TestingConfig(BaseConfig):
    CARS_DB = dict(
        username="postgres",
        password="56457",
        host='localhost',
        port='5432',
        db_name="carChoicePrompt_test",
        driver="postgresql"
    )

    USERS_DB = dict(
        username="postgres",
        password="56457",
        host='localhost',
        port='5432',
        db_name="carChoicePrompt_test",
        driver="postgresql"
    )
    


class DevelopmentConfig(BaseConfig):
    CARS_DB = dict(
        username=getenv('CARS_DB_USERNAME', 'postgres'),
        password=getenv('CARS_DB_PASSWORD', '56457'),
        host=getenv('CARS_DB_HOST', 'localhost'),
        port=getenv('CARS_DB_PORT', '5432'),
        db_name=getenv('CARS_DB_NAME', 'carChoicePrompt'),
        driver=getenv('CARS_DB_driver', 'postgresql')
    )

    USERS_DB = dict(
        username=getenv('CARS_DB_USERNAME', 'postgres'),
        password=getenv('CARS_DB_PASSWORD', '56457'),
        host=getenv('CARS_DB_HOST', 'localhost'),
        port=getenv('CARS_DB_PORT', '5432'),
        db_name=getenv('CARS_DB_NAME', 'carChoicePrompt'),
        driver=getenv('CARS_DB_driver', 'postgresql')
    )
    


class ProductionConfig(BaseConfig):
    CARS_DB = dict(
        username=getenv('CARS_DB_USERNAME', 'postgres'),
        password=getenv('CARS_DB_PASSWORD', '56457'),
        host=getenv('CARS_DB_HOST', 'localhost'),
        port=getenv('CARS_DB_PORT', '5432'),
        db_name=getenv('CARS_DB_NAME', 'carChoicePrompt'),
        driver=getenv('CARS_DB_driver', 'postgresql')
    )


    USERS_DB = dict(
        username=getenv('CARS_DB_USERNAME', 'postgres'),
        password=getenv('CARS_DB_PASSWORD', '56457'),
        host=getenv('CARS_DB_HOST', 'localhost'),
        port=getenv('CARS_DB_PORT', '5432'),
        db_name=getenv('CARS_DB_NAME', 'carChoicePrompt'),
        driver=getenv('CARS_DB_driver', 'postgresql')
    )

if __name__ == "__main__":
    db_url = ProductionConfig.get_db_url("CARS_DB")
    print(db_url)